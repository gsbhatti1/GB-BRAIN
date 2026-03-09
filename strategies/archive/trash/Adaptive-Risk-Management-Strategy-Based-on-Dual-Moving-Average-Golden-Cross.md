``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-09-24 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Golden Cross with 1.5% Stop-Loss & MA Exit", overlay=true)

// Define the 50-day and 200-day moving averages
ma50 = ta.sma(close, 50)
ma200 = ta.sma(close, 200)

// Entry condition: 50-day MA crosses above 200-day MA (Golden Cross)
goldenCross = ta.crossover(ma50, ma200)

// Exit condition: price drops below the 200-day MA
exitCondition = close < ma200

// Set the stop-loss to 1.5% below the 200-day moving average
stopLoss = ma200 * 0.985  // 1.5% below the 200-day MA

// Risk management (1.5% of total equity)
riskPercent = 0.025  // 2.5% risk
equity = strategy.equity
riskAmount = equity * riskPercent

// Calculate the distance between the entry price (close) and the stop-loss
stopDistance = close - stopLoss

// Calculate position size based on the risk amount and stop-loss distance
if (goldenCross and stopDistance > 0)
    positionSize = riskAmount / stopDistance
    strategy.entry("Golden Cross", strategy.long, stop=stopLoss, qty=positionSize)
    
// Exit on 200-day MA
if (exitCondition)
    strategy.close("Golden Cross")
```

This Pine Script code implements the trading strategy described, ensuring all original code blocks, numbers, and formatting are preserved.