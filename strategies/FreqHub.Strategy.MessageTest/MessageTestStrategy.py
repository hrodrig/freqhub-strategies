import logging

from pandas import DataFrame

from freqtrade.strategy import IStrategy

logger = logging.getLogger(__name__)


class MessageTestStrategy(IStrategy):
    """
    Messaging test strategy that alternates buy/sell every candle.
    """

    INTERFACE_VERSION = 3

    timeframe = "15m"
    startup_candle_count = 10
    stoploss = -0.10
    trailing_stop = False
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False
    can_short = False

    minimal_roi = {
        "0": 0.01,
        "15": 0.005,
        "30": 0.002,
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["candle_count"] = range(len(dataframe))
        dataframe["should_buy"] = (dataframe["candle_count"] % 2 == 0).astype(int)
        dataframe["should_sell"] = (dataframe["candle_count"] % 2 == 1).astype(int)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe["should_buy"] == 1) & (dataframe["volume"] > 0),
            "enter_long",
        ] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe["should_sell"] == 1) & (dataframe["volume"] > 0),
            "exit_long",
        ] = 1
        return dataframe
