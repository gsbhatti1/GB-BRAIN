> Name

Dynamic Donchian Channel and Simple Moving Average Combination Quantitative Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/12ff8190fd73cc4670f.png)
[trans]
#### Overview
This strategy combines two technical indicators: Donchian Channel and Simple Moving Average (SMA). When the price breaks below the lower band of the Donchian Channel and is above the SMA, a long position is opened. Conversely, when the price breaks above the upper band of the Donchian Channel and is below the SMA, a short position is opened. Long positions are closed when the price reaches the upper band of the Donchian Channel, while short positions are closed when the price reaches the lower band. This strategy is suitable for markets with strong trends.

#### Strategy Principle
1. Calculate the upper and lower bands of the Donchian Channel. The upper band is the highest high over the past n periods, and the lower band is the lowest low over the past n periods.
2. Calculate the Simple Moving Average. The SMA is the arithmetic mean of the closing prices over the past m periods.
3. Long entry: Open a long position when the price is below the lower band of the Donchian Channel and the closing price is above the SMA.
4. Short entry: Open a short position when the price is above the upper band of the Donchian Channel and the closing price is below the SMA.
5. Long exit: Close the long position when the price reaches the upper band of the Donchian Channel.
6. Short exit: Close the short position when the price reaches the lower band of the Donchian Channel.

#### Strategy Advantages
1. Combines two market elements: trend and volatility. The SMA captures the trend, while the Donchian Channel captures the volatility, enabling the strategy to seize pullback opportunities in trending markets.
2. Clear profit-taking conditions help lock in profits in a timely manner. Long and short positions are closed when the price reaches the upper and lower bands of the Donchian Channel, respectively, allowing the strategy to exit profitable trades before the trend reverses.
3. Few parameters make optimization easier. The strategy only has three parameters: Donchian Channel period, offset, and SMA period, which simplifies optimization.

#### Strategy Risks
1. Frequent trading. The strategy has a high frequency of position entries and exits, which can erode returns in markets with high trading costs. This can be mitigated by moderately relaxing entry conditions or increasing the timeframe.
2. Poor performance in rangebound markets. The strategy may suffer more losses when the trend is unclear. Volatility indicators can be used to identify rangebound markets and suspend the strategy.
3. Insufficient parameter stability. The optimal parameters may vary significantly across different instruments and timeframes, indicating poor parameter stability. The live performance may not match the backtest. Extensive out-of-sample testing and sensitivity analysis are needed to confirm parameter robustness.

#### Strategy Optimization Directions
1. Add optional entry conditions combined with other indicators. For example, require the ADX of the DMI to be above a certain threshold for entry, or only enter long when the RSI leaves the oversold zone. This can improve the win rate of entries.
2. Use dynamic profit-taking lines instead of fixed Donchian Channel lines to achieve a profit-trailing function. For example, after the price reaches the upper band of the Donchian Channel for a long position, switch to closing the position at the ATR stop-loss line or the SAR stop-loss line.
3. Dynamically adjust the Donchian Channel period based on volatility levels. Shorten the Donchian Channel period in high-volatility market conditions and lengthen the period in low-volatility conditions. This helps adapt to different markets.

#### Summary
The Dynamic Donchian Channel and Simple Moving Average Combination Strategy is a simple and easy-to-use quantitative trading strategy framework. It constructs entry and exit logic from the perspectives of trend following and volatility breakout, making it suitable for instruments with strong trends. However, the strategy performs poorly in frequently rangebound markets, and its parameter robustness is mediocre. The adaptability and robustness of the strategy can be improved by introducing auxiliary entry conditions, dynamic profit-taking, and parameter self-adaptation mechanisms. Overall, this strategy can serve as a basic strategy framework to be further modified and improved upon to create more advanced quantitative strategies.

[/trans]

> Source (PineScript)

```pinescript
//@version=5
strategy("Dynamic Donchian Channel and Simple Moving Average Combination Strategy", overlay=true)

// Parameters
n = input.int(20, title="Donchian Channel Period")
offset = input.float(1.0, title="Offset")
m = input.int(20, title="SMA Period")

// Calculations
upperBand = ta.highest(high, n) * (1 + offset)
lowerBand = ta.lowest(low, n) * (1 - offset)
sma = ta.sma(close, m)

// Long Entry Condition
longCondition = close < lowerBand and close > sma

// Short Entry Condition
shortCondition = close > upperBand and close < sma

// Plot Bands
plot(upperBand, color=color.red, title="Upper Band")
plot(lowerBand, color=color.green, title="Lower Band")

// Strategy Execution
if (longCondition)
    strategy.entry("Long", strategy.long)

if (shortCondition)
    strategy.entry("Short", strategy.short)

// Exit Conditions
if (close >= upperBand)
    strategy.close("Long")

if (close <= lowerBand)
    strategy.close("Short")
```
[/trans]