> Name

Quantitative-Trading-Strategy-Based-on-Three-Consecutive-Bullish-Bearish-Candles-and-Dual-Moving-Averages

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/af52f95d89308db335.png)
[trans]

## Strategy Overview

This strategy is based on the pattern of three consecutive bullish/bearish candles and a dual moving average system. By judging the change in body size of three consecutive candles and the crossover signals of the moving average system, it generates buy or sell signals at the close of the third candle to capture potential trend turning points and price reversal opportunities.

## Strategy Principle

1. Calculate the body size of three consecutive candles and determine if they show an increasing trend.
2. If the bodies of three consecutive candles increase in size and the third candle closes bullish, a buy signal is generated; if the bodies of three consecutive candles increase in size and the third candle closes bearish, a sell signal is generated.
3. Introduce two moving averages of 50-day and 200-day periods, representing medium-short term and long-term trends respectively.
4. Plot buy/sell signals and the two moving averages on the chart to visually demonstrate the strategy logic and trend status.
5. Execute corresponding entry operations based on the buy/sell signals.

The core of this strategy lies in capturing the starting point of a trend through the three consecutive bullish/bearish candle pattern, while using the dual moving average system to verify trend strength and direction. The combination of these two dimensions aims to effectively enter positions at the beginning of a trend and reduce the risk of counter-trend trading.

## Strategy Advantages

1. The three consecutive bullish/bearish candle pattern is a strong bullish/bearish signal, representing the continuous strengthening of long/short forces and providing momentum for trend continuation.
2. The dual moving average system can effectively verify the direction and strength of the trend. When the short-term moving average crosses above/below the long-term moving average, it indicates that the trend is starting to strengthen/weaken.
3. The two dimensions corroborate each other, forming a relatively reliable entry signal that helps improve the strategy's win rate and profit/loss ratio.
4. The chart annotations are intuitive and clear, making it easy to track the strategy's execution and trend evolution.

## Strategy Risks

1. Market noise and fluctuations may lead to frequent false signals, resulting in unstable strategy performance.
2. Sudden trend reversals or accelerations may cause the strategy's entry timing to be less than ideal, exposing it to additional risk.
3. Lack of explicit take-profit, stop-loss, and position management rules may cause the strategy's drawdown and maximum loss to exceed expectations.

## Optimization Directions

1. Fine-tune the definition of the three consecutive bullish/bearish candle pattern, such as considering additional conditions like the amplitude, length, and color of consecutive candles, to improve signal accuracy.
2. Introduce more moving average period parameters, such as 5-day, 10-day, 20-day, etc., to construct a multi-moving average system and enrich the dimensions of trend judgment.
3. Based on the entry signals, set reasonable take-profit and stop-loss levels and position management rules, such as fixed ratio take-profit/stop-loss, percentage take-profit/stop-loss, trailing stop-loss, etc., to control the risk exposure of a single trade.
4. Consider adding volume indicators, such as volume-price divergence, volume breakouts, etc., to further validate trend turning points and improve the reliability of entry signals.

## Strategy Summary

By combining the classic three consecutive bullish/bearish candle pattern with a dual moving average system, this strategy aims to capture the starting point of a trend and profit from potential price spreads at the beginning of the trend. Its advantages lie in clear signals, simple logic, and ease of implementation and optimization; at the same time, it also has potential risks and room for improvement, such as frequent trading, unstable signals, and insufficient risk control. In the future, we can start from aspects like signal filtering, position management, take-profit/stop-loss, etc., to continuously enrich and strengthen the overall performance of this strategy and provide more references for quantitative trading practice.

||

## Source (PineScript)

```pinescript
//@version=4
strategy("Consecutive Candles with MAs", shorttitle="CCMAs", overlay=true)

// Calculate the size of the bodies of three consecutive candles and determine if they show an increasing trend.
var int bull_candle_count = 0
if close[0] > open[0] and close[1] > open[1] and close[2] > open[2]
    bull_candle_count := 3
else if close[0] < open[0] and close[1] < open[1] and close[2] < open[2]
    bull_candle_count := -3
else
    bull_candle_count := 0

// Plot buy/sell signals and the two moving averages on the chart.
plotshape(series=bull_candle_count > 0, location=location.belowbar, color=color.green, style=shape.labelup, title="Buy Signal")
plotshape(series=bull_candle_count < 0, location=location.abovebar, color=color.red, style=shape.labeldown, title="Sell Signal")

// Introduce two moving averages of 50-day and 200-day periods.
ma50 = ta.sma(close, 50)
ma200 = ta.sma(close, 200)

// Plot the two moving averages.
plot(ma50, title="50-day MA", color=color.blue)
plot(ma200, title="200-day MA", color=color.orange)
```

[/trans]