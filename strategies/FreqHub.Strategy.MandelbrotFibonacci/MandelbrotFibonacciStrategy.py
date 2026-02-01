import logging

import talib.abstract as ta
from pandas import DataFrame

from freqtrade.strategy import DecimalParameter, IStrategy

logger = logging.getLogger(__name__)


class MandelbrotFibonacciStrategy(IStrategy):
    """
    Mandelbrot + Fibonacci Strategy

    Uses Bill Williams-style fractals to define swing ranges and
    Fibonacci retracements to identify pullback zones in trend.
    """

    INTERFACE_VERSION = 3

    # Optimizable parameters
    fib_low = DecimalParameter(0.35, 0.45, default=0.382, space="buy", optimize=True)
    fib_high = DecimalParameter(0.55, 0.7, default=0.618, space="buy", optimize=True)
    volume_factor = DecimalParameter(0.8, 2.0, default=1.0, space="buy", optimize=True)

    # Fixed parameters
    timeframe = "1h"
    stoploss = -0.08
    trailing_stop = True
    trailing_stop_positive = 0.015
    trailing_stop_positive_offset = 0.03
    trailing_only_offset_is_reached = True
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False
    startup_candle_count = 210
    can_short = False

    minimal_roi = {
        "0": 0.06,
        "360": 0.03,
        "720": 0.01
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ema_fast"] = ta.EMA(dataframe, timeperiod=50)
        dataframe["ema_slow"] = ta.EMA(dataframe, timeperiod=200)
        dataframe["volume_sma"] = dataframe["volume"].rolling(window=20).mean()

        fractal_high = (
            (dataframe["high"] > dataframe["high"].shift(1)) &
            (dataframe["high"] > dataframe["high"].shift(2)) &
            (dataframe["high"] >= dataframe["high"].shift(-1)) &
            (dataframe["high"] >= dataframe["high"].shift(-2))
        )
        fractal_low = (
            (dataframe["low"] < dataframe["low"].shift(1)) &
            (dataframe["low"] < dataframe["low"].shift(2)) &
            (dataframe["low"] <= dataframe["low"].shift(-1)) &
            (dataframe["low"] <= dataframe["low"].shift(-2))
        )

        dataframe["fractal_high"] = dataframe["high"].where(fractal_high).shift(2)
        dataframe["fractal_low"] = dataframe["low"].where(fractal_low).shift(2)

        dataframe["swing_high"] = dataframe["fractal_high"].ffill()
        dataframe["swing_low"] = dataframe["fractal_low"].ffill()
        dataframe["swing_range"] = dataframe["swing_high"] - dataframe["swing_low"]

        dataframe["fib_382_long"] = dataframe["swing_high"] - dataframe["swing_range"] * self.fib_low.value
        dataframe["fib_618_long"] = dataframe["swing_high"] - dataframe["swing_range"] * self.fib_high.value

        dataframe["fib_382_short"] = dataframe["swing_low"] + dataframe["swing_range"] * self.fib_low.value
        dataframe["fib_618_short"] = dataframe["swing_low"] + dataframe["swing_range"] * self.fib_high.value

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        trend_up = (dataframe["ema_fast"] > dataframe["ema_slow"]) & (dataframe["close"] > dataframe["ema_slow"])
        trend_down = (dataframe["ema_fast"] < dataframe["ema_slow"]) & (dataframe["close"] < dataframe["ema_slow"])
        volume_ok = (dataframe["volume"] > dataframe["volume_sma"] * self.volume_factor.value) & (
            dataframe["volume"] > 0
        )

        fib_long_low = dataframe[["fib_382_long", "fib_618_long"]].min(axis=1)
        fib_long_high = dataframe[["fib_382_long", "fib_618_long"]].max(axis=1)

        fib_short_low = dataframe[["fib_382_short", "fib_618_short"]].min(axis=1)
        fib_short_high = dataframe[["fib_382_short", "fib_618_short"]].max(axis=1)

        valid_range = dataframe["swing_range"] > 0

        dataframe.loc[
            (
                valid_range &
                trend_up &
                volume_ok &
                (dataframe["close"] >= fib_long_low) &
                (dataframe["close"] <= fib_long_high) &
                (dataframe["close"] > dataframe["ema_fast"]) &
                (dataframe["close"] > dataframe["open"])
            ),
            "enter_long"
        ] = 1

        dataframe.loc[
            (
                valid_range &
                trend_down &
                volume_ok &
                (dataframe["close"] >= fib_short_low) &
                (dataframe["close"] <= fib_short_high) &
                (dataframe["close"] < dataframe["ema_fast"]) &
                (dataframe["close"] < dataframe["open"])
            ),
            "enter_short"
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                ((dataframe["close"] < dataframe["ema_fast"]) &
                 (dataframe["close"].shift(1) >= dataframe["ema_fast"].shift(1))) |
                (dataframe["close"] < dataframe["ema_slow"])
            ),
            "exit_long"
        ] = 1

        dataframe.loc[
            (
                ((dataframe["close"] > dataframe["ema_fast"]) &
                 (dataframe["close"].shift(1) <= dataframe["ema_fast"].shift(1))) |
                (dataframe["close"] > dataframe["ema_slow"])
            ),
            "exit_short"
        ] = 1

        return dataframe
