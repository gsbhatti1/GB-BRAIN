``` pinescript
/*backtest
start: 2023-10-24 00:00:00
end: 2023-11-23 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © fenirlix

//@version=5
// Strategy parameter incl. position size, commission and initial capital
strategy("ACTIONZONE-ATR REVERSEORDER STRATEGY", "ACTIONZONEATR-REVERSEORDER", overlay=true)

// User Input Variable
fastMaInput     = input.int(12, "Fast MA Period", minval=2, step=1)
slowMaInput     = input.int(26, "Slow MA Period", minval=2, step=1)

atrLengthInput  = input.int(14, "ATR length", minval=2, step=1)
atrInnerMultInput = input.float(1, "ATR inner multiplier", minval=0.1, step=0.1)
atrMidMultInput = input.float(2, "ATR mid multiplier", minval=0.1, step=0.1) //***** MOST OF RISK MANAGEMENT LOGIC BASED ON THIS INPUT *****//
atrOuterMultInput = input.float(3, "ATR outer multiplier", minval=0.1, step=0.1)

// Backtesting Date range
startYearInput      = input.int(2021, "Start Year", minval=1900, maxval=2100, step=1)
startMonthInput     = input.int(12, "Start Month", minval=1, maxval=12, step=1)
startDateInput      = input.int(1, "Start Day", minval=1, maxval=31, step=1)
setEndRangeInput    = input.bool(false, "Using Specific End Test Date")
endYearInput        = input.int(2022, "End Year", minval=1900, maxval=2100, step=1)
endMonthInput       = input.int(true, "End Month", minval=1, maxval=12, step=1)
endDateInput        = input.int(31, "End Day", minval=1, maxval=31, step=1)

// Minimum position hold limit
minPositionHoldLimit = input.int(8, "Minimum Position Hold Limit", minval=1, step=1)

// EMA calculations
fastMa = ta.ema(close, fastMaInput)
slowMa = ta.ema(close, slowMaInput)

// ATR calculation
atrLen = atrLengthInput
lenATR = ta.atr(atrLen)
atrInner = atrInnerMultInput * lenATR
atrMid  = atrMidMultInput * lenATR
atrOuter = atrOuterMultInput * lenATR

longCondition = ta.crossover(fastMa, slowMa)
shortCondition = ta.crossunder(fastMa, slowMa)

// Position management
var float stopLossPrice = na
if (na(stopLossPrice) or (not longCondition and not shortCondition))
    // Calculate stop loss price based on ATR
    if (longCondition)
        stopLossPrice := close - atrInner
    else if (shortCondition)
        stopLossPrice := close + atrOuter

// Entry logic
if (longCondition)
    strategy.entry("Long", strategy.long, stop=stopLossPrice)

if (shortCondition)
    strategy.entry("Short", strategy.short, stop=stopLossPrice)

// Exit logic
if (not na(stopLossPrice) and ta.crossover(close, stopLossPrice))
    strategy.close("Long")
    strategy.close("Short")

// Adjust stop loss when price enters overbought or oversold zone
if (ta.highest(high, atrLengthInput + 1)[atrLengthInput] > close)
    // Sell to cover if in long position and price is above highest ATR zone
    strategy.close("Long", comment="Exited due to high ATR zone")
else if (ta.lowest(low, atrLengthInput + 1)[atrLengthInput] < close)
    // Buy to open if in short position and price is below lowest ATR zone
    strategy.entry("Short", strategy.short)

// Additional settings
strategy.exit("Exit Long", "Long", stop=close + atrMid)
strategy.exit("Exit Short", "Short", stop=close - atrMid)

```