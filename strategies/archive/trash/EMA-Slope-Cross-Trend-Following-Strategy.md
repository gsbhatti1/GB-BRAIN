> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|2018|start year|
|v_input_2|true|start month|
|v_input_3|true|start day|
|v_input_4|2020|end year|
|v_input_5|true|end month|
|v_input_6|true|end day|
|v_input_7|0|Source MA Type: EMA|SMA|
|v_input_8|130|Fast MA Length|
|v_input_9|400|Slow MA Length|
|v_input_10|0|Smoothing MAs Type: EMA|SMA|
|v_input_11|3|Smoothing MAs Length|
|v_input_12|true|Trend Filter|
|v_input_13|200|Trend Filter MA Period|
|v_input_14|0|Trend Filter MA Type: EMA|SMA|
|v_input_15|false|Volatility Filter|
|v_input_16|0.0003|Delta Slopes EMA|


> Source (PineScript)

```pinescript
//@version=4
strategy(title="EMA-Slope-Cross-Trend-Following-Strategy", initial_capital=1000, default_qty_type=strategy.percent_of_equity, commission_type=strategy.commission.percent, commission_value=0.06, slippage = 2, default_qty_value=30, overlay=false)

// Define inputs
start_year = input(2018, "Start Year")
start_month = input(true, "Start Month")
start_day = input(true, "Start Day")
end_year = input(2020, "End Year")
end_month = input(true, "End Month")
end_day = input(true, "End Day")

// Calculate timestamps
start_time = timestamp(start_year, start_month, start_day, 0, 0)
end_time = timestamp(end_year, end_month, end_day, 0, 0)

source_ma_type = input("EMA", title="Source MA Type", type=input.string, options=["EMA", "SMA"])
fast_ema_length = input(130, title="Fast MA Length")
slow_ema_length = input(400, title="Slow MA Length")
smoothing_ma_type = input("EMA", title="Smoothing MAs Type", type=input.string, options=["EMA", "SMA"])
smoothing_ma_length = input(3, title="Smoothing MAs Length")

trend_filter = input(true, title="Trend Filter")
trend_filter_ema_length = input(200, title="Trend Filter MA Period")
trend_filter_ma_type = input("EMA", title="Trend Filter MA Type", type=input.string, options=["EMA", "SMA"])
volatility_filter = input(false, title="Volatility Filter")
delta_slopes_ema = input(0.0003, title="Delta Slopes EMA")

// Calculate EMAs and slopes
fast_ema = ema(close, fast_ema_length)
slow_ema = ema(close, slow_ema_length)

if (source_ma_type == "EMA")
    source_ma = ema(close, fast_ema_length + slow_ema_length)
else
    source_ma = sma(close, fast_ema_length + slow_ema_length)

fast_slope = sma(source_ma, 3) - sma(source_ma[1], 3)
slow_slope = sma(source_ma, 3) - sma(source_ma[2], 3)

// Trend filter
if (trend_filter and trend_filter_ema_type == "EMA")
    trend_filter_ema = ema(close, trend_filter_ema_length)
else
    trend_filter_ema = sma(close, trend_filter_ema_length)

// Volatility filter
volatility = high - low

long_condition = fast_slope > slow_slope and close > trend_filter_ema and volatility < delta_slopes_ema
short_condition = fast_slope < slow_slope and close < trend_filter_ema and volatility < delta_slopes_ema

if (long_condition)
    strategy.entry("Long", strategy.long)

if (short_condition)
    strategy.entry("Short", strategy.short)

// Close positions when slopes cross in the opposite direction
if (fast_slope > slow_slope[1] and fast_slope < slow_slope and close > trend_filter_ema) or 
   (fast_slope < slow_slope[1] and fast_slope > slow_slope and close < trend_filter_ema)
    strategy.close("Long")
    strategy.close("Short")

// Plotting
plot(fast_ema, title="Fast EMA", color=color.blue)
plot(slow_ema, title="Slow EMA", color=color.red)

```

This Pine Script defines the EMA-Slope-Cross-Trend-Following-Strategy with all necessary input parameters and logic to generate buy/sell signals based on the slope crosses of EMAs.