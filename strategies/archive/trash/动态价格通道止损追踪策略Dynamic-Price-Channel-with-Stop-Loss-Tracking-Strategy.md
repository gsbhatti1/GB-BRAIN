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
strategy(title = "Dynamic-Price-Channel-with-Stop-Loss-Tracking-Strategy", shorttitle = "Dynamic Price Channel Strategy", overlay = true, default_qty_type = strategy.percent_of_equity, initial_capital = 100, default_qty_value = 100, commission_value = 0.1)

//Settings
needlong = input(true, title="Long Position")
needshort = input(true, title="Short Position")
take_profit_percent = input(20, title="Take-profit, %")
take_profit_type = input(0, title="Take-profit type: 2. Fix; 1. None; 3. Trailing", type=input.integer)
take_profit_center = input(0, title="Take-profit type: 2. Center", type=input.integer)
risk_long = input(5, title="Risk size for long, %")
risk_short = input(5, title="Risk size for short, %")
price_channel_length = input(50, title="Price Channel Length")
show_lines = input(true, title="Show lines")
show_background = input(false, title="Show Background")
show_offset = input(true, title="Show Offset")
show_label = input(true, title="Show label")
from_year = input(1900, title="From Year")
to_year = input(2100, title="To Year")
from_month = input(true, title="From Month")
to_month = input(12, title="To Month")
from_day = input(true, title="From day")
to_day = input(31, title="To day")

// Functions
long_condition = ta.crossover(close, h) and close < center
short_condition = ta.crossunder(close, l) and close > center

// Positions
if (needlong and long_condition)
    strategy.entry("Long", strategy.long)

if (needshort and short_condition)
    strategy.entry("Short", strategy.short)

// Stop Loss and Take Profit
stop_loss_long = center
stop_loss_short = center

take_profit_long = na
take_profit_short = na

switch take_profit_type
    case 1
        // No trailing stop loss or take profit
    case 2
        take_profit_long := l * (1 + take_profit_percent / 100)
        take_profit_short := h * (1 - take_profit_percent / 100)
    case 3
        // Trailing stop loss and take profit

// Risk management
risk_size = na
if (needlong and long_condition)
    risk_size := close < center ? ta.valuewhen(close > center, stop_loss_long, 0) : stop_loss_long
if (needshort and short_condition)
    risk_size := close > center ? ta.valuewhen(close < center, stop_loss_short, 0) : stop_loss_short

// Exit conditions
exit_long = low <= stop_loss_long or high >= take_profit_long
exit_short = high >= stop_loss_short or low <= take_profit_short

if (needlong and exit_long)
    strategy.close("Long")

if (needshort and exit_short)
    strategy.close("Short")

// Plotting
plot(h, title="Upper Channel", color=color.blue, linewidth=2)
plot(l, title="Lower Channel", color=color.red, linewidth=2)
plot(center, title="Middle Line", color=color.gray, linewidth=1)

if (show_lines)
    hline(price=h, title="Upper Channel H")
    hline(price=l, title="Lower Channel L")
    hline(price=center, title="Middle Line")

if (show_background)
    bgcolor(ta.crossover(close, l) ? color.red : na)
    bgcolor(ta.crossunder(close, h) ? color.green : na)

if (show_offset)
    plotchar(show_offset and needlong ? 1 : 0, "Long Entry", "▲", location.top, size=size.tiny)
    plotchar(show_offset and needshort ? -1 : 0, "Short Entry", "▼", location.bottom, size=size.tiny)

if (show_label)
    label.new(x=bar_index, y=h, text="Upper Channel", color=color.blue, style=label.style_label_down)
    label.new(x=bar_index, y=l, text="Lower Channel", color=color.red, style=label.style_label_up)
    label.new(x=bar_index, y=center, text="Middle Line", color=color.gray, style=label.style_label_left)

// Date filtering
if (year(time) < from_year or year(time) > to_year or month(time) < from_month or month(time) > to_month or dayofmonth(time) < from_day or dayofmonth(time) > to_day)
    strategy.close("All")
```

This Pine Script translates the provided Chinese text into English, ensuring all code blocks and formatting remain unchanged.