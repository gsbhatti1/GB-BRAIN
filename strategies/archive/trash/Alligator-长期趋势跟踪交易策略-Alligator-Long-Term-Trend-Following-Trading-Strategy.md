> Source (PineScript)

```pinescript
/*backtest
start: 2023-05-11 00:00:00
end: 2024-05-16 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//_______ <licence>
// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://www.mozilla.org/en-US/MPL/2.0/
// Please ensure you understand and agree to the terms before using this script.
//_______

//@version=5
indicator("Alligator-Long-Term-Trend-Following-Trading-Strategy", overlay=true)

// Parameters
jawLength = 13
teethLength = 8
lipsLength = 5
jawShift = 8
teethShift = 5
lipsShift = 3

// Calculate Alligator Indicators
jaw = smma(close, jawLength)
teeth = smma(close, teethLength)
lips = smma(close, lipsLength)

// Plot Alligator Indicators
plot(jaw, title="Jaw", color=color.blue, linewidth=2, style=plot.style_line)
plot(teeth, title="Teeth", color=color.orange, linewidth=2, style=plot.style_line)
plot(lips, title="Lips", color=color.red, linewidth=2, style=plot.style_line)

// Strategy Logic
var float jawPrice = na
var float teethPrice = na
var float lipsPrice = na

if (barstate.islast)
    jawPrice := close[jawShift]
    teethPrice := close[teethShift]
    lipsPrice := close[lipsShift]

longCondition = crossover(jaw, teeth) and crossover(teeth, lips) and close > max(jaw, teeth, lips)
if (longCondition)
    strategy.entry("Long", strategy.long)

shortCondition = crossunder(jaw, teeth) and crossunder(teeth, lips) and close < min(jaw, teeth, lips)
if (shortCondition)
    strategy.close("Long")

// Plot Long Signal
plotshape(series=longCondition, title="Long Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="Long")

// Plot Short Signal
plotshape(series=shortCondition, title="Short Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="Short")

//_______ <disclaimer>
// This script is provided "as is" without any warranty, express or implied.
// The authors and contributors do not guarantee the accuracy or completeness of the information provided.
// The script is intended for educational and informational purposes only.
// Users should conduct their own research and due diligence before using any trading strategy.
//_______
```

This Pine Script code implements the Alligator Long-Term Trend Following Trading Strategy, with parameters and logic as described.