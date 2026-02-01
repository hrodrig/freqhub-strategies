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

# FreqHub FailureToReturn Strategy

Practical implementation of the Failure to Return (FTR) concept, designed for
trend-following entries after a breakout and a controlled pullback that fails
to revisit the prior support or resistance. This approach is especially
recommended for Forex pairs where clean structure and liquid sessions help
validate the pattern.

FreqHub reference: https://github.com/hrodrig/freqhub

## Strategy Summary

| Feature | Value |
|----------------|-------|
| **Risk Level** | Medium |
| **Stop Loss** | -8% |
| **Trailing Stop** | Enabled (1.0% activation / 2.0% offset) |
| **Target ROI** | 4% initial, 3% after 4h, 1% after 12h |
| **Timeframe** | 1h |
| **Max Open Trades** | 2 (from `config.json.example`) |
| **Recommended Pairs** | EUR/USD, GBP/USD, USD/JPY |
| **Best For** | Trend continuation after failed pullback |
| **Sides** | Long + Short (Futures) |

## About the Strategy

The FTR pattern focuses on a key principle: after a strong breakout, the market
often tries to return to the previous level but fails to reach it. That failure
creates a new base or zone (the FTR zone). When price revisits that zone and
re-engulfs the breakout direction, we seek a continuation entry.

This strategy models that behavior with simple, explainable rules:

1. Identify a prior swing level (support/resistance).
2. Confirm a strong breakout above that level.
3. Wait for a pullback that fails to fully return below the level.
4. Enter on re-engulfment with trend and volume confirmation.

## Strategy Logic

### Indicators Used

- **ATR (14)** to size breakout and pullback thresholds.
- **EMA 50 / EMA 200** for trend direction.
- **Volume SMA (20)** for basic confirmation.
- **Rolling swing high** for structural resistance.

### Entry Conditions (Long)

The strategy opens a long when all of the following are true:

1. **Trend filter**: price above EMA 200 and EMA 50 above EMA 200.
2. **Breakout impulse**: close breaks the recent swing high by a minimum ATR
   threshold and the candle body is strong.
3. **Failure to return**: price pulls back toward the breakout level but does
   not reclaim it (stays above the level by a small ATR buffer).
4. **Re-engulf**: price closes back above the breakout level with strength.
5. **Volume confirmation**: volume above its rolling average.
6. **Session filter**: only during London or New York sessions.
7. **Volatility filter**: ATR/price above a minimum threshold.

### Entry Conditions (Short)

The short setup mirrors the long logic:

1. **Trend filter**: price below EMA 200 and EMA 50 below EMA 200.
2. **Breakout impulse**: close breaks the recent swing low by a minimum ATR
   threshold and the candle body is strong.
3. **Failure to return**: price pulls back toward the breakout level but does
   not reclaim it (stays below the level by a small ATR buffer).
4. **Re-engulf**: price closes back below the breakout level with strength.
5. **Volume confirmation**: volume above its rolling average.
6. **Session filter**: only during London or New York sessions.
7. **Volatility filter**: ATR/price above a minimum threshold.

### Exit Conditions

Positions are closed when trend momentum weakens:

- Close crosses below EMA 50, or
- Close falls back under EMA 200.

Shorts close when:

- Close crosses above EMA 50, or
- Close rises back above EMA 200.

## Why This Works

FTR setups align with continuation flows: the breakout establishes a new order
imbalance, the pullback tests liquidity, and the failure to return suggests
buyers or sellers are defending the new structure. This is particularly clean
in Forex during liquid sessions and clear trends.

## Pros

- Clear, rule-based structure tied to market mechanics.
- Works well in trending Forex pairs with strong liquidity.
- Uses volatility (ATR) to adapt to different regimes.

## Cons

- Underperforms in choppy, mean-reverting markets.
- Requires clean swing structure; noisy price action can mislead signals.
- FTR zones can be subjective in discretionary trading.

## Risk and Performance Notes

- Best in trending conditions; avoid low-volatility ranges.
- London (07:00-16:00 UTC) and New York (12:00-21:00 UTC) session filter is
  enforced by default to avoid low-liquidity hours, but it is configurable.
- A minimum ATR/price ratio filter reduces trades in dead ranges.
- You can also add a **daily bias filter** (e.g., based on prior daily close,
  daily trend, or session volume) as an optional entry gate.
  A simple approach is to create a daily trend flag from a higher timeframe
  (like `1d`), then require that flag to agree with the entry direction.
