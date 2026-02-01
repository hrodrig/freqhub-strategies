import logging

import pandas as pd
import talib.abstract as ta
from pandas import DataFrame

from freqtrade.strategy import DecimalParameter, IntParameter, IStrategy, merge_informative_pair

logger = logging.getLogger(__name__)


class RSIEMA50Strategy(IStrategy):
    """
    RSI + EMA50 trend-following strategy with momentum confirmation.
    """

    INTERFACE_VERSION = 3

    # Optimizable parameters
    buy_rsi_min = IntParameter(45, 60, default=50, space="buy", optimize=True)
    buy_rsi_max = IntParameter(65, 80, default=70, space="buy", optimize=True)
    buy_ema_period = IntParameter(40, 60, default=50, space="buy", optimize=True)
    buy_volume_factor = DecimalParameter(1.0, 2.5, default=1.5, space="buy", optimize=True)

    # Fixed parameters
    timeframe = "15m"
    startup_candle_count = 30
    stoploss = -0.06
    trailing_stop = True
    trailing_stop_positive = 0.015
    trailing_stop_positive_offset = 0.025
    trailing_only_offset_is_reached = True
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False
    can_short = False

    minimal_roi = {
        "0": 0.10,
        "30": 0.05,
        "60": 0.03,
        "120": 0.01,
    }

    informative_timeframe = "1h"

    def informative_pairs(self):
        pairs = self.dp.current_whitelist()
        return [(pair, self.informative_timeframe) for pair in pairs]

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ema"] = ta.EMA(dataframe, timeperiod=int(self.buy_ema_period.value))
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)

        macd = ta.MACD(dataframe, fastperiod=12, slowperiod=26, signalperiod=9)
        dataframe["macd"] = macd["macd"]
        dataframe["macdsignal"] = macd["macdsignal"]
        dataframe["macdhist"] = macd["macdhist"]

        dataframe["volume_sma"] = dataframe["volume"].rolling(window=20).mean()

        informative = self.dp.get_pair_dataframe(
            pair=metadata["pair"], timeframe=self.informative_timeframe
        )
        informative["ema"] = ta.EMA(informative, timeperiod=50)
        informative["rsi"] = ta.RSI(informative, timeperiod=14)
        dataframe = merge_informative_pair(
            dataframe,
            informative,
            self.timeframe,
            self.informative_timeframe,
            ffill=True,
        )

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe["close"] > dataframe["ema"])
                & (dataframe["rsi"] > self.buy_rsi_min.value)
                & (dataframe["rsi"] < self.buy_rsi_max.value)
                & (dataframe["macd"] > dataframe["macdsignal"])
                & (dataframe["close"] > dataframe[f"ema_{self.informative_timeframe}"])
                & (dataframe[f"rsi_{self.informative_timeframe}"] > 50)
                & (
                    dataframe["volume"]
                    > dataframe["volume_sma"] * self.buy_volume_factor.value
                )
                & (dataframe["volume"] > 0)
            ),
            "enter_long",
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (
                    (dataframe["close"] < dataframe["ema"])
                    & (dataframe["close"].shift(1) >= dataframe["ema"].shift(1))
                )
                | (dataframe["rsi"] > 75)
                | (dataframe["macd"] < dataframe["macdsignal"])
                | (dataframe["close"] < dataframe[f"ema_{self.informative_timeframe}"])
                | (dataframe[f"rsi_{self.informative_timeframe}"] < 40)
            ),
            "exit_long",
        ] = 1

        return dataframe
