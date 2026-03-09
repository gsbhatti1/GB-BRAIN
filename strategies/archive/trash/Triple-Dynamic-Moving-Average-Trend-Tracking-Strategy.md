> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_float_1|10000|(?-------------------- Risk Management  --------------------)Initial Balance|
|v_input_bool_1|true|qty based on equity %|
|v_input_float_2|false|MarginFactor|
|v_input_float_3|3.5|Quantity Contracts|
|v_input_bool_2|true|(?-------------------- Moving Average 1 --------------------)Plot MA trend?|
|v_input_timeframe_1|15|Higher Time Frame|
|v_input_int_1|21|Length MA|
|v_input_string_1|0|MA type:: McGinley|DEMA|TEMA|SMA|WMA|HMA|EMA|
|v_input_bool_3|true|(?-------------------- Moving Average 2 --------------------)Plot Second MA trend?|
|v_input_timeframe_2|60|HTF|
|v_input_int_2|21|Length Second MA|
|v_input_string_2|0|MA type:: McGinley|DEMA|TEMA|SMA|WMA|HMA|EMA|
|v_input_bool_4|true|(?-------------------- Moving Average 3 --------------------)Plot third MA trend?|
|v_input_timeframe_3|240|HTF|
|v_input_int_3|50|Length third MA|
|v_input_string_3|0|MA type:: McGinley|DEMA|TEMA|SMA|WMA|HMA|EMA|


> Source (PineScript)

```pinescript
//@version=5
strategy("Triple Dynamic Moving Average Trend Tracking Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=v_input_float_1, initial_capital=v_input_float_1)

// Risk Management
risk_management = v_input_bool_1

// Trading Signals
plot_ma_trend_1 = v_input_bool_2
plot_ma_trend_2 = v_input_bool_3
plot_ma_trend_3 = v_input_bool_4

ma_type_1 = v_input_string_1
ma_length_1 = v_input_int_1
ma_timeframe_1 = v_input_timeframe_1

ma_type_2 = v_input_string_2
ma_length_2 = v_input_int_2
ma_timeframe_2 = v_input_timeframe_2

ma_type_3 = v_input_string_3
ma_length_3 = v_input_int_3
ma_timeframe_3 = v_input_timeframe_3

// Calculate Moving Averages
ma1 = ta.sma(close, ma_length_1)
ma2 = ta.sma(ta.resample(ma_type_2, close, ma_timeframe_2), ma_length_2)
ma3 = ta.sma(ta.resample(ma_type_3, close, ma_timeframe_3), ma_length_3)

// Buy Condition
buy_signal = na
if (plot_ma_trend_1 and plot_ma_trend_2 and plot_ma_trend_3)
    buy_signal := ta.crossover(ma1, ma2) and ta.upcross(ma2, ma3, 0.95)

// Sell Condition
sell_signal = ta.crossunder(ma1, ma2)

// Plot MA Trends
plot_shape(series=buy_signal, style=shape.labelup, title="Buy Signal", color=color.green, text="BUY")
plot_shape(series=sell_signal, style=shape.labeldown, title="Sell Signal", color=color.red, text="SELL")

// Execute Trade
if (buy_signal and not risk_management)
    strategy.entry("Long", strategy.long)

if (sell_signal and not risk_management)
    strategy.close("Long")
```