``` pinescript
/*backtest
start: 2023-12-19 00:00:00
end: 2023-12-26 00:00:00
period: 3m
backtest-only: true
*/

//@version=5
indicator("Dual RSI Breakthrough Strategy", overlay=true)

v_input_1 = input.int(14, title="Period")
v_input_2 = input.int(75, title="Upper Threshold")
v_input_3 = input.int(25, title="Lower Threshold")
v_input_4 = input.bool(false, title="Inverse Algorithm")
v_input_5 = input.bool(true, title="Show Lines")
v_input_6 = input.bool(true, title="Show Labels")
v_input_7 = input.float(2, title="Risk %")
v_input_8 = input.bool(false, title="Is this a 2 digit pair? (JPY, XAU, XPD...)")
v_input_9 = input.int(250, title="Stop Loss Pips")
v_input_10 = input.int(2500, title="Take Profit Pips")

rsiValue = rsi(close, v_input_1)

longCondition = rsiValue > v_input_2
shortCondition = rsiValue < v_input_3

plotshape(series=longCondition, title="Long Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="Long")
plotshape(series=shortCondition, title="Short Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="Short")

if (longCondition and not v_input_4)
    strategy.entry("Long", strategy.long)
    strategy.exit("Take Profit", "Long", profit_points=v_input_10)
    strategy.exit("Stop Loss", "Long", loss_points=v_input_9)
    
if (shortCondition and not v_input_4)
    strategy.entry("Short", strategy.short)
    strategy.exit("Take Profit", "Short", profit_points=v_input_10)
    strategy.exit("Stop Loss", "Short", loss_points=v_input_9)

if (v_input_5)
    hline(v_input_2, "Upper Threshold", color=color.blue)
    hline(v_input_3, "Lower Threshold", color=color.blue)

if (v_input_6)
    label.new(x=bar_index, y=high, text="Period: " + str.tostring(v_input_1), color=color.white, size=size.small)
    label.new(x=bar_index, y=low, text="Upper Threshold: " + str.tostring(v_input_2), color=color.white, size=size.small)
    label.new(x=bar_index, y=low, text="Lower Threshold: " + str.tostring(v_input_3), color=color.white, size=size.small)

// Plot the RSI value
plot(rsiValue, title="RSI Value", color=color.blue, linewidth=2)
```
```