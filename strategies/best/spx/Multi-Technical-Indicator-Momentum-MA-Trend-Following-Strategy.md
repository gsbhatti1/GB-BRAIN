---

### Name

Multi-Technical-Indicator-Momentum-MA-Trend-Following-Strategy

### Author

ChaoZhang

### Strategy Description

![IMG](https://www.fmz.com/upload/asset/158791d2c381c2f1ab7.png)

[trans]
#### Overview
This strategy is a trend-following trading system based on multiple technical indicators, combining MACD, RSI, and Moving Averages (MA) for trade signal confirmation. It employs a conservative money management approach with stop-loss and multiple profit targets for risk control. The strategy focuses on capturing upward market trends through long-only positions.

#### Strategy Principle
The core logic is based on triple technical indicator confirmation:
1. MACD for momentum identification - generates initial buy signal when MACD line crosses above signal line
2. RSI for strength confirmation - requires RSI value above set threshold (default 50) to confirm upward momentum
3. Moving Average system for trend confirmation - MA50 above MA200 confirms overall uptrend
Additionally, the strategy implements comprehensive money management:
- Risk exposure based on total account capital
- Fixed percentage stop-loss for individual trade risk control
- Dual profit targets (TP1 and TP2) for optimized returns

#### Strategy Advantages
1. Multiple technical indicator cross-validation increases signal reliability
2. Comprehensive money management system for effective risk control
3. Adjustable strategy parameters for high adaptability
4. Dual profit targets protect profits while capturing larger trends
5. Clear code structure for easy maintenance and optimization

#### Strategy Risks
1. Potential false signals in consolidating markets
2. Multiple indicator confirmation may lead to slightly delayed entries
3. Long-only approach lacks hedging in declining markets
4. Parameter optimization risks overfitting

#### Optimization Directions
1. Incorporate volume indicators for additional confirmation
2. Add market volatility filtering mechanism
3. Enhance exit mechanism with trailing stops
4. Implement adaptive parameter system based on market conditions
5. Add drawdown control mechanism

#### Summary
This strategy builds a robust trend-following system through the synergy of multiple technical indicators. Its comprehensive money management mechanism and adjustable parameter design provide good practicality and adaptability. Future improvements can focus on market state identification and exit mechanism optimization to further enhance strategy stability and profitability.

|| 

#### Overview
This strategy is a trend-following trading system based on multiple technical indicators, combining MACD, RSI, and Moving Averages (MA) for trade signal confirmation. It employs a conservative money management approach with stop-loss and multiple profit targets for risk control. The strategy focuses on capturing upward market trends through long-only positions.

#### Strategy Principle
The core logic is based on triple technical indicator confirmation:
1. MACD for momentum identification - generates initial buy signal when MACD line crosses above signal line
2. RSI for strength confirmation - requires RSI value above set threshold (default 50) to confirm upward momentum
3. Moving Average system for trend confirmation - MA50 above MA200 confirms overall uptrend
Additionally, the strategy implements comprehensive money management:
- Risk exposure based on total account capital
- Fixed percentage stop-loss for individual trade risk control
- Dual profit targets (TP1 and TP2) for optimized returns

#### Strategy Advantages
1. Multiple technical indicator cross-validation increases signal reliability
2. Comprehensive money management system for effective risk control
3. Adjustable strategy parameters for high adaptability
4. Dual profit targets protect profits while capturing larger trends
5. Clear code structure for easy maintenance and optimization

#### Strategy Risks
1. Potential false signals in consolidating markets
2. Multiple indicator confirmation may lead to slightly delayed entries
3. Long-only approach lacks hedging in declining markets
4. Parameter optimization risks overfitting

#### Optimization Directions
1. Incorporate volume indicators for additional confirmation
2. Add market volatility filtering mechanism
3. Enhance exit mechanism with trailing stops
4. Implement adaptive parameter system based on market conditions
5. Add drawdown control mechanism

#### Summary
This strategy builds a robust trend-following system through the synergy of multiple technical indicators. Its comprehensive money management mechanism and adjustable parameter design provide good practicality and adaptability. Future improvements can focus on market state identification and exit mechanism optimization to further enhance strategy stability and profitability.

[/trans]

### Source (PineScript)

```pinescript
/*backtest
start: 2024-12-29 00:00:00
end: 2025-01-05 00:00:00
period: 15m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("Saudi Market Buy-Only Strategy (Customizable)", overlay=true)

// User inputs for customizing values
// Capital and risk management
capital = input.float(10000, title="Capital (SAR)", minval=1000)    // Default capital
riskPercent = input.float(2, title="Risk Percentage (%)", minval=0.1, maxval=10) / 100  // Risk percentage
buySLPercent = input.float(1, title="Stop Loss Percentage (%)", minval=0.1, maxval=10) / 100  // Stop loss percentage
tp1Percent = input.float(2, title="Take Profit 1 Percentage (%)", minval=0.1, maxval=20) / 100   // Take profit 1 percentage
tp2Percent = input.float(3, title="Take Profit 2 Percentage (%)", minval=0.1, maxval=30) / 100 // Take profit 2 percentage

// Technical indicator settings
macdFastLength = input.int(12, title="MACD - Fast MA Length", minval=1)
macdSlowLength = input.int(26, title="MACD - Slow MA Length", minval=1)
macdSignalLength = input.int(9, title="MACD - Signal MA Length", minval=1)

rsiLength = input.int(14, title="RSI - RSI Length", minval=1)
rsiThreshold = input.int(50, title="RSI - Entry Level", minval=1, maxval=100)

ma50Length = input.int(50, title="MA50 - MA Length", minval=1)
ma200Length = input.int(200, title="MA200 - MA Length", minval=1)

// Calculating risk management
riskAmount = capital * riskPercent  // Risk amount

// Calculating technical indicators
[macdLine, signalLine, _] = ta.macd(close, macdFastLength, macdSlowLength, macdSignalLength)
rsiValue = ta.rsi(close, rsiLength)
ma50 = ta.sma(close, ma50Length)
ma200 = ta.sma(close, ma200Length)

// Defining overall market trend using moving averages
isBullishTrend = ma50 > ma200

// Conditions for entering only long positions
if ta.crossover(macdLine, signalLine) and rsiValue > rsiThreshold and isBullishTrend
    entryPrice = close
    stopLoss = entryPrice * (1 - buySLPercent)   // Stop loss below the entry price
    takeProfit1 = entryPrice * (1 + tp1Percent) // Take profit 1
    takeProfit2 = entryPrice * (1 + tp2Percent) // Take profit 2
    strategy.entry("Buy", strategy.long)        // Enter long position
    strategy.exit("TP1", "Buy", limit=takeProfit1, stop=stopLoss)
    strategy.exit("TP2", "Buy", limit=takeProfit2)

// Plotting moving average lines
plot(ma50, color=color.blue, title="MA50")
plot(ma200, color=color.orange, title="MA200")

```

### Detail

https://www.fmz.com/strategy/477612

### Last Modified

2025-01-06 16:56:14