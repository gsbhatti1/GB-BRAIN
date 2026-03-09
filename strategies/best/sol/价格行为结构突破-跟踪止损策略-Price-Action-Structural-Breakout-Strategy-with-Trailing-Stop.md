``` pinescript
/*backtest
start: 2025-04-22 00:00:00
end: 2025-04-23 00:00:00
period: 2m
basePeriod: 2m
exchanges: [{"eid":"Futures_Binance","currency":"DOGE_USDT"}]
*/

//@version=6
strategy("SMC + EMA + Candles + RSI/CCI + BOS + Trailing", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === EMAs
ema20 = ta.ema(close, 20)
ema200 = ta.ema(close, 200)
plot(ema20, color=color.orange, linewidth=1)
plot(ema200, color=color.blue, linewidth=1)

// === RSI and CCI
rsi = ta.rsi(close, 14)
cci = ta.cci(close, 20)
rsi_ok_long = rsi > 50
rsi_ok_short = rsi < 50
cci_ok_long = cci > 0
cci_ok_short = cci < 0

// === ATR
atr = ta.atr(14)
tp_mult = 2.0
sl_mult = 1.0
trail_offset = atr * 1.0
trail_step = atr * 0.5
trail_profit = strategy.position_avg_price + (strategy.position_size * tp_mult * atr)
trail_stop = strategy.position_avg_price - (strategy.position_size * sl_mult * atr)

// === Entry Conditions
var long_entry = false
var short_entry = false

if ta.crossover(ema20, ema200) and rsi_ok_long and cci_ok_long
    long_entry := true

if ta.crossunder(ema20, ema200) and rsi_ok_short and cci_ok_short
    short_entry := true

// === Exit Conditions
trail_profit_level = na
trail_stop_level = na

if strategy.position_size > 0
    trail_profit_level := trail_profit
    if close < trail_offset
        strategy.exit("Trail Stop Loss", "Long Entry", stop=trail_stop)

if strategy.position_size < 0
    trail_stop_level := trail_stop
    if close > trail_offset
        strategy.exit("Trail Take Profit", "Short Entry", limit=trail_profit)
```

This script continues the provided Pine Script, implementing the trading logic described in the strategy. It includes entry and exit conditions based on EMA crossovers, RSI/CCI levels, and trailing stops.