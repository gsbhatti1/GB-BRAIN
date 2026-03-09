``` pinescript
/*backtest
start: 2025-02-16 17:00:00
end: 2025-02-18 03:00:00
period: 2m
basePeriod: 2m
exchanges: [{"eid":"Binance","currency":"SOL_USDT"}]
*/

//@version=6
strategy("Inverted FVG Strategy with Trend Check and Trailing Stops", overlay=true)

// Function to detect FVG
fvgDetected(src, high, low) =>
    var float prevHigh = na
    var float prevLow = na
    var float prevClose = na
    var bool fvg = false
    if (not na(src[1]))
        prevHigh := high[1]
        prevLow := low[1]
        prevClose := src[1]
        if (src > prevClose and low > prevHigh) or (src < prevClose and high < prevLow)
            fvg := true
    [fvg, prevHigh, prevLow]

// Detect FVG on the chart
[fvg, fvgHigh, fvgLow] = fvgDetected(close, high, low)

// Detect IFVG - Inversion of FVG
var bool ifvg = false
var float ifvgHigh = na
var float ifvgLow = na
if (fvg)
    if not na(fvgHigh) and not na(fvgLow)
        if (close > fvgHigh and close[1] < fvgHigh) or (close < fvgLow and close[1] > fvgLow)
            ifvg := true
            ifvgHigh := close > fvgHigh ? high : na
            ifvgLow := close < fvgLow ? low : na

// Plot FVG and IFVG zones for visualization
bgcolor(ifvg ? color.new(color.red, 80) : na)
plot(ifvgHigh, title="IFVG High", color=color.red, linewidth=2, style=plot.style_cross)
plot(ifvgLow, title="IFVG Low", color=color.red, linewidth=2, style=plot.style_cross)

// Trend Check using Simple Moving Averages
smaShort = ta.sma(close, 50)  // Short term
smaLong = ta.sma(close, 200)  // Long term

// Entry Conditions
longCondition = crossover(smaShort, smaLong)
shortCondition = crossunder(smaShort, smaLong)

// Risk Management: Fixed Stop Loss and ATR-based Trailing Stops
atrValue = ta.atr(14)
trailPercent = 0.02

if (longCondition)
    strategy.entry("Long", strategy.long)
    stopLossPrice = ifvgLow - atrValue * trailPercent
    strategy.exit("Profit Target Long", "Long", stop=stopLossPrice, limit=stopLossPrice + atrValue * 3)

if (shortCondition)
    strategy.entry("Short", strategy.short)
    stopLossPrice = ifvgHigh + atrValue * trailPercent
    strategy.exit("Profit Target Short", "Short", stop=stopLossPrice, limit=stopLossPrice - atrValue * 3)
```

Note: The original PineScript code provided only included the FVG and IFVG detection logic. The full entry and risk management conditions have been added to complete the strategy.