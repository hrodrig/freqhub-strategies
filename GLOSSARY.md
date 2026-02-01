/*
 * FreqHub Strategies - Curated Strategies for Freqtrade to be used with FreqHub
 * Copyright (C) 2025 - 2026  FreqHub Strategies Contributors
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 * ⚖️ DISCLAIMER
 * USE AT YOUR OWN RISK
 *
 * This software is provided "as is", without warranty of any kind, express or implied,
 * including but not limited to the warranties of merchantability, fitness for a particular
 * purpose and noninfringement. In no event shall the authors or copyright holders be liable
 * for any claim, damages or other liability, whether in an action of contract, tort or
 * otherwise, arising from, out of or in connection with the software or the use or other
 * dealings in the software.
 *
 * Trading cryptocurrencies involves substantial risk of loss and is not suitable for every
 * investor. The value of cryptocurrencies may fluctuate, and you may lose some or all of
 * your investment. Past performance is not indicative of future results.
 */

# Glossary

This glossary covers the most common terms used across strategies and configs.

## A

- **ADX (Average Directional Index)**: Measures trend strength, regardless of direction.
- **ADX Min**: Minimum ADX threshold used for trend strength filtering.
- **ATR (Average True Range)**: Volatility metric based on recent price ranges.
- **ATR Ratio/Percent**: ATR divided by price, used as a volatility filter.
- **ATR Min**: Minimum ATR percent threshold for volatility filtering.

## B

- **Bollinger Bands**: Volatility bands around a moving average using standard deviation.
- **BB Percent**: Position within Bollinger Bands (0 = lower band, 1 = upper band).
- **BB Period**: Lookback period used for Bollinger Band calculation.
- **BB Standard Deviation**: Standard deviation multiplier for Bollinger Bands.
- **BB Delta**: Absolute distance between the middle and lower Bollinger Bands.
- **BB Lower/Middle/Upper Band**: Individual Bollinger Band lines.
- **Break Even**: Price level where a trade has no profit or loss after fees.
- **Breakout Impulse**: Strong price move that breaks through a key level.
- **Breakout**: Price moving beyond a key level (support/resistance) with momentum.
- **Bullish Candle**: Candle where close is above open (upward move).
- **Bearish Candle**: Candle where close is below open (downward move).

## C

- **Chikou Span**: Ichimoku lagging line (current close shifted backward).
- **Candle Body**: Portion of a candle between open and close prices.
- **Candle Tail (Lower Tail/Wick)**: Distance between close and low of a candle.
- **Close Delta**: Absolute change between the current close and previous close.
- **Crossover**: When one indicator line crosses another (e.g., EMA crossover).
- **CORS**: Cross-Origin Resource Sharing, browser rules for API access.
- **Custom Stoploss**: Dynamic stoploss function that adjusts based on profit levels.

## D

- **Daily Bias Filter**: Entry filter based on higher timeframe trend direction.
- **Daily Profit Guard**: Rule that blocks new trades after a daily profit target.
- **Daily Profit Target**: Profit threshold used by the daily profit guard.
- **Drawdown**: Peak-to-trough decline in equity during a period.
- **Dry Run**: Simulated trading mode without real funds.
- **Dry Run Wallet**: Simulated balance used in dry-run mode.

## E

- **EMA (Exponential Moving Average)**: Moving average with more weight on recent prices.
- **EMA Crossover**: Signal where a shorter EMA crosses above/below a longer EMA.
- **Entry/Exit Signal**: Strategy rule that opens or closes a trade.

## F

- **Fibonacci Retracement**: Price levels (e.g., 38.2%, 61.8%) used to locate pullbacks.
- **Fractal (Bill Williams)**: Swing high/low pattern used to identify local turning points.
- **Fail ATR**: Maximum ATR distance below an impulse level that still qualifies as a failure to return.
- **FTR (Failure to Return)**: Breakout followed by a pullback that fails to retest a level.
- **Fast EMA / Slow EMA**: Shorter/longer period EMAs used for trend comparison.

## H

- **Hyperopt**: Automated parameter optimization in Freqtrade.
- **Hard Stoploss (HSL)**: Fixed stoploss level used before dynamic adjustments.

## I

- **Ichimoku Cloud**: Multi-line indicator for trend, support/resistance, momentum.
- **Informative Timeframe**: Higher timeframe data used to confirm lower timeframe signals.
- **Impulse Level**: Price level where a breakout impulse occurred, used as pullback reference.
- **Impulse Body ATR**: Minimum candle body size (in ATR multiples) for a valid impulse.

## J

- **JWT (JSON Web Token)**: Token used for API authentication.

## K

- **Kijun-sen**: Ichimoku base line (26-period midpoint).

## L

- **Leverage / Margin**: Borrowed capital used to increase position size (and risk).
- **Long**: Buy first, sell later (profit from price increases).
- **London Start/End Hour**: Session filter parameters for London trading hours.

## M

- **MACD (Moving Average Convergence Divergence)**: Momentum indicator based on EMA spreads.
- **MACD Signal Line**: EMA of MACD used for cross/confirmation.
- **Mean Reversion**: Expectation that price returns to an average after extremes.
- **Markov Chain**: Model where next state depends only on current state.
- **Markov State**: Discrete market state assigned by EMA/RSI conditions.
- **Momentum**: Strength or speed of price movement.
- **Momentum Confirmation**: Extra signal confirming momentum direction.

