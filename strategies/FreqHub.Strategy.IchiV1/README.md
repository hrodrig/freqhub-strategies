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

# FreqHub IchiV1 Strategy

This folder contains the **IchiV1** (Ichimoku Cloud) strategy for Freqtrade.

## 📖 Strategy Origin

This strategy is based on the **IchiV1** strategy published on
[FreqST](https://freqst.com/strategy/0e1e73046f96bb72d955553b1fd5420aa4de5bf2cc43a4bb25ec037de9688ffd38adfef89d2c0/),
an automated trading strategy that uses the Ichimoku Cloud indicator to
identify trends, support/resistance levels, and potential reversals.

**Note:** The original FreqST strategy is no longer actively maintained, but it
remains available for reference. This implementation has been adapted and
optimized for use with Freqtrade/FreqHub.

FreqHub reference: https://github.com/hrodrig/freqhub

## 📊 Strategy Summary

| Feature | Value |
|----------------|-------|
| **Risk Level** | 🟡 Medium |
| **Stop Loss** | -8% (dynamic with custom trailing stoploss) |
| **Target ROI** | 15% (initial), scaled to 2% after 120 min |
| **Timeframe** | 15m |
| **Max Open Trades** | 5 (from `config.json.example`) |
| **Stake per Trade** | Unlimited (from `config.json.example`) |
| **Total Balance** | 1000 USDT (dry_run_wallet) |
| **Mode** | Dry Run by default (configurable) |
| **Recommended Pairs** | BTC/USDT, BCH/USDT, ETH/USDT, LINK/USDT, LTC/USDT, SOL/USDT, BNB/USDT, XRP/USDT, ADA/USDT, DOT/USDT, ETC/USDT, ALGO/USDT, LUNA/USDT |
| **Best For** | Trend identification, support/resistance, and reversals |

## 📦 Contents

- `IchiV1Strategy.py`: strategy code
- `config.json.example`: example Freqtrade config for this strategy
- `config.header.txt`: GPL header to keep alongside the config
- `requirements.txt`: optional extra dependencies installed during image build

## ⚙️ Setup

Copy the example config and edit it:

```
cp config.json.example config.json
```

## 🚀 Run the Bot

1) Ensure the shared network exists (usually created by FreqHub):

```
./scripts/net up
```

2) Preferably use the helper script from repo root:

```
./scripts/bot up strategies/FreqHub.Strategy.IchiV1
```

3) Stop the bot (preferred):

```
./scripts/bot down strategies/FreqHub.Strategy.IchiV1
```

Alternative (manual compose):

```
docker compose -f strategies/FreqHub.Strategy.IchiV1/docker-compose.yml up -d --build
```

```
docker compose -f strategies/FreqHub.Strategy.IchiV1/docker-compose.yml down
```

Notes:

- The API is exposed on `http://localhost:8017` (see `docker-compose.yml`).
- Use port `8010` for the template. For additional strategies, use `8011+`
  (e.g. 8011, 8012, 8013) and avoid port collisions.
- To change ports, edit the `ports:` section in `docker-compose.yml`.

## 📈 About the Strategy

**IchiV1 Strategy** is based on the **Ichimoku Cloud** indicator, combining
symmetrical, leading, and lagging indicators to generate entry and exit
signals. It also uses a "fan" indicator to analyze volume.

### 🎯 Special Features

#### Daily Profit Protection
The strategy includes a **daily profit protection** feature that prevents new
trades after achieving a positive profit for the day:

- ✅ **If the bot closes a trade with a positive profit** → It will not open
  more trades that day
- ✅ **Next day (00:00 UTC)** → It resets automatically and can trade normally
- ✅ **Informative logs**: Logs when it blocks an entry due to daily profit
- ✅ **Error handling**: If profit calculation fails, it allows entry (does not
  block the bot)

This feature helps to:
- Protect the day's profits
- Avoid overtrading after a good day
- Maintain trading discipline
- Reduce the risk of giving back gains

#### Enhanced Startup Message
The bot sends a complete startup message to Telegram/Mattermost including:
- Exchange and operation mode (Real/Dry-Run)
- Stake per trade (exact USDT amount)
- Maximum open trades
- Configured minimum ROI
- Trailing stoploss
- Timeframe and strategy
- Startup candles

#### Current Configuration (Example)
- **Mode**: Dry Run (dry_run: true)
- **Available balance**: 1000 USDT (dry_run_wallet)
- **Stake per trade**: Unlimited (stake_amount)
- **Max open trades**: 5

### Ichimoku Cloud Components:

