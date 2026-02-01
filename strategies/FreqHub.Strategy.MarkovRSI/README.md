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

# FreqHub Markov RSI Strategy

Markov strategy with optimizable RSI thresholds and period.

## 📊 Strategy Summary

| Feature | Value |
|----------------|-------|
| **Risk Level** | 🟡 Medium |
| **Stop Loss** | -5% |
| **Target ROI** | 10% initial, then 5% @ 4h, 2% @ 12h, 1% @ 24h |
| **Timeframe** | 1h |
| **Daily Rule** | If there's profit today, no more trades |

## 🧠 Strategy Logic

Entry/exit follows the standard Markov transitions, but RSI thresholds are
optimizable so you can tune regime boundaries per market. Entry also requires:

- ADX above `adx_min`
- ATR% above `atr_min`

Exit adds an RSI overbought condition (`sell_rsi_overbought`).

## 🧪 Hyperopt

Optimizable parameters:

- `roi_t1`, `roi_t2`, `roi_t3`
- `roi_p1`, `roi_p2`, `roi_p3`, `roi_p4`
- `stoploss_opt`
- `rsi_period` (10-21)
- `rsi_low` (30-50)
- `rsi_high` (55-75)
- `adx_min`, `atr_min`
- `sell_rsi_overbought`

Note: keep `rsi_low < rsi_high` to avoid overlapping states.

## ⏱️ Timeframe

If you want a different timeframe, update **both**:

- `timeframe` in `MarkovRSIStrategy.py`
- `timeframe` in `config.json`

## ⚙️ Setup

```
cp config.json.example config.json
```

## 🚀 Run the Bot

```
./scripts/bot up strategies/FreqHub.Strategy.MarkovRSI
```

## 🧪 Run Hyperopt (Docker)

```
docker compose -f docker-compose.hyperopt.yml up --build --abort-on-container-exit
```

Defaults:

- `FREQTRADE_HYPEROPT_EPOCHS=200`
- `FREQTRADE_HYPEROPT_TIMERANGE=20230101-`

## 🧪 Run Hyperopt (Freqtrade CLI)

```
freqtrade hyperopt \
  --strategy MarkovRSIStrategy \
  --hyperopt-loss SharpeHyperOptLoss \
  --spaces buy sell \
  -e 200 \
  --timerange 20230101-
```

Notes:

- The API is exposed on `http://localhost:8015`.

## 📚 References

- [Freqtrade Documentation](https://www.freqtrade.io/)
