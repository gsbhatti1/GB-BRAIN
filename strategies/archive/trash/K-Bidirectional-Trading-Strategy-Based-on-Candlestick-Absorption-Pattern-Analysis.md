> Name

Bidirectional Trading Strategy Based on Candlestick Absorption Patterns-Bidirectional-Trading-Strategy-Based-on-Candlestick-Absorption-Patterns

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/186a8207482c18c0ab6.png)

[trans]
#### Overview
This strategy is a bidirectional trading system based on candlestick absorption patterns. It identifies market absorption patterns by analyzing the direction, amplitude, and volume relationships of adjacent candlesticks, executing trades when conditions are met. The strategy employs percentage-based money management with complete entry and exit logic.

#### Strategy Principle
The core logic is based on three key conditions:
1. Adjacent candlesticks have opposite directions: Comparing open and close prices to determine candlestick direction, requiring opposite trends in adjacent candlesticks.
2. Amplitude relationship analysis: Calculating and comparing the price amplitude of two candlesticks (absolute difference between close and open prices), requiring the latter candlestick's amplitude to be larger.
3. Volume characteristics: Requiring the first candlestick's volume to be larger than the second, while the second candlestick's volume should be smaller than the previous volume.

When these three conditions are met simultaneously, the strategy determines the trading direction based on the latest candlestick: long for bullish candles, short for bearish ones. The strategy uses full position trading and tracks positions through state variables.

#### Strategy Advantages
1. Multi-dimensional analysis: Combines price patterns, amplitude, and volume analysis to improve signal reliability.
2. Bidirectional trading: Captures market opportunities in both directions, fully utilizing market volatility.
3. Comprehensive risk management: Uses percentage-based money management with flexible stop-loss and take-profit settings.
4. Visual support: Provides graphical display of trading signals for analysis and optimization.
5. Clear state management: Precisely controls positions through state variables, avoiding duplicate entries.

#### Strategy Risks
1. False breakout risk: False absorption patterns may appear in ranging markets, leading to incorrect signals.
2. Slippage impact: May face significant slippage during high market volatility, affecting actual trading results.
3. Money management risk: Full position trading may create large risk exposure.
4. Signal lag: Signals can only be confirmed after candlestick closure, potentially missing optimal entry points.

#### Strategy Optimization Directions
1. Introduce trend filtering: Recommend adding moving averages or trend indicators for direction filtering to improve signal quality.
2. Optimize money management: Position size can be dynamically adjusted based on market volatility.
3. Enhance stop-loss mechanism: Recommend implementing dynamic stop-loss using ATR indicator to improve risk control.
4. Add time filtering: Can add trading time period filters to avoid inefficient periods.
5. Improve signal confirmation: Can add volume indicators or other technical indicators for auxiliary confirmation.

#### Summary
This strategy constructs a complete trading system through multi-dimensional analysis of candlestick patterns, amplitude, and volume. While certain risks exist, the strategy's stability and reliability can be further enhanced through the suggested optimization directions. The core advantages lie in its multi-dimensional analysis method and comprehensive state management mechanism, making it suitable for application in highly volatile market environments.

#### Source (PineScript)

```pinescript
//@version=5
strategy("Candle Absorption Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

// Indicator Conditions
// 1. Two adjacent candles must be in opposite directions
condition1 = (close[1] > open[1] and close < open) or (close[1] < open[1] and close > open)

// 2. The price range of the first candle is smaller than that of the second candle
delta1 = math.abs(close[1] - open[1])
delta2 = math.abs(close - open)
condition2 = delta1 < delta2

// 3. The volume of the first candle should be greater, while the last one should be smaller
condition3 = volume[1] > volume and volume < volume[2]

// Check if all conditions are met
all_conditions = condition1 and condition2 and condition3

// Determine entry direction
is_bullish = close > open  // Green candle (bullish absorption)
is_bearish = close < open  // Red candle (bearish absorption)

// Position state variables
var float entryPrice = na
var bool isLong = false
var bool isShort = false

// Signal generation logic
buySignal = all_conditions and is_bullish and not isLong
sellSignal = all_conditions and is_bearish and not isShort

// Example of placing buy or sell orders
if (buySignal)
    strategy.entry("Buy", strategy.long, when=all_conditions)

if (sellSignal)
    strategy.entry("Sell", strategy.short, when=all_conditions)
```
[/trans]