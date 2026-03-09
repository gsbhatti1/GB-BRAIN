> Name

Multi-timeframe-Trading-Strategy-with-Bollinger-Bands

> Author

ChaoZhang

> Strategy Description

[trans]


## Overview

This strategy is based on adaptive Bollinger Bands and designs two different trailing stop strategies to validate them systematically across multiple timeframes. It belongs to the category of trend-following trading strategies.

## Strategy Logic

1. Calculate the upper and lower bands of adaptive Bollinger Bands with adjustable channel width.
2. Breakout tracking strategy: Open positions when price breaks out of the bands, and stop out when the price reverts back inside the bands.
3. Reversion reversal strategy: Open positions when the price reaches the bands, and stop out when the price reverts back inside the bands.
4. Use CCI indicator to assist in determining long/short sides.
5. Backtest across multiple timeframes to verify the viability of both strategies.

## Advantages

1. Bollinger Bands are intuitive in capturing price trends.
2. The two strategies can adapt to different market conditions, increasing robustness.
3. CCI helps determine long/short direction.
4. Multi-timeframe backtesting makes results more convincing.
5. Simple and clear strategy rules make it easy to implement.

## Risks

1. Bollinger Bands may fail in certain situations.
2. Both strategies carry the risk of premature or delayed stops.
3. CCI may generate incorrect signals.
4. Handle backtest biases carefully.
5. Parameter optimization risks overfitting.

## Enhancement

1. Test different parameters to find optimal combinations.
2. Evaluate adding other indicators for signal filtering.
3. Optimize stop-loss strategies to reduce risk.
4. Research adaptive methods for calculating channel width.
5. Verify with more symbols and timeframes.
6. Use machine learning methods to dynamically optimize parameters.

## Conclusion

This strategy designs two trailing stop strategies based on Bollinger Bands and validates them across multiple timeframes. By refining through parameter optimization, improving stop-loss strategies, etc., it can enhance robustness into a mature trend-following trading system.


[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|75|Length|
|v_input_2_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_3|1.9|Deviation|
|v_input_4|20|Period for CCI|
|v_input_5|false|Test Reverse to the Mean instead|
|v_input_6|true|Enable testing|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-09-13 00:00:00
end: 2023-09-19 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy(title = "Underworld Hunter", overlay=true)

len = input(75, minval=1, title="Length")
src = input(close, title="Source")
basis = 0.0
basis := na(basis[1]) ? sma(src, len) : ema(ema(ema(src,len),len),len)

mult = input(1.9, minval=0.001, maxval=50, title="Deviation")
dev = mult * stdev(src, len)
upper = basis + dev
lower = basis - dev

//CCI calculation and inputs

lengthcci = input(20, minval=1, title="Period for CCI")
ma = sma(close, lengthcci)
ccivalue = (src - ma) / (0.015 * dev(src, lengthcci))

//CCI plotting

cciover0 = ccivalue >= 100 and ccivalue <= 120
cciover1 = ccivalue > 120 and ccivalue <= 140
cciover2 = ccivalue > 140 and ccivalue <= 160
cciover3 = ccivalue > 160 and ccivalue <= 180
cciover4 = ccivalue > 180

cciunder0 = ccivalue <= -100 and ccivalue >= -120
cciunder1 = ccivalue <= -120 and ccivalue > -140
cciunder2 = ccivalue <= -140 and ccivalue > -160
cciunder3 = ccivalue <= -160 and ccivalue > -180
cciunder4 = ccivalue <= -180

plotshape(cciover0, title="CCIO0", location=location.abovebar, color=#c6ff1a, transp=0, style=shape.circle, size=size.tiny)
plotshape(cciunder0, title="CCIU0", location=location.belowbar, color=#c6ff1a, transp=0, style=shape.circle, size=size.tiny)
plotshape(cciover1, title="CCIO1", location=location.abovebar, color=#ffff00, transp=0,style=shape.circle, size=size.tiny)
plotshape(cciunder1, title="CCIU1", location=location.belowbar, color=#ffff00, transp=0, style=shape.circle, size=size.tiny)
plotshape(cciover2, title="CCIO2", location=location.abovebar, color=#ff9900, transp=0, style=shape.circle, size=size.tiny)
plotshape(cciunder2, title="CCIU2", location=location.belowbar, color=#ff9900, transp=0, style=shape.circle, size=size.tiny)
plotshape(cciover3, title="CCIO3", location=location.abovebar, color=#ff0000, transp=0, style=shape.circle, size=size.tiny)
plotshape(cciunder3, title="CCIU3", location=location.belowbar, color=#ff0000, transp=0, style=shape.circle, size=size.tiny)
plotshape(cciover4, title="CCIO4", location=location.abovebar, color=#cc00cc, transp=0,style=shape.circle, size=size.tiny)
plotshape(cciunder4, title="CCIU4", location=location.belowbar, color=#cc00cc, transp=0,style=shape.circle, size=size.tiny)

//plotting

plot(upper, title="Upper shadow", color=color.black, transp = 30, linewidth = 4)
plot(upper, title="Upper line", color=#FF2E00, transp = 0, linewidth = 2)
plot(lower, title="Lower shadow", color=color.black, transp = 30, linewidth = 4)
plot(lower, title="Lower line", color=#FF2E00, transp = 0, linewidth = 2)
plot(basis, title="Basic line", color=color.red, transp = 50, linewidth = 2)

mean = input(title="Test Reverse to the Mean instead", type=input.bool, defval=false)
test = input(title="Enable testing", type=input.bool, defval=true)

orders
```