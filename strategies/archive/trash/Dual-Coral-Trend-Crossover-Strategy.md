> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-09-24 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("D-Stryker LT", overlay=true)

// Input settings for Coral Trend 1
smoothingPeriod1 = input.int(3, title="Coral Trend 1 Smoothing Period")
constantD1 = input.float(0.2, title="Coral Trend 1 Constant D")

// Input settings for Coral Trend 2
smoothingPeriod2 = input.int(6, title="Coral Trend 2 Smoothing Period")
constantD2 = input.float(0.2, title="Coral Trend 2 Constant D")

// Function to calculate Coral Trend
coralTrend(source, smoothingPeriod, constantD) =>
    emaValue = ta.ema(source, smoothingPeriod)
    smoothEma = ta.ema(emaValue, smoothingPeriod)
    trendLine = smoothEma + constantD * (emaValue - smoothEma)
    trendLine

// Calculate Coral Trends
coralTrend1 = coralTrend(close, smoothingPeriod1, constantD1)
coralTrend2 = coralTrend(close, smoothingPeriod2, constantD2)

// Plot Coral Trends
plot(coralTrend1, title="Coral Trend 1", color=color.blue, linewidth=2)
plot(coralTrend2, title="Coral Trend 2", color=color.red, linewidth=2)

// Generate buy signal when Coral Trend 1 crosses above Coral Trend 2
buySignal = crossover(coralTrend1, coralTrend2)
if (buySignal)
    strategy.entry("Buy", strategy.long)
```

Note: The `crossover` function checks if the first argument crosses above the second one. If a cross occurs, it triggers a long entry in the strategy.