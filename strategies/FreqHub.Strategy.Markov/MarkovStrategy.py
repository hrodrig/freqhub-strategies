import logging
from datetime import datetime, timezone
from typing import Optional, Tuple

import numpy as np
import talib.abstract as ta
from pandas import DataFrame

from freqtrade.strategy import DecimalParameter, IntParameter, IStrategy

logger = logging.getLogger(__name__)


class MarkovStrategy(IStrategy):
    """
    Markov strategy using discrete market states.
    Uses EMA and RSI to classify 4 states and trade state transitions.
    """

    INTERFACE_VERSION = 3

    # --- General parameters (optimized via properties below) ---
    timeframe = "1h"
    startup_candle_count = 60

    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # --- Optimizable ROI/stoploss parameters ---
    roi_t1 = IntParameter(60, 240, default=240, space="sell", optimize=True)
    roi_t2 = IntParameter(240, 720, default=720, space="sell", optimize=True)
    roi_t3 = IntParameter(720, 1440, default=1440, space="sell", optimize=True)
    roi_p1 = DecimalParameter(0.04, 0.20, default=0.10, space="sell", optimize=True)
    roi_p2 = DecimalParameter(0.02, 0.12, default=0.05, space="sell", optimize=True)
    roi_p3 = DecimalParameter(0.01, 0.08, default=0.02, space="sell", optimize=True)
    roi_p4 = DecimalParameter(0.005, 0.04, default=0.01, space="sell", optimize=True)
    stoploss_opt = DecimalParameter(-0.20, -0.03, default=-0.05, space="sell", optimize=True)

    # --- Indicator parameters ---
    slow_ema = 55
    rsi_period = 14
    rsi_high = 60
    rsi_low = 40
    adx_period = 14
    atr_period = 14

    # --- Optimizable filters ---
    adx_min = DecimalParameter(15.0, 35.0, default=20.0, space="buy", optimize=True)
    atr_min = DecimalParameter(0.003, 0.03, default=0.01, space="buy", optimize=True)
    sell_rsi_overbought = IntParameter(65, 85, default=75, space="sell", optimize=True)

    # --- Daily profit guard ---
    _current_day = None
    _daily_profit_checked = False
    _daily_profit_positive = False

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ema_slow"] = ta.EMA(dataframe, timeperiod=self.slow_ema)
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=self.rsi_period)
        dataframe["adx"] = ta.ADX(dataframe, timeperiod=self.adx_period)
        dataframe["atr"] = ta.ATR(dataframe, timeperiod=self.atr_period)
        dataframe["atr_percent"] = dataframe["atr"] / dataframe["close"]

        conditions = [
            (dataframe["close"] < dataframe["ema_slow"])
            & (dataframe["rsi"] < self.rsi_low),
            (dataframe["close"] < dataframe["ema_slow"])
            & (dataframe["rsi"] >= self.rsi_low),
            (dataframe["close"] > dataframe["ema_slow"])
            & (dataframe["rsi"] < self.rsi_high),
            (dataframe["close"] > dataframe["ema_slow"])
            & (dataframe["rsi"] >= self.rsi_high),
        ]

        choices = [0, 1, 2, 3]
        dataframe["markov_state"] = np.select(conditions, choices, default=1)
        dataframe["prev_state"] = dataframe["markov_state"].shift(1)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (
                    ((dataframe["prev_state"] == 0) & (dataframe["markov_state"] == 1))
                    | ((dataframe["prev_state"] == 1) & (dataframe["markov_state"] == 2))
                    | ((dataframe["prev_state"] == 2) & (dataframe["markov_state"] == 3))
                )
                & (dataframe["adx"] > self.adx_min.value)
                & (dataframe["atr_percent"] > self.atr_min.value)
            ),
            "enter_long",
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                ((dataframe["prev_state"] == 3) & (dataframe["markov_state"] == 2))
                | ((dataframe["prev_state"] == 2) & (dataframe["markov_state"] == 1))
                | (dataframe["markov_state"] == 0)
                | (dataframe["rsi"] > self.sell_rsi_overbought.value)
            ),
            "exit_long",
        ] = 1

        return dataframe

    def get_daily_profit(self) -> Tuple[float, bool]:
        """
        Calculate profit for the current day.
        Returns: (profit_total, has_profit)
        """
        try:
            now = datetime.now(timezone.utc)
            current_day = now.date()

            if self._current_day != current_day:
                self._current_day = current_day
                self._daily_profit_checked = False
                self._daily_profit_positive = False

            if self._daily_profit_checked:
                return (0.0, self._daily_profit_positive)

            daily_profit = 0.0
            has_profit = False

            if hasattr(self.dp, "wallets"):
                try:
                    if hasattr(self.dp.wallets, "get_today_profit"):
                        daily_profit = self.dp.wallets.get_today_profit()
                        has_profit = daily_profit > 0.0
                        logger.info(
                            "Daily profit (wallets): %.4f USDT",
                            daily_profit,
                        )
                    elif hasattr(self.dp.wallets, "get_profit"):
                        start_of_day = datetime.combine(
                            current_day, datetime.min.time()
                        ).replace(tzinfo=timezone.utc)
                        profit_data = self.dp.wallets.get_profit(start_of_day, now)
                        if profit_data and hasattr(profit_data, "profit_abs"):
                            daily_profit = profit_data.profit_abs
                            has_profit = daily_profit > 0.0
                            logger.info(
                                "Daily profit (get_profit): %.4f USDT",
                                daily_profit,
                            )
                except Exception as e:
                    logger.debug("Could not get wallet profit: %s", e)

            if not self._daily_profit_checked and hasattr(self.dp, "trade"):
                try:
                    if hasattr(self.dp.trade, "get_closed_trades"):
                        closed_trades = self.dp.trade.get_closed_trades()
                        if closed_trades:
                            for trade in closed_trades:
                                if hasattr(trade, "close_date") and trade.close_date:
                                    close_date = trade.close_date
                                    if isinstance(close_date, datetime):
                                        if close_date.date() == current_day:
                                            if (
                                                hasattr(trade, "profit_abs")
                                                and trade.profit_abs
                                            ):
                                                daily_profit += trade.profit_abs
                    elif hasattr(self.dp.trade, "get_trades"):
                        all_trades = self.dp.trade.get_trades()
                        if all_trades:
                            for trade in all_trades:
                                if hasattr(trade, "is_open") and not trade.is_open:
                                    if hasattr(trade, "close_date") and trade.close_date:
                                        close_date = trade.close_date
                                        if isinstance(close_date, datetime):
                                            if close_date.date() == current_day:
                                                if (
                                                    hasattr(trade, "profit_abs")
                                                    and trade.profit_abs
                                                ):
                                                    daily_profit += trade.profit_abs
                except Exception as e:
                    logger.debug("Could not get closed trades: %s", e)

            has_profit = daily_profit > 0.0

            self._daily_profit_checked = True
            self._daily_profit_positive = has_profit

            if daily_profit != 0.0 or has_profit:
                logger.info(
                    "Daily profit %s: %.4f USDT, has profit: %s",
                    current_day,
                    daily_profit,
                    has_profit,
                )

            return (daily_profit, has_profit)
        except Exception as e:
            logger.warning("Error calculating daily profit: %s", e)
            return (0.0, False)

    @property
    def minimal_roi(self):
        if hasattr(self, "_minimal_roi_override") and self._minimal_roi_override is not None:
            return self._minimal_roi_override
        return {
            "0": float(self.roi_p1.value),
            str(int(self.roi_t1.value)): float(self.roi_p2.value),
            str(int(self.roi_t2.value)): float(self.roi_p3.value),
            str(int(self.roi_t3.value)): float(self.roi_p4.value),
        }

    @minimal_roi.setter
    def minimal_roi(self, value):
        self._minimal_roi_override = value

    @property
    def stoploss(self):
        if hasattr(self, "_stoploss_override") and self._stoploss_override is not None:
            return self._stoploss_override
        return float(self.stoploss_opt.value)

    @stoploss.setter
    def stoploss(self, value):
        self._stoploss_override = value

    def confirm_trade_entry(
        self,
        pair: str,
        order_type: str,
        amount: float,
        rate: float,
        time_in_force: str,
        current_time: datetime,
        entry_tag: Optional[str],
        side: str,
        **kwargs,
    ) -> bool:
        """
        Block new entries if there is already positive profit today.
        """
        try:
            daily_profit, has_profit = self.get_daily_profit()
            if has_profit:
                logger.info(
                    "Blocking entry for %s: daily profit already positive (%.4f USDT)",
                    pair,
                    daily_profit,
                )
                return False
            return True
        except Exception as e:
            logger.warning("Error in confirm_trade_entry: %s", e)
            return True
