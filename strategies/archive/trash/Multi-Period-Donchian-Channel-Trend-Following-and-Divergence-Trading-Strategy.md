```pinescript
/*backtest
start: 2024-06-12 00:00:00
end: 2025-02-19 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=6
strategy("Donchian Trend Ribbon Strategy", shorttitle="DonchianTrendRibbonStrat", overlay=true, precision=0)

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Parameters
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
dlen = input.int(defval=20, title="Donchian Channel Period", minval=10)

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Helper function to determine color
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
f_color(mainTrend, localTrend) =>
    // mainTrend = 1 => uptrend, -1 => downtrend
    // localTrend = 1 => local uptrend, -1 => local downtrend
    // Return color based on whether local trend aligns with the main trend
    color c = na
    if mainTrend == 1
        c := localTrend == 1 ? color.new(color.lime, 0) : color.new(color.lime, 60)
    else if mainTrend == -1
        c := localTrend == -1 ? color.new(color.red, 0) : color.new(color.red, 60)
    else
        c := na
    c

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Main logic
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Main trend determination
mainTrend = ta.sma(highest(high, dlen), dlen) > ta.sma(lowest(low, dlen), dlen) ? 1 : -1

// Local trend determination
localTrend = ta.sma(highest(high, dlen), dlen) > ta.sma(lowest(low, dlen), dlen) ? 1 : -1

// Trend ribbon
for i = 1 to 10
    strategy.entry("Long Entry " + tostring(i), strategy.long, when=mainTrend == 1 and localTrend == 1)
    strategy.close("Long Exit " + tostring(i), when=mainTrend == -1 or not na(localTrend) and localTrend == -1)
```

This Pine Script code defines a strategy that uses Donchian Channels to determine both the main and local trends, and visualizes them on a trend ribbon. The script also includes a function to determine the color of the trend based on the alignment of local trends with the main trend.