> Name

Bugra-Trading-Strategy-Based-on-Dual-Kinetic-Moving-Average

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1bdba9db7874729a2db.png)
[trans]
## Overview

The Dual Kinetic Moving Average trading strategy is a strategy that combines the OTT indicator and the Wavetrend Oscillator indicator. It integrates the OTT indicator developed by teacher Anıl Özekşi and the Wavetrend Oscillator indicator by lonestar108, forming a successful trading indicator. The strategy can perform long and short trading in two-way markets.

## Strategy Principle 

The Dual Kinetic Moving Average trading strategy first calculates the midline of Bollinger Bands, which is the moving average line MAvg. Then, based on the percentage range and period set by the user, it calculates the long stop loss longStop and the short stop loss shortStop. When the price breaks through the upper rail, go long. When it breaks through the lower rail, go short. The closing signal is when the price returns to around the moving average.

Specifically, the core indicator of this strategy is the OTT indicator. The OTT indicator consists of a moving average and boundary lines. It adjusts the position of the boundary lines according to the volatility of the market based on certain algorithms. When the price breaks through the lower boundary line OTT, go short. When it breaks through the upper boundary line OTT, go long.

This strategy also uses the Wavetrend indicator to determine the direction of the price trend. If it is judged to be a downward trend, only go short, not long. If it is judged to be an upward trend, only go long, not short.

## Advantage Analysis

The Dual Kinetic Moving Average trading strategy combines the advantages of moving averages, Bollinger Bands, and OTT indicators. It can automatically adjust stop loss positions, reducing the probability of stop loss being triggered. At the same time, by incorporating trend judgment indicators, it avoids being trapped in oscillating trends.

Specifically, the main advantages of this strategy are:

1. It can automatically adjust stop loss positions, effectively controlling risks.
2. The OTT indicator can relatively accurately determine reversal points.
3. By incorporating trend judgment indicators, it avoids being trapped in oscillating markets.
4. Its rules are relatively simple and clear, easy to understand and apply.

## Risk Analysis

The Dual Kinetic Moving Average trading strategy also has some risks, mainly in the following aspects:

1. In violent market conditions, stop loss may be broken, causing greater losses.
2. The reversal signals judged by the OTT indicator may not be accurate, and faulty signals may occur.
3. Trend judgments can also be wrong. Going long in an downward oscillation will cause losses.
4. Improper parameter settings will also affect strategy performance.

The countermeasures are mainly:

1. Appropriately loosen the stop loss range to ensure that stop loss lines are not easily activated.
2. Combine with other indicators to judge the reliability of OTT signals to avoid false signals.
3. Appropriately adjust parameters to make trend judgments more reliable.
4. Optimize parameters to find the best parameter combination.

## Optimization Directions

There is still room for further optimization of the dual kinetic moving average trading strategy:

1. Consider combining with other indicators to improve the accuracy of signal judgment.
2. Study adaptive stop loss algorithms so that stop loss lines can be adjusted according to market volatility.
3. Add trading volume indicators to avoid false breakouts with low volume.
4. Test different types of moving averages to find the most suitable moving average.
5. Try machine learning and other methods to automatically optimize parameters.

## Summary

The dual kinetic moving average trading strategy integrates the advantages of multiple indicators. It can automatically adjust stop loss positions, judge reversal signals, and identify trend directions. It has advantages such as strong risk control capabilities and easy to understand and use. But it also has risks like being trapped and inaccurate signals. This strategy can be further optimized by combining with other indicators, studying adaptive algorithms, etc. In general, the dual kinetic moving average trading strategy is a practical breakout trading strategy.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|5|Period|
|v_input_2|true|Magical Percentage|
|v_input_3|0|Moving Average Type: VAR|EMA|WMA|TMA|SMA|WWMA|ZLEMA|TSF|
|v_input_4|10|Channel Period|
|v_input_5|21|Average Length|
|v_input_6|20200101|Start Date (YYYYMMDD)|
|v_input_7|20201231|End Date (YYYYMMDD)|


> Source (PineScript)

```pinescript
//@version=5
indicator("Bugra Trading Strategy - Dual Kinetic Moving Average", overlay=true)
period = input.int(5, title="Period")
magical_percentage = input.bool(true, title="Magical Percentage")
moving_average_type = input.string("VAR", title="Moving Average Type", options=["VAR", "EMA", "WMA", "TMA", "SMA", "WWMA", "ZLEMA", "TSF"])
channel_period = input.int(10, title="Channel Period")
average_length = input.int(21, title="Average Length")
start_date = input.int(20200101, title="Start Date (YYYYMMDD)")
end_date = input.int(20201231, title="End Date (YYYYMMDD)")

// Calculate Bollinger Bands midline (MAvg)
bb = ta.sma(close, average_length)

// Calculate long and short stop losses
long_stop = bb - (bb * 0.01)  // 1% below midline
short_stop = bb + (bb * 0.01)  // 1% above midline

// Determine trend using Wavetrend
wv = ta.wv(close, channel_period, 0)

if (wv < 0)
    strategy.entry("Short", strategy.short)
else
    strategy.entry("Long", strategy.long)

// Close position when price returns to around MAvg
if (close > bb - (bb * 0.005) and close < bb + (bb * 0.005))
    strategy.close("Long")
    strategy.close("Short")

// Plot Bollinger Bands and stop loss levels
plot(bb, color=color.blue, title="Bollinger Bands Midline (MAvg)")
plot(long_stop, color=color.red, title="Long Stop Loss")
plot(short_stop, color=color.green, title="Short Stop Loss")
```