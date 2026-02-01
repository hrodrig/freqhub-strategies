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

# Trading Overview

This is a high-level overview of how discretionary traders typically approach
markets, and how our strategies attempt to replicate parts of that workflow.

## References

- **Glossary**: See `GLOSSARY.md` for indicator and config definitions.
- **Strategy Catalog**: See `README.md` for the list of available strategies.

## 1) Define the Market Context

- **Market type**: trend vs range, high vs low volatility.
- **Timeframe alignment**: higher timeframe bias + lower timeframe execution.
- **Liquidity/session**: when trading conditions are best (e.g., London/NY).

## 2) Gather Signals (Technical + Structure)

- **Trend filters**: moving averages, Ichimoku, regime states.
- **Structure**: swing highs/lows, breakouts, pullbacks, FTR zones.
- **Momentum/confirmation**: RSI, ADX, volume, volatility filters.

## 3) Optional Fundamental Bias

- Macro news, economic calendars, and event risk can influence directional bias.
- Strategies may include a **daily bias filter** concept, but do not interpret news.

## 4) Define the Plan (Rules First)

- **Entry**: clear, repeatable conditions.
- **Exit**: ROI schedule, stoploss, trailing stop, or rule-based exits.
- **Risk**: position sizing, max open trades, daily profit guard.

## 5) Execute and Manage Emotion

- Stick to rules; avoid manual overrides without a documented reason.
- Use logs and dry-run to validate behavior before risking capital.

## 6) Review and Iterate

- Backtest and forward-test in multiple market regimes.
- Adjust parameters carefully, one variable at a time.
- Track drawdown, win rate, and risk/reward, not just profit.

## How This Maps to Our Strategies

- **Indicators and structure**: encoded as deterministic rules.
- **Risk management**: stoploss, trailing stop, ROI schedules, daily guards.
- **Session filters and volatility thresholds**: emulate trader discretion.

This is not financial advice. Use it as a framework for understanding the
mechanics behind each strategy.

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
