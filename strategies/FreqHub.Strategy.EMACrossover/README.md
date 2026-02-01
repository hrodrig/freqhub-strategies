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

# FreqHub EMACrossover Strategy

EMA crossover strategy with momentum and higher-timeframe confirmation.

## 📊 Strategy Summary

| Feature | Value |
|----------------|-------|
| **Risk Level** | 🟡 Low-Medium |
| **Stop Loss** | -6% |
| **Target ROI** | 10% initial, then 5% @ 30m, 3% @ 60m, 1% @ 120m |
| **Timeframe** | 15m (with 1h context) |
| **Max Open Trades** | 5 |
| **Recommended Pairs** | BTC/USDT, ETH/USDT, BNB/USDT, SOL/USDT |
| **Best For** | Clear trending markets |
| **Strategy Type** | EMA crossover + momentum confirmation |

## 🧠 Strategy Logic

Entry requires:

1. EMA fast > EMA mid > EMA slow (bullish crossover confirmation)
2. Recent crossover (fast was below mid on previous candle)
3. 1h trend filter: EMA fast > EMA slow
4. RSI within a healthy band (`buy_rsi_min` to `buy_rsi_max`)
5. MACD > signal and histogram > 0
6. Volume above its SMA times `volume_factor`

Exit triggers when any of the following is true:

- EMA fast < EMA mid
- MACD < signal
- RSI > 75
- 1h trend weakens (EMA fast < EMA slow or RSI < 40)

## 📈 Indicators

- EMA fast/mid/slow
- RSI (14)
- MACD (12/26/9)
- Volume SMA (20)
- 1h informative EMA/RSI

## 🧪 Hyperopt Parameters

- `buy_ema_fast` (5-15)
- `buy_ema_mid` (15-30)
- `buy_ema_slow` (30-60)
- `buy_rsi_min` (40-55)
- `buy_rsi_max` (60-75)
- `volume_factor` (1.0-2.5)

## ⚙️ Setup

```bash
cp config.json.example config.json
```

## 🚀 Run the Bot

```bash
./scripts/bot up strategies/FreqHub.Strategy.EMACrossover
```

Notes:

- The API is exposed on `http://localhost:8021`.

## 📚 References

- [Freqtrade Documentation](https://www.freqtrade.io/)
- [EMA - Investopedia](https://www.investopedia.com/terms/e/ema.asp)
- [RSI - Investopedia](https://www.investopedia.com/terms/r/rsi.asp)
- [MACD - Investopedia](https://www.investopedia.com/terms/m/macd.asp)
