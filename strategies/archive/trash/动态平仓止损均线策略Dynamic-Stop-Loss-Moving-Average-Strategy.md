> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|22|ATR Period|
|v_input_float_1|3|ATR Multiplier|
|v_input_bool_1|true|Use Close Price for Extremums|
|v_input_int_2|true|Risk-Reward Ratio|


> Source (PineScript)

```pinescript
//backtest
start: 2023-01-01

//@version=5
strategy("Dynamic Stop Loss Moving Average Strategy", overlay=true)

length = input.int(22, title="ATR Period")
mult = input.float(3.0, title="ATR Multiplier")
useCloseForExtremums = input.bool(true, title="Use Close Price for Extremums")
riskRewardRatio = input(1, title="Risk-Reward Ratio", type=input.integer)

// Calculate ATR
atrValue = ta.atr(length)

// Determine highest and lowest price based on close or high/low
if useCloseForExtremums
    highestPrice = ta.highest(high, length)
    lowestPrice = ta.lowest(low, length)
else
    highestPrice = ta.highest(high, length + 1)
    lowestPrice = ta.lowest(low, length + 1)

// Calculate stop loss lines
longStop = highestPrice - atrValue * mult
shortStop = lowestPrice + atrValue * mult

// Plot the stop loss lines
plot(longStop, title="Long Stop", color=color.red, linewidth=2)
plot(shortStop, title="Short Stop", color=color.green, linewidth=2)

// Determine entry direction based on breakout
var longEntry = 0.0
var shortEntry = 0.0

if ta.change(candle_color) > 0 and close > longStop[1] and close < longStop
    strategy.entry("Long", strategy.long)
    longEntry := close

if ta.change(candle_color) < 0 and close < shortStop[1] and close > shortStop
    strategy.entry("Short", strategy.short)
    shortEntry := -close

// Set risk-reward ratio based on the stop loss lines
stopLoss = if useCloseForExtremums
            longStop + atrValue * mult
        else
            highestPrice - (atrValue * 2 * mult)

takeProfit = stopLoss * (riskRewardRatio + 1)

// Plot the take profit levels
plot(takeProfit, title="Take Profit", color=color.blue, linewidth=2)
```
```