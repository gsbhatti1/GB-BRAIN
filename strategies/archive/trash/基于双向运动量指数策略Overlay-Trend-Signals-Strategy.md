> Name

Overlay-Trend-Signals-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/15ddca237f70ec00059.png)
[trans]
### Overview

This strategy generates trading signals by calculating the Directional Movement Indexes (DMI) DI+ and DI- along with the Average Directional Index (ADX) and Exponential Moving Average (EMA). It triggers a long signal when DI+ crosses above DI- and ADX is above 20. A short signal is triggered when DI- crosses below DI+ and ADX is above 25. The stop loss signal is when DI- crosses above DI+ with ADX above 30.

### Strategy Logic

1. Calculate DI+, DI-, ADX
    - Use `ta.dmi()` to compute DI+, DI-, ADX
    - DI+/DI- measures directional price movement 
    - ADX measures strength of price movement

2. Calculate Exponential Moving Average 
    - Use custom `my_ema()` function to compute EMA
    - EMA smoothes price data  

3. Generate trading signals
    - Long signal: DI+ crosses above DI- and ADX > 20 and close > EMA
        - Indicates upward trend and increased volatility  
    - Short signal: DI- crosses below DI+ and ADX > 25 and close < EMA
        - Indicates downward trend and high volatility

4. Set stop loss
    - Long stop loss: DI- crosses above DI+ and ADX > 30 
        - Indicates trend reversal  
    - Short stop loss: DI+ crosses below DI- and ADX > 30
        - Indicates trend reversal  

In summary, this strategy combines momentum and trend analysis indicators to trade when strong price trends emerge, with stop losses to limit losses.  

### Advantage Analysis

1. Dual DI avoids false signals  
    - Single DI can give false signals, dual DI ensures trend  
2. ADX threshold requires increased volatility 
    - Only trades high volatility moves, avoids ranging  
3. EMA complements DI
    - EMA identifies mid/long term trends
4. Strict stop loss  
    - Cuts losses quickly  

### Risk Analysis

1. Frequent stop loss
    - Volatile swings may trigger frequent stops
2. Parameter dependence
    - Optimal DI and ADX parameters need to be found
3. Low trade frequency
    - Strict rules reduce trades

Can optimize by expanding stop loss, tuning parameters, adding filters to increase frequency.  

### Optimization Opportunities

1. Parameter optimization 
    - Optimize DI and ADX parameters  
2. Add filters 
    - Volume, divergence etc.
3. Widen stop loss
    - Relax stops to reduce frequency  

### Conclusion

This strategy combines momentum and trend analysis indicators to trade strong trends, with strict stops to control risk. Can further improve performance through parameter optimization, additional filters, and relaxed stops.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|14|DI Length|
|v_input_int_2|14|ADX Smoothing|
|v_input_int_3|26|EMA Length|
|v_input_source_1_close|0|EMA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_bool_1|true|Signal Labels|


> Source (PineScript)

```pinescript
//@version=5
strategy("Overlay Signals by TFOT", overlay=true)

// Calculate DMI
len = input.int(14, minval=1, title="DI Length")
lensig = input.int(14, title="ADX Smoothing", minval=1, maxval=50)
[diplus, diminus, adx] = ta.dmi(len, lensig)

// Get EMA
emalen = input.int(26, minval=1, title = "EMA Length")
emasrc = input.source(close, title = "EMA Source")

my_ema(src, length) =>
    alpha = 2 / (length + 1)
    sum = 0.0
    sum := na(sum[1]) ? src : alpha * src + (1 - alpha) * nz(sum[1])
EMA2 = my_ema(emasrc, emalen)

// Variables
var bool buycondition1 = false
var bool sellcondition1 = false

var int firstbuybar = na
var int firstsellbar = na

var int buyexitbar = na
var int sellexitbar = na

var bool buyexit1 = false
var bool sellexit1 = false

// Buy & Sell Conditions
buycondition1 := (ta.crossover(diplus, diminus)) and (adx > 20) and (close > EMA2) and na(firstbuybar)
sellcondition1 := (ta.crossover(diminus, diplus)) and (adx > 25) and (close < EMA2) and na(firstsellbar)

buyexit1 := ta.crossover(diminus, diplus) and (adx > 30) and na(buyexitbar)
sellexit1 := ta.crossover(diplus, diminus) and (adx > 30) and na(sellexitbar)

if buycondition1
    if(na(firstbuybar))
        firstbuybar := bar_index
        buyexitbar := na
        firstsellbar := na
        strategy.entry("Buy", strategy.long)

if sellcondition1
    if(na(firstsellbar))
        firstsellbar := bar_index
        sellexitbar := na
        firstbuybar := na
        strategy.entry("Sell", strategy.short)
```