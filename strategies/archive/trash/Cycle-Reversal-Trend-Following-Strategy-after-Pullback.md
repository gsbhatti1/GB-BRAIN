> Name

Cycle-Reversal-Trend-Following-Strategy-after-Pullback

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/c760c51271c87b663f.png)
[trans]

## Overview

This strategy combines two indicators: moving average reversal and price detrend oscillator to generate trading signals and catch the rebound trend after cycle reversals.

## Principles 

This strategy mainly utilizes the following two technical indicators for trading signal judgment:

1. Moving Average Reversal

    It calculates the price uptrend or downtrend in the past two days combined with the fast line K value to determine if a reversal signal occurs. When the price keeps rising in the past two days and the fast line K value is lower than the slow line K value, a buy signal is generated. When the price keeps falling in the past two days and the fast line K value is higher than the slow line K value, a sell signal is generated.

2. Price Detrend Oscillator

    The Detrend Price Oscillator draws a horizontal moving average line and identifies price cycles based on the relationship between the price and the line. It filters out trends longer than the calculation period, thus revealing hidden short-term fluctuations. When the price is above the moving average line, it is a buy signal. When the price is below the line, it is a sell signal.

This strategy combines the signals of the two indicators. That is, when a moving average reversal signal appears and the price detrend oscillator also gives a confirming reversal signal, a trading order is generated. This can filter out some invalid reversal signals and catch the rebound trend after reversals.

## Advantages

The biggest advantage of this strategy is that it makes good use of the strengths of the two indicators for complementary confirmation, which can effectively filter out invalid signals and increase signal reliability.

The moving average reversal indicator itself tends to generate false signals. Relying solely on it for judgments tends to chase tops and hit bottoms. The introduction of the price detrend oscillator for combination can avoid reversal operations in non-ideal oscillation zones. 

The parameter settings of the price detrend oscillator also determine that it only identifies short-term fluctuations, which matches very well with the judgment of the moving average reversal and can identify reasonable reversal timing.

## Risks

The main risks of this strategy include:

1. Insufficient rebound momentum, tends to be trapped

Moving average reversals tend to occur in sideways ranges. If the rebound momentum is insufficient, it is likely to callback and touch the stop loss again, failing to profit.

2. Improper parameter settings  

If the parameters of the price detrend oscillator are set too large, it will identify medium- and long-term trends; if too small, it will increase misjudgment risks. Parameters need to be carefully tested for different products.

3. Reversal failures due to sudden events

Major news events can disrupt existing trend judgments, resulting in failure of reversal signals. It is necessary to pay attention to fundamentals and avoid trading blindly when news events occur.

## Optimization Directions

The strategy can be further optimized in the following aspects:

1. Add stop loss mechanisms

Reasonably set stop loss or time stop loss to control single loss.

2. Combine with volume indicators

Add volume confirmation, such as issuing signals only when breaking through the average volume, to avoid ineffective breakthroughs due to insufficient momentum.

3. Dynamic parameter optimization

Dynamically optimize parameters according to market conditions, relax parameters appropriately during obvious trends, and tighten parameters during consolidations.

4. Use machine learning methods for dynamic optimization

Use machine learning methods like random forest to evaluate and select parameter combinations to achieve dynamic intelligent optimization.

## Summary

This strategy combines the strengths of two indicators reasonably to catch the rebound trend at reversal points. Although problems like being trapped and parameter optimization remain, the overall idea is clear and logical. It is worth further testing and optimization to achieve stable profits.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|Length|
|v_input_2|true|KSmoothing|
|v_input_3|3|DLength|
|v_input_4|50|Level|
|v_input_5|14|LengthDPO|
|v_input_6|false|Trade reverse|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-10-15 00:00:00
end: 2023-11-14 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/
```