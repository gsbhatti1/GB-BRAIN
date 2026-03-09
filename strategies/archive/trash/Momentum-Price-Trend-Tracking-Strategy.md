> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|3000|Take Profit|
|v_input_2|2200|Stop Loss|
|v_input_3|186|ROC Length|
|v_input_4|50|Smoothing Length|
|v_input_5_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_6|53|Upper Channel|
|v_input_7|53|Lower Channel|
|v_input_8|91|Offset Bars|
|v_input_9|0|Divergence Length|


## Overview

The momentum price trend tracking strategy uses multiple momentum indicators to identify price trends, establishes positions at the beginning of trends, and locks in profits through stop profit and stop loss settings to track price trends.

## Strategy Logic

The momentum price trend tracking strategy mainly applies the following technical indicators:

1. ROC indicator: This indicator calculates the percentage rate of change in price over a certain period to determine price momentum. When ROC is positive, it means prices are rising. When ROC is negative, it means prices are falling. The strategy uses the ROC indicator to determine the direction of the price trend.

2. Bulls Power and Bears Power indicator: This indicator reflects the power comparison between bulls and bears. Bulls Power > 0 indicates bulls power is greater than bears power and prices rise. The strategy uses this indicator to predict price direction by comparing bull and bear power.

3. Divergence: This indicator identifies trend reversal by calculating price and volume divergence. The strategy uses divergence signals as entry timing.

4. Donchian Channel: This indicator constructs a channel using highest and lowest prices, and the channel boundaries can serve as support and resistance. The strategy uses the channel to determine trend direction.

5. Moving Average: This indicator smooths out price fluctuations to identify the overall trend direction. The strategy uses it to determine the general price trend.

The strategy determines price trends and reversal points based on the above indicators, and establishes long or short positions according to indicator signals at the beginning of trends. It then closes positions in a timely manner based on stop profit and stop loss points to capture price trends.

## Advantage Analysis

The advantages of this strategy include:

1. Using multiple indicators to determine trends reduces misjudgement probability.

2. Using indicator divergences enables accurately capturing trend reversal points.

3. Combining channels and moving averages helps determine the overall trend.

4. Setting stop profit and stop loss secures profits timely and avoids expanded drawdowns.

5. Adjustable parameters make the strategy adaptable to different periods and products.

6. The clear logic facilitates further optimization.

## Risk Analysis

The potential risks of this strategy include:

1. The multiple indicators may increase erroneous signal probability. Optimizing indicator weights is needed.

2. Stop loss points set too small may increase stop loss probability, while too wide may expand drawdowns. Reasonable points need comprehensive consideration.

3. Blind application across varying market periods may lead to inadaptability. Periodic parameter tuning is required.

4. Sufficient capital to support high position units is required to achieve excess returns.

5. Backtest overfitting risks exist. Real-trading performance has uncertainties.

## Optimization Directions

The strategy can be optimized in the following aspects:

1. Optimize indicator parameters to find the optimal combinations for different periods and products.

2. Introduce machine learning algorithms to find the optimal parameters automatically.

3. Build in adaptive stop loss mechanisms based on market conditions.

4. Incorporate high-frequency factors and fundamentals to improve alpha.

5. Develop automated testing frameworks for parameter optimization and performance verification.

6. Introduce risk management modules to control position sizing and reduce drawdowns.

7. Add simulated and live trading and testing to improve stability.

## Conclusion

This strategy combines multiple momentum indicators to determine price trends and uses stop profit/loss to lock in profits. It can effectively capture trends with strong stability. Further enhancements in parameter tuning, structure optimization and risk control will improve its performance and risk management. The strategy provides a reliable and easy-to-use trend following solution for quantitative trading.

[/trans]