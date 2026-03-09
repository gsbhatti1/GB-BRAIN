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

useStopLoss = input(true, "Use Stoploss Points?", group="Risk Management")
stopLossPoints = useStopLoss ? 100 : na
trailStop = input(true, "Use Stoploss Trail?", group="Risk Management")
trailStopPercent = trailStop ? input.float(0.1, title="Stop Loss Trail%", group="Risk Management") : na

// Load Supertrend Indicator
[supertrend, supertrendDir] = ta.supertrend(atrPeriod, factor)

// Define the trading session time
[session_start, session_end] = session == "0915-1510" ? [9.15, 15.10] : na

// Initialize variables for strategy logic
in_session = false
last_candle = na
entry_price = na

// Strategy logic
for t in time >= start_date and time <= end_date
    if session_start <= hour(time) < session_end
        // Wait for 3 candles to form
        if not na(last_candle)
            if not in_session
                // Long Entry Signal
                if supertrendDir == -1 and supertrend > close[2]
                    in_session := true
                    entry_price := close

                // Short Entry Signal
                if supertrendDir == 1 and supertrend < close[2]
                    in_session := true
                    entry_price := close

        last_candle := close

// Set stop loss and trailing stop
if in_session
    strategy.entry("Long", strategy.long, when=not na(entry_price), comment="Enter Long")
    
    if trailStop
        strategy.exit("Exit Long with Trail Stop", "Long", stop=entry_price - (trailStopPercent * entry_price))
        
    else
        strategy.exit("Exit Long with Fixed Stop Loss", "Long", stop=entry_price - stopLossPoints)

    // Exit at the end of the session
    if hour(time) >= session_end
        strategy.close("Long")
```