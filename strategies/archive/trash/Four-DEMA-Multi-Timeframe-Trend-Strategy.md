``` pinescript
/*backtest
start: 2023-02-19 00:00:00
end: 2024-02-25 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
//Author: HighProfit

//Lead-In
strategy("Four DEMA Multi Timeframe Trend Strategy", shorttitle="4DEMA-MTTS", overlay=true)

short = input(10, minval=1)
srcShort = input(close, title="Source Dema 1")

long = input(15, minval=1)
srcLong = input(close, title="Source Dema 2")

long2 = input(21, minval=1)
srcLong2 = input(close, title="Source Dema 3")

long3 = input(30, minval=1)
srcLong3 = input(close, title="Source Dema 4")

e1 = ema(srcShort, short)
e2 = ema(e1, short)
dema1 = 2 * e1 - e2
plot(dema1, color=color.green, linewidth = 2)

e3 = ema(srcLong, long)
e4 = ema(e3, long)
dema2 = 2 * e3 - e4
plot(dema2, color=color.blue, linewidth = 2)

e5 = ema(srcLong2, long2)
e6 = ema(e5, long2)
dema3 = 2 * e5 - e6
plot(dema3, color=color.black, linewidth = 2)

e7 = ema(srcLong3, long3)
e8 = ema(e7, long3)
dema4 = 2 * e7 - e8
plot(dema4, color=color.red, linewidth = 2)

//Conditions
longCondition = (dema1>dema2) and (dema1>dema3) and (dema1>dema4) and (dema2>dema3) and (dema2>dema4) and (dema3>dema4)
if (longCondition)
    strategy.entry("Long", strategy.long)

shortCondition = (dema4>dema3) and (dema4>dema2) and (dema4>dema1) and (dema3>dema2) and (dema3>dema1) and (dema2>dema1)
if (shortCondition)
    strategy.entry("Short", strategy.short)

strategy.close("Long",  cross(dema1,dema2))
strategy.close("Short", cross(dema1,dema2))

bgcolor(longCond)
```