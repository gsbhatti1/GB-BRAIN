``` pinescript
/*backtest
start: 2024-03-24 00:00:00
end: 2024-03-25 05:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Short-Term Scalable Trend Following Strategy", overlay=true)

// Define strategy parameters
fastMA_length = input(5, title="Fast MA Length")
slowMA_length = input(10, title="Slow MA Length")
rsi_length = input(7, title="RSI Length")
rsi_oversold = input(20, title="RSI Oversold Level")
rsi_overbought = input(80, title="RSI Overbought Level")

// Calculate Moving Averages
fastMA = ta.sma(close, fastMA_length)
slowMA = ta.sma(close, slowMA_length)

// Calculate RSI
rsi = ta.rsi(close, rsi_length)

// Determine entry and exit conditions
long_condition = ta.crossover(fastMA, slowMA) and rsi < rsi_oversold
short_condition = ta.crossunder(fastMA, slowMA) and rsi > rsi_overbought

// Enter long position
if (long_condition)
    strategy.entry("Long", strategy.long)

// Enter short position
if (short_condition)
    strategy.entry("Short", strategy.short)

// Exit positions
if (ta.crossover(fastMA, slowMA) or rsi > rsi_overbought)
    strategy.close("Long")
if (ta.crossunder(fastMA, slowMA) or rsi < rsi_oversold)
    strategy.close("Short")
```

This Pine Script code defines the strategy based on the provided description and parameters. It calculates the moving averages and RSI, and uses these to determine entry and exit conditions for both long and short positions.