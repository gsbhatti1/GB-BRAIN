> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Long|
|v_input_2|true|Short|
|v_input_3|100|Lot|
|v_input_4|50|MA 1 Length|
|v_input_5|100|MA 2 Length|
|v_input_6|200|MA 3 Length|
|v_input_7_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_8|false|Show Background|
|v_input_9|1900|From Year|
|v_input_10|2100|To Year|
|v_input_11|true|From Month|
|v_input_12|12|To Month|
|v_input_13|true|From day|
|v_input_14|31|To day|


> Source (PineScript)

```pinescript
//@version=3
strategy(title = "Williams' Alligator Strategy", shorttitle = "Alligator", overlay = true)

// Input parameters
longCondition = input(true, title="Long")
shortCondition = input(true, title="Short")
lotSize = input(100, title="Lot")
ma1Length = input(50, title="MA 1 Length")
ma2Length = input(100, title="MA 2 Length")
ma3Length = input(200, title="MA 3 Length")
source = input(close, title="Source")
showBackground = input(false, title="Show Background")
fromYear = input(1900, title="From Year")
toYear = input(2100, title="To Year")
fromMonth = input(true, title="From Month")
toMonth = input(12, title="To Month")
fromDay = input(true, title="From day")
toDay = input(31, title="To day")

// Moving Averages
sma1 = sma(source, ma1Length)
sma2 = sma(source, ma2Length)
sma3 = sma(source, ma3Length)

// Trend determination
longCondition = crossover(sma1, sma2) and crossover(sma2, sma3)
shortCondition = crossunder(sma1, sma2) and crossunder(sma2, sma3)

// Plotting
plotshape(series=longCondition, title="Long Entry", location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)
plotshape(series=shortCondition, title="Short Entry", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)

// Background color for trend indication
bgcolor(color=color.new(color.green, 90), title="Uptrend", condition=longCondition)
bgcolor(color=color.new(color.red, 90), title="Downtrend", condition=shortCondition)

// Strategy entries and exits
if (longCondition)
    strategy.entry("Long", strategy.long, lot=lotSize)

if (shortCondition)
    strategy.entry("Short", strategy.short, lot=lotSize)

// Exit conditions
if (sma1 < sma2 or sma2 < sma3)
    strategy.close("Long")
    strategy.close("Short")
```

This Pine Script implements the Williams Alligator strategy with the specified inputs and logic.