||

## Overview

The Dual-Trend-Tracking Strategy combines two different strategy signals to more accurately capture market trends and generate excess returns. It first uses the 123 Reversal Strategy to determine price reversal signals, and then combines the Overbought-Oversold Indicator to determine position direction, tracking trends while avoiding being trapped.

## Strategy Logic

The strategy consists of two parts:

1. **123 Reversal Strategy**

   The 123 Reversal Strategy first judges the closing price relationship between the previous two days. If the closing prices reversed recently (e.g., the closing price rose yesterday and fell the day before), it indicates a potential turning point.

   It then combines the Stoch Indicator to determine buy and sell timing. When the Stoch fast line is below a certain level (e.g., 50) and the slow line is above the fast line, it is considered oversold and generates a buy signal. Conversely, when the Stoch fast line is above a certain level (e.g., 50) and the slow line is below the fast line, it is considered overbought and generates a sell signal.

   Therefore, the 123 Reversal Strategy requires confirmation from the Stoch Indicator in addition to identifying price reversal before generating actual trading signals.

2. **Overbought-Oversold Indicator**

   The Overbought-Oversold Indicator directly uses the Stoch Indicator. When the Stoch Indicator is above a certain level (e.g., 90), it is considered overbought and generates a sell signal. Conversely, when the Stoch Indicator is below a certain level (e.g., 20), it is considered oversold and generates a buy signal.

   This indicator judges overbought/oversold levels directly through the Stoch Indicator to track trends.

Finally, the strategy combines the signals from the two strategies—only when the signals are in the same direction will final buy or sell signals be generated to more accurately capture market trends.

## Advantage Analysis

The biggest advantage of the Dual-Trend-Tracking Strategy is that it can verify both price trends and overbought/oversold conditions, avoiding wrong trading signals. Specific advantages include:

1. Combining two strategy signals provides a more robust verification mechanism, reducing losses caused by errors in a single strategy.
2. The 123 Reversal Strategy can capture potential trend reversal points in a timely manner.
3. The Overbought-Oversold Indicator can verify current market conditions and avoid chasing highs and selling lows.
4. The two strategies can verify each other, avoiding wrong signals to improve stability.
5. It combines simple and effective indicators with clear logic that is easy to understand and apply.

## Risk Analysis

Although the strategy improves stability through combined verification, some risks still exist:

1. The 123 Reversal Strategy cannot perfectly identify reversal points and may miss some opportunities. Fine-tune parameters to lower the reversal signal threshold.
2. The Overbought-Oversold Indicator relies solely on one Stoch Indicator and may generate false signals. Add Moving Average (MA) lines etc. for verification.
3. The two strategy signals may cancel each other out, missing trading opportunities. Adjust parameters to reduce constraints.
4. The strategy is only backtested on historical data. Parameters need continuous optimization in live trading. Add stop loss mechanisms to control losses.
5. Parameters need independent testing and optimization for different products and trading periods. Do not directly copy parameters.

## Optimization Directions

The strategy can be further optimized in the following aspects:

1. Optimize parameters for both strategies to form parameter pools for optimization programs under different market conditions.
2. Add filter conditions based on Moving Averages (MA), Bollinger Bands, etc., to avoid false signals.
3. Add stop loss mechanisms such as trailing stops, moving stops, and time-based stops to control maximum drawdown.
4. Consider adding filters on volume or positions for different products to avoid low liquidity issues.
5. Study the evolution of parameters over time and use machine learning techniques to automatically optimize them.
6. Optimize entry frequency to avoid overtrading in trendless markets.

## Conclusion

The Dual-Trend-Tracking Strategy accurately identifies trend reversals by combining the 123 Reversal Strategy with the Overbought-Oversold Indicator, ensuring that it filters out false signals and captures actual trends for excess returns. Compared to single-indicator strategies, this strategy offers higher stability and profitability. However, risk control measures such as stop losses should be implemented, and parameters need ongoing testing and optimization in real trading environments. Future improvements can include parameter optimization, adding filter conditions, and automation to enhance the performance of the strategy.