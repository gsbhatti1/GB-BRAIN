> Name

Ichimoku Cloud Trading Strategy

> Author

ChaoZhang

> Strategy Description

## Overview

This strategy implements simple trend-following trading based on the ichimoku cloud indicator on daily charts. It generates buy and sell signals by calculating the conversion line, base line, leading span 1, and leading span 2, and then combining the current closing price's position relative to the cloud. When the closing price is above the cloud, it is considered an upward trend, and a buy signal is generated. When the closing price is below the cloud, it is considered a downward trend, and a sell signal is generated.

## Strategy Logic

The strategy mainly calculates the five lines of the ichimoku cloud indicator based on the following formulas:

1. Conversion Line: 9-period average of the highest high and lowest low
2. Base Line: 26-period average of the highest high and lowest low
3. Leading Span 1: average of the conversion line and base line
4. Leading Span 2: 52-period average of the highest high and lowest low
5. Lagging Span: closing price plotted 26 periods behind

When the closing price is above the cloud, it is considered an upward trend and a buy signal is generated. When the closing price is below the cloud, it is considered a downward trend and a sell signal is generated.

Specifically, the strategy implements this logic through the following steps:

1. Calculate the conversion line, base line, leading span 1, and leading span 2
2. Plot the lagging span of the closing price 26 periods behind
3. Check if the closing price is above the cloud (leading span 1 and 2), generate buy signal if true
4. Check if the closing price is below the cloud, generate sell signal if true
5. Enter trades on buy/sell signals based on strategy settings

## Advantage Analysis

The main advantages of this strategy are:

1. Using the ichimoku cloud can effectively identify trends and generate signals along the trend direction, avoiding unnecessary trades in range-bound markets.
2. The calculation parameters are optimized for daily trading.
3. Using both leading span 1 and 2 combines multiple signals to filter out false signals.
4. The lagging span delay helps reduce risk of immediate pullback after cloud breakout.
5. Simple and clear logic, easy to understand and implement.
6. No other indicators needed, complete trend following system.

## Risk Analysis

There are some risks to consider:

1. The cloud may fail in certain market conditions, generating incorrect signals.
2. If parameters are not adapted to changing market dynamics, it weakens the system.
3. The fixed lagging span delay may miss some opportunities.
4. Still cannot completely avoid whipsaws.
5. There is some time lag, unable to capture quick reversals.
6. Cannot differentiate major trends vs shorter corrections, may cause losses.

## Improvement Areas

Some ways to improve the strategy:

1. Optimize parameters like conversion line for different market conditions.
2. Add trend filtering indicators to confirm strength and direction.
3. Implement stop loss and take profit to control loss per trade.
4. Only take cloud breakout signals with high volume.
5. Use different parameter sets based on market regime.
6. Add machine learning to auto-optimize parameters.
7. Consider dynamic lagging span instead of fixed delay.

## Summary

Overall, this ichimoku cloud strategy implements basic trend following rules, although improvements can be made. The core logic is sound, parameters optimized, good baseline algo trading strategy. With further cloud parameter enhancement, adding filters and risk controls, it can become a very practical quantitative trading system.

|Argument|Default|Description|
|----|----|----|
|v_input_1|9|Conversion Line Periods|
|v_input_2|26|Base Line Periods|
|v_input_3|52|Lagging Span 2 Periods|
|v_input_4|26|Displacement|


> Source (PineScript)

```pinescript
//@version=4
strategy(title="Ichimoku Cloud", shorttitle="Ichimoku", overlay=true, commission_type=strategy.commission.percent, commission_value=0.075, initial_capital=1000, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

conversionPeriods = input(9, minval=1, title="Conversion Line Periods")
basePeriods = input(26, minval=1, title="Base Line Periods")
laggingSpan2Periods = input(52, minval=1, title="Lagging Span 2 Periods")
displacement = input(26, minval=0, title="Displacement")

plotshape(series=cross(close, hline(0.5)), title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")
plotshape(series=close < hline(0.5), title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

// Conversion Line
conversionLine = ta.sma(high, conversionPeriods) + ta.sma(low, conversionPeriods) / 2

// Base Line
baseLine = ta.sma(high, basePeriods) + ta.sma(low, basePeriods) / 2

// Leading Span 1
leadingSpan1 = (conversionLine + baseLine) / 2

// Leading Span 2
leadingSpan2 = ta.sma(high, laggingSpan2Periods) + ta.sma(low, laggingSpan2Periods) / 2

// Lagging Span
laggingSpan = close[displacement]

// Plot the cloud
plot(conversionLine, color=color.blue, title="Conversion Line")
plot(baseLine, color=color.red, title="Base Line")
plot(leadingSpan1, color=color.blue, title="Leading Span 1")
plot(leadingSpan2, color=color.red, title="Leading Span 2")
plot(laggingSpan, color=color.orange, title="Lagging Span", style=plot.style_circles)
```