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

# Changelog

All notable changes to FreqHub Strategies will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.14] - 2026-02-01
### Added
- BinHV45 strategy package with Dockerfile, compose, and documentation
- Bulk `scripts/bots` helper for starting/stopping all strategies

### Changed
- IchiV1 no longer sends startup messages via RPC
- FailureToReturn now supports older Freqtrade without BoolParameter
- Glossary expanded with Bollinger and candle terminology
- README updated with BinHV45 and bulk script usage

## [0.2.13] - 2026-02-01
### Changed
- Standardize strategy filenames for MarkovRSI, MarkovVolume, and TemplateStrategy
- Update README naming guidance to match new strategy filename convention

## [0.2.12] - 2026-02-01
### Added
- Glossary with common trading and config terms
- Trading overview with a beginner-friendly workflow

### Changed
- README updated to link glossary and trading overview

## [0.2.11] - 2026-02-01
### Added
- MandelbrotFibonacci strategy package with Dockerfile, compose, and documentation
- Crypto-focused defaults with guidance to adapt for forex

## [0.2.10] - 2026-02-01
### Added
- FailureToReturn strategy package with Dockerfile, compose, and documentation
- Long/short FTR signals with session filtering and daily profit guard
- Forex-focused example config using OANDA

## [0.2.5] - 2026-01-15
### Added
- IchiV1 strategy package with Dockerfile, compose, and documentation

### Changed
- Strategy docs updated to include IchiV1 setup/run guidance

### Fixed
- Remove user_data artifacts and keep only `.keep` placeholders
- Align IchiV1 example config values with documentation

## [0.2.4] - 2026-01-15
### Added
- Strategy packages for Template and RSI_Bollinger
- Strategy-level Dockerfiles and compose files
- Bot/network scripts (`scripts/bot`, `scripts/net`)
- Strategy docs with setup, logic, and run instructions
- Version file and README badges

### Changed
- Ports aligned to start at 8010 and increment from 8011+
- Configs moved to `config.json.example` workflow
