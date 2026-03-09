> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|---- 123 Reversal ----|
|v_input_2|14|Length|
|v_input_3|true|KSmoothing|
|v_input_4|3|DLength|
|v_input_5|50|Level|
|v_input_6|true|---- Price-Volume Trend ----|
|v_input_7|true|LevelPVT|
|v_input_8|true|Scale|
|v_input_9|23|LengthPVT|
|v_input_10|false|Trade reverse|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-17 00:00:00
end: 2024-01-24 00:00:00
period: 15m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 23/02/2021
// This is combo strategies for get a cumulative signal. 
//
// First strategy
// This System was created from the Book "How I Tripled My Money In The 
// Futures Market" by Ulf Jensen, Page 183. This is reverse type of strategies.
// The strategy buys at market, if close price is higher than the previous close 
// during 2 days and the meaning of 9-days Stochastic Slow Oscillator is lower than 50. 
// The strategy sells at market, if close price is lower than the previous close price 
// during 2 days and the meaning of 9-days Stochastic Fast Oscillator is higher than 50.
//
// Second strategy
//  The related article is copyrighted material from
//  Stocks & Commodities.
//
// WARNING:
```

## Overview

This strategy combines double factors reversal and improved price volume trend sub-strategies to generate cumulative trading signals. The first strategy, based on Ulf Jensen's book "How I Tripled My Money In The Futures Market," Page 183, generates buy signals when the close price is higher than the previous day's close for two consecutive days and the 9-day Stochastic Slow Oscillator is below 50. It generates sell signals when the close price is lower than the previous day's close for two consecutive days and the 9-day Stochastic Fast Oscillator is above 50.

The second strategy, based on copyrighted material from Stocks & Commodities, evaluates the joint impact of price and volume to determine market trends and momentum. The calculation formula is: `PxVFactor = PriceFactor + Scale * CumPVT`, where `PriceFactor` is the price factor, and `CumPVT` is the cumulative power indicator. A simple moving average of `LengthPVT` days is then calculated for `PxVFactor` to assess market trends and momentum.

## Strategy Principles

The first strategy uses the principle of two-day closing price reversals combined with stochastic indicators to generate signals. If today's close is lower than yesterday’s, and the fast stochastic indicator is above 50 while the slow stochastic is below it, a short signal is generated. Conversely, if today’s close is higher than yesterday’s, and the fast stochastic is below 50 while the slow stochastic is above it, a long signal is generated.

The second strategy evaluates price and volume to determine market trends and momentum. The formula `PxVFactor = PriceFactor + Scale * CumPVT` calculates the combined impact of price and volume. A simple moving average of `LengthPVT` days for `PxVFactor` is then compared with the current value to determine the market’s direction and strength.

The combo strategy combines signals from both sub-strategies, generating corresponding long or short positions when they align in the same direction.

## Advantage Analysis

- The double factors reversal strategy integrates price reversals and stochastic indicators, effectively identifying short-term extremums and capturing reversal opportunities.
- The improved price volume trend strategy incorporates trading volume to judge market consolidation and momentum.
- Both strategies validate each other, enhancing stability and reducing false signals.
- Using medium-term parameters (9 or 14 days) is suitable for intraday and short-term operations.

## Risk and Optimization

- Reversal strategies carry the risk of being trapped; stop loss should be set to control risk.
- Volume price strategies may increase drawdowns if market direction is incorrectly judged.
- Testing the optimal weights for `PriceFactor` and `CumPVT` can improve performance.
- Different day parameters can be tested to find the best return-to-drawdown ratio.

## Conclusion

In summary, the combo strategy of double factors reversal and improved price volume trend combines judgments from both reversal and trend dimensions. This approach ensures that signals are validated by each other, enhancing stability. Adding a trend indicator as an auxiliary judgment is necessary in reversal strategies where trapping is likely. Incorporating trading volume indicators also helps determine market reversals and momentum. The strategy uses medium-term parameters suitable for intraday and short-term operations, offering practical value.

[/trans]