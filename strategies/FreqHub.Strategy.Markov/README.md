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

# FreqHub Markov Strategy

**MarkovStrategy** is based on a **discrete Markov chain** to detect regime
changes using a slow EMA and RSI.

FreqHub reference: https://github.com/hrodrig/freqhub

## 📊 Strategy Summary

| Feature | Value |
|----------------|-------|
| **Risk Level** | 🟡 Medium |
| **Stop Loss** | -5% |
| **Target ROI** | 10% inicial, luego 5% @ 4h, 2% @ 12h, 1% @ 24h |
| **Timeframe** | 1h |
| **Max Open Trades** | 5 (from `config.json.example`) |
| **Stake per Trade** | Unlimited (from `config.json.example`) |
| **Mode** | Dry Run by default (configurable) |
| **Daily Rule** | If there's profit today, no more trades |

## 🧠 Strategy Logic

### The Markov idea (discrete regimes)

This strategy models the market as a **finite-state Markov chain**. Each candle
is mapped to a regime (state) based on trend + momentum. The key assumption is
that the **next state depends only on the current state**, so we trade **state
transitions** rather than raw indicator thresholds.

### Regime classification (4 states)

We use a slow EMA and RSI to discretize the market into 4 states:

- **State 0 (Strong Bear):** price < slow EMA and RSI < 40
- **State 1 (Weak Bear / correction):** price < slow EMA and RSI >= 40
- **State 2 (Weak Bull / consolidation):** price > slow EMA and RSI < 60
- **State 3 (Strong Bull):** price > slow EMA and RSI >= 60

This creates a simple, interpretable market "map" where each candle has a
single state label.

### Transitions (the chain)

We detect the **transition** by comparing the current state with the previous
one (`prev_state` vs `markov_state`). The transitions encode regime change:

- **0 ➜ 1:** bearish exhaustion begins
- **1 ➜ 2:** bearish to bullish shift
- **2 ➜ 3:** bullish acceleration

### Entry (Long)

We open a position only when a bullish transition occurs:

- 0 ➜ 1
- 1 ➜ 2
- 2 ➜ 3

Additional quality filters:

- **ADX > `adx_min`** to avoid weak / noisy trends
- **ATR% > `atr_min`** to avoid very low volatility regimes

### Exit

We exit on loss of regime strength:

- 3 ➜ 2
- 2 ➜ 1
- or drop to **State 0**

Extra exit:

- **RSI > `sell_rsi_overbought`** to protect gains in overbought conditions

### Why this helps

Instead of "RSI < X => buy", the strategy uses **context**: it only acts when
the market **changes state**. This reduces noisy entries and improves timing
around regime shifts.

### Markov assumption warning

Markov models assume **stationarity**: transition probabilities remain stable.
In crypto, regime changes can be abrupt (news, black swans). Keep stoploss
strict and backtest in multiple regimes.

### Daily profit rule

If the bot detects **positive profit** for the current UTC day, it blocks
new entries until the next day.

## 🧪 Hyperopt

Optimizable parameters:

- `roi_t1`, `roi_t2`, `roi_t3`
- `roi_p1`, `roi_p2`, `roi_p3`, `roi_p4`
- `stoploss_opt`
- `adx_min`, `atr_min`
- `sell_rsi_overbought`

### Tuning tips

- **RSI bounds:** try tightening (35/65) or widening (30/70)
- **EMA length:** slow EMA controls regime definition (50/200 for macro trend)
- **Timeframe:** 1h is a balanced default; 4h for macro, 5m for scalping

## 📦 Contents

- `MarkovStrategy.py`: strategy code
- `config.json.example`: example Freqtrade config for this strategy
- `config.header.txt`: GPL header to keep alongside the config
- `requirements.txt`: optional extra dependencies installed during image build

## ⚙️ Setup

Copy the example config and edit it:

```bash
cp config.json.example config.json
```

## 🚀 Run the Bot

1) Ensure the shared network exists (usually created by FreqHub):

```bash
./scripts/net up
```

2) Preferably use the helper script from repo root:

```bash
./scripts/bot up strategies/FreqHub.Strategy.Markov
```

## 🧪 Run Hyperopt (Docker)

```bash
docker compose -f docker-compose.hyperopt.yml up --build --abort-on-container-exit
```

Defaults:

- `FREQTRADE_HYPEROPT_EPOCHS=200`
- `FREQTRADE_HYPEROPT_TIMERANGE=20230101-`

## 🧪 Run Hyperopt (Freqtrade CLI)

```bash
freqtrade hyperopt \
  --strategy MarkovStrategy \
  --hyperopt-loss SharpeHyperOptLoss \
  --spaces buy sell \
  -e 200 \
  --timerange 20230101-
```

3) Stop the bot (preferred):

```bash
./scripts/bot down strategies/FreqHub.Strategy.Markov
```

Alternative (manual compose):

```bash
docker compose -f strategies/FreqHub.Strategy.Markov/docker-compose.yml up -d --build
```

```bash
docker compose -f strategies/FreqHub.Strategy.Markov/docker-compose.yml down
```

Notes:

- The API is exposed on `http://localhost:8012` (see `docker-compose.yml`).
- Use port `8010` for the template, `8011` for RSI_Bollinger, and `8012` for Markov.
- To change ports, edit the `ports:` section in `docker-compose.yml`.

## 📚 References

- [Freqtrade Documentation](https://www.freqtrade.io/)
- [Markov chain - Wikipedia](https://en.wikipedia.org/wiki/Markov_chain)
- [Relative Strength Index (RSI) - Wikipedia](https://en.wikipedia.org/wiki/Relative_strength_index)

## 📝 License

This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

**Copyright (C) 2025 - 2026 FreqHub Contributors**

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

## 🙏 Acknowledgments

- [Freqtrade](https://github.com/freqtrade/freqtrade) - The amazing trading bot this project is built for
- [FreqHub](https://github.com/hrodrig/freqhub) - Amazing UI for Freqtrade with multi-bots
- [FreqUI](https://github.com/freqtrade/frequi) - Inspiration and reference implementation

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/hrodrig/freqhub-strategies/issues)
- **Discussions**: [GitHub Discussions](https://github.com/hrodrig/freqhub-strategies/discussions)
- **Donations**: [Donations](DONATIONS.md)

---

**Note**: FreqHub Strategies is an independent project and is not officially affiliated with the Freqtrade project.
