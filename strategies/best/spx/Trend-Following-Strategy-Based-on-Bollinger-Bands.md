``` pinescript
/*backtest
start: 2024-01-22 00:00:00
end: 2024-02-21 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// © Valente_F
//@version=4
strategy(title="Trend-Following Strategy Based on Bollinger Bands", shorttitle="Bollinger Bands TFS", overlay = true, pyramiding = 0, default_qty_type = strategy.percent_of_equity)

// Inputs
length = input(20, title="Length")
stdDev = input(2, title="StdDev")
enableLongEntrys = input(true, title="Enable Long Entrys")
enableShortEntrys = input(true, title="Enable Short Entrys")

// Bollinger Bands Calculation
src = close
upperBB, lowerBB, midBB = bband(src, length, stdDev)

// Long Entry Conditions
longCondition = close > upperBB and prevClose < upperBB

// Short Entry Conditions
shortCondition = close < lowerBB and prevClose > lowerBB

// Execute Trades
if (enableLongEntrys and longCondition)
    strategy.entry("Long", strategy.long)

if (enableShortEntrys and shortCondition) 
    strategy.entry("Short", strategy.short)

// Stop Loss at Middle Band
stopLossLevel = midBB
```

This code block translates the provided human-readable text into English while maintaining the original Pine Script structure, including comments and default settings.