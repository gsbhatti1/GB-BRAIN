> Name

Momentum-Combined-with-Trend-Judgment-Multi-factor-Quantitative-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1bbbf7ca5a8d4e242d4.png)
[trans]
## Overview
This strategy is a multi-factor judged quantitative trading strategy that combines momentum indicators and trend indicators. The strategy judges the overall trend and momentum direction of the market by calculating mathematical combinations of multiple moving averages, and generates trading signals based on threshold conditions.

## Strategy Principle  
1. Calculate multiple moving averages and momentum indicators
    - Calculate Harmonics moving average, short-term moving average, medium-term moving average, long-term moving average and other multiple moving averages 
    - Calculate the difference between each moving average to reflect the trend of price changes
    - Calculate the first order derivative of each moving average to reflect the momentum of price changes  
    - Calculate the sine and cosine indicators to determine the trend direction
2. Comprehensively judge trading signals
    - Weighted calculation of momentum indicators, trend indicators and other multi-factors
    - Judge the current market state according to the distance between the result value and the threshold 
    - Issue long and short trading signals

## Advantage Analysis  
1. Multi-factor judgment improves signal accuracy
    - Comprehensively consider price, trend, momentum and other factors
    - Different factors can be configured with different weights
2. Adjustable parameters, adaptable to different markets
    - Parameters of moving averages, boundary of trading range can be customized
    - Can adapt to different cycles and market environments  
3. Clear code structure, easy to understand
    - Naming specifications, complete comments
    - Easy to secondary development and optimization

## Risk Analysis  
1. Difficulty in parameter optimization is high
    - Requires a lot of historical data backtesting to find the optimal parameters
2. Trading frequency may be too high
    - Multi-factor combination judgment may result in too many transactions
3. High correlation with market
    - Trend judgment strategies are prone to irrational behavior

## Optimization Directions  
1. Add stop loss logic
    - Avoid major losses caused by irrational behaviors
2. Optimize parameter settings 
    - Find optimal parameter combinations to improve strategy stability
3. Increase machine learning elements
    - Use deep learning to judge current market state and assist strategy decisions   

## Summary
This strategy judges the market state through the multi-factor combination of momentum indicators and trend indicators, and issues trading signals based on set thresholds. The advantages of the strategy are strong configurability, adaptability to different market environments, and easy understanding; the disadvantages are the difficulty in parameter optimization, possibly too high trading frequency, and high correlation with the market. Future optimizations can be made by adding stop loss, parameter optimization and machine learning.

||

## Overview  
This strategy is a multi-factor judged quantitative trading strategy that combines momentum indicators and trend indicators. The strategy judges the overall trend and momentum direction of the market by calculating mathematical combinations of multiple moving averages, and generates trading signals based on threshold conditions.

## Strategy Principle  
1. Calculate multiple moving averages and momentum indicators
    - Calculate Harmonics moving average, short-term moving average, medium-term moving average, long-term moving average and other multiple moving averages 
    - Calculate the difference between each moving average to reflect the trend of price changes
    - Calculate the first order derivative of each moving average to reflect the momentum of price changes  
    - Calculate the sine and cosine indicators to determine the trend direction
2. Comprehensively judge trading signals
    - Weighted calculation of momentum indicators, trend indicators and other multi-factors
    - Judge the current market state according to the distance between the result value and the threshold 
    - Issue long and short trading signals

## Advantage Analysis  
1. Multi-factor judgment improves signal accuracy
    - Comprehensively consider price, trend, momentum and other factors
    - Different factors can be configured with different weights
2. Adjustable parameters, adaptable to different markets
    - Parameters of moving averages, boundary of trading range can be customized
    - Can adapt to different cycles and market environments  
3. Clear code structure, easy to understand
    - Naming specifications, complete comments
    - Easy to secondary development and optimization

## Risk Analysis  
1. Difficulty in parameter optimization is high
    - Requires a lot of historical data backtesting to find the optimal parameters
2. Trading frequency may be too high
    - Multi-factor combination judgment may result in too many transactions
3. High correlation with market
    - Trend judgment strategies are prone to irrational behavior

## Optimization Directions  
1. Add stop loss logic
    - Avoid major losses caused by irrational behaviors
2. Optimize parameter settings 
    - Find optimal parameter combinations to improve strategy stability
3. Increase machine learning elements
    - Use deep learning to judge current market state and assist strategy decisions   

## Summary
This strategy judges the market state through the multi-factor combination of momentum indicators and trend indicators, and issues trading signals based on set thresholds. The advantages of the strategy are strong configurability, adaptability to different market environments, and easy understanding; the disadvantages are the difficulty in parameter optimization, possibly too high trading frequency, and high correlation with the market. Future optimizations can be made by adding stop loss, parameter optimization and machine learning.

---

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|10|Harmonic|
|v_input_2|9|BuyBand|
|v_input_3|-9|SellBand|
|v_input_4|false|Trade reverse|


> Source (PineScript)

```pinescript
/*backtest
start: 2022-11-16 00:00:00
end: 2023-11-22 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 14/03/2017
// This is modified version of Dale Legan's "Confluence" indicator written by Gary Fritz.
// ================================================================
// Here is Gary`s commentary:
// Since the Confluence indicator returned several "states" (bull, bear, grey, and zero), 
// he modified the return value a bit:
// -9 to -1 = Bearish
// -0.9 to 0.9 = "grey" (and zero)
// 1 to 9 = Bullish
// The "grey" range corresponds to the "grey" values plotted by Dale's indicator, but 
// they're divided by 10.
//
// You can change long to short in the Input Settings
// Please, use it only for learning or paper trading. Do not for real trading.
////////////////////////////////////////////////////////////

strategy(title="Confluence", shorttitle="Confluence")
Harmonic = input(10, minval=1)
BuyBand = input(9)
SellBand = input(-9)
reverse = input(false, title="Trade reverse")
hline(SellBand, color=red, linestyle=line)
hline(BuyBand, color=green, linestyle=line)

Price = close

STL = round((Harmonic * 2) - 1 - 0.5)
ITL = round((STL * 2) - 1 - 0.5)
LTL = round((ITL * 2) - 1 - 0.5)
HOFF = round(Harmonic / 2 - 0.5)
SOFF = round(STL / 2 - 0.5)
IOFF = round(ITL / 2 - 0.5)

xHavg = sma(Price, Harmonic)
xSavg = sma(Price, STL)
xIavg = sma(Price, ITL)
xLavg = sma(Price, LTL)

xvalue2 = xSavg - xHavg[HOFF]
xvalue3 = xIavg - xSavg[SOFF]
xvalue12 = xLavg - xIavg[IOFF]

xmomsig = xvalu