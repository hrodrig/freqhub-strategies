<!--
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
 -->

# Copyright Header Guide

This document explains how to add copyright headers to source files in FreqHub.

## Standard Header Format

For all source files (TypeScript, JavaScript, etc.), use the following header format:

```typescript
/*
 * FreqHub - Multi-bot dashboard for Freqtrade
 * Copyright (C) 2025 - 2026  FreqHub Contributors
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
 */
```

## Compatibility with GPL v3

This header format is **fully compatible** with GPL v3. In fact, it's the recommended format according to section 0 of the GPL v3 license:

> "To do so, attach the following notices to the program. It is safest to attach them to the start of each source file to most effectively state the exclusion of warranty; and each file should have at least the "copyright" line and a pointer to where the full notice is found."

## What This Header Provides

1. **Copyright Notice**: Establishes copyright ownership
2. **License Information**: Clearly states the software is GPL v3
3. **Warranty Disclaimer**: Explicitly disclaims all warranties (required by GPL v3)
4. **Redistribution Rights**: Explains users can redistribute and modify
5. **License Reference**: Points to the full GPL v3 license

## Where to Add Headers

### Recommended
- **New files**: Always add the header to new source files
- **Major files**: Core application files (`app.ts`, `App.tsx`, etc.)
- **Library files**: Shared utilities and services

### Optional
- **Small utility files**: Very small helper functions
- **Configuration files**: Config files that are mostly data
- **Test files**: Test files can use a shorter header or omit it

## Example Usage

### TypeScript/JavaScript File

```typescript
/*
 * FreqHub - Multi-bot dashboard for Freqtrade
 * Copyright (C) 2025 - 2026  FreqHub Contributors
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
 */

import express from 'express';
// ... rest of the file
```

### Short Version (for very small files)

For very small utility files, you can use a shorter version:

```typescript
/*
 * Copyright (C) 2025 - 2026  FreqHub Contributors
 * SPDX-License-Identifier: GPL-3.0-or-later
 */
```

However, the full header is preferred as it provides better legal protection.

## FAQ

### Q: Is this compatible with GPL v3?
**A:** Yes, this is the exact format recommended by GPL v3 section 0.

### Q: Can I add additional disclaimers?
**A:** Yes, you can add additional disclaimers (like trading risk warnings) as long as they don't contradict GPL v3 terms.

### Q: Do I need to add this to every file?
**A:** It's recommended for all source files, but especially important for:
- Main application files
- Public APIs
- Library code that might be reused

### Q: What about generated files?
**A:** Generated files typically don't need headers, but if you're generating source code, include the header in the generator template.

### Q: Can I change "FreqHub Contributors" to my name?
**A:** If you're the sole author of a file, you can use your name. For files with multiple contributors, "FreqHub Contributors" is appropriate.

## References

- [GPL v3 License Text](https://www.gnu.org/licenses/gpl-3.0.html)
- [GPL v3 Section 0](https://www.gnu.org/licenses/gpl-3.0.html#section0)
- [How to Apply GPL v3](https://www.gnu.org/licenses/gpl-howto.html)

