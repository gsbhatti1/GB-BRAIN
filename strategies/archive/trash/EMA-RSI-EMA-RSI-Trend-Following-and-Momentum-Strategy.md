``` pinescript
/*backtest
start: 2024-03-21 00:00:00
end: 2024-03-28 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// @BryanAaron

//@version=5
strategy("Bybit EMA RSI Strategy", overlay=true)

// Input parameters
fastLength = input(90, title="Fast EMA Length")
slowLength = input(300, title="Slow EMA Length")
rsiLength = input(5, title="RSI Length")
upperThreshold = input(85, title="RSI Upper Threshold")
lowerThreshold = input(45, title="RSI Lower Threshold")
takeProfitPct = input(5, title="Take Profit %")
stopLossPct = input(3, title="Stop Loss %")
accountLevel = input.string("0", title="Bybit Account Level")

// Calculate EMAs
emaFast = ta.ema(close, fastLength)
emaSlow = ta.ema(close, slowLength)

// Calculate RSI
rsiValue = ta.rsi(close, rsiLength)

// Generate trading signals
longCondition = emaFast > emaSlow and rsiValue < lowerThreshold
shortCondition = emaFast < emaSlow and rsiValue > upperThreshold

// Plot EMAs and RSI on the chart
plot(emaFast, color=color.blue, title="Fast EMA")
plot(emaSlow, color=color.red, title="Slow EMA")
hline(lowerThreshold, "Lower Threshold", color=color.green)
hline(upperThreshold, "Upper Threshold", color=color.orange)

// Set order parameters based on account level
commissionRate = 0.075 - (0.04 * accountLevel)
entryPrice = na

if longCondition and not na(entryPrice)
    entryPrice := close
    strategy.entry("Long Entry", strategy.long)
    strategy.exit("Take Profit & Stop Loss", "Long Entry", profit=takeProfitPct, loss=stopLossPct)

if shortCondition and not na(entryPrice)
    entryPrice := close
    strategy.entry("Short Entry", strategy.short)
    strategy.exit("Take Profit & Stop Loss", "Short Entry", profit=takeProfitPct, loss=stopLossPct)
```

This Pine Script code implements the described EMA-RSI trend-following and momentum strategy. The script includes all the necessary components such as input parameters, calculation of EMAs and RSI, generation of trading signals based on specified conditions, and execution of trades with stop-loss and take-profit orders.