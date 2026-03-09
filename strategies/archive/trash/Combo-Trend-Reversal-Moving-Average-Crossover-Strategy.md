> Name

Dual Trend Reversal Moving Average Combo Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/15a9804b4e882693d9a.png)

[trans]

## Overview

This is a dual trend reversal moving average combo strategy. It combines the 123 Reversal strategy and Bill Williams Average Line strategy to generate more accurate trading signals by using signals from both strategies.

## Strategy Logic

The strategy consists of two parts:

1. **123 Reversal Strategy**: Go long when close price rises for 2 consecutive days and 9-day slow stochastic is below 50; Go short when close price falls for 2 consecutive days and 9-day fast stochastic is above 50.
   
2. **Bill Williams Average Line Strategy**: Calculate the median prices for 13, 8, and 5 day moving averages. Go long when the shorter term moving average crosses above the longer term moving average; go short when the shorter term moving average crosses below the longer term moving average.

Finally, a trade is only executed if both strategies agree on the direction; otherwise, no trade is made.

## Advantage Analysis

The strategy combines dual trend validations to reduce false signals and improve signal accuracy. Additionally, the use of moving averages can filter out some noise.

## Risk Analysis

Risks include:

1. Dual filtering may miss some good trading opportunities.
2. Incorrectly set moving average parameters may misjudge market trends.
3. The reversal strategies themselves have inherent risk of loss.

These risks can be reduced by optimizing moving average parameters or refining the entry and exit logic.

## Optimization Directions

The strategy can be optimized in several ways:

1. Test different combinations of moving averages to find optimal parameters.
2. Add stop-loss strategies to limit potential losses.
3. Incorporate volume indicators to identify signal quality.
4. Use machine learning methods to automatically optimize parameters.

## Conclusion

This strategy integrates dual trend validations and moving average indicators to effectively filter noise and improve trading decision accuracy. However, it also carries certain risks that require continuous testing and optimization of the entry and exit logic to achieve stable profitability in real trading scenarios.

||

## Overview

This is a combo strategy that combines trend reversal and moving average crossover strategies to generate more accurate trading signals.

## Strategy Logic

The strategy consists of two parts:

1. **123 Reversal Strategy**: Go long when close price rises for 2 consecutive days and 9-day slow stochastic is below 50; Go short when close price falls for 2 consecutive days and 9-day fast stochastic is above 50.

2. **Bill Williams Average Line Strategy**: Calculate the median prices for 13, 8, and 5 day moving averages. Go long when the shorter term moving average crosses above the longer term moving average; go short when the shorter term moving average crosses below the longer term moving average.

Finally, a trade is only executed if both strategies agree on the direction; otherwise, no trade is made.

## Advantage Analysis

The strategy combines dual trend validations to reduce false signals and improve signal accuracy. Additionally, the use of moving averages can filter out some noise.

## Risk Analysis

Risks include:

1. Dual filtering may miss some good trading opportunities.
2. Incorrectly set moving average parameters may misjudge market trends.
3. The reversal strategies themselves have inherent risk of loss.

These risks can be reduced by optimizing moving average parameters or refining the entry and exit logic.

## Optimization Directions

The strategy can be optimized in several ways:

1. Test different combinations of moving averages to find optimal parameters.
2. Add stop-loss strategies to limit potential losses.
3. Incorporate volume indicators to identify signal quality.
4. Use machine learning methods to automatically optimize parameters.

## Conclusion

This strategy integrates dual trend validations and moving average indicators to effectively filter noise and improve trading decision accuracy. However, it also carries certain risks that require continuous testing and optimization of the entry and exit logic to achieve stable profitability in real trading scenarios.

||

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|14|Length|
|v_input_2|true|KSmoothing|
|v_input_3|3|DLength|
|v_input_4|50|Level|
|v_input_5|13|LLength|
|v_input_6|8|MLength|
|v_input_7|5|SLength|
|v_input_8|8|LOffset|
|v_input_9|5|MOffset|
|v_input_10|3|SOffset|
|v_input_11|false|Trade reverse|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-10-28 00:00:00
end: 2023-11-27 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 18/06/2019
// This is a combo strategy for getting 
// a cumulative signal. A result signal will return 1 if both strategies 
// are long, -1 if all strategies are short and 0 if signals of the strategies are not equal.
//
// First Strategy:
// This System was created from the Book "How I Tripled My Money In The 
// Futures Market" by Ulf Jensen, Page 183. This is a reverse type of strategy.
// The strategy buys at market price, if close price is higher than the previous close 
// for two consecutive days and the meaning of 9-days Stochastic Slow Oscillator is lower than 50. 
// The strategy sells at market price, if close price is lower than the previous close 
// for two consecutive days and the meaning of 9-days Stochastic Fast Oscillator is higher than 50.
//
// Second Strategy:
// This indicator calculates three moving averages with default values of
// 13, 8 and 5 days, with displacements 8, 5 and 3 days: Median Price (High+Low/2).
// The most popular method of interpreting a moving average is to compare 
// the relationship between a moving average of the security's price with 
// the security's price itself (or between several moving averages).
//
// WARNING:
// - For educational purpose only
// - This script changes bar colors.
////////////////////////////////////////////////////////////
Reversal123(Length, KSmoothing, DLength, Level) =>
    vFast = sma(stoch(close, high, low, Length), KSmoothing) 
    vSlow = sma(vFast, DLength)
    pos = 0.0
    pos := iff(close[2] < close[1] and close > close[1] and vFast < vSlow and vFast > Level, 1,
              iff(close[2] > close[1] and close < close[1] and vFast > vSlow and vFast < Level, -1, nz(pos[1], 0))) 
    pos

BillWilliamsAverages(LLength, MLength, SLength, LOffset, MOffset, SOffset ) =>
    xLSma = sma(hl2, LLength)[LOffset]
    xMSma = sma(hl2, MLength)[MOffset]
    xSSma = sma(hl2, SLength)[SOffset]
    pos = 0
    pos := iff(close < xSSma and xSSma < xMSma and xMSma < xLSma, -1,
              iff(close > xSSma and xSSma > xMSma and xMSma > xLSma, 1, nz(pos[1], 0))) 
    pos

strategy(title="Dual Trend Reversal Moving Average Combo Strategy", shorttitle="Combo", overlay = true)
Length = input(14, minval=1)
KSmoothing = input(1, minval=1)
DLength = input(3, minval=1)
Level = input(50, minval=1)
//-------------------------
LLength = input(13, minval=1)
MLength = input(8,minval=1)
SLength = input(5,minval=1)
LOffset = input(8,minval=1)
MOffset = input(5,minval=1)
SOffset = input(3,minval=1)
reverse = input(false, title="Trade reverse")
posReversal123 = Reversal123(Length, KSmoothing, DLength, Level)
posBillWilliamsAverages = BillWilliamsAverages(LLength, MLength,SLength, LOffset, MOffset, SOffset)
pos = iff(posReversal123 == 1 and posBillWilliamsAverages == 1 , 1,
         iff(posReversal123 == -1 and posBillWilliamsAverages == -1, -1, 0))
```