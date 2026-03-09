> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|90|selllevel|
|v_input_2|65|drop|
|v_input_3|50|buylevel|


> Source (PineScript)

```pinescript
//@version=5
strategy("PlanB RSI Tracking Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)
selllevel = input(90.0, "selllevel")
drop = input(65.0, "drop")
buylevel = input(50.0, "buylevel")

// Calculate RSI
rsi = ta.rsi(close, 14)

// Sell condition: highest RSI in the past 6 months > selllevel and current RSI < drop
if (ta.highest(rsi, 183) > selllevel and rsi < drop)
    strategy.entry("Sell", strategy.short)

// Buy condition: lowest RSI in the past 6 months < buylevel and RSI bounces >2% from the lowest point
var float low_rsi = na
if (ta.lowest(rsi, 183) < buylevel)
    low_rsi := ta.lowest(rsi, 183)
if rsi > low_rsi * 1.02
    strategy.entry("Buy", strategy.long)

// Plot RSI on chart
plot(rsi, title="RSI", color=color.blue)
```

[/trans]