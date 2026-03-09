> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|false|Trade reverse|
|v_input_2|14|Length|
|v_input_3|true|KSmoothing|
|v_input_4|3|DLength|
|v_input_5|50|Level|
|v_input_6|10|Period|
|v_input_7|false|Trade reverse|


> Source (PineScript)

``` pinescript
// This source code is subject to the terms of the Creative Commons CCZero license.
// If you use this code, please attribution to Aladdin Aghaie and indicate that it is a derivative of his work.

//@version=5
strategy("Dual-Factor-Mean-Reversion-Tracking-Strategy", overlay=true)

// 123 Reversal Strategy
length = input(14, title="Length")
d_length = input(3, title="D Length")
level = input(50, title="Level")

// Calculate Stochastic
stoch_k = stoch(close, high, low, length)
stoch_d = sma(stoch_k, d_length)

// Keltner Channel Strategy
k_period = input(10, title="Period")
upper_band = sma(high, k_period) + (sma(abs((high - low)), k_period) / 2)
lower_band = sma(low, k_period) - (sma(abs((high - low)), k_period) / 2)

// Buy Signal
buy_signal = close[1] < close[0] and stoch_d < level and close[2] > close[1]
if (buy_signal)
    strategy.entry("Buy", strategy.long)

// Sell Signal
sell_signal = close[1] > close[0] and stoch_d > level and close[2] < close[1]
if (sell_signal)
    strategy.exit("Sell", "Buy")

// Plot Keltner Bands
plot(upper_band, color=color.red, title="Upper Band")
plot(lower_band, color=color.green, title="Lower Band")
```