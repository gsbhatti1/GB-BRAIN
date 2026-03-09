```pinescript
/*backtest
start: 2023-09-23 00:00:00
end: 2023-10-23 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © exlux99

//@version=4


strategy(title="Swing HULL + T3 avg", shorttitle="Swing HULL T3 AVG", overlay=true)

fromDay = input(defval = 1, title = "From Day", minval = 1, maxval = 31)
fromMonth = input(defval = 1, title = "From Month", minval = 1, maxval = 12)
fromYear = input(defval = 2000, title = "From Year", minval = 1970)

// To Date Inputs
toDay = input(defval = 31, title = "To Day", minval = 1, maxval = 31)
toMonth = input(defval = 12, title = "From Month", minval = 1, maxval = 12)
toYear = input(defval = 2021, title = "To Year", minval = 1970)

startDate = timestamp(fromYear, fromMonth, fromDay, 00, 00)
finishDate = timestamp(toYear, toMonth, toDay, 00, 00)
time_cond = true


////////////////////////////GENERAL INPUTS//////////////////////////////////////

length_Ma= input(defval=50, title="Length MAs", minval=1)

//==========HMA
getHULLMA(src, len) =>
    hullma = wma(2*wma(src, len/2)-wma(src, len), round(sqrt(len)))
    hullma

//==========T3 MA
t3Len = 5
t3Ma = na
for i = 1 to t3Len
    temp := (src * ((100 - input(8.0, title="T3 Mult", minval=1)) / 100) + src.shift(i))
    if na(t3Ma)
        t3Ma := temp
    else
        t3Ma := (t3Ma * ((100 - input(8.0, title="T3 Mult", minval=1)) / 100) + temp)

plot(hullma(src, length_Ma), color=color.blue, linewidth=2, title="HULL MA")
plot(t3Ma, color=color.red, linewidth=2, title="T3 MA")

//==========Entry/Exit Conditions
hullAvg = (getHULLMA(close, length_Ma) + t3Ma) / 2

longCond = crossover(hullAvg, hullAvg.shift(-1))
shortCond = crossunder(hullAvg, hullAvg.shift(-1))

plotshape(series=longCond, location=location.belowbar, color=color.green, style=shape.triangleup, title="Long Entry")
plotshape(series=shortCond, location=location.abovebar, color=color.red, style=shape.triangledown, title="Short Entry")

//==========Stop Loss and Take Profit
longTp = input(0.08, title="TP Long")
longSl = input(true, title="SL Long")
shortTp = input(0.03, title="TP Short")
shortSl = input(0.06, title="SL Short")

strategy.entry("Long", strategy.long, when=longCond)
strategy.exit("Take Profit & Stop Loss", "Long", limit=strategy.close + longTp * close, stop=strategy.close - (close * shortSl))
strategy.entry("Short", strategy.short, when=shortCond)
strategy.exit("Take Profit & Stop Loss", "Short", limit=strategy.close - shortTp * close, stop=strategy.close + (close * longSl))

```
```