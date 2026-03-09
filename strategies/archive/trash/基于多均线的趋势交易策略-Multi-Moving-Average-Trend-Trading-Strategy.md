``` pinescript
/*backtest
start: 2024-04-01 00:00:00
end: 2024-04-30 23:59:59
period: 3h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Multi-Moving Average Trend Trading Strategy", overlay=true)

// Inputs for start and end date
start_year = input.int(2020, title="Start Year")
start_month = input.int(1, title="Start Month")
start_day = input.int(1, title="Start Day")

end_year = input.int(2020, title="End Year")
end_month = input.int(12, title="End Month")
end_day = input.int(31, title="End Day")

// Converting day, month, and year to timestamp
start_timestamp = timestamp(start_year, start_month, start_day, 0, 0)
end_timestamp = timestamp(end_year, end_month, end_day, 23, 59)

// Define moving averages
long_sma = sma(close, 200)
medium_sma = sma(close, 21)
short_sma = sma(close, 9)

// Buy condition
buy_condition = close > long_sma and close > medium_sma and close > short_sma

// Plot moving averages
plot(long_sma, color=color.blue, title="200 SMA")
plot(medium_sma, color=color.red, title="21 SMA")
plot(short_sma, color=color.green, title="9 SMA")

// Define stop gain and stop loss levels
stop_gain = input.float(10, title="Stop Gain (in points)")
stop_loss = input.float(5, title="Stop Loss (in points)")

// Enter trade
if (not strategy.position_size and buy_condition)
    strategy.entry("Buy", strategy.long)

// Exit trade
if (strategy.position_size)
    strategy.exit("Exit", "Buy", stop=stop_gain, limit=stop_loss)

// Close all positions at 17:00 each day
time_close = time == time[1] and time >= timestamp(start_year, start_month, start_day, 17, 0) and time <= timestamp(start_year, start_month, start_day, 17, 59)
if (time_close)
    strategy.close("Buy")

// Plot text label for strategy information
label.new(x=bar_index, y=high, text="Multi-Moving Average Trend Trading Strategy", color=color.white, textcolor=color.black, style=label.style_label_left)
```

This Pine Script code implements the "Multi-Moving Average Trend Trading Strategy" as described in the document. The strategy uses three simple moving averages (SMA) with default periods of 200, 21, and 9, and exits all positions at 17:00 each day. It also includes stop gain and stop loss levels to manage risk.