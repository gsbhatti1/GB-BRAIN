```pinescript
/*backtest
start: 2023-10-14 00:00:00
end: 2023-11-13 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
//Copyright Boris Kozak 
strategy("XBT Weekend Trade Strategy", overlay=false)
leverage = input(10, "Leverage")
profitTakingPercentThreshold = input(0.10, "Profit Taking Percent Threshold")

//****Code used for setting up backtesting.****///
testStartYear = input(2017, "Backtest Start Year")
testStartMonth = input(12, "Backtest Start Month")
testStartDay = input(10, "Backtest Start Day")
testPeriodStart = timestamp(testStartYear, testStartMonth, testStartDay, 0, 0)

testStopYear = input(2025, "Backtest Stop Year")
testStopMonth = input(12, "Backtest Stop Month")
testStopDay = input(30, "Backtest Stop Day")
testPeriodStop = timestamp(testStopYear, testStopMonth, testStopDay, 0, 0)

// Record Friday's closing price
var float fridayClose = na
if (dayofweek == 5 and not na(close[1]))
    fridayClose := close

// Check if it's Saturday or Sunday
var bool isWeekend = na
if (dayofweek == 6 or dayofweek == 7)
    isWeekend := true

// Go short if price is more than 4.5% above Friday's close
if (isWeekend and fridayClose != na and (close - fridayClose) / fridayClose > 0.045)
    strategy.entry("Short", strategy.short, when=isWeekend, qty=100 * leverage)

// Go long if price is more than 4.5% below Friday's close
if (isWeekend and fridayClose != na and (fridayClose - close) / fridayClose > 0.045)
    strategy.entry("Long", strategy.long, when=isWeekend, qty=100 * leverage)

// Close all positions if profit reaches 10% of initial capital
profitTarget = strategy.equity * 0.10
if (strategy.equity > initialEquity + profitTarget)
    strategy.close("Short")
    strategy.close("Long")

// Close all positions on Monday
if (dayofweek == 1)
    strategy.close_all()

initialEquity = strategy.equity
```

Note: The Pine Script version used here is 3, as specified in the original script. The initial equity is tracked and compared against the profit target to close positions when the threshold is met.