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

[![Version](https://img.shields.io/badge/version-0.2.15-blue)](VERSION)
[![License](https://img.shields.io/badge/license-GPL--3.0-green)](LICENSE)
[![FreqHub](https://img.shields.io/badge/FreqHub-Repo-blue)](https://github.com/hrodrig/freqhub)

Strategies for **Freqtrade**, intended to run as individual bots in **FreqHub**.
The goal is to keep multiple strategies in one repository and provide a consistent 
way to run them.

## Structure

- `strategies/`: Freqtrade strategies (one folder per strategy).
- `GLOSSARY.md`: Definitions of common trading and config terms.

## Glossary

See `GLOSSARY.md` for definitions of indicators, pattern names, and config fields.

## Trading Overview

See `TRADING_OVERVIEW.md` for a general, beginner-friendly trading workflow and
how these strategies map to it.

## Included strategies

- `BinHV45`: Mean reversion strategy with Bollinger Bands.
- `EMACrossover`: EMA crossover strategy with momentum confirmation.
- `FailureToReturn`: Failure to Return (FTR) breakout continuation strategy.
- `IchiV1`: Ichimoku Cloud strategy.
- `MandelbrotFibonacci`: Fractals + Fibonacci pullback strategy.
- `Markov`: discrete Markov state transitions.
- `MarkovFastEMA`: Markov with fast EMA confirmation.
- `MarkovRSI`: Markov with optimizable RSI thresholds.
- `MarkovVolume`: Markov with volume confirmation.
- `MessageTest`: Messaging test strategy (do not use for live trading).
- `RSI_Bollinger`: RSI + Bollinger example.
- `RSIEMA50`: RSI + EMA50 trend-following strategy.
- `TemplateStrategy`: minimal example strategy.

## Requirements

- Docker (for build and run).
- Freqtrade (included in the base image).
- FreqHub (to manage bots).
  Reference: https://github.com/hrodrig/freqhub

## Freqtrade configuration

Each strategy includes its own `config.json.example`. Copy it to `config.json`
and use that as your base, then adjust:

- `exchange.key` and `exchange.secret`
- `pairlists`
- `api_server` (user, password, and port) so FreqHub can connect

## Run a strategy (generic example)

Each strategy folder includes a `config.json.example` (copy to `config.json`)
and may include its own
`docker-compose.yml`. For strategy-specific details, see the `README.md` inside
each strategy folder.

### Option A (Recommended): Helper scripts

Start a bot using the strategy's `config.json` (after copying from the example):

```bash
./scripts/bot up strategies/FreqHub.Strategy.TemplateStrategy
```

Stop it:

```bash
./scripts/bot down strategies/FreqHub.Strategy.TemplateStrategy
```

Run all strategies with a `config.json` present:

```bash
./scripts/bots up
```

Stop all strategies:

```bash
./scripts/bots down
```

### Option B: Docker Compose (manual,advanced)

From any directory:

```bash
docker compose -f strategies/FreqHub.Strategy.TemplateStrategy/docker-compose.yml up -d
```

Stop it with:

```bash
docker compose -f strategies/FreqHub.Strategy.TemplateStrategy/docker-compose.yml down
```

In FreqHub, add the bot pointing to the Freqtrade API using the service name:
`http://<service-name>:8080` (for example, `http://freqtrade-template-strategy:8080`).

Notes:

- If a `docker-compose.yml` exists in the strategy folder, `up` runs
  `docker compose up -d --build`, and `down` runs
  `docker compose down`.
- To clean orphaned containers explicitly, set `REMOVE_ORPHANS=true`.
- The `freqtrade-network` is expected to already exist (usually created by
  FreqHub or another compose stack).
- For local testing, you can create or remove the network manually:
  `./scripts/net up` and `./scripts/net down` (or set `NETWORK_NAME`).
- Port guidance: use `8010` for the template strategy, and `8011+` for
  additional strategies (avoid port collisions).

## Environment variables (bot up)

When you use `scripts/bot up`, these variables are supported:

- `IMAGE`: Docker image to run (default: `freqhub-strategy-<dir>:latest`).
- `STRATEGY`: Strategy class name (default: read from `config.json`).
- `STRATEGY_DIR`: Strategy folder name (default: basename of the folder).
- `API_PORT`: Host port for Freqtrade API (default: `8080`).
- `BOT_SUFFIX`: Optional suffix for container name.
- `CONTAINER_NAME`: Optional override for container name.
- `DATA_DIR`: Host data dir (default: `<strategy_dir>/data`).
- `REMOVE_ORPHANS`: Set to `true` to clean orphaned containers (compose only).
- `COMPOSE_IGNORE_ORPHANS`: Set to `1` to ignore orphan warnings (default).

## Common overrides

- `API_PORT=8012` to avoid port conflicts.
- `IMAGE=your-registry/freqhub-strategy-template:latest` to use a custom image.
- `STRATEGY=TemplateStrategy` to override the strategy class.

## Add new strategies

1) Create a folder: `strategies/FreqHub.Strategy.<StrategyName>/`
2) Add the strategy file:
   `<StrategyName>Strategy.py` with a class inheriting `IStrategy`.
3) Optionally add a `config.json.example` and a `README.md` inside the strategy folder.
4) Update `docker-compose.yml` to use it via `--strategy <StrategyName>`.

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
