``` pinescript
/*backtest
start: 2024-11-10 00:00:00
end: 2024-12-09 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("LL Crypto - SUI", overlay=true)

// Time parameters for cryptocurrencies
fast_ema_len = input.int(11, minval=5, title="Fast EMA")
slow_ema_len = input.int(34, minval=20, title="Slow EMA")
sqm_lengthKC = input.int(20, title="SQM KC Length")
kauf_period = input.int(20, title="Kauf Period")
kauf_mult = input.float(2, title="Kauf Mult factor")
min_profit_sl = input.float(5, minval=0.01, maxval=100.0, title="Min profit to start moving SL [%]")
longest_sl = input.float(10, minval=0.01, maxval=100.0, title="Maximum possible of SL [%]")
sl_step = input.float(0.5, minval=0.0, maxval=1.0, title="Take profit factor")

// Adapted parameters for cryptocurrencies
CMF_length = input.int(11, minval=1, title="CMF length")
show_plots = input.bool(true, title="Show plots")
plot_color = input.color(color.blue, title="Plot color")

// EMA Calculation
fast_ema = ta.ema(close, fast_ema_len)
slow_ema = ta.ema(close, slow_ema_len)

// SQM Calculation
sqm_source = close[1]
sqm_kc_length = sqm_lengthKC
sqm_source2 = open[1]
sqm_kc_mult = 0.5
sqm_kc_factor = 2
sqm_kc = ta.sma(sqm_source * sqm_kc_factor, sqm_kc_length) - ta.sma(sqm_source2 * sqm_kc_factor, sqm_kc_length)
sqm = sqm_kc + (sqm_source - sqm_source2) * sqm_kc_mult

// CMF Calculation
cmf = 0.0
trades = barssince(ta.valuewhen(high[1] == high and low[1] == low, true, 99))
for i = 0 to (bar_index - 1)
    cmf += ((close[i] - low[i]) * volume[i] / (high[i] - low[i]))
cmf /= volume

// Strategy logic
if ta.crossover(fast_ema, slow_ema) and sqm > 0.0 and cmf > 0.0
    strategy.entry("Long", strategy.long)
else if ta.crossunder(fast_ema, slow_ema) or sqm < 0.0 or cmf < 0.0
    strategy.close("Long")

// Dynamic Stop Loss
if is_long := strategy.opentrades.get_entry_price(strategy.opentrades.entry_id(1), "Long") > 0 and strategy.opentrades.get_position_size(strategy.opentrades.entry_id(1)) > 0
    current_profit = (close - is_long) / is_long * 100.0
    if current_profit >= min_profit_sl
        new_sl = max(is_long, longest_sl)
        sl = ta.valuewhen(strategy.opentrades.get_entry_price(strategy.opentrades.entry_id(1), "Long") > 0 and strategy.opentrades.get_position_size(strategy.opentrades.entry_id(1)) > 0, new_sl, 0)
        strategy.exit("Exit Long", from_entry="Long", stop=sl * (1 - sl_step))
    else
        current_sl = strategy.opentrades.get_stop_price(strategy.opentrades.entry_id(1), "Long")
        if current_profit < min_profit_sl and current_sl > new_sl
            new_sl = ta.valuewhen(current_profit < min_profit_sl, current_sl, 0)
        strategy.exit("Exit Long", from_entry="Long", stop=new_sl)

// Plotting
plot(sqm, title="SQM Indicator", color=plot_color)
plot(cmf, title="CMF Indicator", color=color.red)
```