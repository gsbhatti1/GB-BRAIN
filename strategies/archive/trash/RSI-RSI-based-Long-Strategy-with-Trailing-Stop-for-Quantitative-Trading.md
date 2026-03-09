``` pinescript
// RSI-based Long Strategy with Trailing Stop for Quantitative Trading
study("RSI-based Long Strategy with Trailing Stop", shorttitle="RSI-Long-Strategy", overlay=true)

// Strategy Arguments
length = input(14, title="Length")
overSold = input(30, title="OverSold")
overBought = input(70, title="OverBought")
percent_diff = input(5, title="Percent Diff")

// Calculate RSI
rsi = rsi(close, length)

// Determine entry and exit conditions
longCondition = rsi < overSold and rsi[1] >= overSold
shortCondition = rsi > overBought and rsi[1] <= overBought

// Calculate stop loss price
stopLossPrice = na
if (longCondition)
    stopLossPrice := close - (close * (percent_diff / 100))

// Plot RSI and stop loss price
plot(rsi, title="RSI", color=color.blue, linewidth=2)
plot(stopLossPrice, title="Stop Loss Price", color=color.red, linewidth=1)

// Entry and exit logic
if (longCondition)
    strategy.entry("Long", strategy.long, when=longCondition)
    strategy.exit("Stop Loss", from_entry="Long", stop=stopLossPrice)

// Optional: Plot strategy performance
plotshape(series=strategy.position_size > 0, location=location.belowbar, color=color.green, style=shape.triangleup, title="Long Position")

```
[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|14|length|
|v_input_2|30|overSold|
|v_input_3|70|overBought|
|v_input_4|5|percent_diff|


> Source (PineScript)

``` pinescript
// RSI-based Long Strategy with Trailing Stop for Quantitative Trading
study("RSI-based Long Strategy with Trailing Stop", shorttitle="RSI-Long-Strategy", overlay=true)

// Strategy Arguments
length = input(14, title="Length")
overSold = input(30, title="OverSold")
overBought = input(70, title="OverBought")
percent_diff = input(5, title="Percent Diff")

// Calculate RSI
rsi = rsi(close, length)

// Determine entry and exit conditions
longCondition = rsi < overSold and rsi[1] >= overSold
shortCondition = rsi > overBought and rsi[1] <= overBought

// Calculate stop loss price
stopLossPrice = na
if (longCondition)
    stopLossPrice := close - (close * (percent_diff / 100))

// Plot RSI and stop loss price
plot(rsi, title="RSI", color=color.blue, linewidth=2)
plot(stopLossPrice, title="Stop Loss Price", color=color.red, linewidth=1)

// Entry and exit logic
if (longCondition)
    strategy.entry("Long", strategy.long, when=longCondition)
    strategy.exit("Stop Loss", from_entry="Long", stop=stopLossPrice)

// Optional: Plot strategy performance
plotshape(series=strategy.position_size > 0, location=location.belowbar, color=color.green, style=shape.triangleup, title="Long Position")

```