> Name

Momentum-Trend-Tracking-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/16bd1ddf5b6100c9a72.png)

[trans]

### Overview

The Momentum Trend Tracking Strategy is a strategy that utilizes Relative Strength Index (RSI), Stochastic, and Momentum indicators to identify trends. It integrates signals from multiple indicators, resulting in good backtesting outcomes and making it suitable for medium-to-long-term holdings.

### Strategy Logic

First, the 9-period RSI, Stochastic, and Momentum indicators are calculated separately. Then, the value of Stochastic is multiplied by that of RSI and divided by the value of Momentum to derive an integrated indicator called KNRP. This indicator reflects information from multiple sub-indicators simultaneously.

Next, a 2-period moving average of KNRP is computed. Trading signals are generated when this moving average crosses above or below its previous value. That is, go long when the average is greater than the previous period and go short when less than the previous period. This signal reflects the short-term trend of the KNRP indicator.

### Advantage Analysis

The biggest advantage of this strategy is that the indicator design is reasonable, effectively combining information from multiple technical indicators to accurately determine trend direction. Compared with a single indicator, it reduces the probability of erroneous signals and improves signal reliability.

Additionally, the main basis for determining trends in the strategy is the moving average of KNRP, which avoids the risk of chasing highs and selling lows, aligning with the concept of trend trading. Moreover, parameter settings are flexible, allowing users to adjust according to their own style.

### Risk Analysis

The primary risk associated with this strategy lies in the combination of multiple indicators. If the combination method is inappropriate, conflicts may arise between different indicators, increasing erroneous signals and impacting strategy performance. Improper parameter settings can also significantly affect results.

To mitigate risks, it is recommended to optimize parameters and test different lengths and combinations of parameters for their impact on the strategy indicator and overall backtest outcomes. It is also crucial to monitor the long-term market environment's effect on parameter stability.

### Optimization Directions

This strategy can be optimized in several aspects:

1. Test various types of technical indicators' combinations to find more effective ways to determine trends.
2. Optimize indicator parameters to find values better suited for current market conditions.
3. Add stop loss and take profit logic to lock in profits and reduce losses.
4. Test on longer time frames such as daily or weekly to evaluate performance as a medium-to-long-term strategy.
5. Add position sizing modules to adjust positions based on market conditions.

### Summary

The Momentum Trend Tracking Strategy is generally a relatively stable and reliable trend-following strategy. It addresses the issue of single indicators being prone to false signals by effectively using multiple weighted indicators to determine trends. Parameters are flexible with significant optimization potential, making it suitable for technical indicator traders. With further refinements, this strategy has the potential to become a long-term quantitative strategy worth holding.

||

### Overview

The Momentum Trend Tracking Strategy is a trend-following strategy that uses Relative Strength Index (RSI), Stochastic, and Momentum indicators to identify trends. It combines signals from multiple indicators with good backtesting results and is suitable for medium-to-long-term holdings.

### Strategy Logic

First, the 9-period RSI, Stochastic, and Momentum indicators are calculated separately. Then, the value of Stochastic is multiplied by that of RSI and divided by the value of Momentum to derive an integrated indicator called KNRP. This indicator reflects information from multiple sub-indicators simultaneously.

Afterward, a 2-period moving average of KNRP is computed. Trading signals are generated when this moving average crosses above or below its previous value. That is, go long when the average is greater than the previous period and go short when less than the previous period. This signal reflects the short-term trend of the KNRP indicator.

### Advantage Analysis

The biggest advantage of this strategy is that the indicator design is reasonable, effectively combining information from multiple technical indicators to accurately determine trend direction. Compared with a single indicator, it reduces the probability of erroneous signals and improves signal reliability.

Additionally, the main basis for determining trends in the strategy is the moving average of KNRP, which avoids the risk of chasing highs and selling lows, aligning with the concept of trend trading. Moreover, parameter settings are flexible, allowing users to adjust according to their own style.

### Risk Analysis

The primary risk associated with this strategy lies in the combination of multiple indicators. If the combination method is inappropriate, conflicts may arise between different indicators, increasing erroneous signals and impacting strategy performance. Improper parameter settings can also significantly affect results.

To mitigate risks, it is recommended to optimize parameters and test different lengths and combinations of parameters for their impact on the strategy indicator and overall backtest outcomes. It is also crucial to monitor the long-term market environment's effect on parameter stability.

### Optimization Directions

This strategy can be optimized in several aspects:

1. Test various types of technical indicators' combinations to find more effective ways to determine trends.
2. Optimize indicator parameters to find values better suited for current market conditions.
3. Add stop loss and take profit logic to lock in profits and reduce losses.
4. Test on longer time frames such as daily or weekly to evaluate performance as a medium-to-long-term strategy.
5. Add position sizing modules to adjust positions based on market conditions.

### Summary

The Momentum Trend Tracking Strategy is generally a relatively stable and reliable trend-following strategy. It addresses the issue of single indicators being prone to false signals by effectively using multiple weighted indicators to determine trends. Parameters are flexible with significant optimization potential, making it suitable for technical indicator traders. With further refinements, this strategy has the potential to become a long-term quantitative strategy worth holding.

||

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|9|Length_Momentum|
|v_input_2|9|Length_RSI|
|v_input_3|9|Length_Stoch|
|v_input_4|2|Length_NRP|
|v_input_5|false|Trade reverse|


> Source (PineScript)

```pinescript
//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 27/07/2021
// To calculate the coordinates in which the kink of the line will cross, 
//the standard Forex instruments are used - Relative Strenght Index, Stochastic and Momentum.
//It is very easy to optimize them for the existing trading strategy: they all have very 
//flexible and easily customizable parameters. Signals to enter the market can be 2 situations:
//    Change of color of the indicator line from red to blue. At the same time, it is worth entering into the purchase;
//    Change of color of the indicator line from blue to red. In this case, it is worth entering for sale.
//The signals are extremely clear and can be used in practice even by beginners. The indicator 
//itself shows when to make deals: the user only has to accompany them and set the values 
//of Take Profit and Stop Loss. As a rule, the signal to complete trading is the approach of 
//the indicator level to the levels of the maximum or minimum of the previous time period.  
/////////////////////////////////////////////////////
```