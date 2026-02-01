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

# FreqHub BinHV45 Strategy

Mean reversion strategy based on Bollinger Bands that looks for rebounds after a strong
move below the lower band.

## 📊 Strategy Summary

| Feature | Value |
|----------------|-------|
| **Risk Level** | 🟡 Medium |
| **Stop Loss** | -5% |
| **Target ROI** | 1.25% |
| **Timeframe** | 15m |
| **Max Open Trades** | 5 |
| **Recommended Pairs** | BTC/USDT, ETH/USDT, BNB/USDT, SOL/USDT |
| **Best For** | Volatile markets with snap-back behavior |
| **Strategy Type** | Mean Reversion + Bollinger Bands |

## 🧠 Strategy Logic

Entry requires all of the following:

1. Price is below the previous lower Bollinger Band.
2. Band width (bbdelta) is large enough to confirm volatility.
3. Close-to-close move (closedelta) is significant.
4. The lower tail is relatively small compared to band width.
5. Price is stabilizing (current close <= previous close).

There are **no custom exit signals**. Exits use ROI and stoploss settings.

## 📈 Indicators

### Bollinger Bands
- Period: 40
- Standard deviations: 2

### Derived Metrics
- **bbdelta**: `abs(mid - lower)`
- **closedelta**: `abs(close - close.shift())`
- **tail**: `abs(close - low)`

## 🧪 Hyperopt Parameters

Optimizable parameters:

- `buy_bbdelta` (1-15, default: 7)
- `buy_closedelta` (15-20, default: 17)
- `buy_tail` (20-30, default: 25)

Default tuned values:

```python
buy_params = {
    "buy_bbdelta": 7,
    "buy_closedelta": 17,
    "buy_tail": 25
}
```

## ⚙️ Setup

```bash
cp config.json.example config.json
```

## 🚀 Run the Bot

```bash
./scripts/bot up strategies/FreqHub.Strategy.BinHV45
```

Notes:

- The API is exposed on `http://localhost:8019`.
- If Freqtrade messaging is configured, the strategy sends a startup message.

## 📚 References

- [Freqtrade Documentation](https://www.freqtrade.io/)
- [Bollinger Bands - Investopedia](https://www.investopedia.com/terms/b/bollingerbands.asp)
- [Mean Reversion - Investopedia](https://www.investopedia.com/terms/m/meanreversion.asp)
