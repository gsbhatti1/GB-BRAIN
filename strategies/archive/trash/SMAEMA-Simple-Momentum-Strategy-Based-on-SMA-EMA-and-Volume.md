```pinescript
plot(sma_line, color = #8b0000, title = "SMA Line", linewidth = 2)
plot(ema_line, color = #008b8b, title = "EMA Line", linewidth = 2)
plotshape(series = crossover(sma_line, ema_line), location = location.abovebar, color = #00cc00, style = shape.triangleup, title = "Entry Signal")
plotshape(series = crossunder(sma_line, ema_line), location = location.belowbar, color = #ff0000, style = shape.triangledown, title = "Exit Signal")
```

// Entry and Exit Conditions
long_entry = ta.crossover(sma_line, ema_line) and (ta.barssince(sma_line < ema_line) >= 1) and (ta.barssince(sma_line > ema_line) >= 3 or ta.barssince(sma_line > ema_line) >= 4) and (ta.lowest(sma_line, 2)[1] >= open[1])
long_exit = ta.crossunder(sma_line, ema_line)

// Execute trades
if (long_entry)
    strategy.entry("Long", strategy.long)
if (long_exit)
    strategy.exit("Exit Long", "Long")

// Volume Trigger
vol_trigger = volume > volume_trigger

// Combine Entry and Volume conditions
long_condition = long_entry and vol_trigger

// Execute trades based on combined conditions
if (long_condition)
    strategy.entry("Long", strategy.long)
if (long_exit)
    strategy.close("Long")

// Plotting
plot(sma_line, color = #8b0000, title = "SMA Line", linewidth = 2)
plot(ema_line, color = #008b8b, title = "EMA Line", linewidth = 2)
plotshape(series = long_entry, location = location.abovebar, color = #00cc00, style = shape.triangleup, title = "Entry Signal")
plotshape(series = long_exit, location = location.belowbar, color = #ff0000, style = shape.triangledown, title = "Exit Signal")
```

```