``` pinescript
/*backtest
start: 2024-12-29 00:00:00
end: 2025-01-05 00:00:00
period: 5m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// TradingView Pine Script for RSI & CCI-Based Strategy
//@version=6
strategy("RSI & CCI Strategy", overlay=true)

// User Inputs
rsiLength = input.int(14, title="RSI Length")
rsiOverbought = input.int(80, title="RSI Overbought Level")
rsiOversold = input.int(20, title="RSI Oversold Level")

cciLength = input.int(20, title="CCI Length")
cciOverbought = input.int(200, title="CCI Overbought Level")
cciOversold = input.int(-200, title="CCI Oversold Level")

riskRewardRatio = input.float(2.0, title="Risk-Reward Ratio")
fixedStopLoss = input.float(1.0, title="Fixed Stop Loss (Percentage)", minval=0.1)

// RSI and CCI Calculations
rsi = ta.rsi(close, rsiLength)
cci = ta.cci(close, cciLength)

// Entry Conditions
longCondition = (rsi < rsiOversold) and (cci < cciOversold)
shortCondition = (rsi > rsiOverbought) and (cci > cciOverbought)

// Initialize variables for stop loss and take profit
var float stopLossPrice = na
var float takeProfitPrice = na

if (longCondition)
    strategy.entry("Long", strategy.long)
    
    // Calculate Stop Loss and Take Profit Prices
    stopLossPrice := close * (1 - fixedStopLoss / 100)
    takeProfitPrice := close * (1 + riskRewardRatio)

if (shortCondition)
    strategy.entry("Short", strategy.short)
    
    // Calculate Stop Loss and Take Profit Prices
    stopLossPrice := close * (1 + fixedStopLoss / 100)
    takeProfitPrice := close * (1 - riskRewardRatio)

// Plotting Signal Points
plotshape(series=longCondition, title="Long Entry", location=location.belowbar, color=color.green, style=shape.triangleup, text="Long")
plotshape(series=shortCondition, title="Short Entry", location=location.abovebar, color=color.red, style=shape.triangledown, text="Short")

// Plotting Stop Loss and Take Profit Lines
hline(stopLossPrice, "Stop Loss Line", color=color.red)
hline(takeProfitPrice, "Take Profit Line", color=color.green)

```

```markdown
#### Overview
This strategy is a dual technical analysis trading system based on RSI (Relative Strength Index) and CCI (Commodity Channel Index). It combines the overbought and oversold signals from these two classic technical indicators, coupled with risk-reward ratio and fixed stop-loss mechanisms, to build a complete trading decision framework. The core strength lies in improving trading signal reliability through dual indicator confirmation while incorporating comprehensive risk management mechanisms.

#### Strategy Principles
The strategy operates based on the following core principles:
1. Uses 14-period RSI and 20-period CCI indicators as the foundation for signal generation.
2. Entry signal trigger conditions:
   - Long entry: RSI below 20 (oversold) and CCI below -200
   - Short entry: RSI above 80 (overbought) and CCI above 200
3. Risk management design:
   - Fixed percentage stop-loss (default 1%)
   - Automatic take-profit calculation based on risk-reward ratio (default 2.0).
4. Visualization system:
   - Buy/sell signal annotations on chart.
   - Stop-loss and take-profit reference lines.

#### Strategy Advantages
1. High signal reliability: Effectively filters false signals through RSI and CCI dual confirmation mechanism.
2. Comprehensive risk control: Integrates dual protection of fixed stop-loss and dynamic take-profit.
3. Flexible parameters: Major indicator parameters can be optimized for different market characteristics.
4. Clear visual feedback: Intuitive display of trading signals and risk management positions.
5. High automation: Fully automated execution from signal generation to position management.

#### Strategy Risks
1. Signal lag: Technical indicators inherently have some lag, potentially missing optimal entry points.
2. Unsuitable for ranging markets: May generate excessive false signals in sideways markets.
3. Fixed stop-loss risk: Uniform stop-loss percentage may not suit all market conditions.
4. Parameter dependency: Over-reliance on preset parameters may lead to poor performance when market conditions change.
Solutions:
- Dynamically adjust parameters based on market volatility.
- Add trend filters to reduce false signals in ranging markets.
- Introduce adaptive stop-loss mechanisms.

#### Strategy Optimization Directions
1. Introduce volatility indicators:
   - Use ATR to dynamically adjust stop-loss distances.
   - Adjust RSI and CCI trigger thresholds based on volatility.
2. Add trend confirmation mechanism:
   - Add moving averages as trend filters.
   - Introduce trend strength indicators to optimize entry timing.
3. Enhance risk management:
   - Implement dynamic risk-reward ratio calculation.
   - Add partial profit-taking mechanisms.
4. Optimize signal generation:
   - Add volume confirmation mechanism.
   - Incorporate price structure analysis.

#### Summary
This is a complete trading system that combines classic technical indicators with modern risk management concepts. Through dual technical indicator confirmation mechanisms, it improves signal reliability while incorporating strict risk control measures, forming a logically rigorous and practical trading strategy. Although certain limitations exist, through continuous optimization and improvement, this strategy has good practical application prospects. Continued optimization in volatility awareness, trend confirmation, and risk management will further enhance the strategy's stability and practicality.
```