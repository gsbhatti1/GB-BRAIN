## Overview

The Cross-Momentum Trend Following Strategy is a simple yet effective trading system that cleverly combines two technical indicators - Simple Moving Average (SMA) and Relative Strength Index (RSI) - to form an automated buy and sell signal generation system. The strategy utilizes price crossovers with the 20-period SMA as the primary signal trigger condition, while incorporating RSI momentum confirmation to filter out low-quality trading signals. The strategy also includes a performance tracking module that monitors success and failure rates in real-time, providing traders with decision-making reference.

## Strategy Principles

The core principle of this strategy is to capture trend reversal points through price and moving average crossovers, while using the RSI momentum indicator for signal confirmation:

1. **Buy Condition**: When price crosses above the 20-period SMA and the RSI value is greater than 60, the system generates a buy signal. This condition combines two dimensions: price breaking above the moving average indicates a potential uptrend formation, while an RSI value above 60 confirms the presence of upward momentum.

2. **Sell Condition**: When price crosses below the 20-period SMA and the RSI value is less than 40, the system generates a sell signal. Similarly, this condition identifies potential trend reversals and confirms downward momentum through the sub-40 RSI value.

3. **Performance Tracking Mechanism**: The strategy has a built-in trade performance monitoring system that tracks the following metrics:
   - Total Signal Count: Records the number of all generated buy signals
   - Success Count: Number of times price rises more than 2% after buying
   - Failure Count: Number of times price falls below the buy candle's low within 7 periods

4. **Visualization**: The strategy marks buy and sell points on the chart with "B" (Buy) and "S" (Sell), and displays performance statistics in real-time through a table.

## Strategy Advantages

1. **Simplicity and Efficiency**: Uses only two common technical indicators (SMA and RSI) to build a complete trading system, reducing the risk of over-optimization and overfitting.

2. **Dual Confirmation Mechanism**: Combines trend indicator (SMA) and momentum indicator (RSI), improving signal reliability. Price must not only break through the moving average but also have sufficient momentum to trigger a trade.

3. **High Degree of Automation**: The strategy completely automates the generation of buy and sell signals, reducing emotional interference and is suitable for systematic traders.

4. **Built-in Performance Evaluation**: Real-time tracking of key performance metrics allows traders to objectively assess strategy performance and timely adjust parameters or exit underperforming strategies.

5. **Risk Control Awareness**: By monitoring price behavior within 7 periods after buying, it helps identify potential stop-loss points and cultivates risk management awareness.

6. **Intuitive Visualization**: Through chart markers and performance tables, traders can intuitively understand strategy execution, facilitating backtesting analysis and strategy improvement.

## Strategy Risks

1. **False Breakout Risk**: Despite using RSI for filtering, the strategy may still produce numerous false breakout signals in consolidating markets, leading to frequent trading and unnecessary transaction costs.

2. **Parameter Sensitivity**: Strategy performance highly depends on the selection of SMA period (20) and RSI period (8) and their thresholds (60/40). These fixed parameters may perform poorly in different market environments or on different asset classes.

3. **Lack of Adaptability**: The strategy lacks the ability to identify market conditions and may perform well in trending markets but frequently lose money in volatile markets.

4. **Simple Stop-Loss Mechanism**: Although the strategy tracks failures, it does not implement a dynamic stop-loss feature, which could result in significant losses during volatile market conditions.

5. **Lack of Position Sizing Management**: The strategy uses fixed position sizing for entry and exit, without adjusting the size of positions based on market volatility or signal strength, which could optimize capital utilization.

6. **Limited Performance Assessment**: Success is defined as a price increase of 2%, which may not be applicable in all market environments. High-volatility assets may require higher thresholds.

## Strategy Optimization Directions

1. **Add Market Condition Filters**: Introduce volatility indicators (such as ATR) or trend strength indicators (such as ADX) to help identify market states, reducing trading frequency or adjusting parameters in consolidating markets.

2. **Dynamic Parameter Mechanism**: Implement dynamic adjustments for SMA and RSI parameters based on recent market performance, automatically optimizing periods and thresholds to improve adaptability.

3. **Optimize Position Sizing**: Design a dynamic position allocation system based on signal strength (such as RSI deviation), market volatility, or account risk to control individual trade risk.

4. **Enhance Stop-Loss Mechanisms**: Implement dynamic stop-loss or trailing stop-loss features based on ATR, more precisely controlling the risk of each trade.

5. **Increase Time Filtering**: Consider market time factors, avoiding trading during times of abnormal volatility or low liquidity to improve signal quality.

6. **Multi-Period Confirmation**: Incorporate multi-period analysis, requiring that the overall trend direction across larger time periods aligns with the trade direction, filtering out trades against the larger trend.

7. **Refine Performance Assessment**: Improve the definition of success/failure, considering risk-adjusted returns or return/risk ratios for more comprehensive evaluation metrics.

## Conclusion

The Cross-Momentum Trend Following Strategy is a simple yet practical trading system that combines SMA and RSI indicators to effectively identify trend reversal points and momentum confirmation, filtering out low-quality signals. This strategy is particularly suitable for traders new to quantitative trading, providing clear trading signals while incorporating performance tracking functionality to help traders objectively assess strategy performance.

While the strategy is relatively simple in design, it reflects key principles of quantitative trading: trend following, signal confirmation, and performance monitoring. By suggesting optimizations such as market condition filtering, dynamic parameter adjustment, and enhanced stop-loss mechanisms, traders can significantly enhance the strategy's robustness and adaptability while maintaining its core logic.

Such a simple strategy combined with classic technical indicators often proves more reliable and robust, especially when equipped with risk management and performance assessment mechanisms. For traders seeking an entry-level quantitative strategy, this is an ideal starting point, offering practical experience and laying the groundwork for subsequent strategy development.