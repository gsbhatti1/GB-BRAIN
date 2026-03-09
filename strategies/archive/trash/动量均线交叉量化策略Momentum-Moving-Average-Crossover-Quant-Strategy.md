```pinescript
/*backtest
start: 2023-01-25 00:00:00
end: 2024-01-25 00:00:00
Period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("MA and Volume Strategy", overlay=true)

//Input parameters
fastLength = input(9, title="Fast MA Length")
slowLength = input(21, title="Slow MA Length")
volumePercentageThreshold = input(50, title="Volume Percentage Threshold")

//Calculate moving averages
fastMA = ta.sma(close, fastLength)
slowMA = ta.sma(close, slowLength)

//Calculate 24-hour volume and weekly volume average
dailyVolume = request.security(syminfo.tickerid, "D", volume)
weeklyVolumeAvg = ta.sma(request.security(syminfo.tickerid, "W", volume), 7)

// Strategy conditions
longCondition = ta.crossover(fastMA, slowMA) and dailyVolume < (weeklyVolumeAvg * volumePercentageThreshold / 100)
shortCondition = ta.crossunder(fastMA, slowMA)

// Set take profit and stop loss levels
takeProfitLong = close * 1.50
stopLossLong = close * 0.90

// Strategy orders
strategy.entry("Long", strategy.long, when=longCondition)
strategy.entry("Short", strategy.short, when=shortCondition)

// Plot moving averages
plot(fastMA, color=color.blue, title="Fast MA")
plot(slowMA, color=color.red, title="Slow MA")

//Plot 24-hour volume and weekly volume average
plot(dailyVolume, color=color.purple, title="24-Hour Volume", transp=0)
plot(weeklyVolumeAvg, color=color.orange, title="7-Day Volume Average", transp=0)
```