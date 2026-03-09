> Name

RSI Divergence Trading Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/207f2040e5d0e5104ed.png)
[trans]

## Overview
The RSI Divergence Trading Strategy captures mispricing opportunities by analyzing the divergence between the RSI indicator and price. It goes long or short when the divergence appears.

## Strategy Logic  
The strategy is based on value-price divergence when the RSI diverges from the price. The RSI reflects strength while price reflects supply-demand dynamics. When these two indicators diverge, it indicates market mispricing for arbitrage purposes.

Specifically, a regular bullish divergence happens when RSI forms a higher low while price prints a lower low. This shows that although the market looks weak on the surface, it is actually gathering strength internally for a bounce. When RSI diverges from price and breaks above the 50-line, it presents an opportunity to catch the bounce.

A regular bearish divergence happens when RSI makes a lower high while price forms a higher high. This suggests that although the market looks strong externally, it is showing weakness signals internally. When RSI diverges from price and breaks below the 50-line, it allows profiting from the short side.

There are also hidden bullish and bearish divergences where the relationship between RSI and price is opposite of regular divergences, but the logic remains the same for taking profits.

## Advantages
1. Captures market mispricing from value-price divergence  
2. Improves win rate combining indicator and price divergence  
3. Covers more opportunities distinguishing all types of divergences

## Risk Analysis   
1. Fake divergences can happen under special market conditions  
2. Breaking 50-line has relatively low success rate, can optimize
3. Picking wrong direction could lead to big losses

## Optimization Directions
1. Optimize RSI parameters for higher accuracy
2. Combine signals from other indicators to confirm divergences
3. Assess risk-reward for longs and shorts to control per trade loss

## Summary
The RSI Divergence Strategy arbitrages market mispricing through analyzing divergence between value and price signals. Its advantage lies in timely catching trend reversal opportunities, while its risk comes from the accuracy of divergence recognition. With continuous optimization, steady gains can be achieved in live trading.
[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_int_1|14|RSI Period|
|v_input_1_close|0|RSI Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|5|Pivot Lookback Right|
|v_input_3|5|Pivot Lookback Left|
|v_input_4|60|Max of Lookback Range|
|v_input_5|5|Min of Lookback Range|
|v_input_6|true|Plot Bullish|
|v_input_7|true|Plot Hidden Bullish|
|v_input_8|true|Plot Bearish|
|v_input_9|true|Plot Hidden Bearish|


> Source (PineScript)

```pinescript
//@version=5
strategy(title="Divergence Indicator")
len = input.int(title="RSI Period", minval=1, defval=14)
src = input(title="RSI Source", defval="close")
lbR = input(title="Pivot Lookback Right", defval=5)
lbL = input(title="Pivot Lookback Left", defval=5)
rangeUpper = input(title="Max of Lookback Range", defval=60)
rangeLower = input(title="Min of Lookback Range", defval=5)
plotBull = input(title="Plot Bullish", defval=true)
plotHiddenBull = input(title="Plot Hidden Bullish", defval=true)
plotBear = input(title="Plot Bearish", defval=true)
plotHiddenBear = input(title="Plot Hidden Bearish", defval=true)
bearColor = color.red
bullColor = color.green
hiddenBullColor = color.new(color.green, 80)
hiddenBearColor = color.new(color.red, 80)
textColor = color.white
noneColor = color.new(color.white, 100)
osc = ta.rsi(src, len)

plot(osc, title="RSI", linewidth=2, color=#2962FF)
hline(50, title="Middle Line", color=#787B86, linestyle=hline.style_dotted)
obLevel = hline(70, title="Overbought", color=#787B86, linestyle=hline.style_dotted)
osLevel = hline(30, title="Oversold", color=#787B86, linestyle=hline.style_dotted)
fill(obLevel, osLevel, title="Background", color=color.rgb(33, 150, 243, 90))

plFound = na(ta.pivotlow(osc, lbL, lbR)) ? false : true
phFound = na(ta.pivothigh(osc, lbL, lbR)) ? false : true
_inRange(cond) =>
	bars = ta.barssince(cond == true)
	rangeLower <= bars and bars <= rangeUpper

//------------------------------------------------------------------------------
// Regular Bullish
// Osc: Higher Low

oscHL = osc[lbR] > ta.valuewhen(plFound, osc[lbR], 1) and _inRange(plFound[1])

// Price: Lower Low

priceLL = low[lbR] < ta.valuewhen(plFound, low[lbR], 1)
bullCond = plotBull and priceLL and oscHL and plFound // Bullish Divergence?
strategy.entry("Bullish Divergence Entry", strategy.long, when=bullCond)
strategy.close("Bullish Divergence Exit", when=ta.crossover(osc, 50)) 
plot(
    plFound ? osc[lbR] : na,
    offset=-lbR,
    title="Regular Bullish",
    linewidth=2,
    color=(bullCond ? bullColor : noneColor)
)

plotshape(
    bullCond ? osc[lbR] : na,
    offset=-lbR,
    title="Regular Bullish Plot",
    style=shape.triangleup,
    location=location.belowbar,
    size=size.small
)
```