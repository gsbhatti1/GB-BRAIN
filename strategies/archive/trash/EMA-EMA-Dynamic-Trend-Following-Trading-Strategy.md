``` pinescript
/*backtest
start: 2023-05-05 00:00:00
end: 2024-05-10 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Maboi_q

//@version=5
strategy("buy sell Trend", overlay=true)

atr_length = input.int(defval=14, title='atr length')
highest_length = input.int(defval=60, title='highest length')
highest_s_length = input.int(defval=60, title='sell highest length')
lowest_length = input.int(defval=30, title='lowest length')
sell_l_length = input.int(defval=55, title='sell line length')

f = 2.382
f2 = 5.618

atr = ta.atr(atr_length)
highest = ta.highest(highest_length)
lowest = ta.lowest(lowest_length)

f_atr = atr * f
ema_hl = ta.ema((highest[1] + lowest[1]) / 2, 14)
ema_highest = ema_hl + f_atr
ema_lowest = ema_hl - f_atr
ema_mid = (ema_highest + ema_lowest) / 2

bs_hi = ta.highest(highest_s_length)
sell_line = highest + atr * f2

long_condition = lowest < ema_lowest and close > ema_mid
short_condition = ema_highest - f_atr <= lowest or high >= sell_line

strategy.entry("Long", strategy.long, when=long_condition)
strategy.close("Long", when=short_condition)

// Plotting indicators
plot(ema_highest, title="EMA Highest", color=color.blue)
plot(ema_lowest, title="EMA Lowest", color=color.red)
hline(bs_hi, title="Sell Line", color=color.orange, linestyle=hline.style_dashed)
```