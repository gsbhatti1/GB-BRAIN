``` pinescript
/*backtest
start: 2024-01-27 00:00:00
end: 2024-02-26 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy(title="DMI Strategy with ADX and ATR-based Trailing SL (Long Only) and Seasonality", shorttitle="MBV-SP500-CLIMBER", overlay=true)

// Input parameters for long positions
len = input.int(14, minval=1, title="DI Length")
lensig = input.int(14, title="ADX Smoothing", minval=1, maxval=50)
adxLongThreshold = input.float(27.0, title="ADX Threshold for Long", minval=0)
atrLength = input.int(14, title="ATR Length")
atrLongMultiplier = input.float(5.5, title="ATR Multiplier for Trailing SL (Long)")

startTimeHH = input.int(9, title="startTime hh")
startTimeMM = input.int(30, title="startTime mm")

endTimeHH = input.int(20, title="endTime hh")
endTimeMM = input.int(30, title="endTime mm")

// User's timezone offset as an input parameter
timezoneOffset = input.int(1, title="Timezone Offset (Hours from UTC)", minval=-12, maxval=14)

// Additional settings for S&P500 seasonality
enableSeasonality = input.bool(false, title="Enable SP500 Seasonality")
seasonColor = color.new(color.blue, 90)
activeTimeColor = color.new(color.yellow, 90) // Color for active trading times

// Trading days and times
tradeMonday = input.bool(true, title="Trade on Monday")
tradeTuesday = input.bool(true, title="Trade on Tuesday")
tradeWednesday = input.bool(true, title="Trade on Wednesday")
tradeThursday = input.bool(true, title="Trade on Thursday")
tradeFriday = input.bool(true, title="Trade on Friday")

// Conversion of time to Unix timestamp
getUnixTime(hour, minute) =>
    adjustedHour = hour - timezoneOffset
    sessionDate = timestamp(year, month, dayofmonth, 0, 0)
    sessionDate + adjustedHour * 60 * 60000 + minute * 60000

// Start and end times as Unix timestamps
// + 1 hour due to UTC
startTime = getUnixTime(startTimeHH, startTimeMM)
endTime = getUnixTime(endTimeHH, endTimeMM)

// Calculate ATR
atrValue = ta.atr(atrLength)

// DMI calculation
plusDM = ta.higher(ta.highest(high - close, len), 0)
minusDM = ta.lower(ta.lowest(close - low, len), 0)
tr = high - low + ta.math.abs(ta.close[1] - high) + ta.math.abs(ta.close[1] - low)
avgTR = ta.ema(tr, lensig)

// ADX calculation
adxValue = ta.rma(avgTR / avgTR.sum(lensig), lensig)

// Generate buy signal when conditions are met
if (time >= startTime and time <= endTime) and tradeMonday and not enableSeasonality or (enableSeasonality and isSP500Bullish())
    if adxValue > adxLongThreshold and ta.crossover(ta.plus_di(len), ta.minus_di(len))
        strategy.entry("Long", strategy.long)

// Set trailing stop loss
if strategy.opentrades > 0
    for i = 0 to strategy.opentrades.count - 1
        pos_id = strategy.opentrades.id(i)
        entry_price = strategy.opentrades.price(i)
        
        if time >= startTime and time <= endTime
            trailStopPrice = entry_price - atrValue * atrLongMultiplier
            strategy.exit(id="TrailStop", from_entry="Long", limit=trailStopPrice)

// Function to check S&P500 seasonality
isSP500Bullish() =>
    // Implement logic here based on historical performance data of SP500

plot(time >= startTime and time <= endTime ? timezoneOffset : na, title="Timezone Offset", color=activeTimeColor)
```