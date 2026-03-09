> Name

Dual-Moving-Average-Confluence-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1252f2fc5d8bc19d0ce.png)
 [trans]

## Overview

The Dual Moving Average Confluence strategy is a trend-following strategy. It constructs fast line group and slow line group by calculating two sets of moving averages, and judges the trend direction based on the relationship between prices and moving averages.

When the fast line crosses above the slow line, it is a long signal. When the fast line crosses below the slow line, it is a short signal. This strategy combines the direction of fast and slow moving averages, the number of price breakout candles, and other conditions to determine specific entry and exit timings.

## Strategy Logic

The Dual Moving Average Confluence strategy calculates two sets of moving averages, which represent short-term and long-term trend judgment criteria respectively. Specifically, the strategy defines:

1. Fast Moving Average Group, including lower fast line and upper fast line, representing short-term trends;
2. Slow Moving Average Group, including lower slow line and upper slow line, representing long-term trends.

The strategy judges the rationality of short-term and long-term trends and the specific entry and exit timings based on the price relationship between the fast line group and the slow line group.

**Entry Conditions** are:

- When the upper fast line breaks above the upper slow line for 2 or more candles, it is a long entry.
- When the lower fast line breaks below the lower slow line for 2 or more candles, it is a short entry.

The **exit conditions** are:

- For long positions, exit when fast MA crosses below slow MA.
- For short positions, exit when fast MA crosses above slow MA.

In addition, the strategy also sets profit-taking, stop-loss, trailing stop-loss, and other functions to control risks.

## Advantage Analysis

The main advantages of the Dual Moving Average Confluence strategy are:

1. By double moving average judgment, it can effectively filter market noise and lock in trend direction.
2. Combining fast and slow moving averages and price relationships, the reliability of signals is higher.
3. The strategy rules are simple and clear, easy to understand and implement, suitable for quantitative trading.
4. Built-in profit-taking, stop-loss, trailing stop-loss, and other risk control means can effectively control trading risks.

## Risk Analysis

The Dual Moving Average Confluence strategy also has some risks, mainly reflected in:

1. In range-bound markets, false signals may be generated, resulting in unnecessary trades.
2. Moving average systems react slowly to sudden events (such as major bearish/bullish news), which may lead to greater losses.
3. Trailing stop loss may be breached in certain market conditions, thus enlarging losses.

To control the above risks, methods such as optimizing moving average parameters, combining with other indicators for filtering, etc., can be used to improve.

## Optimization Directions

The Dual Moving Average Confluence strategy can be optimized in the following dimensions:

1. Optimize moving average parameters, adjust average cycle to adapt to different cycle markets.
2. Increase other indicator filters to form multi-indicator combined strategies to improve signal accuracy.
3. Optimize stop loss, profit taking settings, set drawdown thresholds to control maximum losses.
4. Introduce machine learning models to predict trends and assist in determining entry timing.

## Summary

In summary, the Dual Moving Average Confluence strategy is a very practical trend-following strategy. Its judging rules are simple and clear, with solid theoretical basis of controlling risks through the dual moving average system. Next steps can be taken to further improve the profitability and stability of the strategy by optimizing parameters, controlling risks, and so on.

||

## Overview

The Dual Moving Average Confluence strategy is a trend-following strategy. It constructs fast line group and slow line group by calculating two sets of moving averages, and judges the trend direction based on the relationship between prices and moving averages.

When the fast line crosses above the slow line, it is a long signal. When the fast line crosses below the slow line, it is a short signal. This strategy combines the direction of fast and slow moving averages, the number of price breakout candles, and other conditions to determine specific entry and exit timings.

## Strategy Logic

The Dual Moving Average Confluence strategy calculates two sets of moving averages, which represent short-term and long-term trend judgment criteria respectively. Specifically, the strategy defines:

1. Fast Moving Average Group, including lower fast line and upper fast line, representing short-term trends;
2. Slow Moving Average Group, including lower slow line and upper slow line, representing long-term trends.

The strategy judges the rationality of short-term and long-term trends and the specific entry and exit timings based on the price relationship between the fast line group and the slow line group.

**Entry Conditions** are:

- When the upper fast line breaks above the upper slow line for 2 or more candles, it is a long entry.
- When the lower fast line breaks below the lower slow line for 2 or more candles, it is a short entry.

The **exit conditions** are:

- For long positions, exit when fast MA crosses below slow MA.
- For short positions, exit when fast MA crosses above slow MA.

In addition, the strategy also sets profit-taking, stop-loss, trailing stop-loss, and other functions to control risks.

## Advantage Analysis

The main advantages of the Dual Moving Average Confluence strategy are:

1. By double moving average judgment, it can effectively filter market noise and lock in trend direction.
2. Combining fast and slow moving averages and price relationships, the reliability of signals is higher.
3. The strategy rules are simple and clear, easy to understand and implement, suitable for quantitative trading.
4. Built-in profit-taking, stop-loss, trailing stop-loss, and other risk control means can effectively control trading risks.

## Risk Analysis

The Dual Moving Average Confluence strategy also has some risks, mainly reflected in:

1. In range-bound markets, false signals may be generated, resulting in unnecessary trades.
2. Moving average systems react slowly to sudden events (such as major bearish/bullish news), which may lead to greater losses.
3. Trailing stop loss may be breached in certain market conditions, thus enlarging losses.

To control the above risks, methods such as optimizing moving average parameters, combining with other indicators for filtering, etc., can be used to improve.

## Optimization Directions

The Dual Moving Average Confluence strategy can be optimized in the following dimensions:

1. Optimize moving average parameters, adjust average cycle to adapt to different cycle markets.
2. Increase other indicator filters to form multi-indicator combined strategies to improve signal accuracy.
3. Optimize stop loss, profit taking settings, set drawdown thresholds to control maximum losses.
4. Introduce machine learning models to predict trends and assist in determining entry timing.

## Summary

In summary, the Dual Moving Average Confluence strategy is a very practical trend-following strategy. Its judging rules are simple and clear, with solid theoretical basis of controlling risks through the dual moving average system. Next steps can be taken to further improve the profitability and stability of the strategy by optimizing parameters, controlling risks, and so on.

---

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Is this a RENKO Chart|
|v_input_2|false|Alternate TimeFrame Multiplier (0=none)|
|v_input_3|true|Show Coloured MA Ribbons|
|v_input_4|true|Show Ribbon Median MA Lines|
|v_input_5|0|FAST MA Ribbon Type: : EMA|SMA|WMA|VWMA|SMMA|DEMA|TEMA|LAGMA|HullMA|ZEMA|TMA|SSMA|
|v_input_6|5|FAST Ribbon Lower MA Length|
|v_input_7|25|FAST Ribbon Upper Length|
|v_input_8|0|SLOW MA Ribbon Type: : EMA|SMA|WMA|VWMA|SMMA|DEMA|TEMA|LAGMA|HullMA|ZEMA|TMA|SSMA|
|v_input_9|28|SLOW Ribbon Lower MA Length|
|v_input_10|72|SLOW Ribbon Upper Length|
|v_input_11|2018|Backtest Start Year|
|v_input_12|true|Backtest Start Month|
|v_input_13|true|Backtest Start Day|
|v_input_14|false|Use Opposite Trade as a Close Signal|
|v_input_15|true|Colour Candles to Trade Or