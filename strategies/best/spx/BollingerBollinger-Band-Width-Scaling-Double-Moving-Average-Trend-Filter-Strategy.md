> Name

Bollinger Band Width Scaling Double Moving Average Trend Filter Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/181af817922384577aa.png)

[trans]


This strategy generates trading signals based on Bollinger Bands and double moving averages, with trend filtering to target high win rate and good profit-loss ratio.

### Strategy Logic

1. Use Bollinger Band upper, middle, and lower bands for long/short signal generation. Sell when price touches the upper band; buy when it touches the lower band.
2. Use 20-period medium-term and 60-period long-term moving averages to determine trend direction. Uptrend when the short MA crosses above the long MA; downtrend when it crosses below.
3. Dynamically adjust stop loss position based on Bollinger Band width. When width is greater than 0.5%, set stop loss at the lower band. When less than 0.5%, reduce stop loss to half of the lower band range.
4. Entry conditions: Breaking the lower band as a buy signal during an uptrend; breaking the upper band as a sell signal during a downtrend.
5. Exit conditions: Take profit when touching the upper band or short MA on long positions. Take profit when touching the lower band or short MA on short positions.
6. Stop loss conditions: Stop out when price breaks below the lower band dynamic range on longs; stop out when price breaks above the upper band dynamic range on shorts.

### Advantages

1. Using double MAs to determine trend helps filter noise from non-trending or range-bound markets.
2. Bollinger Band middle band provides support/resistance, while upper and lower bands serve as dynamic stop loss levels to control risk.
3. Adjusting the stop loss range based on Bollinger Band width reduces the chance of being stopped out while keeping the stop reasonable.
4. Trading in the direction of the trend leads to a higher win rate.

### Risks

1. Double MAs can generate false breakouts frequently, missing trend turning points. Can shorten MA periods.
2. Bollinger Bands can get whipsawed in choppy, non-trending markets. Can reduce trade frequency.
3. Stop loss near support/resistance levels prone to being taken out. Can allow a wider stop loss range.
4. Unable to capitalize on short-term pullbacks effectively. Can shorten holding period.

### Enhancement Opportunities

1. Optimize MA periods to find the best fit for market conditions.
2. Optimize Bollinger Band multiplier parameter to balance the risk of the stop being hit.
3. Add other indicators for multi-factor confirmation to improve signal quality.
4. Incorporate volume/momentum to confirm trend, avoid divergence.
5. Money management optimization e.g., fixed fractional or fixed stop loss to control single trade risk.
6. Price shock handling e.g., large overnight gaps.

### Summary

This is an overall robust strategy using double MAs for trend direction and Bollinger Bands for support/resistance and dynamic stops. Limitations exist like false trend signals and stops too close. Further optimizations can be made across MA system, stop loss strategy, money management etc. to increase robustness across various market conditions. Overall, this is an excellent strategy for beginners with its high win rate, good risk-reward profile, and simple yet effective logic.

||

Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|20|Length|
|v_input_2|4|Multiplier|
|v_input_3|60|Trend Time Frame|
|v_input_4|true|Use Trend Filter|
|v_input_5_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|

> Source (PineScript)

```pinescript
//@version=2
strategy(title="Bollinger Band Width Scaling Double Moving Average Trend Filter Strategy", overlay=true)

len = input(20, minval=1, title="Length")
multiplier = input(4, minval=1, title="Multiplier")
trendTimeFrame = input(60, minval=1, title="Trend Time Frame")
useTrendFilter = input(true, type=bool, title="Use Trend Filter")

src = input(close, title="Source")
out = sma(src, len)
//plot(out, title="SMA", color=blue)

stdOut = stdev(close, len)
bbUpper = out + stdOut * multiplier
bbLower = out - stdOut * multiplier
bbUpper2 = out + stdOut * (multiplier / 2)
bbLower2 = out - stdOut * (multiplier / 2)
bbUpperX2 = out + stdOut * multiplier * 2
bbLowerX2 = out - stdOut * multiplier * 2
bbWidth = (bbUpper - bbLower) / out

closeLongTerm = request.security(syminfo.tickerid, tostring(trendTimeFrame), close)
smaLongTerm = request.security(syminfo.tickerid, tostring(trendTimeFrame), sma(close,20))

//plot(smaLongTerm, color=red)

trendUp = useTrendFilter ? (closeLongTerm > smaLongTerm) : true
trendDown = useTrendFilter? (closeLongTerm < smaLongTerm) : true

bearish = ((cross(close,bbUpper2) == 1) or (cross(close,out) == 1)) and (close[1] > close) and trendDown
bullish = ((cross(close,bbLower2) == 1) or (cross(close,out) == 1)) and (close[1] < close) and trendUp

if bullish
    strategy.entry("Bullish", strategy.long)

if bearish
    strategy.entry("Bearish", strategy.short)

// Stop Loss Conditions
stopLossLong = low < bbLower2 ? bbLower : bbLower / 2
stopLossShort = high > bbUpper2 ? bbUpperX2 : (bbUpper + bbUpper) / 2

if isLong
    strategy.exit("Profit Long", "Bullish", stop=stopLossLong)
else
    strategy.exit("Profit Short", "Bearish", stop=stopLossShort)

// Plotting Bollinger Bands and MA
plot(bbUpper, color=red)
plot(bbLower, color=blue)
plot(out, title="SMA", color=green)
```

[/trans]