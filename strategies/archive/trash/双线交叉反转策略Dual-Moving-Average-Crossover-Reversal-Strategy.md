> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|Length|
|v_input_2|true|KSmoothing|
|v_input_3|3|DLength|
|v_input_4|50|Level|
|v_input_5|14|LengthDiN|
|v_input_6|false|TriggerDiN|
|v_input_7|false|Trade reverse|


> Source (PineScript)

```pinescript
//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 18/02/2020
// This is combo strategies for get a cumulative signal.

strategy("Dual Moving Average Crossover Reversal Strategy", overlay=false)

// 123 Reversal Strategy
k = sma(close, v_input_1)
k_smooth = sma(k, v_input_2)
d = sma(close, v_input_3)
overbought = k_smooth < d and k_smooth < v_input_4
oversold = k_smooth > d and k_smooth > v_input_4
buy_signal = not oversold and close[1] < close[2] and close > k_smooth
sell_signal = not overbought and close[1] > close[2] and close < k_smooth

// DiNapoli Detrended Oscillator Strategy
len_din = input(v_input_5, title="LengthDiN")
trigger_din = input(v_input_6, title="TriggerDiN")
avg_price = sma(close, len_din)
buy_signal_din = close > avg_price + trigger_din
sell_signal_din = close < avg_price - trigger_din

// Combined Signal
buy_signal_final = buy_signal and buy_signal_din
sell_signal_final = sell_signal and sell_signal_din

// Plot
plotshape(series=buy_signal_final, title="Buy", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")
plotshape(series=sell_signal_final, title="Sell", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

// Optional: Trade Reverse
if (v_input_7)
    strategy.entry("Reverse Buy", strategy.long, when=sell_signal_final)
    strategy.entry("Reverse Sell", strategy.short, when=buy_signal_final)
```

|||