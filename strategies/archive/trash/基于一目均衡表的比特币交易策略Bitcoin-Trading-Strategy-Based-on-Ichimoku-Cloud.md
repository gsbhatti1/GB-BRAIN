```pinescript
/*backtest
start: 2023-12-31 00:00:00
end: 2024-01-30 00:00:00
Period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Alferow

//@version=4
strategy("BTC_ISHIMOKU", overlay=true)

period_max = input(20, minval = 1)
period_med = input(10, minval = 1)
period_min = input(16, minval = 1)

Lmax = highest(high, period_max)
Smax = lowest(low, period_max)

Lmed = highest(high, period_med)
Smed = lowest(low, period_med)

Lmin = highest(high, period_min)
Smin = lowest(low, period_min)

HL1 = (Lmax + Smax + Lmed + Smed)/4
HL2 = (Lmed + Smed + Lmin + Smin)/4

plot(HL1, color=color.blue, title="HL1")
plot(HL2, color=color.red, title="HL2")

longCondition = cross(HL2, HL1)
closeCondition = cross(HL1, HL2)

if (longCondition)
    strategy.entry("Long", strategy.long)

if (closeCondition)
    strategy.close("Long")
```

The Pine Script code completes the strategy by plotting the long-term line (`HL1`) in blue and the short-term line (`HL2`) in red. It also includes conditions for entering a long position when the short-term line crosses above the long-term line and closing the position when the long-term line crosses below the short-term line.