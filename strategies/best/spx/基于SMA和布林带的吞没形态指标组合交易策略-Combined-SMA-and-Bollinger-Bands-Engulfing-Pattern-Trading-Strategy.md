> Name

Combined-SMA-and-Bollinger-Bands-Engulfing-Pattern-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/153e8a098bd3806f243.png)

[trans]
#### Overview
This strategy is a trend-following trading system that combines Moving Average (SMA), Bollinger Bands (BB), and candlestick patterns. It primarily identifies trading signals through engulfing patterns, confirmed by the 200-day moving average and Bollinger Bands middle line, while implementing a 1:2 risk-reward ratio for risk management.

#### Strategy Principles
The core logic relies on the combination of multiple technical indicators to confirm trading signals. Specifically:
1. Uses 200-day SMA to determine the overall trend direction
2. Employs Bollinger Bands middle line as secondary trend confirmation
3. Identifies specific entry points through engulfing patterns
4. Implements a fixed 1:2 risk-reward ratio for stop-loss and take-profit levels

The system enters long positions when bullish engulfing patterns appear above both the 200-day SMA and Bollinger Bands middle line. Conversely, it enters short positions when bearish engulfing patterns form below these levels.

#### Strategy Advantages
1. Multiple technical indicators increase signal reliability
2. Uses classic trend-following indicators that are easy to understand and implement
3. Fixed risk-reward ratio promotes long-term profitable trading
4. Clear entry and exit rules minimize subjective judgment
5. Combines trend and momentum analysis for improved success rate

#### Strategy Risks
1. May generate frequent false signals in ranging markets
2. SMA and Bollinger Bands are lagging indicators, potentially missing opportunities
3. Fixed risk-reward ratio might not suit all market conditions
4. Stop-loss levels may be wide in highly volatile markets
5. Requires a large sample size to demonstrate strategy effectiveness

#### Strategy Optimization
1. Consider implementing dynamic risk-reward ratios based on market volatility
2. Add volume indicators for additional confirmation
3. Incorporate additional technical indicators to filter false signals
4. Optimize entry timing through multi-timeframe signal coordination
5. Introduce adaptive indicator parameters to improve strategy flexibility

#### Summary
This is a well-structured trend-following strategy with clear logic. The combination of moving averages, Bollinger Bands, and engulfing patterns ensures reliable trading signals while providing explicit risk management methods. Despite some inherent lag, it represents a highly operable trading system with controllable risk.

#### Source (PineScript)

```pinescript
/*backtest
start: 2025-01-08 00:00:00
end: 2025-02-07 00:00:00
period: 3h
basePeriod: 3h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © ardhankurniawan

//@version=5
//@version=5
strategy("Engulfing Candles Strategy with Risk-Reward 1:2 by ardhankurniawan", overlay = true)

// Store the opening and closing prices of the previous and current bars
openBarPrevious = open[1]
closeBarPrevious = close[1]
openBarCurrent = open
closeBarCurrent = close

// Calculate the 200-day SMA
sma200 = ta.sma(close, 200)

// Calculate Bollinger Bands (BB) with a period of 14 and standard deviation of 2
length = 14
src = close
mult = 2.0
basis = ta.sma(src, length)  // Middle Bollinger Band (SMA)
dev = mult * ta.stdev(src, length)  // Standard deviation
upperBB = basis + dev
lowerBB = basis - dev
midBB = basis  // Middle Bollinger Band is the SMA

// Bullish Engulfing condition: current open price is lower than previous close, 
// current open price is lower than previous open, and current close is higher than previous open.
bullishEngulfing = (openBarCurrent <= closeBarPrevious) and (openBarCurrent < openBarPrevious) and (closeBarCurrent > openBarPrevious)

// Bearish Engulfing condition: current open price is higher than previous close, 
// current open price is higher than previous open, and current close is lower than previous open.
bearishEngulfing = (openBarCurrent >= closeBarPrevious) and (openBarCurrent > openBarPrevious) and (closeBarCurrent < openBarPrevious)

// Buy condition only if Bullish Engulfing occurs above the 200-day SMA and Middle Bollinger Band
buyCondition = bullishEngulfing and close > sma200 and close > midBB

// Sell condition only if Bearish Engulfing occurs below the 200-day SMA and Middle Bollinger Band
sellCondition = bearishEngulfing and close < sma200 and close < midBB

// Calculate Stop Loss and Take Profit with a 1:2 risk-reward ratio
longSL = low  // SL at the low of the bullish engulfing candle (previous low)
longRR = (close - low) * 2  // TP with a 1:2 risk-reward ratio
longTP = close + longRR  // TP for long positions

shortSL = high  // SL at the high of the bearish engulfing candle (previous high)
shortTP = shortSL - (shortSL - close) * 2  // TP for short positions
```