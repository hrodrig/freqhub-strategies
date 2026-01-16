import logging
from typing import Optional

import pandas as pd
import talib.abstract as ta
from pandas import DataFrame

from freqtrade.strategy import (DecimalParameter, IntParameter, IStrategy, merge_informative_pair)

logger = logging.getLogger(__name__)


class RSI_BollingerStrategy(IStrategy):
    """
    Simple RSI + Bollinger Bands Strategy - Momentum and volatility

    Risk Level: MEDIUM
    Expected Profit: ~8-10% monthly

    This strategy combines RSI to identify momentum with Bollinger Bands
    to locate entry zones in volatile conditions.

    Features:
    - Moderate stop loss (-6%)
    - Trailing stop to protect profits
    - Timeframe: 15m with 1h context
    - Entry when RSI is favorable and price bounces off the lower band
    """
    
    INTERFACE_VERSION = 3
    
    # Optimizable parameters
    buy_rsi_min = IntParameter(45, 60, default=50, space="buy", optimize=True)
    buy_rsi_max = IntParameter(65, 80, default=70, space="buy", optimize=True)
    buy_bb_period = IntParameter(15, 25, default=20, space="buy", optimize=True)
    buy_bb_std = DecimalParameter(1.5, 2.5, default=2.0, space="buy", optimize=True)
    buy_bb_percent = DecimalParameter(0.0, 0.3, default=0.15, space="buy", optimize=True)
    buy_volume_factor = DecimalParameter(1.0, 2.5, default=1.5, space="buy", optimize=True)
    
    # Fixed parameters
    timeframe = '15m'
    stoploss = -0.06  # 6% stop loss
    trailing_stop = True
    trailing_stop_positive = 0.015  # Activate trailing stop after 1.5% profit
    trailing_stop_positive_offset = 0.025  # Keep at least 2.5% profit
    trailing_only_offset_is_reached = True
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False
    
    # ROI table
    minimal_roi = {
        "0": 0.10,   # 10% after 0 minutes
        "30": 0.05,  # 5% after 30 minutes
        "60": 0.03,  # 3% after 60 minutes
        "120": 0.01  # 1% after 120 minutes
    }
    
    # Informative pairs
    informative_timeframe = '1h'
    
    def informative_pairs(self):
        pairs = self.dp.current_whitelist()
        informative_pairs = [(pair, self.informative_timeframe) for pair in pairs]
        return informative_pairs
    
    def bot_start(self, **kwargs) -> None:
        try:
            exchange = self.dp.exchange.name if hasattr(self.dp, 'exchange') and hasattr(self.dp.exchange, 'name') else 'binance'
            stake_currency = self.dp.stake_currency if hasattr(self.dp, 'stake_currency') else 'USDT'
            stake_amount = self.dp.stake_amount if hasattr(self.dp, 'stake_amount') else 'unlimited'
            
            startup_msg = f"""🤖 *FreqTrade Bot Startup - RSI+Bollinger*

*Exchange:* `{exchange}`
*Stake per trade:* `{stake_amount} {stake_currency}`
*Minimum ROI:* `{self.minimal_roi}`
*Trailing Stoploss:* `{self.stoploss}`
*Position adjustment:* `Off`
*Timeframe:* `{self.timeframe}`
*Strategy:* `RSI_BollingerStrategy`
*Startup candles:* `{self.startup_candle_count}`

Bot started successfully and ready to trade."""
            
            if hasattr(self.dp, 'send_msg'):
                self.dp.send_msg(startup_msg)
        except Exception as e:
            logger.warning(f"Could not send startup message: {e}")
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI for momentum
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        
        # Bollinger Bands
        bollinger = ta.BBANDS(dataframe, timeperiod=int(self.buy_bb_period.value), 
                              nbdevup=float(self.buy_bb_std.value), 
                              nbdevdn=float(self.buy_bb_std.value), matype=0)
        dataframe['bb_lowerband'] = bollinger['lowerband']
        dataframe['bb_middleband'] = bollinger['middleband']
        dataframe['bb_upperband'] = bollinger['upperband']
        dataframe['bb_percent'] = (dataframe['close'] - dataframe['bb_lowerband']) / (
            dataframe['bb_upperband'] - dataframe['bb_lowerband']
        )
        
        # EMA for trend
        dataframe['ema'] = ta.EMA(dataframe, timeperiod=21)
        
        # Average volume
        dataframe['volume_sma'] = dataframe['volume'].rolling(window=20).mean()
        
        # Informative timeframe (1h) for context
        informative = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe=self.informative_timeframe)
        informative['rsi'] = ta.RSI(informative, timeperiod=14)
        informative['ema'] = ta.EMA(informative, timeperiod=21)
        dataframe = merge_informative_pair(dataframe, informative, self.timeframe, self.informative_timeframe,
                                          ffill=True)
        
        return dataframe
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # RSI in favorable range
                (dataframe['rsi'] > self.buy_rsi_min.value) &
                (dataframe['rsi'] < self.buy_rsi_max.value) &
                # Price near lower band (expected bounce)
                (dataframe['bb_percent'] < self.buy_bb_percent.value) &
                # Price above EMA (bullish trend)
                (dataframe['close'] > dataframe['ema']) &
                # Bullish trend in higher timeframe
                (dataframe['close'] > dataframe[f'ema_{self.informative_timeframe}']) &
                (dataframe[f'rsi_{self.informative_timeframe}'] > 50) &
                # Volume confirmation
                (dataframe['volume'] > dataframe['volume_sma'] * self.buy_volume_factor.value) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1
        
        return dataframe
    
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Price touches upper band (overbought)
                (dataframe['bb_percent'] > 0.95) |
                # RSI overbought
                (dataframe['rsi'] > 75) |
                # Price crosses below EMA
                (dataframe['close'] < dataframe['ema']) &
                (dataframe['close'].shift(1) >= dataframe['ema'].shift(1)) |
                # Trend change in higher timeframe
                (dataframe['close'] < dataframe[f'ema_{self.informative_timeframe}']) |
                (dataframe[f'rsi_{self.informative_timeframe}'] < 40)
            ),
            'exit_long'] = 1
        
        return dataframe

