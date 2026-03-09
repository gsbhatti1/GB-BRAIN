> Name

Multi-Level-Dynamic-Cost-Averaging-Swing-Trading-Strategy-Based-on-RSI-and-ATR

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8c3db001f80f0759332.png)
![IMG](https://www.fmz.com/upload/asset/2d89dd93f05711f19000e.png)

#### Overview
This strategy is a multi-level dynamic cost averaging (DCA) trading system that combines the Relative Strength Index (RSI) and Average True Range (ATR). It primarily identifies oversold market conditions for staged position building while using ATR to dynamically adjust take-profit levels for swing trading profits. The strategy features risk diversification, cost optimization, and stable returns.

#### Strategy Principles
The strategy operates on 4-hour or daily timeframes, with core logic including:
1. Entry signals based on RSI below 30 indicating oversold conditions, allowing up to 4 staged entries
2. Position sizing based on $200 total risk amount, calculating holdings dynamically using 2x ATR
3. Position management using dynamic average cost tracking, calculating real-time average price after multiple entries
4. Take-profit set at 3x ATR above average price, adapting to market volatility
5. Real-time display of average price and take-profit levels through marker lines for visual tracking

#### Strategy Advantages
1. Precise Risk Control - Achieves exact control of single trade risk through preset risk amount and ATR adjustment
2. Flexible Position Building - Staged entry mechanism reduces cost while fully capturing opportunities
3. Intelligent Take-Profit - Dynamic take-profit based on ATR ensures profits while adapting to market volatility
4. Strong Visualization - Real-time display of average price and take-profit lines provides intuitive trading reference
5. Good Adaptability - Strategy parameters can be flexibly adjusted for different market characteristics

#### Strategy Risks
1. Continuous Oversold Risk - Sustained market decline may lead to excessive entries
Solution: Strictly enforce maximum entry limit, set stop-loss when necessary
2. Take-Profit Setting Risk - Excessive take-profit multiplier may miss profit opportunities
Solution: Dynamically adjust ATR multiplier based on market characteristics
3. Capital Management Risk - Staged entries may occupy excessive capital
Solution: Set reasonable risk limits and position sizes

#### Strategy Optimization Directions
1. Entry Signal Optimization
- Add trend judgment indicators to avoid early entries in strong downtrends
- Incorporate volume indicators to improve oversold judgment reliability
2. Take-Profit Mechanism Improvement
- Introduce trailing stop mechanism for better profit locking
- Consider staged profit-taking for increased flexibility
3. Risk Control Enhancement
- Add overall drawdown control
- Optimize capital allocation algorithm

#### Summary
The strategy achieves a trading system balancing risk control and stable returns through the combination of RSI and ATR indicators. The staged entry mechanism provides cost optimization possibilities, while the dynamic take-profit design ensures reasonable profit realization. Although some potential risks exist, the strategy's overall performance will be further improved through appropriate parameter settings and implementation of optimization directions.

#### Source (PineScript)

```pinescript
//@version=6
strategy("DCA-Based Swing Strategy (Risk $200) with Signals", overlay=true)

// === Main Indicators ===
// RSI for identifying oversold conditions
rsi = ta.rsi(close, 14)

// ATR for volatility estimation
atr = ta.atr(14)

// === Strategy Parameters ===
// Risk management
riskPerTrade = 200                       // Total risk ($200)
atrRisk = 2 * atr                        // Risk in dollars per buy (2 ATR)
positionSize = riskPerTrade / atrRisk    // Position size (shares)

// DCA Parameters
maxEntries = 4                           // Maximum of 4 buys
takeProfitATR = 3                        // Take profit: 3 ATR

// === Position Management ===
var float avgEntryPrice = na             // Average entry price
var int entryCount = 0                   // Number of buys
var line takeProfitLine = na             // Take profit line
var line avgPriceLine = na               // Average entry price line

// === Buy and Sell Conditions ===
buyCondition = rsi < 30 and entryCount < maxEntries  // Buy when oversold
if (buyCondition)
    strategy.entry("DCA Buy", strategy.long, qty=positionSize)
    
    // Update the average entry price
    avgEntryPrice := na(avgEntryPrice) ? close : (avgEntryPrice * entryCount + close) / (entryCount + 1)
    entryCount += 1

    // Display "BUY" signal on the chart
    label.new(bar_index, low, "BUY", style=label.style_label_up, color=color.green)
```

This PineScript code implements the described strategy, using RSI and ATR to manage entries and exits, and dynamically adjusting take-profit levels based on ATR.