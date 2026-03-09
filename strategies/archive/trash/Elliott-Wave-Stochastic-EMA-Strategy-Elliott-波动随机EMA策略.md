``` pinescript
/*backtest
start: 2024-05-30 00:00:00
end: 2024-06-06 00:00:00
period: 3h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License Version 2.0.

//@version=5
indicator("Elliott-Wave-Stochastic-EMA-Strategy", overlay=false)

// Define EMA periods and Stochastic settings
emaShort = input.int(5, title="Short EMA Period")
emaMedium = input.int(10, title="Medium EMA Period")
emaLong  = input.int(20, title="Long EMA Period")
emaVeryLong = input.int(50, title="Very Long EMA Period")
emaExtremelyLong = input.int(200, title="Extremely Long EMA Period")

k = input.float(3, title="%K", minval=1)
d = input.float(3, title="%D", minval=1)

// Calculate EMAs
shortEMA = ta.ema(close, emaShort)
mediumEMA = ta.ema(close, emaMedium)
longEMA  = ta.ema(close, emaLong)
veryLongEMA = ta.ema(close, emaVeryLong)
extremelyLongEMA = ta.ema(close, emaExtremelyLong)

// Calculate Stochastic %K and %D
highLowRange = ta.highest(high, 14) - ta.lowest(low, 14)
stochK = (close - ta.lowest(low, 14)) / highLowRange * 100
stochD = ta.sma(stochK, 3)

// Buy and Sell Signals
buySignal = close > shortEMA and stochK > d
sellSignal = close < shortEMA and stochK < d

plotshape(series=buySignal, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")
plotshape(series=sellSignal, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

// Plot EMAs
plot(shortEMA, title="Short EMA", color=color.blue)
plot(mediumEMA, title="Medium EMA", color=color.orange)
plot(longEMA, title="Long EMA", color=color.green)
plot(veryLongEMA, title="Very Long EMA", color=color.red)
plot(extremelyLongEMA, title="Extremely Long EMA", color=color.purple)

// Plot Stochastic
hline(80, "Overbought")
hline(20, "Oversold")
plot(stochK, title="%K", color=color.blue, linewidth=1)
```