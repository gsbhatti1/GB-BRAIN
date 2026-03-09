``` pinescript
/*backtest
start: 2024-04-01 00:00:00
end: 2024-04-30 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("KDJ Trending View with Signals and MA Strategy", overlay=true)

// KDJ Settings
kdjLength = input.int(9, title="KDJ Length")
kdjSignal = input.int(3, title="KDJ Signal")
kdjOverbought = input.int(80, title="KDJ Overbought Level")
kdjOversold = input.int(20, title="KDJ Oversold Level")

// Margin Settings
longMargin = input.float(2.0, title="Long Margin", step=0.01)
shortMargin = input.float(2.0, title="Short Margin", step=0.01)

// MA Settings
maLength = input.int(20, title="MA Length")
maType = input.string("SMA", title="MA Type (SMA, EMA, etc.)")

// Calculate KDJ
kdj_highest = ta.highest(high, kdjLength)
kdj_lowest = ta.lowest(low, kdjLength)
kdjRSV = 100 * ((close - kdj_lowest) / (kdj_highest - kdj_lowest))
k = 3 * (2 * kdjRSV / 100 + (50 - 2 * kdjRSV / 100) / 3)
d = ta.sma(k, kdjSignal)
j = 3 * k - 2 * d

// Calculate MA
ma = ta.stoch(close, high, low, maLength)

// Determine trend direction
trendDirection = ta.crossover(ma, close) ? "Bullish" : ta.crossunder(ma, close) ? "Bearish" : ""

// Generate trading signals
longCondition = j > kdjOverbought and ta.crossover(j, kdjOverbought)
shortCondition = j < kdjOversold and ta.crossover(kdjOversold, j)

if (longCondition)
    strategy.entry("Long", strategy.long, comment="Long Signal")
    
if (shortCondition)
    strategy.entry("Short", strategy.short, comment="Short Signal")

// Position management
strategy.exit("Exit Long", "Long", stop=ta.atr(7), trail_offset=20)
strategy.exit("Exit Short", "Short", stop=ta.atr(7), trail_offset=20)

```

This Pine Script code defines the KDJ trend following strategy with signals and moving averages. It includes settings for KDJ, margin, and MA, as well as the logic to generate trading signals based on these indicators and MA trends. The script also implements basic position management with stop-loss orders triggered by ATR (Average True Range).