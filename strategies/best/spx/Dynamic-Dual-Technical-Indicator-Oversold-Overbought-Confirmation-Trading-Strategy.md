``` pinescript
/*backtest
start: 2024-12-29 00:00:00
end: 2025-01-05 00:00:00
period: 5m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// TradingView Pine Script for RSI & CCI-Based Strategy
//@version=6
strategy("RSI & CCI Strategy", overlay=true)

// User Inputs
rsiLength = input.int(14, title="RSI Length")
rsiOverbought = input.int(80, title="RSI Overbought Level")
rsiOversold = input.int(20, title="RSI Oversold Level")

cciLength = input.int(20, title="CCI Length")
cciOverbought = input.int(200, title="CCI Overbought Level")
cciOversold = input.int(-200, title="CCI Oversold Level")

riskRewardRatio = input.float(2.0, title="Risk-Reward Ratio")
fixedStopLoss = input.float(1.0, title="Fixed Stop Loss (Percentage)", minval=0.1)

// RSI and CCI Calculations
rsi = ta.rsi(close, rsiLength)
cci = ta.cci(close, cciLength)

// Entry Conditions
longCondition = (rsi < rsiOversold) and (cci < cciOversold)
shortCondition = (rsi > rsiOverbought) and (cci > cciOverbought)

// Initialize variables for stop loss and take profit
var float stopLossPrice = na
var float takeProfitPrice = na

if longCondition
    strategy.entry("Long", strategy.long)
    stopLossPrice := close * (1 - fixedStopLoss / 100)
    takeProfitPrice := stopLossPrice + (stopLossPrice * riskRewardRatio)

if shortCondition
    strategy.entry("Short", strategy.short)
    stopLossPrice := close * (1 + fixedStopLoss / 100)
    takeProfitPrice := stopLossPrice - (takeProfitPrice - close) / riskRewardRatio

// Plot Stop Loss and Take Profit Levels
plot(stopLossPrice, color=color.red, title="Stop Loss")
plot(takeProfitPrice, color=color.green, title="Take Profit")

// Exit Conditions
if strategy.opentrades > 0
    if low[1] < stopLossPrice or high[1] > takeProfitPrice
        strategy.close("Long")
        strategy.close("Short")
```

```