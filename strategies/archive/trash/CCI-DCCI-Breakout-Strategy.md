> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|false|Strategy Direction|
|v_input_2|true|-----------------Strategy Inputs-------------------|
|v_input_3|false|Strategy Stop Mult|
|v_input_4|16|CCI Length|
|v_input_5|5|WMA Length|
|v_input_6|true|-----------------General Inputs-------------------|
|v_input_7|true|Use Stop Loss and Take Profit|
|v_input_8|0|Type Of Stop: ATR Stop|Swing Lo/Hi|Strategy Stop|
|v_input_9|10|Swing Point Lookback|
|v_input_10|2|Swing Point SL Perc Increment|
|v_input_11|14|ATR Length|
|v_input_12|10|ATR Multiple|
|v_input_13|1.5|Take Profit Risk Reward Ratio|
|v_input_14|true|Allow Direct Position Reverse|
|v_input_15|false|Reverse Trades|


> Source (PineScript)

```pinescript
//@version=5
strategy("DCCI Breakout Strategy", shorttitle="DCCI-Breakout-Strategy", default_qty_type=strategy.percent_of_equity, default_qty_value=10, overlay=true)

// Input Arguments
dir_input = input.bool(false, title="Strategy Direction")
use_inputs2 = input.bool(true, title="-----------------Strategy Inputs-------------------")
stop_mult_input = input.bool(false, title="Strategy Stop Mult")
cci_len_input = input.int(16, title="CCI Length", minval=1)
wma_len_input = input.int(5, title="WMA Length", minval=1)
general_inputs = input.bool(true, title="-----------------General Inputs-------------------")
use_sl_tp = input.bool(true, title="Use Stop Loss and Take Profit")
stop_type_input = input.string("", title="Type Of Stop: ATR Stop|Swing Lo/Hi|Strategy Stop", options=["ATR Stop", "Swing Lo/Hi", "Strategy Stop"])
swing_lookback_input = input.int(10, title="Swing Point Lookback", minval=1)
swing_sl_perc_inc_input = input.float(2, title="Swing Point SL Perc Increment", minval=0.5)
atr_len_input = input.int(14, title="ATR Length", minval=1)
atr_mult_input = input.int(10, title="ATR Multiple")
risk_reward_ratio_input = input.float(1.5, title="Take Profit Risk Reward Ratio", minval=1)
allow_reverse_input = input.bool(true, title="Allow Direct Position Reverse")
reverse_trades_input = input.bool(false, title="Reverse Trades")

// CCI Calculation
cci = ta.cci(close, cci_len_input, 14)

// WMA Calculation
wma = ta.wma(close, wma_len_input)

// Swing Points and Stop Loss Calculation
if (dir_input)
    // Long Condition
    long_condition = cci < -100 and close > wma
else
    // Short Condition
    short_condition = cci > 100 and close < wma

swing_high = ta.highest(high, swing_lookback_input)
swing_low = ta.lowest(low, swing_lookback_input)

// Stop Loss Calculation Based on Selected Type
if (use_sl_tp)
    if (stop_type_input == "ATR Stop")
        atr = ta.atr(atr_len_input)
        stop_loss_level = close - (atr * atr_mult_input)
    else if (stop_type_input == "Swing Lo/Hi")
        stop_loss_level = swing_low
    else if (stop_type_input == "Strategy Stop")
        stop_loss_level = wma

// Order Placement
if (dir_input and long_condition and use_sl_tp)
    strategy.entry("Long", strategy.long, stop=stop_loss_level)

if (not dir_input and short_condition and use_sl_tp)
    strategy.entry("Short", strategy.short, stop=stop_loss_level)

// Take Profit Calculation
take_profit_level = close * (1 + risk_reward_ratio_input)

// Reverse Trade Check
reverse_long_cond = long_condition and not reverse_trades_input
reverse_short_cond = short_condition and not reverse_trades_input

if (allow_reverse_input)
    if (dir_input and swing_high > wma and not allow_reverse_input)
        strategy.close("Long", comment="Reverse Condition Met")
    
    if (not dir_input and swing_low < wma and not allow_reverse_input)
        strategy.close("Short", comment="Reverse Condition Met")

// Plotting
plot(cross(close, wma) ? close : na, title="CCI Crossover", color=color.blue, style=plot.style_candlestick)
hline(-100, "Overbought", color=color.red, linestyle=hline.style_dashed)
hline(100, "Oversold", color=color.green, linestyle=hline.style_dashed)

```
```