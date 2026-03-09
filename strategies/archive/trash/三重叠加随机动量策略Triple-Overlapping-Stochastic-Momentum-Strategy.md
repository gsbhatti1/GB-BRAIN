> Strategy Arguments


|Argument|Default|Description|
|---|---|---|
|v_input_1|10|%K Length|
|v_input_2|3|%K Smoothing Length|
|v_input_3|3|%K Double Smoothing Length|
|v_input_4|10|Signal Length|
|v_input_5|ema|Signal MA Type|
|v_input_6|40|Overbought Level|
|v_input_7|-40|Oversold Level|
|v_input_8|20|%K Length 2|
|v_input_9|3|%K Smoothing Length 2|
|v_input_10|3|%K Double Smoothing Length 2|
|v_input_11|10|Signal Length 2|
|v_input_12|ema|Signal MA Type 2|
|v_input_13|40|Overbought Level 2|
|v_input_14|-40|Oversold Level 2|
|v_input_15|5|%K Length 3|
|v_input_16|3|%K Smoothing Length 3|
|v_input_17|3|%K Double Smoothing Length 3|
|v_input_18|10|Signal Length 3|
|v_input_19|ema|Signal MA Type 3|
|v_input_20|40|Overbought Level 3|
|v_input_21|-40|Oversold Level 3|
|v_input_22|8|From Month|
|v_input_23|true|From Day|
|v_input_24|2018|From Year|
|v_input_25|12|To Month|
|v_input_26|31|To Day|
|v_input_27|2018|To Year|


> Source (PineScript)


```pinescript
//@version=2
strategy("Triple Overlapping Stochastic Momentum Strategy", "Triple Overlapping Stochastic Momentum", overlay=false)

// Inputs for SMI1
k_len1 = input(10, title="%K Length 1")
sm_len1 = input(3, title="%K Smoothing Length 1")
dbl_sm_len1 = input(3, title="%K Double Smoothing Length 1")
sig_len1 = input(10, title="Signal Length 1")
sig_matype1 = input("ema", title="Signal MA Type 1", type=input.ma)

// Inputs for SMI2
k_len2 = input(20, title="%K Length 2")
sm_len2 = input(3, title="%K Smoothing Length 2")
dbl_sm_len2 = input(3, title="%K Double Smoothing Length 2")
sig_len2 = input(10, title="Signal Length 2")
sig_matype2 = input("ema", title="Signal MA Type 2", type=input.ma)

// Inputs for SMI3
k_len3 = input(5, title="%K Length 3")
sm_len3 = input(3, title="%K Smoothing Length 3")
dbl_sm_len3 = input(3, title="%K Double Smoothing Length 3")
sig_len3 = input(10, title="Signal Length 3")
sig_matype3 = input("ema", title="Signal MA Type 3", type=input.ma)

// Inputs for date range
from_month = input(8, title="From Month", type=input.integer)
from_day = input(true, title="From Day", type=input.bool)
from_year = input(2018, title="From Year", type=input.integer)
to_month = input(12, title="To Month", type=input.integer)
to_day = input(31, title="To Day", type=input.integer)
to_year = input(2018, title="To Year", type=input.integer)

// SMI1
smi1 = sma(ema(close - (high + low) / 2, k_len1), sm_len1) / (0.5 * sma(ema(high - low, k_len1), sm_len1)) * 100

// SMI2
smi2 = sma(ema(close - (high + low) / 2, k_len2), sm_len2) / (0.5 * sma(ema(high - low, k_len2), sm_len2)) * 100

// SMI3
smi3 = sma(ema(close - (high + low) / 2, k_len3), sm_len3) / (0.5 * sma(ema(high - low, k_len3), sm_len3)) * 100

// Signal line for SMI1
sig_line1 = sma(smi1, sig_len1)
// Signal line for SMI2
sig_line2 = sma(smi2, sig_len2)
// Signal line for SMI3
sig_line3 = sma(smi3, sig_len3)

// Buy conditions
buy_condition = (sig_line1 > sig_line1[1] and sig_line2 > sig_line2[1] and sig_line3 > sig_line3[1])
// Sell conditions
sell_condition = (sig_line1 < sig_line1[1] and sig_line2 < sig_line2[1] and sig_line3 < sig_line3[1])

// Plotting the SMI and Signal lines
plot(smi1, title="SMI1", color=color.blue)
plot(smi2, title="SMI2", color=color.green)
plot(smi3, title="SMI3", color=color.red)
plot(sig_line1, title="Signal Line 1", color=color.blue)
plot(sig_line2, title="Signal Line 2", color=color.green)
plot(sig_line3, title="Signal Line 3", color=color.red)

// Buy and Sell signals
if (buy_condition)
    strategy.entry("Buy", strategy.long)
if (sell_condition)
    strategy.close("Buy")
```

This PineScript code implements the "Triple Overlapping Stochastic Momentum Strategy" by overlaying three different SMI indicators with varying parameters and generating trading signals based on their crossing points.