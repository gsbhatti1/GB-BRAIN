> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Long|
|v_input_2|true|Short|
|v_input_3|30|Price Channel|
|v_input_4|true|Show center-line|
|v_input_5|1900|From Year|
|v_input_6|2100|To Year|
|v_input_7|true|From Month|
|v_input_8|12|To Month|
|v_input_9|true|From day|
|v_input_10|31|To day|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-16 00:00:00
end: 2024-01-15 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//Noro
//2018

//@version=2
strategy(title = "Noro's Price Channel Strategy v1.0", shorttitle = "Price Channel str 1.0", overlay=true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, pyramiding = 0)

//Settings
needlong = input(true, defval = true, title = "Long")
needshort = input(true, defval = true, title = "Short")
pc_channel_length = input(30, title = "Price Channel")
show_center_line = input(true, defval = true, title = "Show center-line")

// Strategy Logic
highs = highest(high, pc_channel_length)
lows = lowest(low, pc_channel_length)
midline = (highs + lows) / 2

// Determine if last candle broke through the channel
breakout_long = not na(close[1]) and close > midline * 1.5 and close[1] <= midline
breakout_short = not na(close[1]) and close < midline / 1.5 and close[1] >= midline

// Generate signals
if (needlong and breakout_long)
    strategy.entry("Long", strategy.long)

if (needshort and breakout_short)
    strategy.entry("Short", strategy.short)

// Plotting
plot(show_center_line ? midline : na, title="Midline", color=color.blue, linewidth=2)
plotshape(series=breakout_long, location=location.belowbar, color=color.green, style=shape.labelup, title="Long Entry")
plotshape(series=breakout_short, location=location.abovebar, color=color.red, style=shape.labeldown, title="Short Entry")
```

This script implements the logic described in the strategy description, including drawing the price channel, detecting the breakout, and generating buy/sell signals.