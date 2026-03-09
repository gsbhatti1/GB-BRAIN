``` pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("OBV EMA X BF ?", overlay=false, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=100, commission_type=strategy.commission.percent, commission_value=0.0)

/////////////// Time Frame ///////////////
testStartYear = input(2017, "Backtest Start Year") 
testStartMonth = input(1, "Backtest Start Month")
testStartDay = input(1, "Backtest Start Day")
testPeriodStart = timestamp(testStartYear, testStartMonth, testStartDay, 0, 0)

testStopYear = input(2019, "Backtest Stop Year")
testStopMonth = input(12, "Backtest Stop Month")
testStopDay = input(31, "Backtest Stop Day")
testPeriodStop = timestamp(testStopYear, testStopMonth, testStopDay, 0, 0)

testPeriod() => true

/////////////// OBV /////////////// 
src = close
atr = atr(input(title="ATR Period", defval=3, minval=1))
atrmult = input(title="ATR Mult", defval=true)
obv = obv(src)

ema6 = ema(obv, 6)
ema24 = ema(obv, 24)

longCondition = ema6 > ema24
shortCondition = ema6 < ema24

// Plot EMA lines
plot(ema6, title="6-day EMA", color=color.blue)
plot(ema24, title="24-day EMA", color=color.red)

// Generate signals
if (longCondition and testPeriod())
    strategy.entry("Long", strategy.long)
if (shortCondition and testPeriod())
    strategy.entry("Short", strategy.short)

// Stop Loss and Take Profit
stopLossPercent = input(3, title="Stop Loss %")
takeProfitPercent = input(5000, title="Take Profit %")

stopLoss = atr * atrmult * stopLossPercent / 100
takeProfit = atr * atrmult * takeProfitPercent / 100

strategy.exit("Take Profit", "Long", stop=true, limit=false, loss=stopLoss)
strategy.exit("Take Profit", "Short", stop=false, limit=true, loss=stopLoss)
```