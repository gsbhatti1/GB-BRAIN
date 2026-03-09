> Name

Dual-Exponential-Moving-Average-Trend-Following-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/e19dc4a68c8652971c.png)
[trans]
### Overview

The Dual Exponential Moving Average Trend Following Strategy is a trend-following strategy based on the crossover of moving averages. This strategy judges the current trend direction by calculating the fast EMA and slow EMA, and acts on their crossovers. When the fast EMA crosses above the slow EMA, it is determined as a bullish signal. When the fast EMA crosses below the slow EMA, it is determined as a bearish signal. Based on the identified trend direction, this strategy can go long or go short accordingly.

### Strategy Logic

The core logic of this strategy lies in calculating two EMA lines of different periods - one acts as the bearish line and one acts as the bullish line. Specifically, the strategy calculates an 8-period fast EMA using the talib indicator as the bullish line. And it calculates a 21-period slow EMA as the bearish line. Then it judges the crossover relationships between the fast EMA line and slow EMA line. When the fast line crosses above the slow line, it determines a bullish signal to go long. When the fast line crosses below the slow line, it determines a bearish signal to go short.

In terms of actual trade execution, this strategy can go long only, go short only, or go both ways when a crossover happens between the fast and slow lines. Also, stop loss and take profit prices are configured in the strategy. After opening positions, if the price goes in an unfavorable direction, stop loss will be triggered to exit positions. If the price reaches the expected target level, take profit will realize and close positions.

### Advantage Analysis

The biggest advantage of the Dual EMA Trend Following strategy lies in the powerful trend identification capability of moving average crossovers. As a common tool for trend analysis, EMA lines can identify trend shifts and turning points through crossovers, avoiding being misled by market noises in the short term and catching the main trend direction.

Also, the flexible settings on trade directions make the strategy adaptable to both one-way trends and two-way oscillations, thus enhancing the strategy's practicality. The configured stop loss and take profit settings control risk and lock in partial profit.

### Risk Analysis

The biggest risk of this strategy is the false signals triggered by frequent small crossovers under range-bound markets. This would lead to excessive position opening and losses. To tackle this, we can increase EMA periods to reduce crossover times and false signal probabilities.

On the other hand, a too tight stop loss setting also increases the chance of getting stopped out. In this case, we need to expand the stop loss range carefully balancing the risk of being trapped.

### Optimization Directions

This strategy can be further optimized in the following aspects:

1. Adaptive adjustment on EMA periods based on market volatility and backtest results, avoiding overfitting under fixed periods.
2. Adding filter conditions to filter out false signals, e.g., combine with trading volumes to filter insignificant crossovers; or combine other indicators like MACD and KDJ to avoid signals in uncertainty.
3. Optimizing stop loss and take profit strategies, e.g., combining ATR to realize dynamic trailing on SL/TP, preventing over-tight SL and premature TP.
4. Testing different holding periods. Too long holding periods can be impacted by incidents, while too short periods lead to high trading costs and slippage costs. Finding the optimum holding days can improve strategy profitability.

### Summary

In general, the Dual EMA Trend Following Strategy is a robust and practical trend trading system. It catches trend directions effectively through the EMA crossover system. Meanwhile, the flexible settings on trade directions make it adaptable; the configured stop loss and take profit control risks. With further optimizations and enhancements, this strategy can become a powerful tool for quantitative trading.

||

### Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|v_input_int_1|8|Fast EMA Length|
|v_input_int_2|21|Slow EMA Length|
|v_input_string_1|0|Sides: Both|Short|Long|None|
|v_input_string_2|0|Percent or Pips: Percent|Pips|
|v_input_float_1|false|Stop Loss Long|
|v_input_float_2|false|Stop Loss Short|
|v_input_float_3|false|Target Profit Long|
|v_input_float_4|false|Target Profit Short|
|v_input_1|timestamp(01 Jan 2021)