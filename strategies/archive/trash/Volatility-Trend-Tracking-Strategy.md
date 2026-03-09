```pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// Noro
// 2018

//@version=2
strategy(title = "Noro's WaveTrend-Tracking-Strategy", shorttitle="WaveTrend-Tracking-Strategy", overlay=true)

input longCondition = true, title="Long Condition"
input shortCondition = true, title="Short Condition"
input useMartingale = false, title="Use Martingale"
input capitalPercent = 100, title="% Capital"
input showArrows = true, title="Show Arrows"
input fromYear = 2018, title="From Year"
input toYear = 2024, title="To Year"
input fromMonth = 1, title="From Month"
input toMonth = 12, title="To Month"
input fromDay = 1, title="From Day"
input toDay = 31, title="To Day"

// WaveTrend Indicator
esa = ema(hlc3, 10)
d = ema(abs(hlc3 - esa), 10)
ci = (hlc3 - esa) / (0.015 * d)
wt = ema(ci, 21)

// RSI Indicator
rsiup = rma(max(change(close), 0), 14)
rsidown = rma(-min(change(close), 0), 14)
rsi = rsidown == 0 ? 100 : rsiup == 0 ? 0 : 100 - (100 / (1 + rsiup / rsidown))

// Overbought/Oversold Conditions
overboughtCondition = rsi > 75 and wt < -60
oversoldCondition = rsi < 25 and wt > -60

// Trading Logic
if (longCondition and oversoldCondition)
    strategy.entry("Long", strategy.long)

if (shortCondition and overboughtCondition)
    strategy.entry("Short", strategy.short)

// Martingale Strategy
if (useMartingale) {
    // Implement Martingale logic here
}

// Plot Arrows
plotshape(series=overboughtCondition, location=location.abovebar, color=color.red, style=shape.triangleup, title="Overbought")
plotshape(series=oversoldCondition, location=location.belowbar, color=color.green, style=shape.triangledown, title="Oversold")

```

This script uses the given Pine Script structure and translates the human-readable text accordingly. The code blocks remain unchanged as per your instruction.