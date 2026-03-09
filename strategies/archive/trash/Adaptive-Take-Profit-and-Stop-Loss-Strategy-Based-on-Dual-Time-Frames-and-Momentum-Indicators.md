``` pinescript
/*backtest
start: 2023-11-15 00:00:00
end: 2023-11-22 00:00:00
period: 15m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("SQZ Multiframe Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)
fast_ema_len = input(11, minval=5, title="Fast EMA")
slow_ema_len = input(34, minval=20, title="Slow EMA")
sqm_lengthKC = input(20, title="SQM KC Length")
kauf_period = input(20, title="Kauf Period")
kauf_mult = input(2, title="Kauf Mult factor")
min_profit_sl = input(5.0, minval=1, maxval=100, title="Min profit to start moving SL [%]")
longest_sl = input(10, minval=1, maxval=100, title="Maximum possible of SL [%]")
sl_step = input(0.5, minval=0.0, maxval=1.0, title="Take profit factor")
// ADMF
CMF_length = input(11, minval=1, title="CMF length") // EMA27 = SMMA/RMA14 ~ lunar month
show_plots = input(true, title="Show plots")

lower_resolution = timeframe.period=='1'?'5':timeframe.period=='5'?'15':timeframe.period=='15'?'30':timeframe.period=='30'?'60':timeframe.period=='60'?'240':timeframe.period=='240'?'D':timeframe.period=='D'?'W':'M'
higher_resolution = timeframe.period=='5'?'1':timeframe.period=='15'?'5':timeframe.period=='30'?'15':timeframe.period=='60'?'30':timeframe.period=='240'?'60':timeframe.period=='D'?'240':timeframe.period=='W'?'D':'W'

// Calculate Squeeze Momentum
sqm_val = linreg(close - avg(avg(highest(high, sqm_lengthKC), lowest(low, sqm_lengthKC)), sma(close, sqm_lengthKC)), sqm_lengthKC, 0)
sqm_val_high = security(syminfo.tickerid, higher_resolution, linreg(close - avg(avg(highest(high, sqm_lengthKC), lowest(low, sqm_lengthKC)), sma(close, sqm_lengthKC)), sqm_lengthKC, 0), lookahead=barmerge.lookahead_on)
sqm_val_low = security(syminfo.tickerid, lower_resolution, linreg(close - avg(avg(highest(high, sqm_lengthKC), lowest(low, sqm_lengthKC)), sma(close, sqm_lengthKC)), sqm_lengthKC, 0), gaps=barmerge.gaps_off, lookahead=barmerge.lookahead_on)

// Emas
high_close = security(syminfo.tickerid, higher_resolution, high)
low_close = security(syminfo.tickerid, lower_resolution, low)
fast_ema = ema(high_close, fast_ema_len)
slow_ema = ema(low_close, slow_ema_len)

// Trading logic
long_condition = (sqm_val > 0 and sqm_val_high > 0)
short_condition = (sqm_val < 0 and sqm_val_low < 0)

if (long_condition)
    strategy.entry("Long", strategy.long)
if (short_condition)
    strategy.entry("Short", strategy.short)

// Stop loss and take profit
stop_loss_level = min_profit_sl * 100
take_profit_level = sl_step * 100

long_entry_price = strategy.position_avg_price
short_entry_price = -strategy.position_avg_price

strategy.exit("Take Profit", from_entry="Long", limit=long_entry_price + take_profit_level)
strategy.exit("Take Profit", from_entry="Short", limit=short_entry_price - take_profit_level)
strategy.exit("Stop Loss", from_entry="Long", stop=long_entry_price - stop_loss_level)
strategy.exit("Stop Loss", from_entry="Short", stop=short_entry_price + stop_loss_level)
```

This updated Pine Script implements the strategy logic, including the trading conditions, stop loss, and take profit updates as described.