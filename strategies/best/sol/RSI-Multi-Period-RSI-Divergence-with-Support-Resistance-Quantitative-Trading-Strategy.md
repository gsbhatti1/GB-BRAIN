> Name

Multi-Period RSI Divergence with Support and Resistance Quantitative Trading Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1efea0a2579ef8168dd.png)

[trans]
#### Overview
This strategy is a quantitative trading system that combines RSI technical indicator, price divergence, and support/resistance levels. The strategy identifies trading signals through RSI-price divergence relationships and support/resistance breakouts, while incorporating stop-loss and take-profit mechanisms for risk control.

#### Strategy Principles
The strategy is based on several core components:
1. RSI Calculation: Uses a 14-period Relative Strength Index (RSI) to measure price momentum
2. Support/Resistance Identification: Determines key price levels using 50-period highs and lows
3. Divergence Detection:
   - Bullish Divergence: When price makes a new low but RSI does not, and price is above support
   - Bearish Divergence: When price makes a new high but RSI does not, and price is below resistance
4. Risk Management:
   - 1% stop-loss after entry
   - 2% take-profit target

#### Strategy Advantages
1. Multiple Confirmation Mechanism: Combines momentum indicator (RSI), price pattern (divergence), and market structure (support/resistance) for more reliable signals
2. Comprehensive Risk Control: Preset stop-loss and take-profit mechanisms effectively control risk per trade
3. High Adaptability: Strategy parameters can be adjusted for different market conditions
4. Clear Signals: Trading conditions are well-defined for easy implementation and backtesting

#### Strategy Risks
1. False Breakout Risk: Frequent false signals may occur in ranging markets
2. Parameter Sensitivity: Choice of RSI period and support/resistance period significantly impacts strategy performance
3. Slippage Impact: Actual execution prices may deviate from signal prices in fast markets
4. Market Environment Dependency: Performs better in trending markets, may generate false signals in ranging markets

#### Optimization Directions
1. Timeframe Optimization: Add multiple timeframe confirmation mechanism to improve signal reliability
2. Stop-Loss Enhancement: Introduce dynamic stop-loss mechanisms, such as trailing stops
3. Filter Implementation: Add volume and volatility filters to reduce false signals
4. Parameter Adaptation: Develop adaptive parameter mechanisms for automatic adjustment based on market conditions

#### Summary
The strategy constructs a relatively complete trading system by combining multiple important concepts in technical analysis. Its strengths lie in multiple confirmation mechanisms and comprehensive risk control, while facing challenges in parameter selection and market environment dependency. Through the suggested optimization directions, the strategy's stability and adaptability can be further improved. In practical application, it is recommended to determine the most suitable strategy configuration through thorough historical data backtesting and parameter optimization.[/trans]

#### Source (PineScript)

```pinescript
/*backtest
start: 2024-12-12 00:00:00
end: 2024-12-19 00:00:00
period: 10m
basePeriod: 10m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("Aggressive Strategy with RSI Divergence and Support/Resistance Levels", overlay=true)

// Parameters for RSI
rsiLength = input.int(14, title="RSI Period", minval=1)   // Period for RSI calculation
rsiOverbought = input.int(70, title="Overbought Level", minval=1, maxval=100)
rsiOversold = input.int(30, title="Oversold Level", minval=1, maxval=100)

// Parameters for stop-loss and take-profit
stopLossPercent = input.float(1, title="Stop-Loss (%)", minval=0.1) / 100
takeProfitPercent = input.float(2, title="Take-Profit (%)", minval=0.1) / 100

// Period for support and resistance levels
supportResistanceLength = input.int(50, title="Support/Resistance Period", minval=1)

// Calculate RSI
rsi = ta.rsi(close, rsiLength)

// Calculate support and resistance levels
support = ta.lowest(close, supportResistanceLength)  // Find minimums over the period for support
resistance = ta.highest(close, supportResistanceLength)  // Find maximums over the period for resistance

// Detect RSI price divergence
priceHigh = ta.highest(close, rsiLength)
priceLow = ta.lowest(close, rsiLength)
rsiHigh = ta.highest(rsi, rsiLength)
rsiLow = ta.lowest(rsi, rsiLength)

// Bullish Divergence: Price makes a new low, but RSI does not, and price is above support
bullishDivergence = priceLow < priceLow[1] and rsiLow > rsiLow[1] and close > support

// Bearish Divergence: Price makes a new high, but RSI does not, and price is below resistance
bearishDivergence = priceHigh > priceHigh[1] and rsiHigh < rsiHigh[1] and close < resistance

// Display support and resistance levels
plot(support, title="Support", color=color.green, linewidth=2, style=plot.style_line)
```