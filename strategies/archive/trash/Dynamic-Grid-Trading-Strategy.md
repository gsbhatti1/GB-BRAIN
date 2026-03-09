> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|300|(?Moving Average Conditions)Moving Average Length|
|v_input_float_1|0.03|(?Grid Conditions)Upper and Lower Grid Deviation|
|v_input_int_2|15|Grid Line Quantity|


> Source (PineScript)

```pinescript
// Strategy Arguments
input int v_input_int_1 = 300 // (?Moving Average Conditions) Moving Average Length
input float v_input_float_1 = 0.03 // (?Grid Conditions) Upper and Lower Grid Deviation
input int v_input_int_2 = 15 // Grid Line Quantity

// Strategy Description
//@version=5
strategy("Dynamic-Grid-Trading-Strategy", overlay=true)

ma_length = input.int(v_input_int_1, title="Moving Average Length")
std_dev = input.float(v_input_float_1, title="Upper and Lower Grid Deviation")
grid_lines = input.int(v_input_int_2, title="Grid Line Quantity")

// Calculate Moving Average
sma_value = sma(close, ma_length)

// Calculate Upper and Lower Tracks
upper_track = sma_value * (1 + std_dev)
lower_track = sma_value * (1 - std_dev)

// Define Grid Lines
grid_lines_array = array.new_float(grid_lines, 0.0)
for i = 0 to grid_lines - 1
    line.new(x1=i, y1=na, x2=i, y2=sma_value + ((i / grid_lines) * (upper_track - sma_value)), color=color.blue)

// Trading Logic
order_array = array.new_bool(grid_lines, false)
for i = 0 to grid_lines - 1
    if close > upper_track and not array.get(order_array, i)
        order_array.set(i, true)
        strategy.entry("Long", strategy.long)
    else if close < lower_track and array.get(order_array, i)
        previous_index = math.max(0, i - 1)
        line.new(x1=i-1, y1=sma_value + ((previous_index / grid_lines) * (upper_track - sma_value)), x2=i, y2=lower_track, color=color.red)
        order_array.set(previous_index, false)
        strategy.close("Long")
```

```