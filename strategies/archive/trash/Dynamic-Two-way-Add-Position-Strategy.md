> Name

Dynamic-Two-way-Add-Position-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1abfd153e9734c9d086.png)
[trans]


## Overview

This is a strategy that takes positions in both directions by using signals of strong breakthroughs in both directions. It will choose a direction to open positions after two consecutive strong candlesticks appear in the same direction, then set stop profit and stop loss for risk management.

## Strategy Principle

This strategy judges market direction based on the signals of two consecutive strong candlesticks. Specifically, it calculates the increase/decrease percentage of each candlestick. When the increase/decrease percentage of two consecutive candlesticks both exceed the threshold set by the user (such as 6%), it determines that the direction is strong and opens a long/short position in the third candlestick.

**Long condition:** The close prices of two consecutive candlesticks rise over 6% compared to previous close price  
**Short condition:** The close prices of two consecutive candlesticks fall over 6% compared to previous close price  

After opening positions, it will set stop profit and stop loss distances to control risks. The stop profit distance is input by the user, and the stop loss distance is a multiple (such as 8 times) of the opening price.

This strategy also has some auxiliary functions to control risks, such as only allowing to open positions during specific time periods, setting maximum loss amount, etc.

## Advantage Analysis

This is a relatively stable and reliable dual-direction trading strategy. The main advantages are:

1. Dual-direction trading can obtain profits when market goes up and down, improving stability.
2. Judging the trend based on two strong signals can effectively filter out noises and improve quality of opened positions.
3. The settings of stop profit and stop loss are reasonable, which is beneficial for risk control and limits losses.
4. The auxiliary functions are comprehensive, such as time control, maximum loss control, etc., they can control risks very well.
5. It is easy to backtest and optimize this strategy as the logic is simple and clear.

## Risk Analysis

The main risks of this strategy are:

1. It is prone to suffering stop loss during market consolidation. We can properly adjust the parameter of first signal to ensure signal quality.
2. The probability of three consecutive super strong candlesticks is relatively small, which may lead to fewer opportunities to open positions. We can reduce the parameter appropriately but need to balance the signal quality.
3. Irrational behaviors caused by sudden events may lead to huge losses exceeding the stop loss distance. We need to set maximum loss amount to solve this problem.
4. For the implementation of dual-direction trading, we need to pay attention to the fund allocation problems; otherwise, it may lead to making profits without stop losses.

## Optimization Directions

This strategy can be further optimized in the following aspects:

1. Optimize the logic of first signal judgment to improve signal quality. More factors can be considered such as change of transaction volume, volatility rate, etc.
2. Optimize standards of stop profit and stop loss. Adjust parameters based on different markets to make risk-reward ratio more reasonable. Stop loss distance can also be set as dynamic stop loss.
3. Add more risk control modules. For example, maximum daily loss, maximum consecutive loss, etc., to ensure efficient and safe use of funds.
4. Optimize allocation ratio of funds, to make the capital allocation of dual-direction trading more reasonable, preventing making profits without stop losses.
5. Set different parameter combinations for backtesting optimization towards different trading varieties, to improve adaptability.

## Summary

This strategy is a relatively robust dual-direction add position strategy. It has high signal quality and certain risk control capabilities. It also has large room for optimization to further improve profit stability. The strategy is suitable for mid-long term trending markets, and it can also seize opportunities during market consolidations.

||

## Overview

This is a strategy that takes positions in both directions by using signals of strong breakthroughs in both directions. It will choose a direction to open positions after two consecutive strong candlesticks appear in the same direction, then set stop profit and stop loss for risk management.

## Strategy Principle

This strategy judges market direction based on the signals of two consecutive strong candlesticks. Specifically, it calculates the increase/decrease percentage of each candlestick. When the increase/decrease percentage of two consecutive candlesticks both exceed the threshold set by the user (such as 6%), it determines that the direction is strong and opens a long/short position in the third candlestick.

**Long condition:** The close prices of two consecutive candlesticks rise over 6% compared to previous close price  
**Short condition:** The close prices of two consecutive candlesticks fall over 6% compared to previous close price  

After opening positions, it will set stop profit and stop loss distances to control risks. The stop profit distance is input by the user, and the stop loss distance is a multiple (such as 8 times) of the opening price.

This strategy also has some auxiliary functions to control risks, such as only allowing to open positions during specific time periods, setting maximum loss amount, etc.

## Advantage Analysis

This is a relatively stable and reliable dual-direction trading strategy. The main advantages are:

1. Dual-direction trading can obtain profits when market goes up and down, improving stability.
2. Judging the trend based on two strong signals can effectively filter out noises and improve quality of opened positions.
3. The settings of stop profit and stop loss are reasonable, which is beneficial for risk control and limits losses.
4. The auxiliary functions are comprehensive, such as time control, maximum loss control, etc., they can control risks very well.
5. It is easy to backtest and optimize this strategy as the logic is simple and clear.

## Risk Analysis

The main risks of this strategy are:

1. It is prone to suffering stop loss during market consolidation. We can properly adjust the parameter of first signal to ensure signal quality.
2. The probability of three consecutive super strong candlesticks is relatively small, which may lead to fewer opportunities to open positions. We can reduce the parameter appropriately but need to balance the signal quality.
3. Irrational behaviors caused by sudden events may lead to huge losses exceeding the stop loss distance. We need to set maximum loss amount to solve this problem.
4. For the implementation of dual-direction trading, we need to pay attention to the fund allocation problems; otherwise, it may lead to making profits without stop losses.

## Optimization Directions

This strategy can be further optimized in the following aspects:

1. Optimize the logic of first signal judgment to improve signal quality. More factors can be considered such as change of transaction volume, volatility rate, etc.
2. Optimize standards of stop profit and stop loss. Adjust parameters based on different markets to make risk-reward ratio more reasonable. Stop loss distance can also be set as dynamic stop loss.
3. Add more risk control modules. For example, maximum daily loss, maximum consecutive loss, etc., to ensure efficient and safe use of funds.
4. Optimize allocation ratio of funds, to make the capital allocation of dual-direction trading more reasonable, preventing making profits without stop losses.
5. Set different parameter combinations for backtesting optimization towards different trading varieties, to improve adaptability.

## Summary

This strategy is a relatively robust dual-direction add position strategy. It has high signal quality and certain risk control capabilities. It also has large room for optimization to further improve profit stability. The strategy is suitable for mid-long term trending markets, and it can also seize opportunities during market consolidations.


---

### Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|6|Signal|
|v_input_2|10000|Signal|
|v_input_3|2021|Year|
|v_input_4|true|Month|
|v_input_5|true|Day|
|v_input_6|false|Hour|
|v_input_7|false|Minute|
|v_input_8|10|Start Hour for Robot Operation|
|v_input_9|40|Minutes to Terminate Everything|
|v_input_10|17|Closing Time|
|v_input_11|50|Minutes to Terminate New Operations|
|v_input_12|50|Minutes to Terminate Everything|
|v_input_13|150000|Profit Target|
|v_input_14|5|Contracts|
|v_input_15|3|Gain|
|v_input_16|8|Loss|

---

### Source (PineScript)

```pinescript
/*backtes