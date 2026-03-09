``` pinescript
/*backtest
start: 2023-08-11 00:00:00
end: 2023-08-25 00:00:00
period: 5m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
// By ChaoZhang
// finished: 3/28/2023
strategy("Multi-Indicator-Configurable-Strategy-Generator", overlay=true, margin_long=100, margin_short=100, pyramiding=10, default_qty_type=strategy.percent_of_equity)

///////////////////////////////////////////////////////////////////////////////////////////////////////
/// PERIOD /// 
testStartYear = input.int(2023, "Backtest Start Year") 
testStartMonth = input.bool(true, "Backtest Start Month", title="Start Month") 
testStartDay = input.bool(true, "Backtest Start Day", title="Start Day") 
testPeriodStart = timestamp(testStartYear,testStartMonth?1:testStartMonth?23:0,testStartDay,0,0) 
 
testStopYear = input.int(2023, "Backtest Stop Year") 
testStopMonth = input.bool(true, "Backtest Stop Month", title="Stop Month") 
testStopDay = input.bool(true, "Backtest Stop Day", title="Stop Day") 
testPeriodStop = timestamp(testStopYear,testStopMonth?12:testStopMonth?0:0,testStopDay,0,0) 
 
testPeriod() => 
    time >= testPeriodStart and time <= testPeriodStop ? true : false
///////////////////////////////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////EMA INPUTS//////////////////////////////////////////////////
EMAON = input.bool(true, "EMA ON?", group = "EMA Settings", tooltip = "Check box for on")
IS1EMA = input.bool(false,"Only 1 EMA", title="Use EMA Fast Length for Input", group = "EMA Settings")
IS2EMA = input.bool(false, "Only 2 EMAs", title="Leave this box checked only if using 2 EMAs. Use EMA Middle and Fast Lengths.", group = "EMA Settings")
EMAFAST = input.int(50,title = "EMA Fast Length", minval = 1, maxval = 2000, group = "EMA Settings")
EMAMIDDLE = input.int(100, title= "EMA middle Length", minval = 1, maxval = 2000, group = "EMA Settings")
EMASLOW = input.int(200, title= "EMA Slow Length", minval = 1, maxval = 2000, group = "EMA Settings")
///////////////////////////////////////////////////////////////////////////////////////////////////////

```