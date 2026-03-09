---

> Name

Reversal-Trend-Catching-and-Dynamic-Stop-Loss-Combo-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/112686506afc4b86b82.png)
[trans]
## Overview
This strategy combines a reversal trend catching strategy and a dynamic stop loss strategy to capture price reversals while controlling risks through dynamically adjusted stop losses.

## Strategy Logic  
### Reversal Trend Catching Strategy
The strategy is based on the K and D values of the Stochastic Oscillator. It generates buy signals when prices fall for two consecutive days, and the K value rises above the D value. Conversely, it generates sell signals when prices rise for two consecutive days, and the K value falls below the D value. This method captures price reversal trends.

### Dynamic Stop Loss Strategy
This strategy sets dynamic stop losses based on price volatility and skewness. It calculates the recent fluctuations of high and low prices to determine whether the market is in an upward or downward channel. Based on this information, it dynamically adjusts the stop loss positions according to the current market environment.

The two strategies work together by capturing reversal signals while setting dynamic stops to control risks.

## Advantage Analysis
- Captures price reversal points, suitable for reversal trading.
- Uses dynamic stop losses that adjust based on market conditions.
- Dual signal confirmation reduces false signals.
- Controls risks and ensures profitability.

## Risk Analysis
- Reversal failure risk: The reversal signals may not be accurate.
- Parameter risk: Incorrect parameter settings can affect the strategy's performance.
- Liquidity risk: Certain trading instruments have low liquidity, making it difficult to execute stop losses.

These risks can be managed by optimizing parameters, implementing strict stop-losses, and selecting liquid products.

## Optimization Directions 
- Optimize stochastic parameters for optimal combinations
- Optimize stop loss parameters for ideal positions  
- Add filters to avoid entering trades in range markets
- Integrate position sizing modules to limit maximum losses

Comprehensive optimizations aim to enhance the strategy's ability to capture reversals while managing risks effectively.

## Summary
This strategy combines a reversal trend catching mechanism and dynamic stop loss features, enabling the capture of price reversals and risk control through dynamically adjusted stops. It is a relatively stable short-term trading strategy that can potentially yield consistent profits with continuous optimization and monitoring.
[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|Length|
|v_input_2|true|KSmoothing|
|v_input_3|3|DLength|
|v_input_4|50|Level|
|v_input_5|30|LengthKDS|
|v_input_6|0|Trade From Level: 4|2|3|1|
|v_input_7|false|Trade reverse|


> Source (PineScript)

```pinescript
//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 07/12/2020
// This is a combination strategy for obtaining a cumulative signal.
//
// First Strategy
// This system was created from the book "How I Tripled My Money In The Futures Market" by Ulf Jensen, page 183. It is a reverse type of strategy. 
// The strategy buys at market if the close price is higher than the previous close for two consecutive days and the 9-day Stochastic Slow Oscillator value is below 50.
// The strategy sells at market if the close price is lower than the previous close for two consecutive days and the 9-day Stochastic Fast Oscillator value is above 50.
//
// Second Strategy
// Kase Dev Stops system finds an optimal statistical balance between allowing profits to run while cutting losses. 
// Kase Dev Stops determine the ideal stop level by considering volatility (risk), variance in volatility, and skewness of volatility.
// Setting stops will help you take as much risk as necessary to stay in a good position but not more.
//
// You can change long to short in the Input Settings
// Please use it only for learning or paper trading. Do not use for real trading.
//
// WARNING:
// - For educational purposes only
// - This script changes bar colors.
////////////////////////////////////////////////////////////
Reversal123(Length, KSmoothing, DLength, Level) =>
    vFast = sma(stoch(close, high, low, Length), KSmoothing) 
    vSlow = sma(vFast, DLength)
    pos = 0.0
    pos := iff(close[2] < close[1] and close > close[1] and vFast < vSlow and vFast > Level, 1,
             iff(close[2] > close[1] and close < close[1] and vFast > vSlow and vFast < Level, -1, nz(pos[1], 0))) 
    pos

KaseDevStops(Length, Level) =>
    pos = 0.0
    RWH = (high - low[Length]) / (atr(Length) * sqrt(Length))
    RWL = (high[Length] - low) / (atr(Length) * sqrt(Length))
    Pk = wma((RWH-RWL),3)
    AVTR = sma(highest(high,2) - lowest(low,2), 20)
    SD = stdev(highest(high,2) - lowest(low,2),20)
    Val4 = iff(Pk>0, highest(high-AVTR-3*SD,20), lowest(low+AVTR+3*SD,20))
    Val3 = iff(Pk>0, highest(high-AVTR-2*SD,20), lowest(low+AVTR+2*SD,20))
    Val2 = iff(Pk>0, highest(high-AVTR-SD,20), lowest(low+AVTR+SD,20)
```