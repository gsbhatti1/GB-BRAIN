``` pinescript
/*backtest
start: 2024-03-18 00:00:00
end: 2024-04-17 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("RsI_RelativeStrengthIndexStrategy", overlay=true)

// RSI Parameters
rsi_length = input(7, title="RSI Period")
rsi_overbought = input(70, title="Overbought (RSI)")
rsi_oversold = input(30, title="Oversold (RSI)")
trail_offset = input(0.005, title="Trailing Stop Offset")
stop_loss_points = input(10, title="Stop Loss Points")
risk_percentage = input(true, title="Risk Percentage (%)")

// Calculate RSI
rsi_value = rsi(close, rsi_length)

// Long Entry Condition
long_condition = rsi_value < rsi_oversold

// Short Entry Condition
short_condition = rsi_value > rsi_overbought

// Position Sizing
position_size = risk_percentage ? 0.01 : 0.02 * account Equity / stop_loss_points

// Trailing Stop Loss for Long Positions
long_stop_loss = na(long_stop_price) ? strategy.position_avg_price - (stop_loss_points * point size) : max(long_stop_price, strategy.position_avg_price - (stop_loss_points * point size))

// Trailing Stop Loss for Short Positions
short_stop_loss = na(short_stop_price) ? strategy.position_avg_price + (stop_loss_points * point size) : min(short_stop_price, strategy.position_avg_price + (stop_loss_points * point size))

// Trail Offset for Long Positions
long_stop_price := na(long_stop_price) ? strategy.position_avg_price - (trail_offset * point size) : max(long_stop_price, strategy.position_avg_price - (trail_offset * point size))

// Trail Offset for Short Positions
short_stop_price := na(short_stop_price) ? strategy.position_avg_price + (trail_offset * point size) : min(short_stop_price, strategy.position_avg_price + (trail_offset * point size))

// Open Long Position
if (long_condition)
    strategy.entry("Long", strategy.long, size=position_size)

// Close Long Position on Stop Loss or Trail Offset
if (close < long_stop_loss)
    strategy.close("Long")

// Open Short Position
if (short_condition)
    strategy.entry("Short", strategy.short, size=position_size)

// Close Short Position on Stop Loss or Trail Offset
if (close > short_stop_loss)
    strategy.close("Short")
```

This Pine Script code implements the RSI-RelativeStrengthIndexStrategy based on the provided description. The script includes calculations for both long and short positions using the specified entry conditions and risk management techniques such as trailing stop losses and position sizing based on account equity.