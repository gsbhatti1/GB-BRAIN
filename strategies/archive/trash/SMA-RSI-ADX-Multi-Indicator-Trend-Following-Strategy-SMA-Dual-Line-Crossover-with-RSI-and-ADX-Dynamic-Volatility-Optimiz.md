``` pinescript
/*backtest
start: 2025-02-16 17:00:00
end: 2025-02-20 00:00:00
period: 4m
basePeriod: 4m
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=6
strategy("SMA + RSI + ADX + ATR Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=2)

// === Input Parameters ===
sma_fast_length = input(10, title="SMA Fast Period")
sma_slow_length = input(200, title="SMA Slow Period")
rsi_length = input(14, title="RSI Period")
adx_length = input(14, title="ADX Period")
adx_smoothing = input(14, title="ADX Smoothing Period")  // <-- New parameter!
atr_length = input(14, title="ATR Period")

// === Filtering Levels for RSI and ADX ===
rsi_buy_level = input(50, title="RSI Buy Level")
rsi_sell_level = input(50, title="RSI Sell Level")
adx_min_trend = input(20, title="ADX Minimum Trend Strength")

// === Trailing Stop ===
use_trailing_stop = input(true, title="Enable Trailing Stop")
trailing_stop_pips = input(30, title="Trailing Stop (Pips)")
trailing_step_pips = input(5, title="Trailing Step (Pips)")

// === Indicators ===
sma_fast = ta.sma(close, sma_fast_length)
sma_slow = ta.sma(close, sma_slow_length)
rsi_value = ta.rsi(close, rsi_length)
[diPlus, diMinus, adx_value] = ta.dmi(adx_length, adx_smoothing)  // <-- Corrected: added `adx_smoothing`
atr_value = ta.atr(atr_length)

// === Entry Logic ===
longCondition = ta.crossover(sma_fast, sma_slow) and rsi_value > rsi_buy_level and adx_value > adx_min_trend
shortCondition = ta.crossunder(sma_fast, sma_slow) and rsi_value < rsi_sell_level and adx_value > adx_min_trend

// === Open Positions ===
if longCondition
    strategy.entry("BUY", strategy.long)

if shortCondition
    strategy.entry("SELL", strategy.short)

// === Trailing Stop Logic ===
if (use_trailing_stop)
    trail_price = strategy.position_avg_price
    strategy.exit("Trailing Stop", from_entry="BUY", stop=trail_price - (atr_value * trailing_stop_pips))
    strategy.exit("Trailing Stop", from_entry="SELL", stop=trail_price + (atr_value * trailing_stop_pips))

// === Trailing Step Logic ===
trail_price = strategy.position_avg_price
strategy.exit("Trailing Step", from_entry="BUY", stop=trail_price - (atr_value * trailing_step_pips))
strategy.exit("Trailing Step", from_entry="SELL", stop=trail_price + (atr_value * trailing_step_pips))
```

This completes the translation while preserving all code blocks and formatting.