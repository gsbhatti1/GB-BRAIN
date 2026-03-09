> Name

Heiken-Ashi Momentum Quant Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1414bd2e5a37b7540ce.png)
[trans]

### Overview

This strategy is based on daily Heiken Ashi candlesticks, combined with momentum analysis across different timeframes to dynamically determine the underlying support behind the current price and identify entry and exit points.

### Strategy Logic

1. Calculate the close prices of Heiken Ashi candlesticks across different timeframes as the basis for subsequent momentum analysis.
2. Calculate the percentage change between open prices and historical close prices over different periods, for both monthly and daily timeframes. This reflects the momentum strength behind the current price relative to historical levels.
3. Take the averages of the daily and monthly momentum fluctuations respectively. This filters out some noise and derives more stable momentum benchmarks.
4. Based on the average momentum fluctuations, we can calculate the market support force truly reflected by the current price, i.e., the dynamic momentum threshold exclusive of market noise.
5. When the close price breaks above the momentum threshold, long positions are initiated monthly. When the price closes below the threshold, positions are closed.

### Pros Analysis

The biggest advantage lies in the fact that instead of simply chasing prices, the strategy calculates the real support force behind prices for entries and exits. This effectively filters out noise from ranging markets and allows us to capture stable uptrends.

Also, all underlying data is derived from Heiken Ashi candlesticks, which intrinsically helps reduce the problem of excessive reliance on linked timeframes that exists in other types of candlestick strategies. So stability is better.

### Risk Analysis

The biggest risk is that momentum calculations rely solely on historical prices. If underlying company fundamentals or market regimes see significant changes, the representativeness of historical prices decreases, leading to errors in identifying entries and exits.

Also, the strategy leverages monthly and daily timeframes. This means real-time performance is not the best, lacking the ability to respond swiftly to drastic price changes. Thus there are risks of exits not triggering in time when prices suddenly turn.

Possible ways to mitigate include incorporating higher frequency data and real-time feedback on company fundamentals. Or complement with more subjective trading signals for validation and optimization.

### Optimization Directions

There are a few ways in which the strategy can be further improved:

1. Further enhance the Heiken Ashi candles themselves, i.e., optimize weight configurations.
2. Incorporate more timeframes, construct an exponentially averaged scoring mechanism to enhance stability.
3. Introduce higher frequency data such as minute bars to improve real-timeness.
4. Incorporate earnings warnings, M&A rumors into momentum calculations to add company fundamentals.
5. Consider adding day & week-based profit-taking and re-entry mechanics on top of the monthly entries.

### Conclusion

In summary, the strategy is very stable overall, with momentum tracking effectively controlling risks. The biggest advantage is using the underlying force behind prices rather than prices themselves to determine true market conditions for entries and exits. Next step is to further improve by incorporating higher frequency and more informative data to better capitalize on market opportunities.

[/trans]

```pinescript
/*backtest
start: 2023-01-12 00:00:00
end: 2024-01-18 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © FrancoPassuello

//@version=5
strategy("Heiken Ashi ADM", overlay=true)
haClose = (open + high + low + close) / 4
// prevHaOpen = line.new(na, na, na, na, width = 1)
haOpen = (open[1] + close[1]) / 2
// line.set_xy1(prevHaOpen, bar_index[1], nz(haOpen[1]))
// line.set_xy2(prevHaOpen, bar_index, haClose[1])


[monopen, _1monopen, _2monopen, _3monopen, _4monopen, _5monopen, _6monopen] = request.security(syminfo.tickerid, "M", [haOpen, haOpen[1], haOpen[2], haOpen[3], haOpen[4], haOpen[5], haOpen[6]] , barmerge.gaps_off, barmerge.lookahead_on)
[monclose, _1monclose, _3monclose, _6monclose] = request.security(syminfo.tickerid, "M", [haClose, haClose[1], haClose[3], haClose[6]] , barmerge.gaps_off, barmerge.lookahead_on)
[dayclose1, _21dayclose, _63dayclose, _126dayclose, dayclose] = request.security(syminfo.tickerid, "1D", [haClose[1], haClose[21], haClose[63], haClose[126], haClose], barmerge.gaps_off, barmerge.lookahead_on)
[d