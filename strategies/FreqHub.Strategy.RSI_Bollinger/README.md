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

# FreqHub RSI_Bollinger Strategy

Independent repository to deploy the **RSI_BollingerStrategy** in Freqtrade,
combining **RSI** momentum with **Bollinger Bands** volatility for entries and
exits.

FreqHub reference: https://github.com/hrodrig/freqhub

## 📊 Strategy Summary

| Feature | Value |
|----------------|-------|
| **Risk Level** | 🟡 Medium |
| **Stop Loss** | -6% |
| **Trailing Stop** | Enabled (1.5% activation / 2.5% offset) |
| **Target ROI** | 10% (initial), then 5% @ 30m, 3% @ 60m, 1% @ 120m |
| **Timeframe** | 15m (with 1h informative context) |
| **Max Open Trades** | 5 (from `config.json.example`) |
| **Stake per Trade** | Unlimited (from `config.json.example`) |
| **Mode** | Dry Run by default (configurable) |
| **Recommended Pairs** | BTC/USDT, ETH/USDT, BNB/USDT, SOL/USDT |
| **Best For** | Ranging markets and controlled pullbacks |

## 📈 About the Strategy

This strategy seeks mean‑reversion entries near the **lower Bollinger Band** in
the direction of a broader uptrend, with **RSI** filtering and **volume**
confirmation. It uses a **15m** timeframe for signals and a **1h** informative
timeframe to validate the trend.

### 🎯 Special Features

#### Informative Timeframe Confirmation
The strategy uses a 1h timeframe to confirm direction:
- 15m price must be above the 15m EMA
- 15m price must also be above the 1h EMA
- 1h RSI must be above 50

#### Enhanced Startup Message
On startup it sends a Telegram/Mattermost message (if configured) with:
- Exchange and stake information
- ROI table and stoploss settings
- Timeframe and strategy name
- Startup candle count

## 🧠 Strategy Logic

### Indicators Used

- **RSI (14)** for momentum
- **Bollinger Bands** with configurable period and standard deviation
- **EMA (21)** for trend direction
- **Volume SMA (20)** for volume confirmation
- **1h RSI/EMA** for higher‑timeframe validation

### Entry Conditions (Long)
The strategy opens a position when all conditions are met:

1. ✅ **RSI in favorable range**:
   - `rsi > buy_rsi_min` and `rsi < buy_rsi_max`
2. ✅ **Price near lower Bollinger Band**:
   - `bb_percent < buy_bb_percent`
3. ✅ **Uptrend on 15m**:
   - `close > ema`
4. ✅ **Uptrend on 1h**:
   - `close > ema_1h` and `rsi_1h > 50`
5. ✅ **Volume confirmation**:
   - `volume > volume_sma * buy_volume_factor`

### Exit Conditions
The strategy closes a position when any of these happen:

- ❌ **Price touches upper Bollinger Band** (`bb_percent > 0.95`)
- ❌ **RSI overbought** (`rsi > 75`)
- ❌ **EMA trend loss on 15m** (cross below EMA)
- ❌ **Trend weakness on 1h** (`close < ema_1h` or `rsi_1h < 40`)

### Optimizable Parameters

**Buy:**
- `buy_rsi_min`: 45–60 (default: 50)
- `buy_rsi_max`: 65–80 (default: 70)
- `buy_bb_period`: 15–25 (default: 20)
- `buy_bb_std`: 1.5–2.5 (default: 2.0)
- `buy_bb_percent`: 0.0–0.3 (default: 0.15)
- `buy_volume_factor`: 1.0–2.5 (default: 1.5)

**Sell/Exit:**
- Exit logic is rule‑based (not hyper‑optimized).

### Risk and Performance Notes

- Best in **sideways** markets or **controlled pullbacks** within uptrends.
- May underperform in strong trends or high volatility whipsaws.
- RSI extremes can persist; avoid aggressive thresholds in trending markets.

## 📦 Contents

- `RSI_BollingerStrategy.py`: strategy code
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
./scripts/bot up strategies/FreqHub.Strategy.RSI_Bollinger
```

3) Stop the bot (preferred):

```
./scripts/bot down strategies/FreqHub.Strategy.RSI_Bollinger
```

Alternative (manual compose):

```
docker compose -f strategies/FreqHub.Strategy.RSI_Bollinger/docker-compose.yml up -d --build
```

```
docker compose -f strategies/FreqHub.Strategy.RSI_Bollinger/docker-compose.yml down
```

Notes:

- The API is exposed on `http://localhost:8011` (see `docker-compose.yml`).
- Use port `8010` for the template. For additional strategies, use `8011+`
  (e.g. 8011, 8012, 8013) and avoid port collisions.
- To change ports, edit the `ports:` section in `docker-compose.yml`.

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

Optimize parameters using Freqtrade:

```bash
# Optimize buy parameters
freqtrade hyperopt --strategy RSI_BollingerStrategy --hyperopt-loss SharpeHyperOptLoss --spaces buy -e 100
```

## 🔧 Troubleshooting

### The strategy does not open trades

1. Verify `dry_run` is configured correctly
2. Check the logs for generated signals
3. Adjust entry parameters if they are too restrictive
4. Confirm volume is sufficient for the chosen pairs

## 📚 References

- [Freqtrade Documentation](https://www.freqtrade.io/)
- [RSI - Wikipedia](https://en.wikipedia.org/wiki/Relative_strength_index)
- [Bollinger Bands - Wikipedia](https://en.wikipedia.org/wiki/Bollinger_Bands)

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
