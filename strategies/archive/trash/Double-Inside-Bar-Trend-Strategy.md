> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_source_1_close|0|(?Entry Seettings)MA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_string_1|0|MA Type: HMA|EMA|SMA|SWMA|VWMA|WMA|
|v_input_int_1|45|HMA Length|
|v_input_string_2|0|(?Trade Seettings)Stop Loss Type: ATR|FIX|
|v_input_int_2|50|   ATR: Length                 |
|v_input_float_1|2.5|Factor       |
|v_input_float_2|2|            TP Ration|
|v_input_float_3|10|   FIX: Stop Loss             |
|v_input_float_4|20|Take Profit|
|v_input_bool_1|true|10useRiskMagmt|
|v_input_float_5|true|Risk in %                |
|v_input_bool_2|false|(?Filter Setings)Filter trades by dates|
|v_input_1|timestamp(2022-01-01T00:00:00+0000)|       Start Date & Time|
|v_input_2|timestamp(2099-12-31T23:59:00+0000)|       End Date & Time  |
|v_input_bool_3|false|Filter trades by session|
|v_input_3|0045-2245|       Session|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Kaspricci

//@version=5
strategy(
     title = "Double Inside Bar & Trend Strategy - Kaspricci", 
     shorttitle = "Double Inside Bar & Trend", 
     overlay=true, 
     initial_capital = 100000, 
     currency = currency.USD, 
     default_qty_type = strategy.percent_of_equity, 
     default_qty_value = 100, 
     calc_on_every_tick = true, 
     close_entries_rule = "ANY")

// ================================================ Entry Inputs ======================================================================
headlineEntry   = "Entry Settings"

maSource        = input.source(defval = close,             group = headlineEntry, title = "MA Source")
maType          = input.string(defval = "HMA",             group = headlineEntry, title = "MA Type", options = ["EMA", "HMA", "SMA", "SWMA", "VWMA", "WMA"])
maLength        = input.int(   defval = 45,    minval = 1, group = headlineEntry, title = "HMA Length")

float ma = switch maType 
    case "EMA"  => ta.ema(maSource,  maLength)
    case "HMA"  => ta.hma(maSource,  maLength)
    case "SMA"  => ta.sma(maSource,  maLength)
    case "SWMA" => ta.swma(maSource)
    case "VWMA" => ta.vwma(maSource, 

// ================================================ Trade Inputs ======================================================================
headlineTrade   = "Trade Settings"

stopLossType    = input.string(defval = "ATR",             group = headlineTrade, title = "Stop Loss Type", options = ["ATR", "FIX"])
atrLength      = input.int(   defval = 50,     minval = 1, group = headlineTrade, title = "ATR Length")
factor         = input.float(defval = 2.5,    minval = 0,  group = headlineTrade, title = "Factor")
tpRatio        = input.float(defval = 2,      minval = 0,  group = headlineTrade, title = "TP Ratio")
fixStopLoss    = input.float(defval = 10,     minval = 0,  group = headlineTrade, title = "FIX: Stop Loss")
takeProfit     = input.float(defval = 20,     minval = 0,  group = headlineTrade, title = "Take Profit")

if stopLossType == "ATR"
    stopLossAmount = ta.atr(atrLength) * factor
else if stopLossType == "FIX" 
    stopLossAmount = fixStopLoss

// ================================================ Risk Management Inputs =============================================================
headlineRisk    = "Risk Management"

riskManagement  = input.bool(defval = true, group = headlineRisk, title = "Use Risk Management")
riskPercentage = input.float(defval = 100, minval = 0.1, maxval = 100, group = headlineRisk, title = "Risk in %")

// ================================================ Date Filters ===================================================================
headlineDate    = "Date Filters"

startDateTime   = input.time(timestamp("2022-01-01T00:00:00+0000"), group = headlineDate, title = "Start Date & Time")
endDateTime     = input.time(timestamp("2099-12-31T23:59:00+0000"), group = headlineDate, title = "End Date & Time")

// ================================================ Session Filters ================================================================
headlineSession  = "Session Filters"

sessionFilter   = input.bool(defval = false, group = headlineSession, title = "Filter trades by session")
sessionTime     = input.time(timestamp("2045-2245"), group = headlineSession, title = "Session")

// ================================================ Main Logic ====================================================================
var float entryPrice  = na
var int   tradeID     = na

if sessionFilter and time[1] < sessionTime and not filterTrade(startDateTime, endDateTime)
    exit
```

This completes the translation of the provided trading strategy document into English while maintaining all code blocks, numbers, and formatting.