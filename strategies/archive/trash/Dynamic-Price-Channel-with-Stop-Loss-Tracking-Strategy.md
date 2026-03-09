``` pinescript
/*backtest
start: 2023-01-31 00:00:00
end: 2024-01-31 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//Noro
//2020

//@version=4
strategy(title = "Noro's RiskDonchian Strategy", shorttitle = "RiskDonchian str", overlay = true, default_qty_type = strategy.percent_of_equity, initial_capital = 100, default_qty_value = 100, commission_value = 0.1)

//Settings
needlong = input(true, title="Long Entry Enabled")
needshort = input(true, title="Short Entry Enabled")
tp_percent = input(20, title="Take-Profit %", type=input.percent)
tp_type_center = input(false, title="Take-Profit Type: Center")
tp_type_fixed = input(false, title="Take-Profit Type: Fixed")
risk_long = input(5, title="Risk Size for Long, %", type=input.percent)
risk_short = input(5, title="Risk Size for Short, %", type=input.percent)
pclen = input(50, title="Price Channel Length")
show_lines = input(true, title="Show Lines")
show_background = input(false, title="Show Background")
show_offset = input(true, title="Show Offset")
show_labels = input(true, title="Show Label")
from_year = input(1900, title="From Year", type=input.integer)
to_year = input(2100, title="To Year", type=input.integer)
from_month = input(false, title="From Month", type=input.datetime.month)
to_month = input(12, title="To Month", type=input.integer)
from_day = input(false, title="From Day", type=input.datetime.day)

// Strategy Description
long_entry = not needlong ? na : (close > h and close < l) ? true : na
short_entry = not needshort ? na : (close < l and close > h) ? true : na

// Calculate Take-Profit Prices
if (tp_type_center)
    tpprice_long = center + tp_percent * (h - l) / 2
    tpprice_short = center - tp_percent * (h - l) / 2
else if (tp_type_fixed)
    tpprice_long = h + tp_percent
    tpprice_short = l - tp_percent

// Calculate Risk Size for Long and Short Positions
long_risk_size = risk_long / 100 * equity
short_risk_size = risk_short / 100 * equity

// Trading Logic
if (long_entry)
    strategy.entry("Long", strategy.long, when=close > h and close < l)

if (needshort and short_entry)
    strategy.entry("Short", strategy.short, when=close < l and close > h)

// Exit Conditions
if (strategy.position_size != 0)
    // Long Exit: Stop Loss or Take Profit
    if (strategy.position_size > 0 and low <= center - risk_long * equity / position_avg_cost)
        strategy.close("Long")
    else if (strategy.position_size > 0 and close >= tpprice_long)
        strategy.close("Long")

    // Short Exit: Stop Loss or Take Profit
    if (strategy.position_size < 0 and high >= center + risk_short * equity / position_avg_cost)
        strategy.close("Short")
    else if (strategy.position_size < 0 and close <= tpprice_short)
        strategy.close("Short")

// Plotting
plot(h, title="Upper Channel Line", color=color.red, linewidth=1)
plot(l, title="Lower Channel Line", color=color.green, linewidth=1)

if (show_labels)
    label.new(x=bar_index, y=h, text="UPL", style=label.style_label_down, color=color.white, size=size.small)
    label.new(x=bar_index, y=l, text="LPL", style=label.style_label_up, color=color.white, size=size.small)

```