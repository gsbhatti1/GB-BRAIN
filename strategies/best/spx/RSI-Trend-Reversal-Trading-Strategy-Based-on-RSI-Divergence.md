``` pinescript
/*backtest
start: 2024-04-01 00:00:00
end: 2024-04-30 23:59:59
period: 3h
basePeriod: 15m
exchanges: [{"eid":"Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("RSI Divergence Strategy", overlay=true)

// Input parameters
rsiLength = input.int(14, title="RSI Length")
rsiOverbought = input.int(70, title="RSI Overbought Level")
rsiOversold = input.int(30, title="RSI Oversold Level")
lookback = input.int(5, title="Lookback Period for Divergence")

// Calculate RSI
rsi = ta.rsi(close, rsiLength)

// Function to detect bullish divergence
bullishDivergence(price, rsi, lookback) =>
    var bool bullDiv = false
    for i = 1 to lookback
        if (low[i] < low and rsi[i] > rsi)
            bullDiv := true
    bullDiv

// Function to detect bearish divergence
bearishDivergence(price, rsi, lookback) =>
    var bool bearDiv = false
    for i = 1 to lookback
        if (high[i] > high and rsi[i] < rsi)
            bearDiv := true
    bearDiv

// Generate buy signal when bullish divergence is detected and RSI crosses above the oversold threshold
if bullishDivergence(low, rsi, lookback) and rsi > rsiOversold
    strategy.entry("Buy", strategy.long)

// Generate sell signal when bearish divergence is detected and RSI crosses below the overbought threshold
if bearishDivergence(high, rsi, lookback) and rsi < rsiOverbought
    strategy.close("Buy")

// Plot RSI on the chart
plot(rsi, title="RSI", color=color.blue)
```