- Always forward-test in dry-run before risking capital.

Example pseudocode:

```python
daily_trend_up = close_1d > ema_1d
daily_trend_down = close_1d < ema_1d

if enter_long_signal and daily_trend_up:
    allow_long_entry()

if enter_short_signal and daily_trend_down:
    allow_short_entry()
```

Alternative (prior day close bias):

```python
daily_bias_up = close_1d > close_1d.shift(1)
daily_bias_down = close_1d < close_1d.shift(1)

if enter_long_signal and daily_bias_up:
    allow_long_entry()

if enter_short_signal and daily_bias_down:
    allow_short_entry()
```

Alternative (session volume confirmation):

```python
session_volume_ok = session_volume > session_volume_sma

if enter_long_signal and session_volume_ok:
    allow_long_entry()

if enter_short_signal and session_volume_ok:
    allow_short_entry()
```

## Contents

- `FailureToReturnStrategy.py`: strategy code
- `config.json.example`: example Freqtrade config for this strategy
- `config.header.txt`: GPL header to keep alongside the config
- `requirements.txt`: optional extra dependencies installed during image build

## Setup

Copy the example config and edit it:

```bash
cp config.json.example config.json
```

For shorting, ensure your exchange and Freqtrade setup supports futures/shorts.
Spot-only setups will ignore `enter_short` signals.

## Exchange Notes

Freqtrade uses **CCXT** exchanges. Some popular FX brokers (like OANDA) are **not**
available via CCXT, so they will fail with `Exchange "oanda" is not known...`.

Use a **supported** exchange name and ensure the pairs exist on that venue.
If you cannot trade FX pairs on your chosen exchange, replace the FX pairs
with crypto pairs and adjust the strategy accordingly.

For the full, up-to-date list of supported exchanges, see:
https://www.freqtrade.io/en/stable/exchanges/

## Tunable Parameters

The strategy exposes key knobs for optimization:

- **Session filter**: `use_session_filter`, `london_start_hour`, `london_end_hour`,
  `ny_start_hour`, `ny_end_hour` (UTC hours).
- **Volatility filter**: `min_atr_ratio` to avoid dead ranges.
- **Daily profit guard**: `use_daily_profit_guard` and `daily_profit_target`
  (ratio, `0.01` = 1%).

Note: The daily profit guard relies on trade history and is intended for
live/dry-run. It is not suitable for backtesting/hyperopt.

## Run the Bot

1) Ensure the shared network exists (usually created by FreqHub):

```bash
./scripts/net up
```

1) Preferably use the helper script from repo root:

```bash
./scripts/bot up strategies/FreqHub.Strategy.FailureToReturn
```

1) Stop the bot (preferred):

```bash
./scripts/bot down strategies/FreqHub.Strategy.FailureToReturn
```

Alternative (manual compose):

```bash
docker compose -f strategies/FreqHub.Strategy.FailureToReturn/docker-compose.yml up -d --build
```

```bash
docker compose -f strategies/FreqHub.Strategy.FailureToReturn/docker-compose.yml down
```

Notes:

- The API is exposed on `http://localhost:8018` (see `docker-compose.yml`).
- Use port `8010` for the template. For additional strategies, use `8011+`
  (e.g. 8011, 8012, 8013) and avoid port collisions.
- To change ports, edit the `ports:` section in `docker-compose.yml`.

## References

- https://xchief.academy/forex-ftr-training/
- https://www.freqtrade.io/

## License

This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

**Copyright (C) 2025 - 2026 FreqHub Contributors**

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

## Acknowledgments

- [Freqtrade](https://github.com/freqtrade/freqtrade) - The amazing trading bot this project is built for
- [FreqHub](https://github.com/hrodrig/freqhub) - Amazing UI for Freqtrade with multi-bots
- [FreqUI](https://github.com/freqtrade/frequi) - Inspiration and reference implementation

## Support

- **Issues**: [GitHub Issues](https://github.com/hrodrig/freqhub-strategies/issues)
- **Discussions**: [GitHub Discussions](https://github.com/hrodrig/freqhub-strategies/discussions)
- **Donations**: [Donations](DONATIONS.md)

---

**Note**: FreqHub Strategies is an independent project and is not officially affiliated with the Freqtrade project.
