## Overview

This strategy is based on the UT Bot indicator developed by QuantNomad and incorporates the idea of a trailing stop loss. The original code was written by @Yo_adriiiiaan and modified by @HPotter. The strategy will be used in conjunction with LuxAlgo's Smart Money Concepts. Currently, the strategy is in the testing phase.

## Strategy Principle

The main principles of this strategy are as follows:

1. When the closing price is higher than the 50-period simple moving average, a long trade is entered.
2. For long positions, a trailing stop loss price is set. The trailing stop loss price is 80% (1-20%) of the current closing price. The trailing stop loss price moves up with rising prices but does not move down, thus protecting profits.
3. For short positions, a trailing stop loss price is also set. The trailing stop loss price is 120% (1+20%) of the current closing price. The trailing stop loss price moves down with falling prices but does not move up.
4. ATR (Average True Range) is used as a reference for the trailing stop. The calculation method for the ATR trailing stop price is: when moving up, take the larger of the previous ATR trailing stop price and (current closing price - ATR * Key Value); when moving down, take the smaller of the previous ATR trailing stop price and (current closing price + ATR * Key Value). The Key Value is a user-set parameter used to adjust the sensitivity of the trailing stop.
5. Based on the breakthrough of the ATR trailing stop price, the current position direction is determined. When the price breaks above the ATR trailing stop price, a long position is held; when the price breaks below the ATR trailing stop price, a short position is held; in other cases, the current position status remains unchanged.

## Advantage Analysis

1. The setting of the trailing stop can effectively protect profits, allowing the strategy to obtain more gains in trend markets.
2. Setting stop losses separately for long and short positions can adapt to different market conditions.
3. Using ATR as a reference for the stop loss allows for dynamic adjustment of the stop loss position, making it more flexible and effective.
4. The Key Value parameter is provided for user optimization, which can be adjusted according to different varieties and cycles to improve adaptability.

## Risk Analysis

1. In choppy markets, frequent stop-outs may lead to excessive transactions, increasing commission costs and reducing returns.
2. The fixed percentage trailing stop method is relatively simple and may not be able to cope well with price fluctuations in some market conditions.
3. The strategy only considers trailing stops and does not set trailing profit targets, which may miss some profit opportunities.
4. The choice of parameters has a significant impact on strategy performance, and inappropriate parameters may bring greater drawdown risks.

## Optimization Direction

1. Other indicators or conditions, such as trading volume and volatility, can be considered to optimize entry conditions and improve signal reliability.
2. For the calculation method of the trailing stop, more complex and effective methods can be explored, such as using parabolic stop loss or dynamic percentage stop loss.
3. A trailing profit target mechanism can be added, for example, setting dynamic profit targets based on ATR or percentages to better lock in profits.
4. Parameter optimization can be performed for different varieties and cycles to find the most suitable parameter combinations. Parameters can also be dynamically adjusted according to changes in market conditions.

## Summary

Based on the UT Bot indicator, this strategy incorporates trailing stop logic, which can protect profits in trend markets. At the same time, the strategy sets stop losses separately for long and short positions, making it highly adaptable. Using ATR as a reference for the trailing stop allows for dynamic adjustment of the stop loss position, improving flexibility. However, this strategy may face the risk of high transaction costs due to frequent stop-outs in choppy markets, and it lacks a trailing profit target setting, which may miss profit opportunities. In addition, the choice of parameters has a significant impact on strategy performance, and inappropriate parameters may bring greater drawdown risks.

Future improvements could include optimizing entry conditions, exploring more complex methods for the trailing stop calculation, adding a trailing profit mechanism, and performing parameter optimization for different varieties and cycles to find the most suitable combinations. Overall, this strategy is simple in concept but has room for further refinement and improvement.