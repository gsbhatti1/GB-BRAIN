> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Enable Ribbon Filter|
|v_input_2|30|Ribbon Period|
|v_input_3|true|useTrueRange|
|v_input_4|80|KELTNER Period|
|v_input_5|3|KELTNER Multiple|
|v_input_6|14|ADX Smoothing|
|v_input_7|14|DI Length|
|v_input_8|32|+DI Trigger Level|
|v_input_9|2019|Backtest Start Year|
|v_input_10|true|Backtest Start Month|
|v_input_11|true|Backtest Start Day|
|v_input_12|2030|Backtest Stop Year|
|v_input_13|12|Backtest Stop Month|
|v_input_14|31|Backtest Stop Day|
|v_input_15|8|Long Take Profit 1 Target %|
|v_input_16|20|Long Take Profit 1 Qty %|
|v_input_17|16|Long Take Profit 2 Target %|
|v_input_18|30|Long Take Profit 2 Qty %|


> Source (PineScript)

```pinescript
//@version=5
indicator("Momentum-Equilibrium-Channel-Trend-Tracking-Strategy", overlay=true)
ribbon_filter = v_input_1
ribbon_period = v_input_2
use_true_range = v_input_3
keltner_period = v_input_4
keltner_multiplier = v_input_5
adx_smoothing = v_input_6
di_length = v_input_7
plus_di_trigger_level = v_input_8
backtest_start_year = v_input_9
backtest_start_month = if v_input_10 then backtest_start_year else na
backtest_start_day = if v_input_11 then backtest_start_year else na
backtest_stop_year = v_input_12
backtest_stop_month = v_input_13
backtest_stop_day = v_input_14
long_take_profit_1_target = v_input_15 / 100
long_take_profit_1_qty = v_input_16 / 100
long_take_profit_2_target = v_input_17 / 100
long_take_profit_2_qty = v_input_18 / 100

// Calculate Keltner Channel
[k_low, k_high, k_mid] = ta.keltner(close, keltner_period, keltner_multiplier)

// Calculate ADX and DI+
[adx, plus_di] = ta.adx(high, low, close, adx_smoothing, di_length)
plus_di_signal = plus_di > plus_di_trigger_level

// Determine entry and exit conditions
long_condition = ribbon_filter and backtest_start_year <= year(time) and backtest_stop_year >= year(time) and backtest_start_month <= month(time) and backtest_stop_month >= month(time) and backtest_start_day <= dayofmonth(time) and backtest_stop_day >= dayofmonth(time) and plus_di_signal
short_condition = false

// Plot Keltner Channel
plot(k_high, title="Keltner High", color=color.blue)
plot(k_mid, title="Keltner Mid", color=color.red)

if long_condition
    strategy.entry("Long", strategy.long)
    strategy.exit("Profit 1", "Long", profit=long_take_profit_1_target * close, quantity_percent=long_take_profit_1_qty)
    strategy.exit("Profit 2", "Long", profit=long_take_profit_2_target * close, quantity_percent=long_take_profit_2_qty)

```
```