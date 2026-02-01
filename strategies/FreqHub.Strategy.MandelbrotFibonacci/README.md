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

# FreqHub MandelbrotFibonacci Strategy

Trend-following strategy that blends **Mandelbrot-style fractals** (Bill Williams
fractals) with **Fibonacci retracement zones** to capture pullbacks in the
direction of the prevailing trend. It is designed for **crypto** by default,
with clear guidance below to adapt it to **forex**.

FreqHub reference: https://github.com/hrodrig/freqhub

## Strategy Summary

| Feature | Value |
|----------------|-------|
| **Risk Level** | Medium |
| **Stop Loss** | -8% |
| **Trailing Stop** | Enabled (1.5% activation / 3.0% offset) |
| **Target ROI** | 6% initial, 3% after 6h, 1% after 12h |
| **Timeframe** | 1h |
| **Max Open Trades** | 2 (from `config.json.example`) |
| **Recommended Pairs** | BTC/USDT, ETH/USDT, SOL/USDT |
| **Best For** | Trend pullbacks into fib zones |
| **Sides** | Long (default), Short (futures optional) |

## About the Strategy

This strategy uses fractals to identify swing highs and lows (a nod to
Mandelbrot's fractal market structure ideas). Once a swing range is defined,
it uses Fibonacci retracements (38.2%–61.8%) as a pullback zone. Entries are
only allowed when the broader trend is aligned.

## Strategy Logic

### Indicators Used

- **Bill Williams fractals** to detect swing highs and lows.
- **Fibonacci retracement** (38.2% and 61.8%) between the last fractal high/low.
- **EMA 50 / EMA 200** for trend direction.
- **Volume SMA (20)** for confirmation.

### Entry Conditions (Long)

1. **Trend filter**: EMA 50 above EMA 200 and price above EMA 200.
2. **Valid swing range**: last confirmed fractal low and high are present.
3. **Fib pullback zone**: price pulls into the 38.2%–61.8% retracement area.
4. **Momentum confirmation**: close above EMA 50 and bullish candle.
5. **Volume confirmation**: volume above its rolling average.

### Entry Conditions (Short)

1. **Trend filter**: EMA 50 below EMA 200 and price below EMA 200.
2. **Valid swing range**: last confirmed fractal low and high are present.
3. **Fib pullback zone**: price pulls into the 38.2%–61.8% retracement area.
4. **Momentum confirmation**: close below EMA 50 and bearish candle.
5. **Volume confirmation**: volume above its rolling average.

### Exit Conditions

Positions are closed when the trend weakens:

- **Long**: close crosses below EMA 50 or below EMA 200.
- **Short**: close crosses above EMA 50 or above EMA 200.

## Pros

- Combines structure (fractals) with price geometry (Fibonacci).
- Filters for trend reduce counter-trend trades.
- Works well on crypto with minimal setup.

## Cons

- Fractals confirm with a lag (2 candles), missing some early entries.
- Pullback zones can be skipped in strong trends.
- Not ideal for choppy, low-volatility conditions.

## Contents

- `MandelbrotFibonacciStrategy.py`: strategy code
- `config.json.example`: example Freqtrade config for this strategy
- `config.header.txt`: GPL header to keep alongside the config
- `requirements.txt`: optional extra dependencies installed during image build

## Setup

Copy the example config and edit it:

```bash
cp config.json.example config.json
```

For shorting, ensure your exchange and Freqtrade setup supports futures/shorts.
Spot-only setups require `can_short = False` (default).

To enable shorts, set:
- `can_short = True` in `MandelbrotFibonacci.py`
- `trading_mode = "futures"` in `config.json`

## Adapting to Forex

To use this strategy on forex, adjust the following:

- **Exchange**: set the exchange (e.g. `oanda`, `fxcm`, `forexcom`) in
  `config.json`.
- **Pairs**: replace crypto pairs with FX pairs like `EUR/USD`, `GBP/USD`,
  `USD/JPY`.
- **Timeframe**: consider `4h` or `1h` depending on session liquidity.
- **Volume**: if your FX feed has unreliable volume, reduce the volume filter
  impact or disable it by setting `volume_factor` closer to `0.8`.

## Run the Bot

1) Ensure the shared network exists (usually created by FreqHub):

```bash
./scripts/net up
```

2) Preferably use the helper script from repo root:

```bash
./scripts/bot up strategies/FreqHub.Strategy.MandelbrotFibonacci
```

3) Stop the bot (preferred):

```bash
./scripts/bot down strategies/FreqHub.Strategy.MandelbrotFibonacci
```

Alternative (manual compose):

```bash
docker compose -f strategies/FreqHub.Strategy.MandelbrotFibonacci/docker-compose.yml up -d --build
```

```bash
docker compose -f strategies/FreqHub.Strategy.MandelbrotFibonacci/docker-compose.yml down
```

Notes:

- The API is exposed on `http://localhost:8013` (see `docker-compose.yml`).
- Use port `8010` for the template. For additional strategies, use `8011+`
  (e.g. 8011, 8012, 8013) and avoid port collisions.
- To change ports, edit the `ports:` section in `docker-compose.yml`.

## References

- https://www.investopedia.com/terms/f/fractal.asp
- https://www.investopedia.com/terms/f/fibonacciretracement.asp
- https://www.freqtrade.io/

## License

This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

**Copyright (C) 2025 - 2026 FreqHub Contributors**

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

## Acknowledgments

- [Freqtrade](https://github.com/freqtrade/freqtrade) - The amazing trading bot this project is built for
- [FreqHub](https://github.com/hrodrig/freqhub) - Amazing UI for Freqtrade with multi-bots
- [FreqUI](https://github.com/freqtrade/frequi) - Inspiration and reference implementation

## Support

- **Issues**: [GitHub Issues](https://github.com/hrodrig/freqhub-strategies/issues)
- **Discussions**: [GitHub Discussions](https://github.com/hrodrig/freqhub-strategies/discussions)
- **Donations**: [Donations](DONATIONS.md)

---

**Note**: FreqHub Strategies is an independent project and is not officially affiliated with the Freqtrade project.
