> Name

Dynamic-Dual-Moving-Average-Breakthrough-Trading-System

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/6201eca6ab89694b39.png)

[trans]
#### Overview
This is an automated trading strategy system based on dual moving average crossover. The system uses 9-period and 21-period Exponential Moving Averages (EMA) as core indicators, generating trading signals through their crossovers. It incorporates stop-loss and take-profit management, along with a visual interface that displays trading signals and key price levels.

#### Strategy Principle
The strategy employs a fast EMA (9-period) and a slow EMA (21-period) to construct the trading system. Long signals are generated when the fast EMA crosses above the slow EMA, while short signals occur when the fast EMA crosses below the slow EMA. The system automatically sets stop-loss and take-profit levels based on preset percentages for each trade. Position sizing uses a percentage-based approach, defaulting to 100% of account equity.

#### Strategy Advantages
1. Clear Signals: Uses moving average crossovers as trading signals, which are clear and easy to understand
2. Risk Control: Integrated stop-loss and take-profit management system for every trade
3. Visual Support: Provides trade label display featuring entry time, price, stop-loss, and take-profit levels
4. Flexible Parameters: Allows adjustment of EMA periods and risk management parameters to adapt to different market conditions
5. Complete Exit Mechanism: Automatically closes positions on contrary signals to avoid position offsetting

#### Strategy Risks
1. Choppy Market Risk: May generate frequent false breakout signals in sideways markets, leading to consecutive losses
2. Slippage Risk: Actual execution prices may deviate from intended levels during high volatility periods
3. Position Sizing Risk: Default 100% equity allocation may expose the account to excessive risk
4. Signal Lag: EMAs inherently lag price action, potentially missing optimal entry points or causing delayed exits
5. Single Indicator Dependency: Reliance solely on moving average crossovers may ignore other important market information

#### Optimization Directions
1. Add Trend Confirmation: Consider incorporating ADX or trend strength indicators to filter false signals
2. Improve Money Management: Add dynamic position sizing based on market volatility
3. Enhanced Stop-Loss Mechanism: Consider implementing trailing stops to better protect profits
4. Market Environment Filtering: Add volatility indicators to suspend trading in unfavorable conditions
5. Optimize Signal Confirmation: Consider adding volume confirmation or complementary technical indicators

#### Summary
This is a well-designed, logically sound moving average crossover strategy system. By combining EMA crossover signals with risk management mechanisms, the strategy can capture profits in trending markets. While inherent risks exist, the suggested optimizations can further enhance the strategy's stability and reliability. This strategy is particularly suitable for tracking medium to long-term trends and represents a solid choice for patient traders.
[/trans]

> Source (PineScript)

```pinescript
//@version=5
strategy("EMA Cross Strategy", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

// 添加策略参数设置
var showLabels = input.bool(true, "显示标签", group="显示设置")
var stopLossPercent = input.float(5.0, "止损百分比", minval=0.1, maxval=20.0, step=0.1, group="风险管理")
var takeProfitPercent = input.float(10.0, "止盈百分比", step=0.1, group="风险管理")

// EMA参数设置
var emaFastLength = input.int(9, "快速EMA周期", minval=1, maxval=200, group="EMA设置")
var emaSlowLength = input.int(21, "慢速EMA周期", minval=1, maxval=200, group="EMA设置")

// 计算EMA
ema_fast = ta.ema(close, emaFastLength)
ema_slow = ta.ema(close, emaSlowLength)

// 绘制EMA线
plot(ema_fast, "快速EMA", color=color.blue, linewidth=2)
plot(ema_slow, "慢速EMA", color=color.red, linewidth=2)

// 检测交叉
crossOver = ta.crossover(ema_fast, ema_slow)
crossUnder = ta.crossunder(ema_fast, ema_slow)

// 生成交易信号
if (crossOver)
    strategy.entry("Long", strategy.long)
if (crossUnder)
    strategy.entry("Short", strategy.short)

// 设置止盈止损
longTakeProfit = strategy.position_avg_price * (1 + takeProfitPercent / 100)
longStopLoss = strategy.position_avg_price * (1 - stopLossPercent / 100)
shortTakeProfit = strategy.position_avg_price * (1 - takeProfitPercent / 100)
shortStopLoss = strategy.position_avg_price * (1 + stopLossPercent / 100)

strategy.exit("Long Exit", "Long", limit=longTakeProfit, stop=longStopLoss)
strategy.exit("Short Exit", "Short", limit=shortTakeProfit, stop=shortStopLoss)
```
```