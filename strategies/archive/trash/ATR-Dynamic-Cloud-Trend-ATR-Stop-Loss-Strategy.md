> Name

Dynamic Cloud Trend ATR Stop-Loss Strategy - Dynamic-Cloud-Trend-ATR-Stop-Loss-Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d7f5063ddf03108ace39.png)
![IMG](https://www.fmz.com/upload/asset/2d85e457c3068a813af63.png)


#### Overview
This strategy is a comprehensive trading system that combines the Ichimoku Cloud and Average True Range (ATR). It identifies market trends through cloud components while using ATR to dynamically adjust stop-loss positions, achieving an organic combination of trend following and risk management. The strategy integrates market information from both momentum and volatility dimensions, providing a comprehensive analytical framework for trading decisions.

#### Strategy Principles
The core logic is built upon the five lines of the Ichimoku Cloud and the ATR indicator. The system triggers trading signals through the crossover of the Conversion Line (Tenkan-Sen) and Base Line (Kijun-Sen), while requiring price to be on the correct side of the cloud (Senkou Span A and B) and confirmation from the Lagging Span (Chikou Span). Specifically:
- Long conditions: Conversion Line crosses above Base Line, price above the cloud, Lagging Span above current close
- Short conditions: Conversion Line crosses below Base Line, price below the cloud, Lagging Span below current close
- Stop-loss setting: Dynamically adjusted through ATR multiplier, default at 1.5x ATR
- Exit conditions: Reverse crossing signals or change in Lagging Span position

#### Strategy Advantages
1. Multi-dimensional confirmation: Combines market information from trend, momentum, and volatility dimensions, improving signal reliability
2. Dynamic risk management: ATR-based stop-loss adjusts automatically with market volatility, avoiding fixed stop-loss drawbacks
3. Systematic operation: Clear strategy rules maintain trading consistency and discipline
4. Visual intuition: Cloud visualization allows traders to intuitively understand market structure
5. High adaptability: Adjustable parameters can adapt to different market environments

#### Strategy Risks
1. Lag risk: Ichimoku Cloud indicators have inherent lag, potentially leading to delayed entries
2. Ranging market risk: May generate false breakout signals in sideways markets
3. Parameter sensitivity: Different timeframe parameter settings significantly affect strategy performance
4. Stop-loss range: ATR multiplier selection requires balance between protection and profit potential
5. Signal frequency: Strict entry conditions may result in relatively fewer trading opportunities

#### Strategy Optimization Directions
1. Introduce trend strength filtering: Add indicators like ADX to measure trend strength and filter weak trend environments
2. Optimize stop-loss mechanism: Consider setting stops at cloud edges or significant support/resistance levels
3. Add time filtering: Avoid high volatility periods during major economic data releases
4. Include volume confirmation: Add volume as supplementary signal confirmation
5. Develop partial position management: Adjust position sizes based on signal strength and market conditions

#### Summary
The Dynamic Cloud Trend ATR Stop-Loss Strategy is a complete trading system integrating classical technical analysis tools. It identifies trends through the Ichimoku Cloud's multiple confirmation mechanism and implements dynamic risk control using ATR, providing traders with a systematic decision-making framework. While the strategy has certain lag and parameter sensitivity issues, it can achieve stable performance in trending markets through proper optimization and risk management. The strategy's visualization features and clear rules make it particularly suitable for investors wanting to practice systematic trading.

``` pinescript
/*backtest
start: 2024-09-01 00:00:00
end: 2025-02-18 00:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"TRB_USDT"}]
*/

//@version=5
strategy("Ichimoku Cloud + ATR Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === Inputs ===
conversionPeriods = input.int(9, title="Tenkan-sen Period", minval=1)
basePeriods = input.int(26, title="Kijun-sen Period", minval=1)
laggingSpan2Periods = input.int(52, title="Senkou Span B Period", minval=1)
displacement = input.int(26, title="Displacement", minval=1)
atrLength = input.int(14, title="ATR Period", minval=1)
atrMultiplier = input.float(1.5, title="ATR Multiplier for Stop-Loss", minval=0.1, step=0.1)

// === Indicator Calculations ===
// Ichimoku Cloud
tenkan = (ta.highest(high, conversionPeriods) + ta.lowest(low, conversionPeriods)) / 2
kijun = (ta.highest(high, basePeriods) + ta.lowest(low, basePeriods)) / 2
senkouSpanA = ta.sma(high, conversionPeriods) + ta.sma(low, conversionPeriods)
senkouSpanB = ta.sma(high, basePeriods) + ta.sma(low, basePeriods)
cloudHigh = (tenkan + kijun) / 2
cloudLow = (tenkan + kijun) / 2

// ATR Stop-Loss Calculation
atrValue = ta.atr(atrLength)

// === Strategy Logic ===
longCondition = ta.crossover(tenkan, kijun) and close > cloudHigh and chikou > close
shortCondition = ta.crossunder(tenkan, kijun) and close < cloudLow and chikou < close

if (longCondition)
    strategy.entry("Long", strategy.long)

if (shortCondition)
    strategy.entry("Short", strategy.short)

// === Stop Loss Logic ===
stopLossValue = atrValue * atrMultiplier
strategy.exit("Stop Loss - Long", from_entry="Long", stop=cloudHigh + stopLossValue)
strategy.exit("Stop Loss - Short", from_entry="Short", stop=cloudLow - stopLossValue)
```