> Name

A-Trend-Following-Strategy Based on RSI Extremes and 200-Day SMA Filtering

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/af1ac74b0f6970576d.png)

[trans]

### Overview

This strategy combines the extremes of the Relative Strength Index (RSI) indicator with filtering based on the 200-day Simple Moving Average (SMA). It tracks trends by entering trades when RSI reaches extreme overbought or oversold levels and using SMA direction to determine long or short positions. The strategy is suitable for US stock indexes, European indexes, Asian indexes, gold, silver, and other varieties. Through simple RSI and SMA rules, it effectively captures trends.

### Strategy Logic

1. Calculate the RSI indicator value. Set the overbought threshold upper limit to 65 and the oversold threshold lower limit to 45.
2. Calculate the 200-day SMA to determine the trend direction.
3. When RSI is below 45 (oversold) and price is above SMA, go long; when RSI is above 65 (overbought) and price is below SMA, go short.
4. When RSI is above 75 (strongly overbought) and price is above SMA, close long positions; when RSI is below 25 (strongly oversold) and price is below SMA, close short positions.

The strategy captures trends effectively by using RSI extremes to time entries and SMA direction for filtering. RSI extremes indicate potential reversals, while SMA direction ensures trades align with the trend. Together, they ensure reasonable trades and higher win rates.

### Advantages

1. Simple and clear strategy logic, easy to understand and master.
2. Based on well-known RSI and SMA indicators, easy to implement.
3. RSI extremes indicate potential reversal points; SMA filters ensure directional correctness.
4. Reasonable parameter settings avoid excessive trading.
5. Applicable to multiple products like indexes and commodities.
6. Captures significant price swings during trends.

Compared to using RSI alone, this strategy adds a trend filter with the 200-day SMA to avoid blind long/short entries. Compared to using the SMA system alone, it improves timing efficiency by entering trades based on RSI extremes. Overall, it combines the strengths of both for a practical trend-following strategy.

### Risks and Solutions

1. The SMA can produce a death cross, posing a risk of trend reversal. A solution is to use shorter SMA periods for increased sensitivity.
2. RSI divergences can risk missing trades. Adding other indicators like MACD can help detect anomalies.
3. Both RSI and SMA may generate false signals during ranging markets. Pausing trading when in range-bound market conditions is detected.
4. Improper parameter settings can lead to overtrading or missed trades. Optimizing parameters will find the best combination.
5. A single product backtest is insufficient for evaluating strategy effectiveness; multiple products need to be validated.
6. Backtesting does not equal live trading. Proper risk and capital management are required in live trading.

### Improvement Directions

1. Optimize RSI period settings for different products.
2. Optimize SMA period parameters, integrating multiple SMAs.
3. Add a stop loss mechanism for better risk control.
4. Integrate other indicators for multi-factor confirmation.
5. Improve entry timing with volatility indicators.
6. Develop an adaptive parameter system for dynamic optimization.
7. Test different capital management approaches to find the optimal strategy.

### Conclusion

The RSI extremes with 200-day SMA filter strategy combines the strengths of both for effective trend following. The logic is clear and parameters solid, making it suitable for multiple products while significantly improving timing efficiency and win rates compared to using RSI or SMA systems alone. There is room for improvement through parameter optimization and stop loss mechanisms to further enhance robustness and adaptability. Overall, it provides trend traders with a very useful and effective tool.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|14|RSI Length|
|v_input_int_2|200|SMA Length|
|v_input_float_1|5|Stop Loss|


> Source (PineScript)

```pinescript
//@version=5
strategy('Relative Strength Index Extremes with 200-Day Moving Average Filter', overlay=true, pyramiding=1, initial_capital=10000, default_qty_type=strategy.cash, default_qty_value=36000, calc_on_order_fills=true)

// This work is licensed under a Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) https://creativecommons.org/licenses/by-nc-sa/4.0/
// © wielkieef

rsiLength = input.int(14, minval=1)
smaLength = input.int(200, minval=1)
stopLoss = input.float(5, minval=0)

rsi = rsi(close, rsiLength)
sma = sma(close, smaLength)

longCondition = rsi < 45 and close > sma
shortCondition = rsi > 65 and close < sma

if (longCondition)
    strategy.entry("Long", strategy.long)
    
if (shortCondition)
    strategy.entry("Short", strategy.short)

if (rsi > 75 and close > sma)
    strategy.close("Long")
    
if (rsi < 25 and close < sma)
    strategy.close("Short")

// Stop loss mechanism
strategy.exit("Stop Loss - Long", from_entry="Long", stop=close * (1 - stopLoss / 100))
strategy.exit("Stop Loss - Short", from_entry="Short", stop=close * (1 + stopLoss / 100))
```