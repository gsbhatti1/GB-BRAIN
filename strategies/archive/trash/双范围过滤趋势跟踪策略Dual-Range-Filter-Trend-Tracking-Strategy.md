```pinescript
//@version=4
strategy("Range Filter [DW] & Labels", shorttitle="RF [DW] & Labels", overlay=true)

// Conditional Sampling EMA Function 
Cond_EMA(x, len, src) =>
    ema(x, len) > ema(x, len + 1) ? ema(x, len) : ema(x, len + 1)

// Input Arguments
filter_type = input(0, title="Filter Type", options=["Type 1", "Type 2"])
movement_source = input(0, title="Movement Source", options=["Close", "Wicks"])
range_size = input(2.618, title="Range Size")
range_scale = input(0, title="Range Scale", options=["Average Change", "Pips", "Ticks", "% of Price", "ATR", "Points", "Standard Deviation", "Absolute"])
range_period = input(14, title="Range Period (for ATR, Average Change, and Standard Deviation)")
smooth_range = input(true, title="Smooth Range")
smoothing_period = input(27, title="Smoothing Period")
avg_filter_changes = input(true, title="Average Filter Changes")
num_changes_avg = input(2, title="Number Of Changes To Average")
take_profit_percent = input(100, title="Take Profit Percentage")
stop_loss_percent = input(100, title="Stop Loss Percentage")

// ATR Calculation
atr = ta.atr(range_period)

// Range Calculation
range_high = ta.highest(high, range_period)
range_low = ta.lowest(low, range_period)

// EMA Calculation
ema1 = ta.ema(close, range_period)
ema2 = ta.ema(close, range_period * range_size)

// Smooth Range
if (smooth_range)
    smooth_range_high = ta.sma(range_high, smoothing_period)
    smooth_range_low = ta.sma(range_low, smoothing_period)
else
    smooth_range_high = range_high
    smooth_range_low = range_low

// Filter Type 1 or 2
filter_type_1 = ema1 > ema2
filter_type_2 = ema1 < ema2

// Movement Source
if (movement_source == 0)  // Close
    movement = close
else  // Wicks
    movement = high - low

// Filter Logic
if (filter_type == 0)  // Type 1
    trend_filter = filter_type_1
else  // Type 2
    trend_filter = filter_type_2

// Range Breakout
range_breakout = movement > (smooth_range_high - smooth_range_low) * range_size

// Strategy Logic
if (range_breakout and trend_filter)
    strategy.entry("Long", strategy.long)

// Stop Loss and Take Profit
if (barstate.islast)
    if (strategy.position_size > 0)
        strategy.exit("Profit", from_entry="Long", limit=close * (1 + take_profit_percent / 100), stop=close * (1 - stop_loss_percent / 100))

// Plotting
plot(trend_filter, color=color.blue, title="Trend Filter")
plot(range_breakout, color=color.red, title="Range Breakout")
```

This Pine Script implements the Dual Range Filter Trend Tracking Strategy as described, with the necessary code blocks and formatting intact.