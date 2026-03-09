> Name

Double-Confirmation-Breakthrough-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/15fb9c57194e95f2f7e.png)
[trans]

## Overview

The double confirmation breakthrough strategy is a trading strategy that combines breakout strategies and moving average strategies. This strategy uses the previous day's highest price and lowest price as key price levels, combined with golden cross and death cross signals of fast and slow moving averages, to make buy and sell operations.

## Strategy Principle  

The core logic of the double confirmation breakthrough strategy is:

1. Detect whether the price breaks through the highest price or lowest price of the previous day. If the price breaks through the highest price of the previous day, it is seen as a bullish signal; if the price breaks through the lowest price of the previous day, it is seen as a bearish signal.

2. When a breakthrough occurs, check if the fast line (10-day line) breaks up the slow line (30-day line). If so, a buy order is made; if the fast line breaks through the slow line downward, then sell.

3. Set a fixed stop loss and take profit ratio to calculate the stop loss price and take profit price. For example, if the strategy sets a stop loss and take profit ratio of 1:4, then the take profit range is 4 times the stop loss range.  

4. After opening a position, if the price triggers the stop loss line, stop loss to exit; if the take profit target is reached, take profit to exit.

It can be seen that the double confirmation breakthrough strategy utilizes the breakthrough of both trend judgment indicators (moving averages) and important price levels (previous day's highs and lows) to confirm trading signals, making it a relatively stable and reliable breakout system.

## Advantage Analysis

The double confirmation breakthrough strategy has the following advantages:

1. Entering after breaking through the previous day's high or low point can effectively reduce the probability of false breakouts, thereby improving the accuracy of entry.

2. The auxiliary judgment of the moving average is superimposed on it to avoid frequent opening positions in shock markets.

3. Adopting fixed stop loss and take profit ratio to manage capital risk can keep risks and returns within an affordable range.

4. The strategy rules are simple and clear, easy to understand and implement, and suitable for quantitative trading.

## Risk Analysis  

The double confirmation breakthrough strategy also has the following risks:

1. It is easy to form short accumulations after breaking through, thus inducing reversals. To guard against this risk, confirmation can be made on the 2nd K-line after breaking through before entering the market.  

2. In oscillating markets, stop loss points are easily triggered. Stop loss range can be appropriately relaxed or trading frequency can be increased to diversify risks.

3. Fixed stop loss and take profit ratios are not suitable for all products and market conditions, and parameters need to be adjusted according to different markets.  

4. Inappropriate setting of moving average parameters can also miss better opportunities or increase unnecessary trading. Parameters should be backtested and optimized regularly.

## Optimization Directions

The double confirmation breakthrough strategy can be optimized in the following directions:

1. Increase the number of confirmation K-lines, for example, observe whether the closing price of 1-2 K-lines after the breakthrough has also broken through that important price level.

2. Adopt different parameter combinations for different products and market environments, such as moving average cycles, stop loss and take profit ratios, etc., for backtesting and optimization.

3. Combine it with other auxiliary indicators, such as a surge in trading volume, to confirm entry signals. 

4. Increase machine learning models to predict market trend probabilities and combine probability signals to adjust strategy parameters.

## Summary

The double confirmation breakthrough strategy makes comprehensive use of breakthrough signals from important price levels and judgment indicators from moving averages, which can effectively improve the quality of trading signals. At the same time, the use of fixed stop loss and take profit to manage capital risk enables it to operate steadily. This is a quantitative strategy that combines trend tracking and breakouts, suitable for traders seeking stable returns.

Although there are some risks with this strategy, risks can be controlled and the strategy's returns improved through continuous backtesting and optimization. This is a quantitative strategy that is worth in-depth research and application.