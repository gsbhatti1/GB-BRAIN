> Name

Dynamic-Cost-Averaging-Strategy-System-Based-on-Bollinger-Bands-and-RSI

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/c34b2567b90dd65450.png)

#### Overview
This strategy is a quantitative trading system that combines Bollinger Bands, Relative Strength Index (RSI), and Dynamic Cost Averaging (DCA). The strategy implements automatic position building through established money management rules during market fluctuations, while integrating technical indicators for buy/sell signal determination to achieve controlled risk execution. The system also includes take-profit logic and cumulative profit tracking functionality for effective monitoring and management of trading performance.

#### Strategy Principles
The strategy operates based on the following core components:
1. Bollinger Bands for determining price volatility ranges, considering buying at lower band and selling at upper band
2. RSI for confirming overbought/oversold conditions, confirming oversold below 25 and overbought above 75
3. DCA module dynamically calculates position sizes based on account equity for adaptive capital management
4. Take-profit module sets 5% profit target for automatic position closing
5. Market state monitoring calculates 90-day market changes to assess overall trends
6. Cumulative profit tracking records each trade's profit/loss for strategy performance evaluation

#### Strategy Advantages
1. Multiple technical indicator cross-validation improves signal reliability
2. Dynamic position management avoids fixed-position risks
3. Reasonable take-profit conditions secure timely profits
4. Market trend monitoring capabilities aid in big-picture understanding
5. Comprehensive profit tracking system facilitates strategy analysis
6. Well-configured alert system provides real-time trading opportunities

#### Strategy Risks
1. Choppy markets may trigger frequent signals increasing trading costs
2. RSI indicators may lag in trending markets
3. Fixed percentage take-profit may exit too early in strong trends
4. DCA strategy may cause significant drawdowns in prolonged downtrends
Risk management recommendations:
- Set maximum position limits
- Dynamically adjust parameters based on market volatility
- Add trend filters
- Implement tiered take-profit strategy

#### Strategy Optimization Directions
1. Parameter Dynamic Optimization:
- Bollinger Bands parameters adapt to volatility
- RSI thresholds vary with market cycles
- DCA allocation adjusts with account size

2. Signal System Enhancement:
- Add volume confirmation
- Include trendline analysis
- Integrate additional technical indicator cross-validation

3. Risk Control Improvement:
- Implement dynamic stop-loss
- Add maximum drawdown control
- Set daily loss limits

#### Summary
The strategy builds a comprehensive trading system through combined technical analysis and money management methods. Its strengths lie in multiple signal confirmation and thorough risk management, though it still requires extensive testing and optimization in live trading. Through continuous improvement in parameter settings and additional auxiliary indicators, the strategy shows promise for stable performance in actual trading.

||

#### Source (PineScript)

```pinescript
//@version=5
strategy("Combined BB RSI with Cumulative Profit, Market Change, and Futures Strategy (DCA)", shorttitle="BB RSI Combined DCA Strategy", overlay=true)

// Input Parameters
length = input.int(20, title="BB Length")  // Adjusted BB length
mult = input.float(2.5, title="BB Multiplier")  // Adjusted BB multiplier
rsiLength = input.int(14, title="RSI Length")  // Adjusted RSI length
rsiBuyLevel = input.int(25, title="RSI Buy Level")  // Adjusted RSI Buy Level
rsiSellLevel = input.int(75, title="RSI Sell Level")  // Adjusted RSI Sell Level
dcaPositionSizePercent = input.float(1, title="DCA Position Size (%)", tooltip="Percentage of equity to use in each DCA step")
takeProfitPercentage = input.float(5, title="Take Profit (%)", tooltip="Take profit percentage for DCA strategy")

// Calculate DCA position size
equity = strategy.equity  // Account equity
dcaPositionSize = (equity * dcaPositionSizePercent) / 100  // DCA position size as percentage of equity

// Bollinger Bands Calculation
basis = ta.sma(close, length)
dev = mult * ta.stdev(close, length)
upper = basis + dev
lower = basis - dev

// RSI Calculation
rsi = ta.rsi(close, rsiLength)

// Plotting Bollinger Bands and RSI levels
plot(upper, color=color.red, title="Bollinger Upper")
plot(lower, color=color.green, title="Bollinger Lower")
hline(rsiBuyLevel, "RSI Buy Level", color=color.green)
hline(rsiSellLevel, "RSI Sell Level", color=color.red)
```
```