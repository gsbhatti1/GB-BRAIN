> Name

V-Reversal SMA Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/bd64708e4561311f31.png)
[trans]
## Overview

The V-Reversal SMA strategy calculates the 14-day absolute difference between the highest price and the previous day's lowest price, and the 14-day absolute difference between the lowest price and the previous day's highest price. Then it calculates their 14-day simple moving averages to form the VI+ and VI- curves. A buy signal is generated when VI+ crosses over VI-. A sell signal is generated when VI- crosses below VI+.

## Principle 

The core indicators of this strategy are VI+ and VI-. VI+ reflects bullish momentum while VI- reflects bearish momentum. The specific calculation formulas are as follows:

```
VMP = SUM(ABS(HIGH - LOW[1]),14)  
VMM = SUM(ABS(LOW - HIGH[1]),14)
STR = SUM(ATR(1),14)
VI+ = VMP/STR
VI- = VMM/STR
```

To remove oscillations in the curves, 14-day simple moving averages are calculated on VI+ and VI- to obtain SMA(VI+) and SMA(VI-). A bullish signal is generated when SMA(VI+) crosses over SMA(VI-). A bearish signal is generated when SMA(VI-) crosses below SMA(VI+).

In addition, the strategy also combines the upward and downward status of VI+ and VI- to judge the trend and filter out signals, going long only when the trend is down and going short only when the trend is up.

## Advantage Analysis

By combining trend status and golden/dead cross of the VI indicator, this strategy can effectively filter out false signals and improve profitability. Compared to simple moving average strategies, its breakout signals are more reliable.

## Risk Analysis

The main risks of this strategy are:

1. The VI indicator may generate misleading signals in certain periods. Trend filtering and stop loss should be used to control risks.
2. Markets with high trading costs and slippage are not suitable for this strategy as it would greatly reduce profit margin.

## Optimization Directions

The strategy can be optimized in the following aspects:

1. Optimize the parameters of the VI indicator to find the best parameter combination.
2. Use machine learning methods to automatically identify misleading signals and improve signal quality.
3. Optimize exit mechanisms with stop loss and money management to control single trade loss.
4. Optimize trading products selection focusing on markets with lower trading costs.

## Conclusion

The V-Reversal SMA strategy determines trading signals by calculating the VI+ and VI- indicators and combining trend status. It is a relatively reliable trend following strategy. Its strength lies in high signal quality and ability to filter out noise. But it also faces risks of being trapped, requiring continuous optimizations to adapt to market changes.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|Period|
|v_input_2|14|WMA Length|


> Source (PineScript)

```pinescript
// This script is a backtest for the V-Reversal SMA strategy. The period and WMA length can be adjusted.

//@version=4
//@author=SIDD
strategy(title="V-Reversal SMA Strategy", shorttitle="VRSMA", overlay=true)
period_ = input(14, title="Period", minval=2)
len = input(14, minval=1, title="WMA Length")

// Calculate VI+ and VI-
VMP = sum(abs(high - low[1]), period_) // 14-day absolute difference between current high and previous low
VMM = sum(abs(low - high[1]), period_) // 14-day absolute difference between current low and previous high
STR = sum(atr(1), period_)             // 14-day simple moving average of ATR
VIPlus = VMP / STR                     // VI+
VIMinus = VMM / STR                    // VI-

// Calculate the 14-day WMA for VI+ and VI-
simpleMAVIPlus = wma(VIPlus, len)
simpleMAVIMinus = wma(VIMinus, len)

// Determine buy/sell signals based on crossovers
buySignal = crossover(simpleMAVIPlus, simpleMAVIMinus)
sellSignal = crossunder(simpleMAVIMinus, simpleMAVIPlus)

plotshape(series=buySignal, title="Buy Signal", location=location.belowbar, color=color.lime, style=shape.labelup, text="BUY")
plotshape(series=sellSignal, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

// Optional: Use this for backtesting without the trading interface
//@version=4
//@author=SIDD
study(title="V-Reversal SMA Strategy", shorttitle="VRSMA", overlay=true)
period_ = input(14, title="Period", minval=2)
len = input(14, minval=1, title="WMA Length")

// Calculate VI+ and VI-
VMP = sum(abs(high - low[1]), period_) // 14-day absolute difference between current high and previous low
VMM = sum(abs(low - high[1]), period_) // 14-day absolute difference between current low and previous high
STR = sum(atr(1), period_)             // 14-day simple moving average of ATR
VIPlus = VMP / STR                     // VI+
VIMinus = VMM / STR                    // VI-

// Calculate the 14-day WMA for VI+ and VI-
simpleMAVIPlus = wma(VIPlus, len)
simpleMAVIMinus = wma(VIMinus, len)

// Determine buy/sell signals based on crossovers
buySignal = crossover(simpleMAVIPlus, simpleMAVIMinus)
sellSignal = crossunder(simpleMAVIMinus, simpleMAVIPlus)

plotshape(series=buySignal, title="Buy Signal", location=location.belowbar, color=color.lime, style=shape.labelup, text="BUY")
plotshape(series=sellSignal, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

```