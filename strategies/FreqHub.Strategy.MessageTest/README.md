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

# FreqHub MessageTest Strategy

Messaging test strategy that alternates buy/sell every candle to validate alerts.

## ⚠️ Important

This strategy is **ONLY** for messaging tests (Telegram/Mattermost/Slack).  
Do **not** use it for live trading.

## 📊 Strategy Summary

| Feature | Value |
|----------------|-------|
| **Risk Level** | 🔴 High (test only) |
| **Stop Loss** | -10% |
| **Target ROI** | 1% initial, then 0.5% @ 15m, 0.2% @ 30m |
| **Timeframe** | 15m |
| **Max Open Trades** | 1 |
| **Pairs** | BTC/USDT (test only) |
| **Purpose** | Validate messaging notifications |
| **Strategy Type** | Test / QA |

## 🧠 Strategy Logic

- Buy on every even candle
- Sell on the next candle
- No indicators or market analysis

## ⚙️ Setup

```
cp config.json.example config.json
```

## 🚀 Run the Bot

```
./scripts/bot up strategies/FreqHub.Strategy.MessageTest
```

Notes:

- The API is exposed on `http://localhost:8022`.
- Use **dry-run only** and stop after validation.

## 📚 References

- [Freqtrade Documentation](https://www.freqtrade.io/)
- [Freqtrade Notifications](https://www.freqtrade.io/en/stable/notifications/)
