> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|20|BB Length|
|v_input_2|2|BB MultFactor|
|v_input_3|14|RSI Length|
|v_input_4|30|RSI Oversold|
|v_input_5|70|RSI Overbought|


> Source (PineScript)

``` pinescript
// backtest
// start: 2024-01-01 00:00:00
// end: 2024-01-31 23:59:59
// period: 1h
// basePeriod: 

//@version=5
strategy("Dual-Moving-Average-and-Bollinger-Band-Combination-Trend-Tracking-Strategy", shorttitle="DMABBTCSS", overlay=true)

bb_length = input(20, title="BB Length")
bb_mult_factor = input(2, title="BB MultFactor")
rsi_length = input(14, title="RSI Length")
rsi_oversold = input(30, title="RSI Oversold")
rsi_overbought = input(70, title="RSI Overbought")

[bb_lower, bb_upper] = ta.bbands(close, bb_length, 2, bb_mult_factor)
rsi = ta.rsi(close, rsi_length)

plot(bb_lower, color=color.red, title="BB Lower")
plot(bb_upper, color=color.green, title="BB Upper")
plot(rsi, color=color.blue, title="RSI")

longCondition = rsi < rsi_oversold and close <= bb_lower
shortCondition = rsi > rsi_overbought and close >= bb_upper

if (longCondition)
    strategy.entry("Long", strategy.long)

if (shortCondition)
    strategy.entry("Short", strategy.short)

// plotshape(series=longCondition, location=location.belowbar, color=color.green, style=shape.labelup, title="Long Entry")
// plotshape(series=shortCondition, location=location.abovebar, color=color.red, style=shape.labeldown, title="Short Entry")
```
```