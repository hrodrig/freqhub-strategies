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

# FreqHub Strategies

Each folder in this directory is a self-contained strategy package. Use this
README for the general usage. Each strategy has its own `README.md` with the
specific logic, parameters, and tuning notes.

FreqHub reference: https://github.com/hrodrig/freqhub

## General usage

Use the helper scripts from the repo root:

```
./scripts/bot up strategies/FreqHub.Strategy.TemplateStrategy
./scripts/bot down strategies/FreqHub.Strategy.TemplateStrategy
```

Bulk helpers:

```
./scripts/bots up
./scripts/bots down
```

First time (or if the `config.json` is missing), copy the example config:

```
cp strategies/FreqHub.Strategy.TemplateStrategy/config.json.example \
  strategies/FreqHub.Strategy.TemplateStrategy/config.json
```

Notes:

- If a `docker-compose.yml` exists in the strategy folder, `up` runs
  `docker compose up -d --build`, and `down` runs
  `docker compose down`.
- To clean orphaned containers explicitly, set `REMOVE_ORPHANS=true`.
- The `freqtrade-network` is expected to already exist (usually created by
  FreqHub or another compose stack).
- For local testing, you can create or remove the network manually:
  `./scripts/net up` and `./scripts/net down` (or set `NETWORK_NAME`).

## Naming convention

Folder name:

- `FreqHub.Strategy.<StrategyName>/`

Inside the folder:

- `<StrategyName>Strategy.py`

Each strategy folder may also include:

- `config.json.example`: example config for that strategy
- `config.header.txt`: GPL header to keep alongside the config (JSON can't include comments)
- `requirements.txt`: extra dependencies installed during image build
- `README.md`: strategy-specific documentation

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
