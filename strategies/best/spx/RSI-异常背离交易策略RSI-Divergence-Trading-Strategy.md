> Strategy Name  
RSI Bullish/Bearish Divergence Trading Strategy

### Overview
This strategy identifies regular and hidden bullish/bearish RSI divergence signals to determine long and short positions.

### Principles  
When price makes a new high and RSI fails to make a new high, it forms a bullish divergence, which is treated as a selling signal. When price makes a new low and RSI fails to make a new low, it forms bearish divergence, which is treated as a buying signal. Regular divergence refers to the obvious divergence between price and RSI while hidden divergence means relatively concealed divergence between them. Long or short positions are determined based on identified regular or hidden bullish/bearish divergence signals.

### Advantage Analysis
1. Divergence signals have relatively high reliability with higher winning rate.
2. Identification of both regular and hidden bullish/bearish divergence provides extensive coverage.
3. Adjustable RSI parameters make it adaptable to different market environments.

### Risk Analysis 
1. Hidden divergence signals have a higher probability of misjudgment.
2. Manual review is needed to filter out misjudged signals.
3. Effectiveness depends on RSI parameter settings.

### Optimization Directions  
1. Optimize RSI parameters to find the best parameter combinations.
2. Add machine learning algorithms for automatic identification of true signals.
3. Incorporate more indicators to verify signal reliability.

### Summary  
This strategy identifies RSI divergence trading signals based on regular and hidden bullish/bearish divergence to determine long or short positions, which provides relatively higher winning rate. Further improvements on strategy effectiveness could be achieved by optimizing RSI parameters, adding other validating indicators.

---

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
src = input(title="RSI Source", defval=close)
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
bullCond = plotBull and priceLL and oscHL and plFound // Bullish Divergence Condition
strategy.entry("Bullish Divergence Entry", strategy.long, when = bullCond)
strategy.close("Bullish Divergence Exit", when = ta.crossover(osc, 50)) 
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
	 title="Regular Bullish Label",
	 text="Bull",
	 style=shape.labelup,
	 location=location.absolute,
	 color=bullColor,
	 textcolor=textColor
	 )

//------------------------------------------------------------------------------
// Hidden Bullish
// Osc: Lower Low

oscLL = osc[lbR] < ta.valuewhen(plFound, osc[lbR], 1) and _inRange(plFound[1])

// Price: Higher Low

priceHL = low[lbR] > ta.valuewhen(plFound, low[lbR], 1)
hiddenBullCond = plotHiddenBull and priceHL and oscLL and plFound
strategy.entry("Hidden Bullish Divergence Entry", strategy.long, when = hiddenBullCond)  
```