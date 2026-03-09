```pinescript
/*backtest
start: 2023-11-07 00:00:00
end: 2023-12-07 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 25/03/2020
// This is a combination strategy to get a cumulative signal. 
//
// First strategy
// This system was created from the book "How I Tripled My Money In The Futures Market" by Ulf Jensen, Page 183. 
// This is a reversal type of strategy.
// The strategy buys at market, if the close price is higher than the previous close for 2 consecutive days 
// and the 9-day Slow Stochastic Oscillator is below 50. 
// The strategy sells at market, if the close price is lower than the previous close for 2 consecutive days.
//

study("Reversal-Dynamic-Pivot-Points-Exponential-Moving-Average-Strategy", shorttitle="RDPP-EMA", precision=2)

length = input(14, title="Length")
kSmoothing = input(true, title="KSmoothing")
dLength = input(3, title="DLength")
level = input(50, title="Level")
tradeReverse = input(false, title="Trade reverse")

// Calculate Slow Stochastic Oscillator
stochSlow = stoch(close, high, low, length, 3, 3, 0)

// Calculate Pivot Points
pivotHigh = highest(high, dLength)
pivotLow = lowest(low, dLength)
pivotClose = close[1]
pivotPoint = (pivotHigh + pivotLow + pivotClose) / 3
support1 = pivotPoint - (pivotHigh - pivotPoint)
resistance1 = pivotPoint + (pivotPoint - pivotLow)

// Reversal Strategy
longCondition = close > close[1] and close > close[2] and stochSlow < level
shortCondition = close < close[1] and close < close[2] and stochSlow > level

// Dynamic Support and Resistance Strategy
buySignal = close > resistance1
sellSignal = close < support1

// Trade based on dual signals
if (longCondition and not tradeReverse) or (shortCondition and tradeReverse)
    if not tradeReverse
        strategy.entry("Long", strategy.long)
    else
        strategy.entry("Short", strategy.short)

// Exit based on support and resistance
if (not longCondition and buySignal) or (not shortCondition and sellSignal)
    if not tradeReverse
        strategy.close("Long")
    else
        strategy.close("Short")

// Plot signals
plotshape(series=longCondition, title="Long Signal", location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)
plotshape(series=shortCondition, title="Short Signal", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)

// Plot support and resistance levels
plot(pivotPoint, title="Pivot Point", color=color.orange, linewidth=2)
plot(support1, title="Support 1", color=color.blue, linewidth=2)
plot(resistance1, title="Resistance 1", color=color.red, linewidth=2)
```