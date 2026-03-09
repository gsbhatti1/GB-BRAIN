> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|22|ATR Period|
|v_input_float_1|3|ATR Multiplier|
|v_input_bool_1|true|Use Close Price for Extremums|
|v_input_int_2|3|Risk-Reward Ratio|


> Source (PineScript)

``` pinescript
// backtest
// start: 20

strategy("Dynamic-Stop-Loss-Moving-Average-Strategy", overlay=true)

length = input(22, title="ATR Period")
mult = input(3.0, title="ATR Multiplier")
use_close_price = input(true, title="Use Close Price for Extremums")
risk_reward_ratio = input(3, title="Risk-Reward Ratio")

// Calculate ATR
atr_length = length
atr_mult = mult
atr = ta.atr(atr_length)

// Calculate high and low extremes
if (use_close_price)
    high_extreme = ta.highest(atr_length)
    low_extreme = ta.lowest(atr_length)
else
    high_extreme = ta.highest(atr_length, close)
    low_extreme = ta.lowest(atr_length, close)

// Calculate stop-loss lines
longStop = high_extreme - atr_mult * atr
shortStop = low_extreme + atr_mult * atr

// Plot stop-loss lines
plot(longStop, color=color.blue, title="Long Stop")
plot(shortStop, color=color.red, title="Short Stop")

// Determine trading direction based on breakout
if (close[1] < longStop and close > longStop)
    strategy.entry("Long", strategy.long)
if (close[1] > shortStop and close < shortStop)
    strategy.entry("Short", strategy.short)

// Set stop loss and take profit based on risk-reward ratio
risk_reward = risk_reward_ratio
take_profit = longStop + risk_reward * atr
stop_loss = shortStop - risk_reward * atr

// Plot take profit and stop loss levels
plot(take_profit, color=color.green, title="Take Profit")
plot(stop_loss, color=color.orange, title="Stop Loss")

// Print signals
alertcondition(take_profit, title="Take Profit Alert", message="Take Profit Hit")
alertcondition(stop_loss, title="Stop Loss Alert", message="Stop Loss Hit")
```