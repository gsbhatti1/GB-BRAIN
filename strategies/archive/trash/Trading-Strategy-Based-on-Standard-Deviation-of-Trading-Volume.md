``` pinescript
```pinescript
/*backtest
start: 2022-11-14 00:00:00
end: 2023-11-20 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © dongyun

//@version=4
strategy("Trading Strategy Based on Standard Deviation of Trading Volume", overlay=true)

options = input(1, "")
length = input(40, "Length")
nlow = input(5, "Nlow")
factor = input(1.0, "Factor")

vavg = 0.0
vavgn = 0.0
vsd = 0.0
lowlimit = 0.0
uplimit = 0.0
mavg = 0.0
aror = 0.0
adjvol = 0.0
savevol = 0.0


// Find average volume, replacing bad values
adjvol := volume

if (volume != 0)
    savevol := volume
else
    savevol := savevol[1]
    adjvol := savevol


// Replace high volume days because they distort standard deviation
if (adjvol > 2 * factor * nz(vsd[1]))
    adjvol := savevol
else
    adjvol := adjvol[1]

vavg := sma(adjvol, length)
vsd := stdev(adjvol, length)
vavgn := sma(adjvol, nlow)

// Extreme volume limits
lowlimit := vavg - factor * vsd
uplimit := vavg + 2 * factor * vsd

// System rules based on moving average trend
mavg := sma(close, length / 2)

// Only enter on new trend signals
if (options == 2)
    if (mavg > mavg[1] and mavg[1] <= mavg[2])
        strategy.entry("Long", strategy.long)
    if (mavg < mavg[1] and mavg[1] >= mavg[2])
        strategy.entry("Short", strategy.short)
else
    if (mavg > mavg[1] and vavgn > lowlimit)
        strategy.entry("Long", strategy.long)
    if (mavg < mavg[1] and vavgn > lowlimit)
        strategy.entry("Short", strategy.short)

// Exit on low volume
if (options != 1)
    if (vavgn < lowlimit or adjvol < uplimit * factor / 2)
        strategy.close("Long")
        strategy.close("Short")
```
```