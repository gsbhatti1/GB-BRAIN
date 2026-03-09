``` pinescript
/*backtest
start: 2022-11-14 00:00:00
end: 2023-11-20 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//Noro
//2018

//@version=2
strategy(title = "Dynamic-Range-Breakout-Strategy", shorttitle = "DRBS", overlay = true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, pyramiding = 10)

//Settings
capitalPercent = input(100, title="Capital, %")
bbPeriod = input(25, title="BB Period")
useBodyFilter = input(false, title="Use Body-Filter")
useColorFilter = input(false, title="Use Color-Filter")
showArrows = input(false, title="Show Arrows")
fromYear = input(1900, title="From Year")
toYear = input(2100, title="To Year")
fromMonth = input(true, title="From Month", type=input.bool)
toMonth = input(12, title="To Month")
fromDay = input(true, title="From day", type=input.bool)
toDay = input(31, title="To day")

//Indicator Calculation
length = bbPeriod
mult = 2
src = low
basis = sma(src, length)
dev = mult * stdev(src, length) 
lower = basis - dev

//Filter Conditions
abody = na
nbody = na
if (barstate.isrealtime)
    abody := close[1] + open[1]
    nbody := abs(close - open)

//Trading Signals
longCondition = low < lower and close < open or not useColorFilter and nbody > abody / 2 or not useBodyFilter 
closeCondition = close > open and nbody > abody / 2

//Position Sizing
lot = strategy.position_size == 0 ? strategy.equity * capitalPercent / 100 / close : valuewhen(strategy.closedtrades.close_time < time[1], lot[1], 0)

//Risk Control
tradeWhen = (time >= timestamp(fromYear, fromMonth ? month(time), fromDay ? dayofmonth(time), 0, 0) and time < timestamp(toYear, toMonth, today, 23, 59))

if tradeWhen and longCondition
    strategy.entry("Long", strategy.long)

if tradeWhen and closeCondition
    strategy.close("Long")

//Plotting
plotshape(series=longCondition, title="Long Entry", location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)
plotshape(series=closeCondition, title="Close Long", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)

```

This script is based on the strategy description and includes all necessary code blocks and formatting as requested.