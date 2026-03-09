---
> Name

Dual-Moving-Average-Trend-Following-Strategy-with-Risk-Management

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1bfc9d0f1ab2bac93ce.png)

[trans]
#### Overview
This strategy is a trend-following trading system based on the crossover of 110-day and 200-day Exponential Moving Averages (EMA). It identifies market trends through the intersection of short-term and long-term EMAs, incorporating stop-loss and take-profit mechanisms for risk control. The system automatically executes long and short positions upon trend confirmation while continuously monitoring position risk.

#### Strategy Principle
The core logic relies on the continuity of price trends, using EMA110 and EMA200 crossovers to capture trend reversal signals. When the shorter-term moving average (EMA110) crosses above the longer-term moving average (EMA200), it signals an uptrend formation, triggering a long position. Conversely, when the shorter-term moving average crosses below the longer-term moving average, it signals a downtrend formation, triggering a short position. For risk management, the strategy sets a 1% stop-loss and 0.5% take-profit level for each position to protect profits and limit potential losses.

#### Strategy Advantages
1. Strong trend capture capability: Effectively filters short-term market noise through dual moving average crossovers
2. Comprehensive risk control: Integrated stop-loss and take-profit mechanisms effectively control single-trade risk
3. Rigorous execution logic: Automatically closes reverse positions before opening new ones, avoiding position overlap
4. Clear signal indication: Trade signals are clearly displayed in the top-right corner table
5. Reasonable parameter settings: 110-day and 200-day periods balance sensitivity and stability

#### Strategy Risks
1. Sideways market risk: Frequent trading in range-bound markets may lead to losses
2. Slippage risk: Significant slippage may occur during high market volatility
3. Trend reversal risk: Stop-losses may not trigger quickly enough during sudden trend reversals
4. Parameter optimization risk: Over-optimization may lead to strategy overfitting
5. Systemic risk: Exposure to systemic risks during extreme market conditions

#### Strategy Optimization Directions
1. Incorporate volume indicators: Confirm trend validity through volume analysis
2. Optimize stop-loss mechanism: Consider implementing trailing stops or ATR-based dynamic stops
3. Add trend filters: Integrate trend strength indicators to filter weak signals
4. Improve position management: Dynamically adjust position sizes based on trend strength
5. Implement drawdown control: Set maximum drawdown limits to pause trading when thresholds are reached

#### Summary
The strategy captures trends through moving average crossovers while managing risk through stop-loss and take-profit mechanisms, demonstrating sound design and logical rigor. Although it may underperform in ranging markets, the suggested optimizations can further enhance strategy stability and profitability. The strategy is suitable for medium to long-term investors seeking steady returns.[/trans]

#### Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-18 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("EMA110/200 Cross with Stop-Loss and Take-Profit", overlay=true)

// Define EMA110 and EMA200
ema110 = ta.ema(close, 110)
ema200 = ta.ema(close, 250)

// Plot the EMAs
plot(ema110, color=color.blue, title="EMA110")
plot(ema200, color=color.red, title="EMA200")

// Calculate crossover signals
longCondition = ta.crossover(ema110, ema200)  // EMA110 crosses above EMA200, long signal
shortCondition = ta.crossunder(ema110, ema200)  // EMA110 crosses below EMA200, short signal

// Set stop-loss and take-profit levels
stopLoss = 0.01  // Stop loss at 1%
takeProfit = 0.005  // Take profit at 0.5%

// Determine if there is an existing position
isLong = strategy.position_size > 0  // Current long position
isShort = strategy.position_size < 0  // Current short position

// Execute the strategy: close shorts when going long, and vice versa
if (longCondition and not isLong)  // If a long condition is met and no long position exists
    if (isShort)  // If currently in a short position, close it first
        strategy.close("Short")
    strategy.entry("Long", strategy.long)  // Execute long entry
    strategy.exit("Take Profit/Stop Loss", "Long", stop=close * (1 - stopLoss), limit=close * (1 + takeProfit))

if (shortCondition and not isShort)  // If a short condition is met and no short position exists
    if (isLong)  // If currently in a long position, close it first
        strategy.close("Long")
    strategy.entry("Short", strategy.short)  // Execute short entry
    strategy.exit("Take Profit/Stop Loss", "Short", stop=close * (1 + stopLoss), limit=close * (1 - takeProfit))

// Display signals in the table
var table myTable = table.new(position.top_right, 1, 1)
if (longCondition and not isLong)
    table.cell(myTable, 0, 0, "Buy Signal", text_color=color.green)
if (shortCondition and not isShort)
    table.cell(myTable, 0, 0, "Sell Signal", text_color=color.red)
```

> Detail

https://www.fmz.com/strategy/475597

> Last Modified

2024-12-20 14:30:29
---