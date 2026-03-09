``` pinescript
/*backtest
start: 2022-12-29 00:00:00
end: 2024-01-04 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © juliopetronilo

//@version=4
strategy("DMI/ADX/Squeeze Robot", shorttitle="DMI/ADX/SQZ", overlay=true)

// Squeeze Momentum Indicator
length = input(20, title="BB Length")
mult = input(2.0, title="BB MultFactor")
lengthKC = input(20, title="KC Length")
multKC = input(1.5, title="KC MultFactor")
useTrueRange = input(true, title="Use TrueRange (KC)")

source = close
basis = sma(source, length)
dev = multKC * stdev(source, length)
upperBB = basis + dev
low
```