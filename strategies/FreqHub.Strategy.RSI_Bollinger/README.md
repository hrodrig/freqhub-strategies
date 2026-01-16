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

This folder contains the **RSI + Bollinger Bands** strategy for Freqtrade.

FreqHub reference: https://github.com/hrodrig/freqhub

## 📊 Strategy Summary

| Feature | Value |
|----------------|-------|
| **Risk Level** | 🟡 Low-Medium |
| **Stop Loss** | -6% |
| **Target ROI** | 10% |
| **Timeframe** | 15m |
| **Max Open Trades** | 5 |
| **Recommended Pairs** | BTC/USDT, ETH/USDT, BNB/USDT, SOL/USDT |
| **Best For** | Range-bound markets |

## 📈 About the Strategy

The strategy uses RSI to detect overbought/oversold conditions and Bollinger
Bands to confirm potential reversals or pullbacks.

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

## 🧠 Strategy Logic

This strategy combines **RSI** with **Bollinger Bands** to identify potential
mean-reversion opportunities:

- **RSI** helps detect overbought/oversold conditions to time entries and exits.
- **Bollinger Bands** provide a volatility envelope; touches or breaks can
  signal potential reversals or pullbacks.

### Why these indicators

- RSI gives a fast momentum signal that often precedes short-term reversals.
- Bollinger Bands adapt to volatility, filtering noisy RSI signals in ranging
  markets.

### Pros

- Works well in **range-bound** or choppy markets.
- Simple and interpretable signals.

### Cons

- Can underperform in strong trending markets (RSI can stay extreme).
- Requires careful tuning of thresholds and period lengths per market.

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
