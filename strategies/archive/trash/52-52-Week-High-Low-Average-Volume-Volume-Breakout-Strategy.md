> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-09-24 08:00:00
period: 1d
basePeriod: 1d
exchange: EXTERNAL_DATA
*/

//@version=5
strategy("52-Week High-Low Average Volume Breakout Strategy", overlay=true)

// Parameters
highLowPercent = input(10, title="High/Low Percent from 52 Week")
volumeMultiplier = input(1.5, title="Volume Multiplier for Breakout")
priceChangeLimitDaily = input(3, title="Daily Price Change Limit (%)")
priceChangeLimitWeeklyMonthly = input(10, title="Weekly/Monthly Price Change Limit (%)")

// Calculate 52-week high and low
high52Week = ta.highest(high, 52 * period)
low52Week = ta.lowest(low, 52 * period)

// Calculate 50-day average volume
avgVolume = ta.volume[50] / 50

// Check conditions for buy signal
closeToHigh = close <= high52Week * (1 + highLowPercent / 100)
volumeBreakout = ta(volume) > avgVolume * volumeMultiplier
priceChangeWithinLimitDaily = math.abs((close - open) / open) < priceChangeLimitDaily / 100
priceChangeWithinLimitWeeklyMonthly = math.abs((close - close[7]) / close[7]) < priceChangeLimitWeeklyMonthly / 100

// Entry signal
if (closeToHigh and volumeBreakout and priceChangeWithinLimitDaily and priceChangeWithinLimitWeeklyMonthly)
    strategy.entry("Buy", strategy.long)

plotshape(series=high52Week, title="52-Week High", location=location.abovebar, color=color.red, style=shape.triangleup, size=size.small)
plotshape(series=low52Week, title="52-Week Low", location=location.belowbar, color=color.green, style=shape.triangledown, size=size.small)

// Plot signals
bgcolor(color.new(color.blue, 90), transp=true) when (closeToHigh and volumeBreakout and priceChangeWithinLimitDaily and priceChangeWithinLimitWeeklyMonthly)
```

This PineScript code defines the "52-Week High-Low Average Volume Breakout Strategy" with the specified parameters. It calculates the 52-week high and low prices, tracks average volume over 50 days, and checks for entry signals based on the defined conditions. The strategy plots visual indicators for 52-week highs and lows as well as buy signals when all criteria are met.