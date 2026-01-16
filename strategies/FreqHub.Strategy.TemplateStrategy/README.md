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

# FreqHub Template Strategy

Minimal example strategy to use as a starting point for new ideas.

FreqHub reference: https://github.com/hrodrig/freqhub

## 📊 Strategy Summary

| Feature | Value |
|----------------|-------|
| **Risk Level** | 🟢 Low |
| **Stop Loss** | -10% |
| **Target ROI** | 4% |
| **Timeframe** | 5m |
| **Max Open Trades** | 1 |
| **Recommended Pairs** | BTC/USDT, ETH/USDT |
| **Best For** | Learning and prototyping |

## 📈 About the Strategy

This is a very small EMA + RSI example designed to keep the logic clear and
easy to extend.

## 📦 Contents

- `FreqHub.Strategy.TemplateStrategy.py`: strategy code
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
./scripts/bot up strategies/FreqHub.Strategy.TemplateStrategy
```

3) Stop the bot (preferred):

```
./scripts/bot down strategies/FreqHub.Strategy.TemplateStrategy
```

Alternative (manual compose):

```
docker compose -f strategies/FreqHub.Strategy.TemplateStrategy/docker-compose.yml up -d --build
```

```
docker compose -f strategies/FreqHub.Strategy.TemplateStrategy/docker-compose.yml down
```

Notes:

- The API is exposed on `http://localhost:8010` (see `docker-compose.yml`).
- Use port `8010` for the template. For additional strategies, use `8011+`
  (e.g. 8011, 8012, 8013) and avoid port collisions.
- To change ports, edit the `ports:` section in `docker-compose.yml`.

## 🧠 Strategy Logic

This template uses a simple **EMA crossover** plus **RSI** filter:

- **EMA(12) vs EMA(26)** provides a basic trend signal.
- **RSI** is used to avoid entries in overheated conditions.

### Why these indicators

- EMAs capture short-term vs medium-term trend shifts with low lag.
- RSI helps reduce false entries when momentum is already extended.

### Pros

- Easy to understand and extend.
- Good baseline for quick experiments.

### Cons

- Not optimized for any specific market regime.
- Can be noisy without additional filters (volume, higher timeframe trend).

## ⚠️ Disclaimer

This strategy is for educational purposes. Trading carries significant risk.
Always test in dry-run first and never invest more than you can afford to lose.

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
