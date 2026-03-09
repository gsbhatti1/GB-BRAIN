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

long_condition = ema20 > ema200 and rsi_ok_long and cci_ok_long
short_condition = ema20 < ema200 and rsi_ok_short and cci_ok_short

// === Break of Structure (BOS)
bos_long_condition = close > ta.highest(high, 14) and ta.barssince(close <= high[1]) == 0
bos_short_condition = close < ta.lowest(low, 14) and ta.barssince(close >= low[1]) == 0

// === Entry Conditions
long_entry = long_condition and bos_long_condition
short_entry = short_condition and bos_short_condition

if (long_entry)
    strategy.entry("Long", strategy.long)

if (short_entry)
    strategy.entry("Short", strategy.short)

// === Trailing Stop Loss
var float stop_loss_price = na
if (strategy.position_size > 0)
    stop_loss_price := math.max(stop_loss_price, close - atr * sl_mult)
else if (strategy.position_size < 0)
    stop_loss_price := math.min(stop_loss_price, close + atr * sl_mult)

trail_stop = strategy.position_size > 0 ? stop_loss_price : na
if (trail_stop != na and strategy.position_size > 0)
    strategy.exit("Trailing Stop", "Long", stop=trail_stop - atr * trail_offset, limit=trail_stop + atr * tp_mult)

```