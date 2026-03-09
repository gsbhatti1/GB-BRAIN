<!-- AUTO-TRANSLATE FAILED: the JSON object must be str, bytes or bytearray, not NoneType -->


> Name

Momentum-Strategy-Based-on-LazyBears-Squeeze

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/d52d9dda4ac8ef2680.png)
[trans]

## Overview

The main idea of this strategy is based on LazyBear's Squeeze Momentum indicator to analyze the timing of buying and selling. It analyzes the inflection points in the momentum trend, locating peaks and troughs as sell and buy signals respectively. As it is a long strategy, it also takes into consideration the 50-period Exponential Moving Average to identify upward trends. If the closing price of the candle is above the 50-day EMA, and the 50-day EMA is trending upwards, then the buy signal is executed.

## Strategy Principle

This strategy incorporates Bollinger Bands and Keltner Channels to identify trends and squeeze zones. Specifically, it calculates a 20-period Bollinger Bands and 20-period Keltner Channels. When Bollinger Bands fall entirely within the Keltner Channels, it is viewed as a squeeze signal. The squeeze zone is identified when the Bollinger Bands lower band goes above the Keltner Channels lower band and the Bollinger Bands upper band goes below the Keltner Channels upper band. Conversely, when the Bollinger Bands lower band falls below the Keltner Channels lower band and the Bollinger Bands upper band rises above the Keltner Channels upper band, it is a non-squeeze zone.

In addition, the strategy utilizes linear regression to analyze the change in momentum slope. It calculates the linear regression value of price over the last 20 periods minus the typical price. When the slope of the linear regression value is positive, it is viewed as an upward trend. When the slope is negative, it is a downward trend. Within the squeeze zone, if there is a reversal in the momentum slope, it signals a buy or sell. Specifically, when within the squeeze zone, a momentum flip from positive to negative issues a sell signal. And when within the squeeze zone, a momentum flip from negative to positive issues a buy signal.

To filter out false signals, the strategy also judges if the closing price is above the 50-day EMA and if the 50-day EMA is in an upward slope. Only when both conditions are met will the buy signal be executed.

## Advantage Analysis

This is a very clever strategy, utilizing two different types of indicators to make a multi-dimensional judgment of the market, which can effectively avoid false signals. Specifically, its advantages include:

1. Comprehensive application of Bollinger Bands, Keltner Channels and momentum indicators for multi-dimensional analysis, improving accuracy.
2. Squeeze zones can effectively identify peaks and troughs of momentum reversals, precisely capturing turns.
3. Trend filtering based on closing price and 50-day EMA avoids repetitive opening of positions during consolidations.
4. Signals only emitting during squeeze zones reduce false signals and improve profitability rate.
5. Large parameter optimization space allows targeted optimizations via adjusting periods, etc.
6. Long and short combined, considers large cycle trends and integrates medium-term indicators, long direction is clear.

## Risk Analysis

Although this strategy has incorporated multiple technical indicators, there are still some risks:

1. Missing buy/sell opportunities when Bollinger Bands and Keltner Channels diverge.
2. Large losses may occur during violent market rises or falls.
3. In high volatility markets, squeeze situations may not be obvious, resulting in fewer signals.
4. Prone to adjustment losses during bull-bear transitions.

To avoid these risks, we can take the following measures:

1. Optimize parameters to synchronize Bollinger Bands and Keltner Channels as much as possible.
2. Set stop loss levels to control single loss.
3. Use this strategy as part of a portfolio strategy, combined with other strategies.
4. Reduce positions appropriately during high volatility markets.

## Optimization Directions

There is still large room for optimizing this strategy, mainly in the following directions:

1. Optimize periods of Bollinger Bands and Keltner Channels to synchronize them as much as possible.
2. Test different multiplier factors to find optimal parameter combinations.
3. Try adding other indicators for confirmation, such as RSI.
4. Use models like the Cultural Five Color Line to determine market phases selectively before applying this strategy.
5. Employ machine learning methods dynamically optimizing parameters.
6. Backtest on different cryptocurrencies to find the most suitable trading pairs.
7. Explore the effectiveness of this strategy in longer time frames (daily, weekly, etc.).

## Summary

