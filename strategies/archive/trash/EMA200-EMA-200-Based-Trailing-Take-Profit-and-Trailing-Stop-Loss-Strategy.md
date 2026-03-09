``` pinescript
/*backtest
start: 2023-12-08 00:00:00
end: 2024-01-07 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © ozgurhan

//@version=5
strategy("EMA 200 Based Trailing Take Profit and Stop Loss", overlay=true, margin_long=100, margin_short=100, default_qty_value=1, initial_capital=100)

// EMA 200 definition
ema200 = ta.ema(close, 200)

// ATR length and multiplier
atr_length = input.int(7, minval=1, title="ATR Length")
atr_multiplier = input.float(1.5, minval=0.1, title="ATR Multiplier")

// Calculate ATR
atr = ta.atr(atr_length)

// Define long and short conditions
long_condition = ta.crossover(close, ema200)
short_condition = ta.crossunder(close, ema200)

// Calculate trailing stop and take profit levels
trail_stop = ta.valuewhen(long_condition, high[1] + atr * atr_multiplier, 0)
trail_profit = ta.valuewhen(long_condition, low[1] - atr * atr_multiplier, 0)

// Set initial position
var float trail_stop_level = na
var float trail_profit_level = na

if (long_condition)
    trail_stop_level := high[1] + atr * atr_multiplier
    trail_profit_level := low[1] - atr * atr_multiplier
    strategy.entry("Long", strategy.long)

if (short_condition)
    strategy.entry("Short", strategy.short)

// Update trailing stop and take profit levels
if (strategy.position_size > 0 and close > trail_stop_level)
    strategy.exit("Take Profit", from_entry="Long", limit=trail_profit_level)
if (strategy.position_size < 0 and close < trail_stop_level)
    strategy.exit("Stop Loss", from_entry="Short", stop=trail_stop_level)

// Plot EMA 200 and ATR
plot(ema200, color=color.blue, title="EMA 200")
plot(atr, color=color.orange, title="ATR")
```

This Pine Script defines a strategy based on EMA200 with trailing stop and take profit mechanisms. The script includes the calculation of EMA200, ATR length, ATR multiplier, and the logic to determine when to enter long and short positions. It also includes the logic to update trailing stop and take profit levels based on the ATR.