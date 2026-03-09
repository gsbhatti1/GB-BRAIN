``` pinescript
/*backtest
start: 2023-05-23 00:00:00
end: 2024-05-28 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
// suitable for : AMZN - 30 minutes, MSFT - 30 minutes, NVDA -15 minutes

strategy("AAPL-SIMPLE_SMA", overlay=true)

// Create Indicator's

// Create Indicator's
shortSMA = ta.sma(close, 10)
longSMA = ta.sma(close, 30)
rsi = ta.rsi(close, 14)
atr = ta.atr(14)
qty = 1

// Specify crossover conditions
longCondition = ta.crossover(shortSMA, longSMA)
shortCondition = ta.crossunder(shortSMA, longSMA)

// Execute trade if condition is met
if (longCondition)
    strategy.entry("Long", strategy.long)
    stopLossLevel = close - 2 * atr
    takeProfitLevel = close + 6 * atr
    strategy.exit("Take Profit & Stop Loss", "Long", stop=stopLossLevel, limit=takeProfitLevel)

if (shortCondition)
    strategy.entry("Short", strategy.short)
    stopLossLevel = close + 2 * atr
    takeProfitLevel = close - 6 * atr
    strategy.exit("Take Profit & Stop Loss", "Short", stop=stopLossLevel, limit=takeProfitLevel)
```

This code snippet translates the given Pine Script strategy, maintaining the original formatting and structure. The script defines the conditions for entering long and short positions based on the crossover of short-term and long-term SMAs, and incorporates the use of ATR for setting stop loss and take profit levels.