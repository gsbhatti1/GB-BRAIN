> Name

Trading Strategy Based on Support and Resistance Levels Using Technical Analysis

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1a4e3ea950138517099.png)

[trans]
#### Overview

This strategy is a technical analysis-based trading strategy that uses support and resistance levels to make trading decisions. The strategy utilizes the `pivothigh()` and `pivotlow()` indicators to determine support and resistance levels. It goes long when the closing price is above the resistance level and goes short when the closing price is below the support level, and the previous high is also below the support level. Positions are closed when the price crosses the support or resistance levels in the opposite direction. The strategy is suitable for the Russian stock market and uses daily data.

#### Strategy Principle

1. Use the `request.security()` function to obtain daily closing price data.
2. Calculate support and resistance levels using the `ta.pivothigh()` and `ta.pivotlow()` functions with a 7-day time window.
3. Execute a long trade when the closing price is above the resistance level.
4. Execute a short trade when the closing price is below the support level, and the previous high is also below the support level.
5. Close all positions when the price crosses the support or resistance levels in the opposite direction.
6. Plot support and resistance levels on the chart, represented by green and red colors.

#### Strategy Advantages

1. The strategy is based on technical analysis and uses market price behavior to make trading decisions, suitable for trending markets.
2. Support and resistance levels are widely recognized by market participants as important price levels. The strategy builds trading signals around these key levels, helping to capture trending opportunities.
3. The strategy logic is clear, easy to understand and implement, making it suitable for beginners to learn and use.
4. By plotting support and resistance levels on the chart, market structure and price behavior can be visually observed, aiding in trading decisions.

#### Strategy Risks

1. The strategy relies entirely on historical price data and may fail when significant fundamental changes or black swan events occur in the market.
2. Support and resistance levels may be breached, leading to consecutive losses for the strategy.
3. The strategy lacks risk management measures, such as stop-loss and position sizing control, which may lead to substantial losses during extreme market volatility.
4. The strategy may perform poorly in choppy markets, and frequent trading may result in high transaction costs.

#### Strategy Optimization Directions

1. Introduce trend confirmation indicators, such as moving averages, to filter out noise and identify the main trend, improving signal quality.
2. Set reasonable stop-loss levels to control individual trade risk and enhance strategy robustness.
3. Optimize the calculation method for support and resistance levels, such as using a combination of multiple time scales, to improve the reliability of price levels.
4. Incorporate position sizing and money management rules to dynamically adjust position sizes based on market volatility and control overall risk exposure.
5. Perform parameter optimization and backtesting on the strategy to find the optimal parameter combination and improve strategy performance.

#### Summary

This strategy is a technical analysis-based trading strategy that uses support and resistance levels to generate trading signals. The strategy logic is straightforward, making it suitable for beginners to learn. However, when applying the strategy in practice, risk management and optimization need to be considered. By introducing other technical indicators, risk control measures, position sizing, and other enhancements, the robustness and profitability of the strategy can be further improved. Before deploying the strategy in a live trading environment, it is recommended to conduct comprehensive backtesting and parameter optimization on historical data.
[/trans]

> Source (PineScript)

```pinescript
//@version=5
strategy("Trading Strategy Based on Support and Resistance Levels", overlay=true)

// Function to determine support and resistance levels
findSR() =>
    // Get the data for finding levels
    data = request.security(syminfo.tickerid, "D", close)
    // Find the support and resistance levels
    pivot_high = ta.pivothigh(data, 7, 7)
    pivot_low = ta.pivotlow(data, 7, 7)
    [pivot_high, pivot_low]

[support, resistance] = findSR()

// Conditions for entering a long position
longCondition = close > resistance
```