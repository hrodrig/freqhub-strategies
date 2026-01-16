from pandas import DataFrame
import talib.abstract as ta

from freqtrade.strategy.interface import IStrategy


class TemplateStrategy(IStrategy):
    """
    Minimal example strategy.
    """

    minimal_roi = {"0": 0.04}
    stoploss = -0.10
    timeframe = "5m"
    startup_candle_count = 50

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ema_fast"] = ta.EMA(dataframe, timeperiod=12)
        dataframe["ema_slow"] = ta.EMA(dataframe, timeperiod=26)
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe["ema_fast"] > dataframe["ema_slow"])
                & (dataframe["rsi"] < 30)
            ),
            "enter_long",
        ] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe["ema_fast"] < dataframe["ema_slow"])
                | (dataframe["rsi"] > 70)
            ),
            "exit_long",
        ] = 1
        return dataframe