## N

- **NY Start/End Hour**: Session filter parameters for New York trading hours.

## O

- **Overbought / Oversold**: RSI levels indicating potential reversal zones.
- **Orderbook**: List of buy/sell orders used for pricing.

## P

- **Pair Whitelist/Blacklist**: Allowed/blocked trading pairs.
- **Pip**: Smallest standard price increment in Forex (usually 0.0001, or 0.01 for JPY pairs).
- **Pullback**: Temporary retracement against the prevailing trend.
- **Pullback Flag**: Outlier signal used to avoid extreme pullbacks.
- **Pullback Lookback**: Candle window used to search for recent pullbacks.
- **Pullback Recent**: Flag indicating a pullback occurred within the lookback window.
- **Pullback Zone**: ATR-bounded price range where pullback is expected.
- **Profit Factor (PF)**: Profit threshold that triggers stoploss adjustments.
- **Position Size**: Amount of capital allocated to a trade.

## R

- **Regime**: Market state (e.g., strong trend, consolidation).
- **Regime Classification**: Process of mapping price action to discrete states.
- **Re-engulf**: Price returns to and breaks through a prior breakout level.
- **Reengulf ATR**: Minimum ATR distance beyond impulse level to confirm re-engulfment.
- **Recent Impulse**: Flag indicating a breakout impulse occurred within a lookback window.
- **Return / Profitability**: How much gain or loss a strategy generates over a period (often expressed as ROI).
- **Retracement Area**: Price zone between Fibonacci levels (e.g., 38.2%–61.8%).
- **Risk/Reward (R:R)**: Expected gain versus potential loss in a trade.
- **ROI (Return on Investment)**: Profit target schedule in Freqtrade.
- **ROI Schedule**: Time-based profit targets (e.g., 10% @ 0m, 5% @ 4h).
- **ROI T1/T2/T3**: Time thresholds for multi-tier ROI schedules.
- **ROI P1/P2/P3/P4**: Profit targets for multi-tier ROI schedules.
- **RSI (Relative Strength Index)**: Momentum oscillator (0-100).
- **RSI Period**: Lookback period used for RSI calculation.
- **RSI High/Low**: Upper/lower RSI thresholds used for regime classification.

## S

- **Slippage**: Difference between expected and actual execution price.
- **Session Filter**: Entry restriction to specific trading hours.
- **Session OK**: Boolean condition that session filter is satisfied.
- **Stake Amount**: Capital allocated per trade.
- **Stake Currency**: Base currency used for trading (e.g., USDT, USD).
- **Senkou Span A/B**: Ichimoku leading lines that form the cloud.
- **Short**: Sell first, buy later (profit from price decreases).
- **Stop Loss**: Price level or percent to cut losses.
- **Stoploss Level (SL)**: Dynamic stoploss distance that increases with profit.
- **Stoploss Opt**: Optimizable stoploss parameter.
- **Support/Resistance**: Price zones where buying/selling pressure often appears.
- **Swing High/Low**: Local peaks and troughs in price.
- **Swing Range**: Price range between recent swing high and low.
- **State Transition**: Change between discrete market states.
- **Spot Trading**: Buying/selling assets for immediate delivery.
- **Stationarity**: Assumption that statistical properties remain stable over time.
- **Spread**: Difference between the best bid and ask prices.

## T

- **Tenkan-sen**: Ichimoku conversion line (9-period midpoint).
- **Timeframe**: Candle interval (e.g., 5m, 1h, 1d).
- **Trailing Stop**: Dynamic stop that follows price in profit.
- **Trading Session**: Active market hours (e.g., London, New York).
- **Trend Filter**: Condition requiring trend alignment before entry.
- **Trend vs Range**: Trending market versus sideways (range-bound) market.
- **Trend Indicator**: Ichimoku-derived signal indicating bullish/bearish bias.
- **Trend Above Senkou**: Distance above the Ichimoku cloud used for bullish confirmation.
- **Trend Bullish Level**: Tenkan/Kijun relationship indicating bullish strength.

## U

- **Use Daily Profit Guard**: Boolean flag that enables daily profit blocking.
- **Use Session Filter**: Boolean flag that enables session-based entry filtering.

## V

- **Volatility Filter**: Condition requiring minimum volatility (e.g., ATR/price).
- **Volatility**: How much and how fast price moves over time; higher volatility means larger swings.
- **Volatility OK**: Boolean condition that volatility filter is satisfied.
- **Volume SMA**: Moving average of volume for activity confirmation.
- **Volume SMA Period**: Lookback window for volume moving average.
- **Volume Confirmation**: Requirement that volume exceeds its moving average.
- **Volume Factor**: Multiplier used for volume confirmation thresholds.
- **Volume Fan**: Volume analysis using EMA ratios to confirm trend strength.
- **Fan Magnitude**: Volume change ratio compared to historical average.
- **Fan Magnitude Gain**: Rolling average of fan magnitude for confirmation.

## W

- **Valid Range**: Condition ensuring swing range is positive before calculations.

