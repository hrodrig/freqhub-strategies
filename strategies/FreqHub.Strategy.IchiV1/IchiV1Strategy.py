import logging
from typing import Optional, Tuple
from datetime import datetime, timezone

import pandas as pd
import numpy as np
import talib.abstract as ta
from pandas import DataFrame

from freqtrade.strategy import (DecimalParameter, IntParameter, IStrategy, merge_informative_pair, stoploss_from_open)

logger = logging.getLogger(__name__)


class IchiV1Strategy(IStrategy):
    """
    IchiV1 strategy based on the Ichimoku Cloud.
    
    Risk Level: MEDIUM
    
    This strategy uses the Ichimoku Cloud, combining leading and lagging
    indicators to generate entry and exit signals. It also uses a "fan"
    indicator to analyze volume.
    
    Features:
    - Configurable stoploss
    - Trailing stop to protect profits
    - Timeframe: 15m
    - Multiple confirmations before entry
    - Trend, support/resistance, and reversal analysis
    """
    
    INTERFACE_VERSION = 3
    
    # Optimizable buy parameters
    buy_trend_above_senkou_level = DecimalParameter(0.0, 2.0, default=0.5, space="buy", optimize=True)
    buy_trend_bullish_level = DecimalParameter(0.0, 1.0, default=0.3, space="buy", optimize=True)
    buy_fan_magnitude_shift_value = DecimalParameter(0.1, 2.0, default=0.5, space="buy", optimize=True)
    buy_min_fan_magnitude_gain = DecimalParameter(0.1, 1.0, default=0.3, space="buy", optimize=True)
    
    # Optimizable sell parameters
    sell_trend_indicator = DecimalParameter(-1.0, 0.0, default=-0.3, space="sell", optimize=True)
    
    # Advanced custom trailing stoploss (from awesome-freqtrade)
    # Credit: @github/perkmeister
    pHSL = DecimalParameter(-0.200, -0.040, default=-0.08, decimals=3, space='sell', optimize=True, load=True)
    pPF_1 = DecimalParameter(0.008, 0.020, default=0.016, decimals=3, space='sell', optimize=True, load=True)
    pSL_1 = DecimalParameter(0.008, 0.020, default=0.011, decimals=3, space='sell', optimize=True, load=True)
    pPF_2 = DecimalParameter(0.040, 0.100, default=0.070, decimals=3, space='sell', optimize=True, load=True)
    pSL_2 = DecimalParameter(0.020, 0.070, default=0.030, decimals=3, space='sell', optimize=True, load=True)
    
    # Fixed parameters
    timeframe = '15m'
    stoploss = -0.08  # Initial 8% stoploss (dynamic via custom_stoploss)
    trailing_stop = False  # Disabled because we use custom_stoploss
    use_exit_signal = True
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False
    
    # ROI table
    minimal_roi = {
        "0": 0.15,   # 15% after 0 minutes
        "30": 0.08,  # 8% after 30 minutes
        "60": 0.04,  # 4% after 60 minutes
        "120": 0.02  # 2% after 120 minutes
    }
    
    # Variables to track daily profit
    _current_day = None
    _daily_profit_checked = False
    _daily_profit_positive = False
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Add Ichimoku Cloud indicators and volume fan to the DataFrame.
        """
        # Standard Ichimoku parameters
        tenkan_period = 9
        kijun_period = 26
        senkou_b_period = 52
        chikou_shift = 26
        
        # Tenkan-sen (Conversion Line): (Highest High + Lowest Low) / 2 for 9 periods
        high_9 = dataframe['high'].rolling(window=tenkan_period).max()
        low_9 = dataframe['low'].rolling(window=tenkan_period).min()
        dataframe['tenkan_sen'] = (high_9 + low_9) / 2
        
        # Kijun-sen (Base Line): (Highest High + Lowest Low) / 2 for 26 periods
        high_26 = dataframe['high'].rolling(window=kijun_period).max()
        low_26 = dataframe['low'].rolling(window=kijun_period).min()
        dataframe['kijun_sen'] = (high_26 + low_26) / 2
        
        # Senkou Span A (Leading Span A): (Tenkan-sen + Kijun-sen) / 2, shifted 26 periods forward
        dataframe['senkou_span_a'] = ((dataframe['tenkan_sen'] + dataframe['kijun_sen']) / 2).shift(chikou_shift)
        
        # Senkou Span B (Leading Span B): (Highest High + Lowest Low) / 2 for 52 periods, shifted 26 periods
        high_52 = dataframe['high'].rolling(window=senkou_b_period).max()
        low_52 = dataframe['low'].rolling(window=senkou_b_period).min()
        dataframe['senkou_span_b'] = ((high_52 + low_52) / 2).shift(chikou_shift)
        
        # Chikou Span (Lagging Span): Closing price shifted 26 periods back
        dataframe['chikou_span'] = dataframe['close'].shift(-chikou_shift)
        
        # Trend indicator: price position relative to the cloud
        # Positive = price above cloud (bullish), Negative = price below (bearish)
        dataframe['trend_indicator'] = np.where(
            dataframe['close'] > dataframe[['senkou_span_a', 'senkou_span_b']].max(axis=1),
            1.0,  # Bullish
            np.where(
                dataframe['close'] < dataframe[['senkou_span_a', 'senkou_span_b']].min(axis=1),
                -1.0,  # Bearish
                0.0  # Neutral (inside cloud)
            )
        )
        
        # Bullish trend level: how far above the cloud the price is
        dataframe['trend_above_senkou'] = np.where(
            dataframe['trend_indicator'] > 0,
            (dataframe['close'] - dataframe[['senkou_span_a', 'senkou_span_b']].max(axis=1)) / dataframe['close'],
            0.0
        )
        
        # Bullish trend level: relationship between Tenkan and Kijun
        dataframe['trend_bullish'] = np.where(
            dataframe['tenkan_sen'] > dataframe['kijun_sen'],
            (dataframe['tenkan_sen'] - dataframe['kijun_sen']) / dataframe['kijun_sen'],
            0.0
        )
        
        # Volume fan indicator
        # Calculate volume change magnitude using an exponential moving average
        volume_ema = dataframe['volume'].ewm(span=20, adjust=False).mean()
        dataframe['volume_shift'] = dataframe['volume'] / volume_ema.shift(int(self.buy_fan_magnitude_shift_value.value * 10))
        dataframe['fan_magnitude'] = dataframe['volume_shift'] - 1.0
        dataframe['fan_magnitude_gain'] = dataframe['fan_magnitude'].rolling(window=5).mean()
        
        # RSI for additional confirmation
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        
        # ATR for volatility
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        
        # Detect Pullback (from awesome-freqtrade)
        # Credit: @github/just-nilux
        dataframe = self.detect_pullback(dataframe, periods=30, method='pct_outlier')
        
        return dataframe
    
    def detect_pullback(self, df: DataFrame, periods=30, method='pct_outlier'):
        """
        Pullback & Outlier Detection
        Know when a sudden move and possible reversal is coming
        Credit: @github/just-nilux (awesome-freqtrade)
        
        Method: Percent-Change Outlier (z-score)
        df['pullback_flag']: 1 (Outlier Up) / -1 (Outlier Down)
        """
        if method == 'pct_outlier':
            outlier_threshold = 2.0
            df["pb_pct_change"] = df["close"].pct_change()
            # Calculate z-score manually
            df['pb_mean'] = df['pb_pct_change'].rolling(window=periods).mean()
            df['pb_std'] = df['pb_pct_change'].rolling(window=periods).std()
            df['pb_zscore'] = (df['pb_pct_change'] - df['pb_mean']) / df['pb_std']
            df['pullback_flag'] = np.where(df['pb_zscore'] >= outlier_threshold, 1, 0)
            df['pullback_flag'] = np.where(df['pb_zscore'] <= -outlier_threshold, -1, df['pullback_flag'])
        
        return df
    
    def custom_stoploss(self, pair: str, trade, current_time: datetime,
                       current_rate: float, current_profit: float, **kwargs) -> float:
        """
        Advanced custom trailing stoploss.
        Credit: @github/perkmeister (awesome-freqtrade)
        
        Implements a dynamic trailing stoploss with multiple levels:
        - For profits between PF_1 and PF_2: stoploss interpolates between SL_1 and SL_2
        - For profits above PF_2: stoploss increases linearly with profit
        - For profits below PF_1: uses hard stoploss (HSL)
        """
        HSL = self.pHSL.value
        PF_1 = self.pPF_1.value
        SL_1 = self.pSL_1.value
        PF_2 = self.pPF_2.value
        SL_2 = self.pSL_2.value
        
        # For profits between PF_1 and PF_2 the stoploss interpolates linearly
        # between SL_1 and SL_2. For profits above PF_2 the stoploss increases
        # linearly with profit. For profits below PF_1 it uses HSL.
        
        if (current_profit > PF_2):
            sl_profit = SL_2 + (current_profit - PF_2)
        elif (current_profit > PF_1):
            sl_profit = SL_1 + ((current_profit - PF_1) * (SL_2 - SL_1) / (PF_2 - PF_1))
        else:
            sl_profit = HSL
        
        # Only for hyperopt invalid return
        if (sl_profit >= current_profit):
            return -0.99
        
        return stoploss_from_open(sl_profit, current_profit)
    
    def get_daily_profit(self) -> Tuple[float, bool]:
        """
        Calculate profit for the current day.
        Returns: (profit_total, has_profit)
        """
        try:
            # Get current date (UTC)
            now = datetime.now(timezone.utc)
            current_day = now.date()
            
            # If it's a new day, reset the cache
            if self._current_day != current_day:
                self._current_day = current_day
                self._daily_profit_checked = False
                self._daily_profit_positive = False
            
            # If already checked today and there is profit, return cached result
            if self._daily_profit_checked:
                return (0.0, self._daily_profit_positive)
            
            # Calculate daily profit
            daily_profit = 0.0
            has_profit = False
            
            # Method 1: Try wallets.get_today_profit() if available
            if hasattr(self.dp, 'wallets'):
                try:
                    # Try to get daily profit using wallet method
                    if hasattr(self.dp.wallets, 'get_today_profit'):
                        daily_profit = self.dp.wallets.get_today_profit()
                        has_profit = daily_profit > 0.0
                        logger.info(f"Daily profit (wallets): {daily_profit:.4f} USDT")
                    # Alternative: use get_profit with date filter
                    elif hasattr(self.dp.wallets, 'get_profit'):
                        # Get profit since start of day
                        start_of_day = datetime.combine(current_day, datetime.min.time()).replace(tzinfo=timezone.utc)
                        profit_data = self.dp.wallets.get_profit(start_of_day, now)
                        if profit_data and hasattr(profit_data, 'profit_abs'):
                            daily_profit = profit_data.profit_abs
                            has_profit = daily_profit > 0.0
                            logger.info(f"Daily profit (get_profit): {daily_profit:.4f} USDT")
                except Exception as e:
                    logger.debug(f"Could not get wallet profit: {e}")
            
            # Method 2: If it didn't work, try closed trades for the day
            if not self._daily_profit_checked and hasattr(self.dp, 'trade'):
                try:
                    # Get all closed trades
                    if hasattr(self.dp.trade, 'get_closed_trades'):
                        closed_trades = self.dp.trade.get_closed_trades()
                        if closed_trades:
                            for trade in closed_trades:
                                # Check if trade closed today
                                if hasattr(trade, 'close_date') and trade.close_date:
                                    close_date = trade.close_date
                                    if isinstance(close_date, datetime):
                                        if close_date.date() == current_day:
                                            if hasattr(trade, 'profit_abs') and trade.profit_abs:
                                                daily_profit += trade.profit_abs
                    # Alternative: use get_trades() and filter
                    elif hasattr(self.dp.trade, 'get_trades'):
                        all_trades = self.dp.trade.get_trades()
                        if all_trades:
                            for trade in all_trades:
                                if hasattr(trade, 'is_open') and not trade.is_open:
                                    if hasattr(trade, 'close_date') and trade.close_date:
                                        close_date = trade.close_date
                                        if isinstance(close_date, datetime):
                                            if close_date.date() == current_day:
                                                if hasattr(trade, 'profit_abs') and trade.profit_abs:
                                                    daily_profit += trade.profit_abs
                except Exception as e:
                    logger.debug(f"Could not get closed trades: {e}")
            
            # Check for positive profit
            has_profit = daily_profit > 0.0
            
            # Cache the result
            self._daily_profit_checked = True
            self._daily_profit_positive = has_profit
            
            if daily_profit != 0.0 or has_profit:
                logger.info(f"Daily profit {current_day}: {daily_profit:.4f} USDT, has profit: {has_profit}")
            
            return (daily_profit, has_profit)
            
        except Exception as e:
            logger.warning(f"Error calculating daily profit: {e}")
            return (0.0, False)
    
    def confirm_trade_entry(self, pair: str, order_type: str, amount: float,
                           rate: float, time_in_force: str, current_time: datetime,
                           entry_tag: Optional[str], side: str, **kwargs) -> bool:
        """
        Confirm whether an entry should be allowed.
        Blocks new entries if there is already positive profit for the day.
        """
        try:
            daily_profit, has_profit = self.get_daily_profit()
            
            if has_profit:
                logger.info(f"Blocking entry for {pair}: daily profit already positive ({daily_profit:.4f} USDT)")
                return False
            
            return True
        except Exception as e:
            logger.warning(f"Error in confirm_trade_entry: {e}")
            return True  # On error, allow entry
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Define entry conditions based on the Ichimoku Cloud.
        """
        dataframe.loc[
            (
                # Price above cloud (bullish trend)
                (dataframe['trend_above_senkou'] >= self.buy_trend_above_senkou_level.value) &
                # Tenkan above Kijun (confirmed bullish trend)
                (dataframe['trend_bullish'] >= self.buy_trend_bullish_level.value) &
                # Chikou Span above price (trend confirmation)
                (dataframe['chikou_span'] > dataframe['close'])
            ) |
            # Or price crossing above the cloud
            (
                (dataframe['close'] > dataframe['senkou_span_a']) &
                (dataframe['close'] > dataframe['senkou_span_b']) &
                (dataframe['close'].shift(1) <= dataframe[['senkou_span_a', 'senkou_span_b']].max(axis=1).shift(1)) &
                (dataframe['tenkan_sen'] > dataframe['kijun_sen'])
            )
            &
            # Volume confirmation with fan
            (dataframe['fan_magnitude_gain'] >= self.buy_min_fan_magnitude_gain.value) &
            # RSI not overbought
            (dataframe['rsi'] < 70) &
            # Volume above average
            (dataframe['volume'] > dataframe['volume'].rolling(window=20).mean()) &
            # Avoid entries during extreme bearish pullback
            (dataframe['pullback_flag'] != -1)
            ,
            'enter_long'
        ] = 1
        
        return dataframe
    
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Define exit conditions based on the Ichimoku Cloud.
        """
        dataframe.loc[
            (
                # Trend indicator turns bearish
                (dataframe['trend_indicator'] <= self.sell_trend_indicator.value) |
                # Tenkan crosses below Kijun
                (
                    (dataframe['tenkan_sen'] < dataframe['kijun_sen']) &
                    (dataframe['tenkan_sen'].shift(1) >= dataframe['kijun_sen'].shift(1))
                ) |
                # Price crosses below the cloud
                (
                    (dataframe['close'] < dataframe['senkou_span_a']) &
                    (dataframe['close'] < dataframe['senkou_span_b']) &
                    (dataframe['close'].shift(1) >= dataframe[['senkou_span_a', 'senkou_span_b']].min(axis=1).shift(1))
                ) |
                # Chikou Span crosses below price
                (
                    (dataframe['chikou_span'] < dataframe['close']) &
                    (dataframe['chikou_span'].shift(1) >= dataframe['close'].shift(1))
                )
            ) &
            # RSI overbought
            (dataframe['rsi'] > 70)
            ,
            'exit_long'
        ] = 1
        
        return dataframe

