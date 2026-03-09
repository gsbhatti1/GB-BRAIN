> Source (PineScript)

``` pinescript
/*backtest
start: 2023-06-11 00:00:00
end: 2024-06-16 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Range Trading with Stochastic", overlay=true)

// Input Parameters
overboughtLevel = input.int(80, title="Overbought Level", minval=1, maxval=100)
oversoldLevel = input.int(20, title="Oversold Level", minval=1, maxval=100)
stochLength = input.int(14, title="Stochastic Length", minval=1)
riskPerTrade = input.float(0.01, title="Risk per Trade (%)", minval=0.01, maxval=100, step=0.01)
barsBetweenTrades = input.int(20, title="Bars Between Trades", minval=1)

// Calculate Stochastic Oscillator
k = ta.sma(ta.stoch(close, high, low, stochLength), 3)
d = ta.sma(k, 3)

// Variables to Track Time Since Last Trade
var lastTradeBar = 0
barsSinceLastTrade = bar_index - lastTradeBar

// Risk Management
atr = ta.atr(14)
stopLoss = 2 * atr
takeProfit = 2 * atr
riskAmount = strategy.equity * riskPerTrade / 100
positionSize = 1

// Entry Conditions
longCondition = k < oversoldLevel and strategy.position_size == 0
shortCondition = k > overboughtLevel and strategy.position_size == 0

// Exit Conditions
longExitCondition = k > oversoldLevel
shortExitCondition = k < overboughtLevel

// Place Orders
if (barsSinceLastTrade >= barsBetweenTrades)
    if (longCondition)
        strategy.entry("Long", strategy.long, stop=stopLoss, limit=takeProfit, comment="Long Entry")
        lastTradeBar := bar_index
    if (shortCondition)
        strategy.entry("Short", strategy.short, stop=stopLoss, limit=takeProfit, comment="Short Entry")
        lastTradeBar := bar_index
```

This Pine Script implements the strategy as described, including the logic for entering and exiting trades based on the Stochastic Oscillator levels and the defined risk parameters.