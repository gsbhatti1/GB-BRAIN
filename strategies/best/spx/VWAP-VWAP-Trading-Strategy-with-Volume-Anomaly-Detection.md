> Source (PineScript)

``` pinescript
/*backtest
start: 2024-05-30 00:00:00
end: 2024-06-06 00:00:00
period: 1 day
*/

//@version=5
indicator("VWAP Trading Strategy with Volume Anomaly Detection", shorttitle="VWAP-Trading-Strategy", overlay=true)

// Define VWAP Levels
openVWAP = request.security(syminfo.tickerid, "240", ta.vwap(ta.open))
highVWAP = request.security(syminfo.tickerid, "240", ta.vwap(ta.highest(high, 14)))
lowVWAP = request.security(syminfo.tickerid, "240", ta.vwap(ta.lowest(low, 14)))
highVolumeCandle = security(syminfo.tickerid, "240", bool(find(highest(volume, 14), highest(high, 14))))
abnormallyHighVWAP = request.security(syminfo.tickerid, "240", ta.vwap(highVolumeCandle ? high : low))

// Calculate Displacement Values
displacement = 3.0

// Check for Gaps
gapOpen = close < open[1]
gapUp = open > highest(high, 1)
gapDown = open < lowest(low, 1)

// Generate Trading Signals
longSignal = close > highVWAP + displacement and not gapOpen and not gapDown
shortSignal = close < lowVWAP - displacement and not gapOpen and not gapUp

plotshape(series=longSignal, title="Long Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="LONG")
plotshape(series=shortSignal, title="Short Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SHORT")

// RSI for Exit Condition
rsiPeriod = 14
rsiLength = input.int(70, minval=1)
rsiExitLong = ta.rsi(close, rsiPeriod) > rsiLength
rsiExitShort = ta.rsi(close, rsiPeriod) < (100 - rsiLength)

// Plot VWAP Levels and RSI
plot(openVWAP, color=color.blue, title="Open VWAP")
plot(highVWAP, color=color.orange, title="High VWAP")
plot(lowVWAP, color=color.purple, title="Low VWAP")
plot(abnormallyHighVWAP, color=color.red, title="Abnormal High Volume VWAP")

hline(rsiLength, "RSI Exit Level Long", color=color.green)
hline(100 - rsiLength, "RSI Exit Level Short", color=color.red)

// Plot Gaps
plotshape(series=gapUp, title="Gap Up", location=location.top, color=color.blue, style=shape.triangleup, text="UP GAP")
plotshape(series=gapDown, title="Gap Down", location=location.bottom, color=color.red, style=shape.triangledown, text="DOWN GAP")

// Exit Conditions
strategy.entry("Long", strategy.long, when=longSignal)
strategy.exit("RSI Exit Long", "Long", loss=(100 - rsiLength), profit=rsiLength)
strategy.exit("RSI Exit Short", "Short", loss=rsiLength, profit=(100 - rsiLength))
```