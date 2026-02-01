import logging

import talib.abstract as ta
from pandas import DataFrame

from freqtrade.strategy import DecimalParameter, IntParameter, IStrategy, merge_informative_pair

logger = logging.getLogger(__name__)


class EMACrossoverStrategy(IStrategy):
    """
    EMA crossover strategy with momentum confirmation.
    """

    INTERFACE_VERSION = 3

    # Optimizable parameters
    buy_ema_fast = IntParameter(5, 15, default=9, space="buy", optimize=True)
    buy_ema_mid = IntParameter(15, 30, default=21, space="buy", optimize=True)
    buy_ema_slow = IntParameter(30, 60, default=50, space="buy", optimize=True)
    buy_rsi_min = IntParameter(40, 55, default=50, space="buy", optimize=True)
    buy_rsi_max = IntParameter(60, 75, default=70, space="buy", optimize=True)
    volume_factor = DecimalParameter(1.0, 2.5, default=1.5, space="buy", optimize=True)

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
        dataframe["ema_fast"] = ta.EMA(dataframe, timeperiod=self.buy_ema_fast.value)
        dataframe["ema_mid"] = ta.EMA(dataframe, timeperiod=self.buy_ema_mid.value)
        dataframe["ema_slow"] = ta.EMA(dataframe, timeperiod=self.buy_ema_slow.value)

        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)

        macd = ta.MACD(dataframe, fastperiod=12, slowperiod=26, signalperiod=9)
        dataframe["macd"] = macd["macd"]
        dataframe["macdsignal"] = macd["macdsignal"]
        dataframe["macdhist"] = macd["macdhist"]

        dataframe["volume_sma"] = dataframe["volume"].rolling(window=20).mean()
        dataframe["atr"] = ta.ATR(dataframe, timeperiod=14)

        informative = self.dp.get_pair_dataframe(
            pair=metadata["pair"], timeframe=self.informative_timeframe
        )
        informative["ema_fast"] = ta.EMA(informative, timeperiod=9)
        informative["ema_slow"] = ta.EMA(informative, timeperiod=50)
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
                (dataframe["ema_fast"] > dataframe["ema_mid"])
                & (dataframe["ema_mid"] > dataframe["ema_slow"])
                & (dataframe["ema_fast"].shift(1) <= dataframe["ema_mid"].shift(1))
                & (
                    dataframe[f"ema_fast_{self.informative_timeframe}"]
                    > dataframe[f"ema_slow_{self.informative_timeframe}"]
                )
                & (dataframe["rsi"] > self.buy_rsi_min.value)
                & (dataframe["rsi"] < self.buy_rsi_max.value)
                & (dataframe["macd"] > dataframe["macdsignal"])
                & (dataframe["macdhist"] > 0)
                & (
                    dataframe["volume"]
                    > dataframe["volume_sma"] * self.volume_factor.value
                )
                & (dataframe["volume"] > 0)
            ),
            "enter_long",
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe["ema_fast"] < dataframe["ema_mid"])
                | (dataframe["macd"] < dataframe["macdsignal"])
                | (dataframe["rsi"] > 75)
                | (
                    dataframe[f"ema_fast_{self.informative_timeframe}"]
                    < dataframe[f"ema_slow_{self.informative_timeframe}"]
                )
                | (dataframe[f"rsi_{self.informative_timeframe}"] < 40)
            ),
            "exit_long",
        ] = 1

        return dataframe