- **Tenkan-sen (Conversion Line)**: Average of highs and lows over 9 periods
- **Kijun-sen (Base Line)**: Average of highs and lows over 26 periods
- **Senkou Span A (Leading Span A)**: Average of Tenkan and Kijun, shifted 26 periods
- **Senkou Span B (Leading Span B)**: Average of highs and lows over 52 periods, shifted 26 periods
- **Chikou Span (Lagging Span)**: Closing price shifted 26 periods backward

### 🎯 Strategy Logic

#### Entry Conditions (Long)
The strategy opens a position when the following Ichimoku Cloud conditions are met:

1. ✅ **Price above the cloud** (bullish trend):
   - `trend_above_senkou >= buy_trend_above_senkou_level`
   - Indicates price is in a strong bullish zone

2. ✅ **Tenkan above Kijun** (confirmed bullish trend):
   - `trend_bullish >= buy_trend_bullish_level`
   - Confirms short-term bullish momentum

3. ✅ **Chikou Span above price** (trend confirmation):
   - `chikou_span > close`
   - Historical price confirms bullish trend

4. ✅ **Volume confirmation with fan**:
   - `fan_magnitude_gain >= buy_min_fan_magnitude_gain`
   - Volume confirms the move

5. ✅ **RSI not overbought**:
   - `rsi < 70`
   - Avoids entries when price is extremely overbought

6. ✅ **Volume above average**:
   - `volume > volume.rolling(20).mean()`
   - Confirms market interest

7. ✅ **Avoid extreme bearish pullback**:
   - `pullback_flag != -1`
   - Prevents entries during extreme bearish moves

**Alternative**: It can also enter when price crosses above the cloud with Tenkan > Kijun confirmation.

#### Exit Conditions
The strategy closes a position when any of these conditions are met:

1. ❌ **Trend indicator flips bearish**: `trend_indicator <= sell_trend_indicator`
2. ❌ **Tenkan crosses below Kijun**: Confirms trend change
3. ❌ **Price crosses below the cloud**: Structural change
4. ❌ **Chikou Span crosses below price**: Reversal confirmation
5. ❌ **RSI overbought**: `rsi > 70`

### Optimizable Parameters:

**Buy:**
- `buy_trend_above_senkou_level`: Trend level above cloud (default: 0.5, range: 0.0-2.0)
- `buy_trend_bullish_level`: Bullish trend level (default: 0.3, range: 0.0-1.0)
- `buy_fan_magnitude_shift_value`: Fan shift value (default: 0.5, range: 0.1-2.0)
- `buy_min_fan_magnitude_gain`: Minimum fan gain (default: 0.3, range: 0.1-1.0)

**Sell:**
- `sell_trend_indicator`: Trend indicator for exit (default: -0.3, range: -1.0-0.0)

**Custom Trailing Stoploss (Advanced):**
- `pHSL`: Hard Stop Loss (default: -0.08, range: -0.200 to -0.040)
- `pPF_1`: Profit Factor 1 (default: 0.016, range: 0.008-0.020)
- `pSL_1`: Stop Loss 1 (default: 0.011, range: 0.008-0.020)
- `pPF_2`: Profit Factor 2 (default: 0.070, range: 0.040-0.100)
- `pSL_2`: Stop Loss 2 (default: 0.030, range: 0.020-0.070)

## 🏗️ Architecture

This repository contains:

- **Dockerfile**: Docker image with the strategy included
- **k8s/**: Full Kubernetes configuration
- **scripts/**: Build and deployment scripts
- **IchiV1Strategy.py**: Strategy code

## 📝 Configuration

### Modify Trading Pairs

Edit `config.json` and update the `pair_whitelist` section:

```yaml
"pair_whitelist": [
  "BTC/USDT",
  "ETH/USDT",
  # ... more pairs
]
```

### Adjust Strategy Parameters

Parameters can be optimized using Freqtrade:

```bash
# Optimize buy parameters
freqtrade hyperopt --strategy IchiV1Strategy --hyperopt-loss SharpeHyperOptLoss --spaces buy -e 100

# Optimize sell parameters
freqtrade hyperopt --strategy IchiV1Strategy --hyperopt-loss SharpeHyperOptLoss --spaces sell -e 100
```

## 🔧 Troubleshooting

### The strategy does not open trades

1. Verify `dry_run` is configured correctly
2. Check the logs for generated signals
3. Adjust entry parameters if they are too restrictive

## 📚 References

- [Freqtrade Documentation](https://www.freqtrade.io/)
- [Original IchiV1 Strategy on FreqST](https://freqst.com/strategy/0e1e73046f96bb72d955553b1fd5420aa4de5bf2cc43a4bb25ec037de9688ffd38adfef89d2c0/) - Original strategy based on Ichimoku Cloud
- [Ichimoku Cloud - Wikipedia](https://en.wikipedia.org/wiki/Ichimoku_Kink%C5%8D_Hy%C5%8D)

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
