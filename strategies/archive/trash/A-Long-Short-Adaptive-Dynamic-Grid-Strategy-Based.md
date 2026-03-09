## Overview

This is a long-short adaptive dynamic grid trading strategy based on Pine Script. The core idea of this strategy is to automatically calculate the upper and lower bounds of a grid based on the recent price highs and lows or a simple moving average, and then divide this range evenly into multiple grid lines. When the price reaches a certain grid line, it will open a long position or close a position at that level. In this way, the strategy can continuously open and close positions in a rangebound market to capture the price spread. At the same time, by dynamically adjusting the grid boundaries, it can also adapt to different market trends.

## Strategy Principles

1. **Calculate Grid Boundaries:** Based on user choice, the boundaries can be calculated from the highest and lowest points of the recent N candles, with an option to widen or narrow the range by a percentage; or they can be based on the simple moving average of the closing prices of the recent N candles, with an option to set the upward and downward deviation ratios.

2. **Generate Grid Line Array:** According to the set number of grid lines, divide the grid range evenly to generate an array of grid line prices.

3. **Entry/Add Position:** Traverse the grid lines from bottom to top. If the current closing price is less than a grid line price and there is no position on that grid line, then open a long position at that level. In this way, when the price reaches higher grid lines, it will continue to add positions.

4. **Exit/Reduce Position:** Traverse the grid lines from top to bottom. If the current closing price is greater than a grid line price and there is a position on the grid line below, then close the long position on the lower grid line. In this way, when the price falls back, it will continue to reduce positions.

5. **Dynamic Adjustment:** If the dynamic grid function is selected, the upper and lower bounds of the grid and the grid line array will be recalculated on each candle, so that the grid can constantly adapt as the market changes.

## Advantage Analysis

1. **Strong Adaptability:** The grid trading strategy can adapt to both rangebound and trending markets. In a rangebound market, the grid strategy can continuously open and close positions to earn the price spread; in a trending market, because the grid follows the price movement, it can also maintain a certain position to obtain trend gains.

2. **Controllable Risk:** The position size of each opening is determined by the set number of grids, so the single risk exposure is small and controllable. At the same time, since reaching the upper grid lines will close positions for profit, it also hedges potential losses to a certain extent.

3. **High Degree of Automation:** This strategy can basically run fully automatically without manual intervention, which is suitable for investors who need long-term steady returns.

4. **Flexible Parameters:** Users can flexibly set the number of grid lines, dynamic grid parameters, etc. according to market characteristics to optimize strategy performance.

## Risk Analysis

1. **Black Swan Risk:** In case of an extreme market crash, if the price directly gaps down below the lowest grid line, the strategy will be fully positioned and face a larger drawdown. To reduce this risk, a stop-loss condition can be set to close all positions once the loss reaches a threshold.

2. **Improper Grid Parameter Setting:** If the grid density is too high, the spread of each open and close will be very small, and transaction costs may erode most of the gains. If the grid width is too large, the one-time opening ratio is high and the risk exposure is large. The characteristics of the underlying asset need to be carefully evaluated to select appropriate grid parameters.

3. **Basis Risk:** This strategy sets the opening and closing conditions based on the current price. In markets such as futures, if the contract price differs greatly from the underlying price, the actual opening and closing prices may deviate significantly from expectations.

## Optimization Directions

1. **Add Trend Filter:** Grid strategies perform poorly in one-sided trending markets. Adding a trend indicator as a filter, such as only enabling the grid when the ADX is below a certain threshold, and disabling the grid when a clear trend is present, holding a one-sided position only, can improve performance.

2. **Signal Optimization:** Overlapping other signals on the grid basis, such as grid + moving average, can determine positions mainly based on the grid, but opening positions only when the price crosses a certain moving average. This can reduce the cost of frequent open and close positions.

3. **Position Management:** Currently, the position size per grid is fixed. Setting a lower position size when the price is far from the market average and increasing the position size when it is close can optimize the use of funds.

4. **Adaptive Grid Density:** Dynamically adjusting the grid density based on price volatility, increasing the number of grids during high volatility and decreasing them during low volatility, can optimize grid width and fund utilization.

## Summary

This strategy through adaptive dynamic grids can continuously open and close positions in a rangebound market to capture the price spread, and also maintain a certain position direction in a trending market to obtain trend gains. It is a relatively robust medium to long-term quantitative strategy. By reasonably setting the grid trigger logic and position management, it can achieve stable returns. However, attention should be paid to extreme market conditions and gaps, which require setting appropriate stop-loss conditions to control. Additionally, there is further room for optimization in parameter settings and risk management, which can be achieved by introducing trend filtering, signal叠加, position management, and adaptive grid density. In summary, this strategy, based on the basic logic of grids, incorporates a dynamic adaptive mechanism, providing new ideas and references for medium to long-term quantitative investors.