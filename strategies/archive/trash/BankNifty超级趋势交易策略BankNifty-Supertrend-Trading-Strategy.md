> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_3|timestamp(01 Dec 2023 23:59:59)|End Date|
|v_input_float_1|3|Factor|
|v_input_1|0915-1510|(?Indian Session Time)Session|
|v_input_2|timestamp(01 Jan 2022 00:00:00)|(?Backtest Specific Range)Start Date|
|v_input_4|50|(?SuperTrend Setting)ATR Length|
|v_input_5|true|(?Delay at Session Start)Use Delay?|
|v_input_6|10|Delay N numbers of candle|
|v_input_7|true|(?Risk Management)Use Stoploss Points?|
|v_input_8|100|Stop Loss Points|
|v_input_9|true|Use Stoploss Trail?|
|v_input_float_2|0.1|Stop Loss Trail%|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-28 00:00:00
end: 2023-12-28 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("BankNifty 5min Supertrend Based Strategy, 09:15 Entry with Date Range and Risk Management")

// Session and date range input variables
session = input("0915-1510", "Session", group="Indian Session Time")
start_date = input(title="Start Date", defval=timestamp("01 Jan 2022 00:00:00"), group="Backtest Specific Range")
end_date = input(title="End Date", defval=timestamp("01 Dec 2023 23:59:59"))
atrPeriod = input(50, "ATR Length", group="SuperTrend Setting")
factor = input.float(3.0, "Factor", step=0.1)

useDelay = input(true, "Use Delay?", group="Delay at Session Start")
Delay = useDelay ? input(10, title="Delay N numbers of candle", group="Delay at Session Start") : na

useStopLossPoints = input(true, "Use Stoploss Points?", group="Risk Management")
stopLoss = useStopLossPoints ? 100 : na

useStopLossTrail = input(true, "Use Stoploss Trail?")
trailPercent = useStopLossTrail ? input.float(0.1, "Stop Loss Trail%", step=0.01) : na

// Calculate Supertrend
[supertrend, _] = ta.supertrend(factor, atrPeriod)

// Entry condition
var entryTime = na
if (time >= start_date and time <= end_date and session == session[1])
    if useDelay
        if bar_index >= Delay
            entryTime := time

longEntry = ta.change(supertrend) > 0
shortEntry = ta.change(supertrend) < 0

// Exit condition
var closeAllPositions = false
if (time >= end_date or session != session[1])
    closeAllPositions := true

if longEntry and not na(entryTime)
    strategy.entry("Long", strategy.long, when=entryTime)

if shortEntry and not na(entryTime)
    strategy.entry("Short", strategy.short, when=entryTime)

// Set stop loss
stopLossValue = useStopLossPoints ? stopLoss : na
if (strategy.position_size > 0 and closeAllPositions or longEntry)
    strategy.exit("Exit Long", "Long", stop=stopLossValue)

if (strategy.position_size < 0 and closeAllPositions or shortEntry)
    strategy.exit("Exit Short", "Short", stop=stopLossValue)

// Trailing stop loss
trailStop = useStopLossTrail ? trailPercent * strategy.position_avg_price : na
if (strategy.position_size > 0 and not na(trailStop) and closeAllPositions or longEntry)
    strategy.exit("Trailing Long", "Long", stop=strategy.position_avg_price + trailStop)

if (strategy.position_size < 0 and not na(trailStop) and closeAllPositions or shortEntry)
    strategy.exit("Trailing Short", "Short", stop=strategy.position_avg_price - trailStop)
```

This completes the translation of your trading strategy document, keeping all code blocks as-is.