> Name

Noros-Bollinger-Tracking-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/d852ec85e6bf00135e.png)

[trans]

## Overview
This is a momentum tracking strategy based on Bollinger Bands. It combines Bollinger Bands to judge market trends and reversal points, and sets long and short positions to track market fluctuations.

## Principles
The core indicator of this strategy is Bollinger Bands, which consists of middle band, upper band, and lower band. The middle band is the moving average of n days, and the upper and lower bands are the offsets of the middle band plus/minus standard deviation. When the price approaches the upper/lower band, it is considered a signal of overbought/oversold. The strategy incorporates trend deviation as the basis for opening positions, i.e., opening positions when the price breaks through the middle band in the opposite direction. To prevent losses caused by false breakouts, the strategy requires that the width of breakout is greater than the mean. The closing condition is that the price turns back after breaking through the middle band.

This strategy also incorporates both trend-following entries and mean-reversion entries, corresponding to different trading opportunities. Trend-following entries require the middle band to be the support/resistance reference and form deviation breakouts. Mean-reversion entries directly reverse near the upper/lower Bollinger bands. The strategy combines these two types of signals and can take both trend tracking and reversal operations.

## Advantage Analysis
This strategy combines the overbought/oversold characteristics of Bollinger Bands with reversal point judgment. This enables it to apply to both trending and ranging markets, capturing different types of trading opportunities. The stop loss exit setting prevents the loss from expanding. Also, the ability to trade both long and short enhances the applicability of the strategy.

Compared with simple Bollinger strategies, the additional trend logic makes entries of this strategy more stable, and it also captures reversal opportunities. This improves the signal-to-noise ratio. In addition, trading both directions utilizes trading opportunities more fully across different market situations.

## Risk Analysis
This strategy mainly relies on the overbought/oversold characteristics of Bollinger Bands. So when there is extreme price fluctuation, the width of Bollinger Bands keeps expanding, which can easily lead to multiple losing trades. This is a potential risk point. In addition, there are still some uncertainties and errors in reversal judgments, causing failed entries and stops.

Against the failure of Bollinger Bands, we can shorten the parameter n to make the bands more sensitive, or reduce the band width to lower the chance of losses. As for reversal curve judgments, optimizing the parameters of breakouts can reduce errors.

## Optimization Directions
The main directions to optimize this strategy include:
1. The parameters of Bollinger Bands can be adjusted according to different markets to find the optimal combination.
2. The magnitude of deviation and the calculation of mean values can be tested with other options.
3. Add more filters to judge entry signals and reduce false positives.
4. Test other stop loss methods like trail stop loss.
5. Parameters can be optimized towards specific products and timeframes.

## Conclusion
This strategy makes effective expansions and optimizations to standard Bollinger strategies. The added trend deviation improves stability and utilizes reversal opportunities well. The ability to trade both directions and stop losses also makes the strategy more robust. Further improvements can be achieved through parameter optimization and adding more filters.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|---|---|---|
|v_input_1|true|Long|
|v_input_2|true|Short|
|v_input_3|20|Bollinger Length|
|v_input_4|2|Bollinger Mult|
|v_input_5_ohlc4|0|Bollinger Source: ohlc4|high|low|open|hl2|hlc3|hlcc4|close|
|v_input_6|true|Use trend entry|
|v_input_7|true|Use counter-trend entry|
|v_input_8|2018|From Year|
|v_input_9|2100|To Year|
|v_input_10|true|From Month|
|v_input_11|12|To Month|
|v_input_12|true|From day|
|v_input_13|31|To day|
|v_input_14|true|Show Bollinger Bands|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-11-20 00:00:00
end: 2023-11-27 00:00:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// Noro
// 2018

//@version=3
strategy("Noro's Bollinger Strategy v1.3", shorttitle = "Bollinger str 1.3", overlay = true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100.0, pyramiding = 5)

// Settings
needlong = input(true, defval = true, title = "Long")
needshort = input(true, defval = true, title = "Short")

length = input(20, defval = 20, minval = 1, maxval = 200, title = "Bollinger Length")
mult = input(2.0, defval = 2.0, minval = 1.0, maxval = 5.0, title = "Bollinger Mult")
source = input(close, title = "Bollinger Source")

// Bollinger Bands
bbands = ta.bbands(source, length, mult)

middleband = bbands[0]
upperband = bbands[1]
lowerband = bbands[2]

// Trend Entry
trend_entry = input(true, defval = true, title = "Use trend entry")

// Counter-trend Entry
counter_trend_entry = input(true, defval = true, title = "Use counter-trend entry")

// Entry Conditions
if (trend_entry and needlong)
    long_entry = close > upperband and close[1] <= upperband
    strategy.entry("Long", strategy.long, when = long_entry)

if (counter_trend_entry and needshort)
    short_entry = close < lowerband and close[1] >= lowerband
    strategy.entry("Short", strategy.short, when = short_entry)

// Exit Conditions
exit_long = not ta.crossover(close, middleband)
exit_short = not ta.crossunder(close, middleband)

if (exit_long)
    strategy.close("Long")

if (exit_short)
    strategy.close("Short")
```

This PineScript code implements the Noros-Bollinger-Tracking-Strategy as described.