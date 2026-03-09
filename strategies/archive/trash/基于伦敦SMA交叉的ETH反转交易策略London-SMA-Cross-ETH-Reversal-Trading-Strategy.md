> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|50|SMA Length|
|v_input_source_1_close|0|SMA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-01-11 00:00:00
end: 2024-01-17 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("London SMA Strategy ", overlay=true)

// Define London session times
london_session_start_hour = 6
london_session_start_minute = 59
london_session_end_hour = 15
london_session_end_minute = 59

// Define SMA input parameters
sma_length = input.int(50, title="SMA Length")
sma_source = input.source(close, title="SMA Source")

// Calculate SMA
sma = ta.sma(sma_source, sma_length)

// Convert input values to timestamps
london_session_start_time = hour + minute / 100
london_session_end_time = hour + minute / 100

// Determine if current time is within London session
is_london_session = (time >= timestamp(year, month, dayofmonth, london_session_start_hour, london_session_start_minute) and time < timestamp(year, month, dayofmonth, london_session_end_hour, london_session_end_minute))

// Determine if current price crossed above or below SMA
golden_cross = ta.crossover(close, sma)
dead_cross = ta.crossunder(close, sma)

// Strategy logic
if (is_london_session)
    if (golden_cross)
        strategy.entry("Long", strategy.long)
    else if (dead_cross)
        strategy.entry("Short", strategy.short)

// Plot SMA and cross signals
plot(sma, color=color.blue)
plotshape(series=golden_cross, title="Golden Cross", location=location.belowbar, color=color.green, style=shape.labelup, text="GC")
plotshape(series=dead_cross, title="Dead Cross", location=location.abovebar, color=color.red, style=shape.labeldown, text="DC")

// Optional: Add stop loss and take profit
stop_loss = input.float(50, title="Stop Loss")
take_profit = input.float(100, title="Take Profit")

strategy.exit("Exit Long", "Long", stop=stop_loss, limit=take_profit)
strategy.exit("Exit Short", "Short", stop=stop_loss, limit=take_profit)
```

This Pine Script code implements the "London SMA Strategy" as described. It calculates the Simple Moving Average (SMA) for the specified period and uses the crossover and crossunder conditions to enter long and short trades during the London session. The script also includes optional stop loss and take profit levels for exiting trades.