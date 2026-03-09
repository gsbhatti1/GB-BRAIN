> Name

Momentum-Breakout-Bi-directional-Tracking-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/207f8a2245b24b751e7.png)
 [trans]

## Overview

This strategy combines the use of momentum indicators and bi-directional tracking indicators to capture breakout signals in strong trends for trend tracking. When prices break out upwards, it goes long; when prices break out downwards, it goes short. It falls into the category of trend tracking strategies.

## Strategy Logic

1. The HiLo Activator indicator calculates the midpoint price using the midpoint of the highest high and lowest low. When prices break out above the midpoint, a buy signal is generated. When prices break down below the midpoint, a sell signal is generated.

2. The Average Directional Index (ADX) is used to gauge the strength of the trend. The higher the ADX value, the stronger the trend. This strategy uses ADX with a threshold to filter signals, only generating signals when the trend is strong enough.

3. The Directional Indicators DI+ and DI- represent the strength of the uptrend and downtrend, respectively. This strategy also uses DI+ and DI- thresholds to confirm the strength and avoid wrong signals.

4. Buy signals are generated when prices break out above the midpoint, ADX is higher than the threshold, and DI+ is higher than the threshold. Sell signals are generated when prices break down below the midpoint, ADX is higher than the threshold, and DI- is higher than the threshold.

## Advantage Analysis

This strategy combines the advantages of momentum and trend-following indicators to capture early breakouts and follow trends closely. The strict trend filter conditions also help avoid wrong signals in consolidation and ranging periods.

Compared to using momentum indicators alone, this strategy adds trend strength evaluation to filter signals and improve profitability. Compared to pure trend-following strategies, this strategy can enter trends earlier through breakout signals.

Overall, the strategy can track trends smoothly, enter and exit timely, and avoid being stuck in consolidations while also reducing losses from trend reversals.

## Risk Analysis

This strategy has some whipsaw risks from temporary price reversals generating wrong signals. Also, using ADX and DI thresholds may cause missing some early opportunities.

To reduce whipsaw risks, tweak the HiLo Activator parameters to increase the breakout range. To capture more opportunities, lower the ADX and DI thresholds at the expense of signal quality.

Users should also note differences across products and market environments. Higher thresholds generally work better for commodities while lower thresholds suit stocks and forex.

## Optimization Directions

The main ways to optimize this strategy include:

1. Adjust the HiLo Activator period and trigger levels to balance whipsaw risks and timing.
2. Tweak ADX period and threshold to balance signal quality and frequency.
3. Set separate thresholds for DI+ and DI- to accommodate differences between uptrends and downtrends.
4. Add stop loss strategies with stop loss levels to control single trade loss.
5. Combine with other auxiliary indicators to improve overall stability.

## Conclusion

This strategy considers both momentum and trend-following indicators to generate signals during strong trends. It has the advantage of following trends smoothly and closely, suitable for capturing early trend opportunities. It also has reasonable risk control abilities to reduce losses from wrong signals and whipsaws. With parameter tuning and stop loss additions, it can achieve steady performance. As a versatile trend tracking strategy fitting different products and markets, it deserves good attention and application from quant traders.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|HiLo Activator Period|
|v_input_2|false|Offset|
|v_input_3|true|Trigger for Buy/Sell|
|v_input_4|14|ADX Period|
|v_input_5|25|ADX Threshold|
|v_input_6|50|DI Threshold|
|v_input_7|1000|Number of Candles for Backtest|


> Source (PineScript)

```pinescript
//@version=4
strategy("HiLo Activator with ADX", shorttitle="HASB_ADX", overlay=true)

// Parameters for the HiLo Activator
length_ha = input(14, title="HiLo Activator Period")
offset_ha = input(0, title="Offset")
trigger_ha = input(1, title="Trigger for Buy/Sell")

// Parameters for ADX
adx_length = input(14, title="ADX Period", minval=1)
adx_threshold = input(25, title="ADX Threshold", minval=1)
di_threshold = input(50, title="DI Threshold", minval=1)

// Calculate HiLo Activator
ha_high = highest(high, length_ha) + offset_ha
ha_low = lowest(low, length_ha) - offset_ha
ha_close = (ha_high + ha_low) / 2

// Generate signals based on HiLo Activator and ADX
if (close > ha_high and adx > adx_threshold and di_pos > di_threshold)
    strategy.entry("Buy", strategy.long)
if (close < ha_low and adx > adx_threshold and di_neg > di_threshold)
    strategy.entry("Sell", strategy.short)

// Plotting
plot(ha_high, color=color.red, linewidth=2, title="HiLo Activator High")
plot(ha_low, color=color.green, linewidth=2, title="HiLo Activator Low")
plot(adx, color=color.blue, linewidth=2, title="ADX")
plot(di_pos, color=color.orange, linewidth=2, title="DI+")
plot(di_neg, color=color.purple, linewidth=2, title="DI-")
```