> Name

Dynamic-Volatility-Adjusted-Dual-Moving-Average-Crossover-System-with-RSI-ATR-Composite-Filter

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d933ad313ea6450ac8d0.png)
![IMG](https://www.fmz.com/upload/asset/2d832437766cdd85d5739.png)

#### Strategy Overview
This strategy is a composite trading system combining dual moving average crossover, RSI overbought/oversold, and ATR volatility filtering. The system generates trading signals using short-term and long-term moving averages, filters market conditions through RSI indicators, assesses volatility using ATR, and implements position management and risk control through percentage-based stop-loss and risk-reward ratios. The strategy demonstrates strong adaptability and can flexibly adjust parameters based on market conditions.

#### Strategy Principles
The core logic of the strategy is based on the following aspects:
1. Signal Generation: Captures trend changes using crossovers of 9-day and 21-day simple moving averages. Long signals are generated when the short-term MA crosses above the long-term MA, and short signals when it crosses below.
2. Condition Filtering: Filters overbought/oversold conditions using RSI indicator to avoid entering trades in extreme market conditions. Uses ATR indicator to ensure market volatility meets trading criteria.
3. Risk Management: Employs percentage-based stop-loss relative to account equity, determines take-profit levels through risk-reward ratios to achieve reasonable returns while hedging risks.

#### Strategy Advantages
1. Strong System Adaptability: Strategy can flexibly adjust to different market environments through enabling/disabling RSI and ATR filters.
2. Comprehensive Risk Control: Effectively controls risk exposure per trade through percentage-based stop-loss and dynamic position management.
3. High Signal Reliability: Reduces impact of false signals through multiple filtering mechanisms, improving trade success rate.
4. Strong Parameter Adjustability: All parameters can be optimized and adjusted according to specific market characteristics.

#### Strategy Risks
1. Ranging Market Risk: Moving average crossovers may generate frequent false signals in sideways markets.
2. Lag Risk: Moving averages have inherent lag, potentially missing optimal entry points.
3. Parameter Optimization Risk: Over-optimization may lead to strategy overfitting, affecting live trading performance.
4. Market Environment Dependency: Strategy performs better in trending markets but may underperform in other market conditions.

#### Strategy Optimization Directions
1. Dynamic Parameter Adjustment: Automatically adjust MA periods and RSI thresholds based on market volatility.
2. Add Trend Strength Filtering: Introduce DMI or ADX indicators to evaluate trend strength.
3. Optimize Stop-Loss Methods: Consider implementing trailing stops or ATR-based dynamic stop-losses.
4. Improve Position Management: Introduce volatility-based dynamic position sizing system.

#### Summary
The strategy constructs a relatively complete trading system by combining multiple technical indicators. It performs excellently in trending markets and demonstrates good risk control capabilities. Through proper parameter settings and necessary filtering conditions, the strategy can adapt to different market environments. Thorough backtesting and parameter optimization are recommended before live implementation.

||

``` pinescript
/*backtest
start: 2025-01-21 00:00:00
end: 2025-02-20 00:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"SOL_USDT"}]
*/

//@version=5
strategy("Simplified MA Crossover Strategy with Disable Options", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// Inputs
shortLength = input.int(9, title="Short MA Length", minval=1)
longLength = input.int(21, title="Long MA Length", minval=1)

// RSI Filter
enableRSI = input.bool(true, title="Enable RSI Filter")
rsiLength = input.int(14, title="RSI Length", minval=1)
rsiOverbought = input.int(70, title="RSI Overbought Level", minval=50, maxval=100)
rsiOversold = input.int(30, title="RSI Oversold Level", minval=0, maxval=50)

// ATR Filter
enableATR = input.bool(true, title="Enable ATR Filter")
atrLength = input.int(14, title="ATR Length", minval=1)
minATR = input.float(0.005, title="Minimum ATR Threshold", minval=0)

// Risk Management
stopLossPerc = input.float(0.5, title="Stop Loss (%)", minval=0.1) / 100
riskRewardRatio = input.float(2, title="Risk-Reward Ratio", minval=1)
riskPercentage = input.float(2, title="Risk Percentage", minval=0.1) / 100

// Indicators
shortMA = ta.sma(close, shortLength)
longMA = ta.sma(close, longLength)
rsi = ta.rsi(close, rsiLength)
atr = ta.atr(atrLength)

// Conditions
longCondition = ta.crossover(shortMA, longMA)
shortCondition = ta.crossunder(shortMA, longMA)

if (enableRSI and enableATR) 
    // RSI Condition
    if ((rsi <= rsiOversold or rsi >= rsiOverbought))
        if (enableATR and atr >= minATR) 
            if (longCondition)
                strategy.entry("Long", strategy.long)
            elif shortCondition
                strategy.close("Long")

// Plotting
plot(shortMA, color=color.blue, title="Short MA")
plot(longMA, color=color.red, title="Long MA")
hline(rsiOversold, "RSI Oversold Level", color=color.green)
hline(rsiOverbought, "RSI Overbought Level", color=color.orange)
```

Note: The code block was continued from where it was left off in the original text.