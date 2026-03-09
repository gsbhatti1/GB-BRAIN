``` pinescript
f_emaRibbon(_src, _e1, _e2, _e3, _e4, _e5, _e6, _e7, _e8) =>
    _ema1 = ta.ema(_src, _e1)
    _ema2 = ta.ema(_src, _e2)
    _ema3 = ta.ema(_src, _e3)
    _ema4 = ta.ema(_src, _e4)
    _ema5 = ta.ema(_src, _e5)
    _ema6 = ta.ema(_src, _e6)
    _ema7 = ta.ema(_src, _e7)
    _ema8 = ta.ema(_src, _e8)

// Variables
var float ema1 = na
var float ema2 = na
var float ema3 = na
var float ema4 = na
var float ema5 = na
var float ema6 = na
var float ema7 = na
var float ema8 = na

// Calculate EMAs and plot them if showRibbon is enabled
if (v_input_1)
    ema1 := f_emaRibbon(close, v_input_2, v_input_3, v_input_4, v_input_5, v_input_6, v_input_7, v_input_8, 0)
    strategy.entry("Buy", strategy.long, when = ta.crossover(ema1, ema8) and ta.highest(close, 1) > ta.valuewhen(ta.crossover(ema1, ema8), close, 1))
    
// Ichimoku Cloud
tenkan_sen = (ta.ema(close, v_input_int_12) + ta.ema(close, v_input_int_13)) / 2
kijun_sen = ta.ema(close, v_input_int_14)
senkou_span_a = (tenkan_sen + kijun_sen) / 2
senkou_span_b = ta.ema(close, v_input_int_15)

// Plot Cloud
plot(tenkan_sen, title="Tenkan-sen", color=color.blue)
plot(kijun_sen, title="Kijun-sen", color=color.red)
hline(0, "Zero Line")

if (v_input_2 or v_input_3 or v_input_4 or v_input_5 or v_input_6 or v_input_7 or v_input_8)
    plot(senkou_span_a, title="Senkou Span A", color=color.blue, style=plot.style_linebr)
    plot(senkou_span_b, title="Senkou Span B", color=color.red, style=plot.style_linebr)

// Signal Generation
if (ta.crossover(ema1, ema8) and close > senkou_span_a[displacement])
    strategy.entry("Buy", strategy.long)
else if (ta.crossunder(ema1, ema8))
    strategy.close("Buy")

// Plotting Cloud
plotchar(v_input_2 or v_input_3 or v_input_4 or v_input_5 or v_input_6 or v_input_7 or v_input_8 ? true : false, title="Show Ribbon", location=location.top, color=color.new(color.blue, 0), size=size.small)
```

This script includes the functions and logic for both the EMA ribbon and Ichimoku cloud. It also handles entry and exit conditions based on the strategy description provided.