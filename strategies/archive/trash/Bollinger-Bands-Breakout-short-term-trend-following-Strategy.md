``` pinescript
/*backtest
start: 2022-11-22 00:00:00
end: 2023-11-04 05:20:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Bollinger Bands - Breakout Strategy", overlay=true)

// Define the length of the Bollinger Bands
bbLengthInput = input.int(15, title="Length", group="Bollinger Bands", inline="BB")
bbDevInput = input.float(2.0, title="StdDev", group="Bollinger Bands", inline="BB")

// Define other inputs for filters and exits
trendFilterPeriodInput = input.int(223, title="Trend Filter Period", group="Filters", inline="TF")
trendFilterTypeInput = input.string("SMA", title="Trend Filter Type", options=["EMA", "SMA", "RMA", "WMA"], group="Filters", inline="TF")
volatilityFilterStDevLengthInput = input.int(15, title="Volatility Filter Length", group="Filters", inline="VF")
rocEnableInput = input.bool(false, title="ROC Filter Enable", group="Filters", inline="RF")
rocThresholdInput = input.float(2.0, title="ROC Threshold", group="Filters", inline="RF")
startFilterDateInput = input.time(timestamp("2017-01-01"), title="Start Date Filter", group="Filters", inline="DF")
endFilterDateInput = input.time(timestamp("2050-01-01"), title="End Date Filter", group="Filters", inline="DF")

// Define exit conditions
longExitTimeStopInput = input.float(2.0, title="Long Exit Time Stop", group="Exits", inline="LS")
longExitTrailingOffsetInput = input.float(0.5, title="Long Exit Trailing Offset", group="Exits", inline="LO")
longExitSLPercentInput = input.float(2.0, title="Long Exit SL (Percent)", group="Exits", inline="LSP")
longExitTPPercentInput = input.float(9.0, title="Long Exit TP (Percent)", group="Exits", inline="LTP")

shortExitTimeStopInput = input.float(2.0, title="Short Exit Time Stop", group="Exits", inline="SS")
shortExitTrailingOffsetInput = input.float(0.5, title="Short Exit Trailing Offset", group="Exits", inline="SO")
shortExitSLPercentInput = input.float(2.0, title="Short Exit SL (Percent)", group="Exits", inline="SSP")
shortExitTPPercentInput = input.float(9.0, title="Short Exit TP (Percent)", group="Exits", inline="STP")

// Define risk management parameters
maxIntradayLossInput = input.int(10, title="Max Intraday Loss (% of Portfolio Value)", group="Risk Management", inline="RMI")

// Define output precision for the results table
resultsTablePrecisionInput = input.int(2, title="Results Table Precision", group="Miscellaneous", inline="RTP")
darkModeInput = input.bool(true, title="Dark Mode", group="Appearance", inline="DM")

// Bollinger Bands calculation
[bbMid, bbUpper, bbLower] = ta.bbands(close, bbLengthInput, bbDevInput)

// Trend filter logic (optional)
trendFilterPeriod = trendFilterTypeInput == "SMA" ? ta.sma(close, trendFilterPeriodInput) : 
                    trendFilterTypeInput == "EMA" ? ta.ema(close, trendFilterPeriodInput) :
                    trendFilterTypeInput == "RMA" ? ta.rma(close, trendFilterPeriodInput) :
                    trendFilterTypeInput == "WMA" ? ta.wma(close, trendFilterPeriodInput) : na

longCondition = close > bbUpper and (trendFilterPeriod > trendFilterPeriod[1] or not na(trendFilterPeriod))
shortCondition = close < bbLower and (trendFilterPeriod < trendFilterPeriod[1] or not na(trendFilterPeriod))

// Volatility filter logic
volatilityFilter = ta.stdev(close, volatilityFilterStDevLengthInput)

// Rate of change filter logic (optional)
rocFilter = rocEnableInput ? ta.rocr(close, 1) > rocThresholdInput : false

// Date filter logic (optional)
dateFilter = startFilterDateInput <= time and endFilterDateInput >= time

// Apply filters
filterCondition = longCondition and shortCondition and volatilityFilter and not dateFilter

// Entry conditions
if (filterCondition and not na(bbUpper) and not na(trendFilterPeriod))
    strategy.entry("Long", strategy.long)

if (filterCondition and not na(bbLower) and not na(trendFilterPeriod)) 
    strategy.entry("Short", strategy.short)

// Exit logic for both long and short positions
longExitTimeStop = ta.valuewhen(strategy.opentrades.exists("Long"), close - longExitTimeStopInput * close, 0)
shortExitTimeStop = ta.valuewhen(strategy.opentrades.exists("Short"), close + shortExitTimeStopInput * close, 0)

longExitTrailingStop = strategy.exit("Long Exit", "Long", stop=longExitTimeStop, trail_offset=longExitTrailingOffsetInput)
shortExitTrailingStop = strategy.exit("Short Exit", "Short", stop=shortExitTimeStop, trail_offset=shortExitTrailingOffsetInput)

// Set take profit and stop loss
strategy.exit("Long TP/SL", "Long", limit=close + longExitTPPercentInput * close / 100, stop=close - longExitSLPercentInput * close / 100)
strategy.exit("Short TP/SL", "Short", limit=close - shortExitTPPercentInput * close / 100, stop=close + shortExitSLPercentInput * close / 100)

// Risk management
intradayLoss = strategy.max.drawdown(strategy.equity) > maxIntradayLossInput
if (intradayLoss)
    strategy.close_all()

// Output for results table
strategy.table(title="Results", precision=resultsTablePrecisionInput, columns=["Symbol", "Profit (%)"])
```