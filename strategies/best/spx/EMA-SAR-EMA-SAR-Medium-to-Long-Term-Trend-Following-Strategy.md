``` pinescript
/*backtest
start: 2024-04-01 00:00:00
end: 2024-04-30 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("EMA SAR Strategy", overlay=true)

// EMA Settings
ema_20 = ta.ema(close, 20)
ema_60 = ta.ema(close, 60)

/// SAR Settings
sar = ta.sar(0.02, 0.2, 0.2)
sar_value = sar
is_trend_up = sar[1] > sar[2] ? true : false  // Evaluating the trend direction

/// Condition for Buy Signal
buy_condition = ta.crossover(ema_20, ema_60) and (sar_value < ema_20) and (is_trend_up)

// Condition for Sell Signal
sell_condition = ta.crossunder(ema_20, ema_60) and (sar_value > ema_20) and (not is_trend_up)

// Entry Conditions
if (buy_condition)
    strategy.entry("Buy", strategy.long)

if (sell_condition)
    strategy.close("Buy")

// Stop Loss at Previous Day's High for Long Positions
stop_loss_long = ta.highest(high, 1)[1]
strategy.exit("Stop Loss Long", from_entry="Buy", stop=stop_loss_long)

// Stop Loss at Previous Day's Low for Short Positions
stop_loss_short = ta.lowest(low, 1)[1]
strategy.exit("Stop Loss Short", from_entry="Buy", stop=stop_loss_short)
```

This code snippet defines the EMA SAR Medium-to-Long-Term Trend Following Strategy using Pine Script. It sets up the necessary parameters for Exponential Moving Averages (EMAs) and Parabolic Stop and Reverse (SAR) indicators, along with conditions to enter long or short positions based on trend direction and indicator signals. The strategy also includes stop-loss mechanisms to manage risk effectively.