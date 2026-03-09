> Name

Momentum-Swing-Effective-Profit-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/de670b298f6f52814f.png)
[trans]

#### Overview

The Momentum-Swing-Effective-Profit-Strategy is a quantitative trading strategy designed to capture profitable opportunities in mid-term financial markets by integrating swing trading principles and momentum indicators. The strategy utilizes a combination of technical indicators including moving averages, crossover signals, and volume analysis to generate buy and sell signals. The goal is to identify market trends and capitalize on price momentum for profits.

#### Strategy Logic

The buy signal is determined by multiple factors including A1, A2, A3, XG, and weeklySlope. Specifically:

A1 Condition: Checks for specific price relationships, verifying the ratio of highest price to closing price is less than 1.03, the ratio of opening price to lowest price is less than 1.03, and the ratio of highest price to previous closing price is greater than 1.06. This condition looks for a specific pattern indicating potential bullish momentum.

A2 Condition: Checks for price relationships related to closing price, verifying the ratio of closing price to opening price is greater than 1.05 or the ratio of closing price to previous closing price is greater than 1.05. This condition looks for signs of upward price movement and momentum.

A3 Condition: Focuses on volume, checking if the current volume crosses above the highest volume over the last 60 periods. This condition aims to identify increased buying interests and potentially confirms the strength of the potential upward price movement.

XG Condition: Combines the A1 and A2 conditions and checks if they are true for both the current and previous bars. It also verifies the ratio of closing price to 5-period EMA crosses above the 9-period SMA of the same ratio. This condition helps identify potential buy signals when multiple factors align, indicating strong bullish momentum and potential entry point.

Weekly Trend Factor: Calculates the slope of 50-period SMA on a weekly timeframe. It checks if the slope is positive, indicating an overall upward trend on a weekly basis. This condition provides additional confirmation that the stock is in an upward trend.

When all these conditions are met, the buy condition is triggered, indicating a favorable time to enter a long position.

The sell condition is relatively simple, it simply checks if the closing price crosses below the 10-period EMA. When this condition is met, it indicates a potential reversal or weakening of the upward price momentum, and a sell signal is generated.

#### Advantage Analysis

- Combines swing trading and momentum indicators, integrating different strategy ideas
- Optimizes the combination of multiple technical indicators to identify high probability trading opportunities
- Employs position sizing and stop loss techniques for risk management
- Good backtest results with considerable net profits and win rate

#### Risk Analysis

- More effective in bull market, unable to adapt to bear markets
- False breakouts may lead to wrong trades
- Improper position sizing and stop loss settings may amplify losses
- Parameters need proper adjusting for different market environments

#### Optimization

- Add filtering indicators to improve signal quality
- Optimize stop loss methods like trailing stop loss
- Dynamically adjust position sizing
- Combine machine learning to improve parameter optimization

#### Conclusion

The Momentum-Swing-Effective-Profit-Strategy integrates swing trading principles and momentum indicators through parameter optimization and conditions integration, achieving considerable profits in backtests. It captures mid-term trends well but should be aware of trend reversal risks. Further optimizations may improve its robustness and live performance.

[/trans]

> Source (PineScript)

```pinescript
//@version=5
strategy("Momentum-Swing-Effective-Profit-Strategy", overlay=true)

// Position Status Definition
var inPosition = false

// Moving Average Definition
ma60 = ta.sma(close, 60)

// A1 Condition Definition
A1 = high / close < 1.03 and open / low < 1.03 and high / close[1] > 1.06

// A2 Condition Definition
A2 = close / open > 1.05 or close / close[1] > 1.05

// A3 Condition Definition
highestVol = ta.highest(volume, 60)
A3 = ta.crossover(volume, highestVol[1])

// XG Condition Definition
ema5 = ta.ema(close, 5)
B1 = close / ema5
XG = B1 > ta.sma(B1, 9) and B1[1] <= ta.sma(B1, 9) and close / open > 1.05 and close / close[1] > 1.05

// Weekly Trend Factor
weeklySlope = ta.slope(ta.sma(close, 50), 50, 1)

// Buy Condition
buyCondition = A1 and A2 and A3 and XG and weeklySlope > 0

// Sell Condition
sellCondition = close < ta.sma(close, 10)

// Order Execution
if (buyCondition and not inPosition)
    strategy.entry("Long", strategy.long)
    inPosition := true

if (sellCondition and inPosition)
    strategy.close("Long")
    inPosition := false
```

This PineScript code implements the described strategy, with detailed conditions for buy and sell signals, and incorporates the weekly trend factor for additional confirmation.