The LazyBear pressure-based momentum strategy comprehensively applies multiple technical indicators to precisely identify momentum reversals for trading during squeeze zones, avoiding frequent opening of positions in non-trending markets. It systemically defines quantitative buy and sell rules, showing excellent performance in backtests. By optimizing parameter settings and introducing new judgment indicators, this strategy has significant room for improvement and is well worth in-depth study and application by quantitative traders.

|| 

## Summary

The main idea of this strategy is based on LazyBear's Squeeze Momentum indicator to analyze the timing of buying and selling. It identifies peaks and troughs as sell and buy signals respectively within momentum trends, aiming to execute buy signals when the 50-day EMA is trending upwards and the closing price of the candle is above it.

## Strategy Principle

This strategy incorporates Bollinger Bands and Keltner Channels to identify trends and squeeze zones. Specifically, a 20-period Bollinger Bands and 20-period Keltner Channels are calculated. When the Bollinger Bands fully fall within the Keltner Channels, this is considered a squeeze signal. A squeeze zone is identified when the lower band of the Bollinger Bands goes above the lower band of the Keltner Channels while the upper band of the Bollinger Bands falls below the upper band of the Keltner Channels. Conversely, if the lower band of the Bollinger Bands falls below the lower band of the Keltner Channels and the upper band of the Bollinger Bands rises above the upper band of the Keltner Channels, this is a non-squeeze zone.

In addition, linear regression is used to analyze changes in momentum slope. The strategy calculates the linear regression value of price over the last 20 periods minus the typical price. If the slope of the linear regression value is positive, it indicates an upward trend; if negative, it signifies a downward trend. Within the squeeze zone, any reversal in the momentum slope acts as a buy or sell signal. Specifically, when within the squeeze zone and momentum shifts from positive to negative, a sell signal is issued. Conversely, when within the squeeze zone and momentum transitions from negative to positive, a buy signal is generated.

To filter out false signals, the strategy also checks if the closing price of the candle is above the 50-day EMA and if the slope of the 50-day EMA is upward. Only when both conditions are met will a buy signal be executed.

## Advantage Analysis

This is a very smart strategy that uses two different types of indicators to make multi-dimensional market judgments, effectively avoiding false signals. Specifically, its advantages include:

1. Comprehensive use of Bollinger Bands, Keltner Channels, and momentum indicators for multidimensional analysis, enhancing accuracy.
2. Squeeze zones can accurately identify the peaks and troughs of momentum reversals, precisely capturing turning points.
3. Trend filtering based on closing prices and 50-day EMA prevents repeated opening positions during consolidation periods.
4. Signals only emitted in squeeze zones reduce false signals and increase profitability.
5. Large parameter optimization space allows targeted optimizations by adjusting parameters such as periods.
6. Long-term and short-term combined, considers large cycle trends while integrating medium-term indicators, making the long-term direction clear.

## Risk Analysis

While this strategy incorporates multiple technical indicators, there are still some risks:

1. Missing buy/sell opportunities when Bollinger Bands and Keltner Channels diverge.
2. Large losses may occur during sudden market rises or falls.
3. In highly volatile markets, squeeze situations might not be noticeable, leading to fewer signals.
4. Bull-bear transitions can result in adjustment losses.

To mitigate these risks, we can take the following measures:

1. Optimize parameters to synchronize Bollinger Bands and Keltner Channels as much as possible.
2. Set stop loss levels to control single loss.
3. Integrate this strategy into a portfolio of strategies combined with other approaches.
4. Reduce positions appropriately during high volatility periods.

## Optimization Directions

There is still significant room for optimizing this strategy, mainly in the following directions:

1. Optimize Bollinger Bands and Keltner Channel periods to achieve synchronization as much as possible.
2. Test different multiplier factors to find optimal parameter combinations.
3. Consider adding other indicators such as RSI for confirmation.
4. Use models like the Cultural Five Color Line to determine market phases selectively before applying this strategy.
5. Employ machine learning methods dynamically optimizing parameters.
6. Backtest on different cryptocurrencies to find the most suitable trading pairs.
7. Explore the effectiveness of this strategy in longer time frames (daily, weekly, etc.).

## Summary

This LazyBear pressure-based momentum strategy uses multiple technical indicators to identify precise momentum reversals for trading during squeeze zones and avoids frequent opening positions in non-trending markets. It systemically defines quantitative buy and sell rules, showing excellent backtest performance. By optimizing parameter settings and introducing new judgment indicators, the strategy has significant improvement potential and is worth in-depth study and application by quantitative traders.