``` pinescript
/*backtest
start: 2024-01-09 00:00:00
end: 2024-01-16 00:00:00
period: 5m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
// This source code is for the Momentum Breakout Optimization strategy
strategy("Momentum Breakout Optimization", overlay=true)

// Inputs
source = input(title="Source", type=source, defval=hl2)
atr_length = input(title="ATR Length", type=int, defval=10)
atr_multiplier = input(title="ATR Multiplier", type=float, defval=3.0)
moving_average_type = input(title="Moving Average Type", type=mvtype, defval=zlema)
moving_average_length = input(title="Moving Average Length", type=int, defval=10)
change_atr_method = input(title="Change ATR Calculation Method?", type=bool, defval=true)
show_moving_average = input(title="Show Moving Average?", type=bool, defval=true)
show_crossing_signals = input(title="Show Crossing Signals?", type=bool, defval=true)
show_price_pmax_crossing_signals = input(title="Show Price/Pmax Crossing Signals?", type=bool, defval=false)
highlighter_on_off = input(title="Highlighter On/Off?", type=bool, defval=true)
use_position_sizing = input(title="Use Position Sizing?", type=bool, defval=true)
risk_percent = input(title="Risk %", type=float, defval=0.5)
start_date = input(title="Start Date", type=datetime, defval=datetime(2019,1,1,0,0))
start_month = input(title="Start Month", type=bool, defval=true)
start_year = input(title="Start Year", type=int, defval=2019)
end_date = input(title="End Date", type=datetime, defval=datetime(2021,12,31,23,59))
end_month = input(title="End Month", type=int, defval=12)
end_year = input(title="End Year", type=int, defval=2021)

// ATR Calculation
atr_value = na
if (change_atr_method)
    atr_value := ta.atr(atr_length)
else
    atr_value := ta.atr(atr_length)

// Moving Average Calculation
if (moving_average_type == zlema)
    ma_value = ta.zlema(close, moving_average_length)
else if (moving_average_type == ema)
    ma_value = ta.ema(close, moving_average_length)
else if (moving_average_type == wma)
    ma_value = ta.wma(close, moving_average_length)
else if (moving_average_type == tma)
    ma_value = ta.tma(close, moving_average_length)
else if (moving_average_type == var)
    ma_value = ta.var(close, moving_average_length)
else if (moving_average_type == wwma)
    ma_value = ta.wwma(close, moving_average_length)
else if (moving_average_type == sma)
    ma_value = ta.sma(close, moving_average_length)
else if (moving_average_type == tsf)
    ma_value = ta.tsf(close, moving_average_length)
else
    ma_value := na

// Stop Loss Calculation
long_stop_loss = close - atr_value * atr_multiplier
short_stop_loss = close + atr_value * atr_multiplier

// Trading Signals
long_entry = ta.crossover(close, ma_value)
short_entry = ta.crossunder(close, ma_value)

// Plotting
if (show_moving_average)
    plot(ma_value, title="Moving Average", color=color.blue, linewidth=2)

if (show_crossing_signals)
    plotshape(series=long_entry, title="Long Entry", location=location.belowbar, color=color.green, style=shape.labelup, text="Long")

if (show_crossing_signals)
    plotshape(series=short_entry, title="Short Entry", location=location.abovebar, color=color.red, style=shape.labeldown, text="Short")

// Highlighter
if (highlighter_on_off)
    label.new(x=bar_index, y=high, text="Highlight", color=color.yellow, textcolor=color.black, style=label.style_label_up, size=size.small)

// Position Sizing
position_size = risk_percent * account.balance
if (use_position_sizing)
    strategy.order("Long", strategy.long, size=position_size)
    strategy.order("Short", strategy.short, size=position_size)
else
    strategy.entry("Long", strategy.long)
    strategy.entry("Short", strategy.short)

// Backtest Period
if (time >= start_date and time <= end_date)
    strategy.entry("Long", strategy.long)
    strategy.entry("Short", strategy.short)
else
    strategy.close_all()

// Plot Stop Loss Lines
plot(long_stop_loss, title="Long Stop Loss", color=color.red, linewidth=2)
plot(short_stop_loss, title="Short Stop Loss", color=color.blue, linewidth=2)
```