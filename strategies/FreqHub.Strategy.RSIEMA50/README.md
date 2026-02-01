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

# FreqHub RSIEMA50 Strategy

Trend-following strategy that combines RSI momentum with EMA50 trend confirmation
and MACD alignment. It uses a 15m execution timeframe with a 1h trend filter.

## 📊 Strategy Summary

| Feature | Value |
|----------------|-------|
| **Risk Level** | 🟡 Medium |
| **Stop Loss** | -6% |
| **Target ROI** | 10% initial, then 5% @ 30m, 3% @ 60m, 1% @ 120m |
| **Timeframe** | 15m (with 1h context) |
| **Max Open Trades** | 5 |
| **Recommended Pairs** | BTC/USDT, ETH/USDT, BNB/USDT, SOL/USDT |
| **Best For** | Clear trending markets |
| **Strategy Type** | Trend following + momentum confirmation |

## 🧠 Strategy Logic

Entry requires:

1. Price above EMA50 (trend confirmation)
2. RSI in a healthy band (`buy_rsi_min` to `buy_rsi_max`)
3. MACD above signal line (momentum confirmation)
4. 1h trend filter: price above EMA50 and RSI > 50
5. Volume above its 20-period SMA multiplied by `buy_volume_factor`

Exit triggers when any of the following is true:

- Price crosses below EMA50
- RSI exceeds 75
- MACD falls below signal line
- 1h trend filter weakens (price below EMA50 or RSI < 40)

## 📈 Indicators

- EMA50 (optimizable period)
- RSI (14)
- MACD (12/26/9)
- Volume SMA (20)
- 1h informative EMA/RSI

## 🧪 Hyperopt Parameters

- `buy_rsi_min` (45-60)
- `buy_rsi_max` (65-80)
- `buy_ema_period` (40-60)
- `buy_volume_factor` (1.0-2.5)

## ⚙️ Setup

```
cp config.json.example config.json
```

## 🚀 Run the Bot

```
./scripts/bot up strategies/FreqHub.Strategy.RSIEMA50
```

Notes:

- The API is exposed on `http://localhost:8020`.

## 📚 References

- [Freqtrade Documentation](https://www.freqtrade.io/)
- [RSI - Investopedia](https://www.investopedia.com/terms/r/rsi.asp)
- [EMA - Investopedia](https://www.investopedia.com/terms/e/ema.asp)
- [MACD - Investopedia](https://www.investopedia.com/terms/m/macd.asp)
