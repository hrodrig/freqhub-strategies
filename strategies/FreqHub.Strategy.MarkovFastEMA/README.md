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

# FreqHub Markov Fast EMA Strategy

Markov variant with an additional fast EMA confirmation.

## 📊 Strategy Summary

| Feature | Value |
|----------------|-------|
| **Risk Level** | 🟡 Medium |
| **Stop Loss** | -5% |
| **Target ROI** | 10% inicial, luego 5% @ 4h, 2% @ 12h, 1% @ 24h |
| **Timeframe** | 1h |
| **Daily Rule** | If there's profit today, no more trades |

## 🧠 Strategy Logic

The Markov state logic is preserved, but entry only occurs if:

- bullish state transition (0➜1, 1➜2, 2➜3)
- **fast EMA > slow EMA**
- price above the fast EMA
- ADX above `adx_min`
- ATR% above `atr_min`

Exit includes state weakening, fast EMA < slow EMA, or RSI above `sell_rsi_overbought`.

## 📦 Contents

- `MarkovFastEMAStrategy.py`: strategy code
- `config.json.example`: example Freqtrade config for this strategy
- `config.header.txt`: GPL header to keep alongside the config
- `requirements.txt`: optional extra dependencies installed during image build

## ⚙️ Setup

```bash
cp config.json.example config.json
```

## 🚀 Run the Bot

```bash
./scripts/bot up strategies/FreqHub.Strategy.MarkovFastEMA
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
  --strategy MarkovFastEMAStrategy \
  --hyperopt-loss SharpeHyperOptLoss \
  --spaces buy sell \
  -e 200 \
  --timerange 20230101-
```

## 🧪 Hyperopt

Optimizable parameters:

- `roi_t1`, `roi_t2`, `roi_t3`
- `roi_p1`, `roi_p2`, `roi_p3`, `roi_p4`
- `stoploss_opt`
- `fast_ema` (8-30)
- `slow_ema` (30-80)
- `adx_min`, `atr_min`
- `sell_rsi_overbought`

## 📚 References

- [Freqtrade Documentation](https://www.freqtrade.io/)
