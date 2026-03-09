> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|8|Fast MA period|
|v_input_2|21|Slow MA period|
|v_input_3_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_4|true|Moving Average Calculation: (1 = SMA), (2 = EMA), (3 = WMA), (4 = Linear)|
|v_input_5|40|length|
|v_input_6|2|BB multiplier|


> Source (PineScript)

```pinescript
//@version=4
// Simple strategy based on MACD and Bollinger Bands

strategy("Momentum Trend", shorttitle="MT", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10, initial_capital=10000)

// Input parameters
fast_ma_period = input(8, title="Fast MA period")
slow_ma_period = input(21, title="Slow MA period")
source = input(close, title="Source")
ma_calculation = input(true, title="Moving Average Calculation: (1 = SMA), (2 = EMA), (3 = WMA), (4 = Linear)")
length = input(40, title="Length")
bb_multiplier = input(2, title="BB multiplier")

// Calculate MACD
[macd_line, signal_line, _] = macd(source, fast_ma_period, slow_ma_period, 9)

// Calculate Bollinger Bands
[bb_upperband, bb_middleband, bb_lowerband] = bollinger(source, length, bb_multiplier)

// Plot Bollinger Bands
plot(bb_upperband, color=color.red, title="BB Upper Band")
plot(bb_lowerband, color=color.blue, title="BB Lower Band")

// Strategy logic
long_condition = crossover(macd_line, signal_line) and close > bb_middleband
short_condition = crossunder(macd_line, signal_line) and close < bb_middleband

if (long_condition)
    strategy.entry("Long", strategy.long)

if (short_condition)
    strategy.entry("Short", strategy.short)

// Close positions when price crosses the middle band
if (close > bb_middleband)
    strategy.close("Long")

if (close < bb_middleband)
    strategy.close("Short")
```

This PineScript code implements a simple trading strategy based on MACD and Bollinger Bands, as described in the document. The strategy uses the default settings for inputs such as period lengths and multipliers, and it enters long or short positions when conditions are met.