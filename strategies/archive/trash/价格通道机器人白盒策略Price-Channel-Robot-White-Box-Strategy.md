``` pinescript
/*backtest
start: 2023-02-21 00:00:00
end: 2024-02-27 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// ChaoZhang

//@version=4
strategy(title = "Price Channel Robot White Box Strategy", shorttitle = "Price Channel RBWBS", overlay = true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100)

// Input Arguments
v_input_1 = input(true, title="Long")
v_input_2 = input(true, title="Short")
v_input_3 = input(true, title="Stop Loss")
v_input_4 = input(100, title="% Lot")
v_input_5 = input(50, title="Price Channel Length (bars)")
v_input_6 = input(true, title="Show Lines")
v_input_7 = input(false, title="Show Background")
v_input_8 = input(1900, title="From Year", minval=1900)
v_input_9 = input(2100, title="To Year", maxval=2100)
v_input_10 = input(true, title="From Month")
v_input_11 = input(12, title="To Month", minval=1, maxval=12)
v_input_12 = input(true, title="From Day")
v_input_13 = input(31, title="To Day", minval=1, maxval=31)

// Calculate Price Channel
len := v_input_5
h := highest(high, len)
l := lowest(low, len)
price_channel_middle := (h + l) / 2

// Determine Entry and Exit Conditions
long_condition = close > price_channel_middle[1] and close <= h
short_condition = close < price_channel_middle[1] and close >= l

// Place Orders
if long_condition
    strategy.entry("Long", strategy.long, comment="Entry Long")
if short_condition
    strategy.entry("Short", strategy.short, comment="Entry Short")

// Stop Loss
stop_loss_level = v_input_3 ? price_channel_middle : na
strategy.exit("Exit Long", "Long", stop=stop_loss_level)
strategy.exit("Exit Short", "Short", stop=stop_loss_level)

// Plot Price Channel Lines
if v_input_6
    plot(h, color=color.red, title="Upper Channel Line")
    plot(l, color=color.green, title="Lower Channel Line")

// Time Filter
time_filter = input.timeframe("1D", title="Trading Hours")
if timeFilter(time.filter, time_filter) not in [v_input_8..v_input_9]
    strategy.close("Long")
    strategy.close("Short")

// Optional: Plot Background
bgcolor(v_input_7 ? color.new(color.blue, 90) : na)
```

Note: The `timeFilter` function is a placeholder and may need to be adjusted or replaced with the actual implementation based on Pine Script's capabilities.