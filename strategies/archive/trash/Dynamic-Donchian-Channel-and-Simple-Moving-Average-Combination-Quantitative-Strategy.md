> Name

Dynamic Donchian Channel and Simple Moving Average Combination Quantitative Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/12ff8190fd73cc4670f.png)
[trans]
#### Overview
This strategy combines two technical indicators: Donchian Channel and Simple Moving Average (SMA). It opens a long position when the price breaks below the lower band of the Donchian Channel and closes above the SMA. Conversely, it opens a short position when the price breaks above the upper band of the Donchian Channel and closes below the SMA. The long position is closed when the price reaches the upper band of the Donchian Channel, while the short position is closed when the price reaches the lower band. This strategy is suitable for markets with strong trends.

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
/*backtest
start: 2023-10-01 00:00:00
end: 2024-09-30 23:59:00
symbol: SPY
interval: 1D
lever: 1
initial_capital: 100000
calculation_mode: gross
slippage: 0.0
fee: 0.0
*/
strategy("Dynamic Donchian Channel and SMA Combination Strategy", overlay = true)

// Parameters
donchian_period = input(20, title="Donchian Channel Period")
sma_period = input(50, title="SMA Period")

// Calculate Donchian Channels
high_donch = donchian(high, donchian_period)
low_donch = donchian(low, donchian_period)

// Simple Moving Average
sma = sma(close, sma_period)

// Long Entry Condition
long_entry = (close < low_donch and close > sma) 

// Short Entry Condition
short_entry = (close > high_donch and close < sma)

// Place Orders
if long_entry
    strategy.entry("Long", strategy.long)
else if short_entry
    strategy.entry("Short", strategy.short)

// Close Long Position
long_close = low_donch == close
strategy.close("Long") when long_close

// Close Short Position
short_close = high_donch == close
strategy.close("Short") when short_close

// Plot Donchian Channels and SMA
plot(high_donch, title="Upper Band", color=color.blue)
plot(low_donch, title="Lower Band", color=color.red)
hline(sma, "SMA", color=color.orange)

```