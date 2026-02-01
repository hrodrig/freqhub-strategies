import logging

import freqtrade.vendor.qtpylib.indicators as qtpylib
from pandas import DataFrame

from freqtrade.strategy import IntParameter, IStrategy

logger = logging.getLogger(__name__)


class BinHV45Strategy(IStrategy):
    INTERFACE_VERSION: int = 3

    minimal_roi = {"0": 0.0125}
    stoploss = -0.05
    timeframe = "15m"
    startup_candle_count = 50

    buy_bbdelta = IntParameter(low=1, high=15, default=7, space="buy", optimize=True)
    buy_closedelta = IntParameter(low=15, high=20, default=17, space="buy", optimize=True)
    buy_tail = IntParameter(low=20, high=30, default=25, space="buy", optimize=True)

    buy_params = {
        "buy_bbdelta": 7,
        "buy_closedelta": 17,
        "buy_tail": 25,
    }

    def bot_start(self, **kwargs) -> None:
        """
        Runs when the bot starts. Sends a startup message using configured messaging.
        """
        try:
            exchange = (
                self.dp.exchange.name
                if hasattr(self.dp, "exchange") and hasattr(self.dp.exchange, "name")
                else "binance"
            )
            stake_currency = (
                self.dp.stake_currency if hasattr(self.dp, "stake_currency") else "USDT"
            )
            stake_amount = (
                self.dp.stake_amount if hasattr(self.dp, "stake_amount") else "unlimited"
            )

            startup_msg = (
                "🤖 *FreqTrade Bot Startup - BinHV45Strategy*\n\n"
                f"*Exchange:* `{exchange}`\n"
                f"*Stake per trade:* `{stake_amount} {stake_currency}`\n"
                f"*Minimum ROI:* `{self.minimal_roi}`\n"
                f"*Stop Loss:* `{self.stoploss}`\n"
                "*Position adjustment:* `Off`\n"
                f"*Timeframe:* `{self.timeframe}`\n"
                "*Strategy:* `BinHV45Strategy`\n"
                f"*Startup candles:* `{self.startup_candle_count}`\n\n"
                "Bot started successfully and ready to trade."
            )

            if hasattr(self.dp, "send_msg"):
                self.dp.send_msg(startup_msg)
        except Exception as e:
            logger.warning("Could not send startup message: %s", e)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        bollinger = qtpylib.bollinger_bands(dataframe["close"], window=40, stds=2)

        dataframe["upper"] = bollinger["upper"]
        dataframe["mid"] = bollinger["mid"]
        dataframe["lower"] = bollinger["lower"]
        dataframe["bbdelta"] = (dataframe["mid"] - dataframe["lower"]).abs()
        dataframe["pricedelta"] = (dataframe["open"] - dataframe["close"]).abs()
        dataframe["closedelta"] = (dataframe["close"] - dataframe["close"].shift()).abs()
        dataframe["tail"] = (dataframe["close"] - dataframe["low"]).abs()
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                dataframe["lower"].shift().gt(0)
                & dataframe["bbdelta"].gt(
                    dataframe["close"] * self.buy_bbdelta.value / 1000
                )
                & dataframe["closedelta"].gt(
                    dataframe["close"] * self.buy_closedelta.value / 1000
                )
                & dataframe["tail"].lt(
                    dataframe["bbdelta"] * self.buy_tail.value / 1000
                )
                & dataframe["close"].lt(dataframe["lower"].shift())
                & dataframe["close"].le(dataframe["close"].shift())
            ),
            "enter_long",
        ] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        No custom exit signal - exits rely on ROI/stoploss.
        """
        dataframe.loc[:, "exit_long"] = 0
        return dataframe
