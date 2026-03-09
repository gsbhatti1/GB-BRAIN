> Name

Adaptive-Trend-Detection-Strategy-with-Dual-Envelope-EMA-System-基于双包络EMA系统的自适应趋势检测策略

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1416bcbc2a64a9f99ae.png)

#### Overview
This strategy is an innovative trend detection system based on dual Exponential Moving Average (EMA) envelope calculations. It analyzes multidimensional price characteristics to calculate real-time bull-bear power comparisons, identifying market trend changes and persistence. The strategy's main feature is its adaptability, allowing dynamic adjustment of signal strength based on market conditions.

#### Strategy Principles
The core principle relies on complex EMA envelope calculations to measure market forces. Specifically:
1. Constructs upper and lower EMA envelopes using open and close prices
2. Derives bullish and bearish power indicators through mathematical calculations
3. Computes a signal line as a supplementary trend confirmation indicator
4. Generates long signals when bullish power exceeds bearish power, and vice versa

#### Strategy Advantages
1. Strong Adaptability - Automatically adjusts sensitivity based on market volatility
2. Stable Signals - Multiple indicator confirmation reduces false signals
3. Comprehensive Risk Control - Built-in money management system limits position sizes
4. Excellent Visualization - Separate panel clearly displays all indicators
5. Flexible Parameters - Adjustable cycle parameters for different market characteristics

#### Strategy Risks
1. Trend Reversal Risk - Potential signal lag in highly volatile markets
2. Money Management Risk - Requires proper initial capital and trading ratio settings
3. Market Adaptability Risk - Parameters need adjustment in different market environments
4. Technical Implementation Risk - Requires stable and accurate calculation processes

#### Optimization Directions
1. Add volatility filters to adjust signal sensitivity during high volatility periods
2. Incorporate volume indicators as confirmation systems
3. Optimize money management with dynamic position sizing
4. Add trend strength filters to improve signal quality
5. Develop adaptive parameter optimization systems

#### Summary
This is a scientifically-based trend following strategy that effectively captures market trends through advanced technical indicator design and strict risk control. The strategy's core strengths lie in its adaptability and reliability, maintaining stable performance across different market environments through proper parameter optimization and risk management.

---

#### Source (PineScript)

```pinescript
/*backtest
start: 2024-02-19 00:00:00
end: 2024-11-14 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This work is licensed under a Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
// https://creativecommons.org/licenses/by-nc-sa/4.0/
// © alexgrover
//
// Original post: 
// https://alpaca.markets/learn/andean-oscillator-a-new-technical-indicator-based-on-an-online-algorithm-for-trend-analysis/

//@version=5
strategy(title="Andean Oscillator [Strategy]",
     shorttitle="AndeanOsc_Strategy",
     overlay=false,              // Can be displayed in a separate window
     initial_capital=10000,      // Initial capital
     default_qty_type=strategy.percent_of_equity,
     default_qty_value=100,      // Use 100% of the account for one trade
     pyramiding=0)               // Do not increase position size

//------------------------------------------------------------------------------
// Inputs
//------------------------------------------------------------------------------
length     = input.int(50, "Length")
sig_length = input.int(9, "Signal Length")

//------------------------------------------------------------------------------
// Calculation of Andean Oscillator
//------------------------------------------------------------------------------
var float alpha = 2.0 / (length + 1)

// Variables must be declared as `var` to maintain state
var float up1 = 0.
var float up2 = 0.
var float dn1 = 0.
var float dn2 = 0.

C = close
O = open

// Calculation of EMA bands
up1 := nz(math.max(C, O, up1[1] - (up1[1] - C) * alpha), C)
up2 := nz(math.max(C * C, O * O, up2[1] - (up2[1] - C * C) * alpha), C * C)

dn1 := nz(math.min(C, O, dn1[1] + (C - dn1[1]) * alpha), C)
dn2 := nz(math.min(C * C, O * O, dn2[1] + (C * C - dn2[1]) * alpha), C * C)

// Bullish and bearish components
bull   = math.sqrt(dn2 - dn1 * dn1)
bear   = math.sqrt(up2 - up1 * up1)

// Signal = EMA of max(bull, bear)
signal = ta.ema(math.max(bull, bear), sig_length)

//------------------------------------------------------------------------------
// Simple STRATEGY LOGIC (for demonstration only)
//------------------------------------------------------------------------------
// Example: 
// - If bull > bear, enter long (bullish power greater than bearish)
// - If bear > bull, enter short (bearish power greater than bullish)
//
// With pyramiding=0, a new position is opened only when the opposite signal arrives – no additional positions are added.
```