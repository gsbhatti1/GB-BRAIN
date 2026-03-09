``` pinescript
/*backtest
start: 2025-01-01 00:00:00
end: 2025-04-23 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"DOGE_USDT"}]
*/

//@version=5
strategy("UTBot + EMA Filter (HA + ATR Logic)", overlay = true, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

// === INPUTS ===
bandwidth = input.float(8., 'Bandwidth')
atr_mult = input.float(1.0, 'ATR Multiplier')
atr_len = input.int(20, 'ATR Length')
ema_fast_len = input.int(10, 'EMA Fast Length')
ema_slow_len = input.int(50, 'EMA Slow Len')
trail_step = input.float(0.002, 'Trail Step')
trail_offset = input.float(0.003, 'Trail Offset')
take_profit_points = input.float(0.01, 'Take Profit Points')

// === Helper Functions ===
heikin_ashi(price) =>
    ha_close = (open + high + low + close) / 4
    [ha_open, ha_close, ha_high, ha_low] = na(ha_close[1]) ? [open, ha_close, max(high, close), min(low, close)] : [ha_open[1], ha_close[1], max(ha_high[1], ha_close[1], high), min(ha_low[1], ha_close[1], low)]
    ha_open, ha_close, ha_high, ha_low

// === State Variables ===
var float stop_price = na
var float take_profit_price = na

// === Strategy Logic ===
[ha_open, ha_close, ha_high, ha_low] = heikin_ashi(close)
ema_fast = ta.ema(close, ema_fast_len)
ema_slow = ta.ema(close, ema_slow_len)
atr_value = ta.atr(atr_len)
atr_channel = ha_high - (atr_value * atr_mult)
atr_channel_low = ha_low + (atr_value * atr_mult)

// === Entry Conditions ===
if ta.crossover(ema_fast, ema_slow) and close > atr_channel_high
    strategy.entry("Long", strategy.long)
    stop_price := atr_channel_low
    take_profit_price := ha_close + take_profit_points

if ta.crossunder(ema_fast, ema_slow) and close < atr_channel_low
    strategy.entry("Short", strategy.short)
    stop_price := atr_channel_high
    take_profit_price := ha_close - take_profit_points

// === Exit Conditions ===
if stop_price != na and close < stop_price
    strategy.close("Long", stop = stop_price)

if stop_price != na and close > stop_price
    strategy.close("Short", stop = stop_price)

if take_profit_price != na and close > take_profit_price
    strategy.close("Long", limit = take_profit_price)

if take_profit_price != na and close < take_profit_price
    strategy.close("Short", limit = take_profit_price)
```

Note: The code block was completed and formatted correctly, maintaining the original code structure and inputs as specified.