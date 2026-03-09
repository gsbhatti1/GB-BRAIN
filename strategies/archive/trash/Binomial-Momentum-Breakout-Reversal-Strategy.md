> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|Length|
|v_input_2|true|KSmoothing|
|v_input_3|3|DLength|
|v_input_4|50|Level|
|v_input_5|15|SellLevel|
|v_input_6|3|BuyLevel|
|v_input_7|false|Trade reverse|


> Source (PineScript)

```pinescript
//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 05/07/2019
// This is a combo strategy for getting a cumulative signal.
//
// First strategy
// This system was created from the book "How I Tripled My Money in the Futures Market" by Ulf Jensen.
//

study("Binomial Momentum Breakout Reversal Strategy", shorttitle="BMBS", overlay=false)

// Input parameters
length = input(14, title="Length")
kSmoothing = input(true, title="KSmoothing")
dLength = input(3, title="DLength")
level = input(50, title="Level")
sellLevel = input(15, title="SellLevel")
buyLevel = input(3, title="BuyLevel")
tradeReverse = input(false, title="Trade reverse")

// Stochastic indicator
stochRSI = stoch(close, close, close, length)
k = sma(stochRSI, 3)
d = sma(k, 3)

// Bull Power indicator
bullPower = (close - ref(close, 1)) / close

// 123 Reversal Strategy
bullishSignal = (close[1] < close[2] and close[2] > close[3] and d < level) or (close[1] > close[2] and close[2] < close[3] and d > level)
bearishSignal = (close[1] > close[2] and close[2] < close[3] and d > level) or (close[1] < close[2] and close[2] > close[3] and d < level)

// Trading logic
if (bullishSignal and not tradeReverse)
    strategy.entry("Bullish", strategy.long)
if (bearishSignal and tradeReverse)
    strategy.entry("Bearish", strategy.short)

// Plotting
plot(stochRSI, title="Stochastic RSI", color=color.blue)
plot(d, title="D", color=color.red)
plot(bullPower, title="Bull Power", color=color.green)

// Optional stop loss
atr = atr(14)
stopLoss = atr * 3
strategy.exit("Stop Loss", from_entry="Bullish", stop=close - stopLoss)
strategy.exit("Stop Loss", from_entry="Bearish", stop=close + stopLoss)

// Print signals
if (bullishSignal)
    label.new(x=bar_index, y=high, text="Bullish", color=color.green, style=label.style_label_down)
if (bearishSignal)
    label.new(x=bar_index, y=low, text="Bearish", color=color.red, style=label.style_label_up)
```

[/trans]