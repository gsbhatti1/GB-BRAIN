``` pinescript
/*backtest
start: 2023-09-26 00:00:00
end: 2023-10-26 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © ROBO_Trading

//@version=5
strategy(title = "Bollinger Stop Strategy", shorttitle = "BBStop", overlay = true, default_qty_type = strategy.percent_of_equity, initial_capital = 10000, default_qty_value = 100, commission_value = 0.1)

//Settings
long = input(true)
short = input(true)
length = input.int(20, minval=1)
mult = input.float(2.0, minval=0.001, maxval=50)
source = input(close)
showbb = input(true, title = "Show Bollinger Bands")
showof = input(true, title = "Show Offset")
startTime = input(defval = timestamp("01 Jan 2000 00:00 +0000"), title = "Start Time", inline = "time1")
finalTime = input(defval = timestamp("31 Dec 2099 23:59 +0000"), title = "Final Time", inline = "time1")

//Bollinger Bands
basis = ta.sma(source, length)
dev = mult * ta.stdev(source, length)
upper = basis + dev
lower = basis - dev

//Show indicator
offset = showof ? 1 : 0
colorBasis = showbb ? color.gray : na
colorUpper = showbb ? color.blue : na
colorLower = showbb ? color.blue : na
colorBands = showbb ? color.blue : na
p0 = plot(basis, "Basis", color = colorBasis, offset = offset)
p1 = plot(upper, "Upper", color = colorUpper, offset = offset)
p2 = plot(lower, "Lower", color = colorLower, offset = offset)
fill(p1, p2, title="BB Bands Fill", color=colorBands)

//Strategy Logic
if (long and ta.crossover(source, upper))
    strategy.entry("Long", strategy.long)

if (short and ta.crossunder(source, lower))
    strategy.entry("Short", strategy.short)

//Close positions on opposite crossover of bands
if (strategy.opentrades > 0)
    if (source <= lower)
        strategy.close("Long")
    elif (source >= upper)
        strategy.close("Short")

plotchar(strategy.position_size != 0, "Position Size", "", location.top, color=color.blue)
```