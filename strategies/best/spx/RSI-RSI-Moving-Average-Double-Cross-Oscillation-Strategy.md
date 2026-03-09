> Name

RSI Moving Average Double Cross Oscillation Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/f8cae4528e6c8aff06.png)
[trans]
## Overview

The RSI moving average double cross oscillation strategy is a quantitative trading strategy that uses both the crossovers of the RSI indicator and moving averages to determine entries and exits. It utilizes the RSI indicator to judge whether the market is overbought or oversold, combined with the trend judgment of moving averages, to issue trading signals when the RSI shows extreme conditions. This can effectively filter out fake signals and improve the stability of the strategy.

## Strategy Logic

The strategy is mainly based on the combined use of the RSI indicator and moving averages. Firstly, calculate the RSI value over a certain period and set overbought/oversold lines. Secondly, calculate fast and slow moving averages. When the RSI crosses above the slow moving average, while the RSI value is below the oversold line and lower band, a buy signal is generated; when the RSI crosses below the slow moving average, while the RSI is above the overbought line and upper band, a sell signal is generated.

## Advantage Analysis

The biggest advantage of this strategy is that it utilizes both the RSI indicator to judge overbought/oversold conditions and moving averages to determine trend direction, which can effectively avoid false breakouts. In addition, the combination of RSI and BOLL channel can further filter noise to make trading signals more accurate.

## Risk Analysis

The main risks of this strategy may include: high trading frequency leading to over-trading; improper parameter settings may reduce signal accuracy. Additionally, losses may occur in range-bound markets.

## Optimization

Consider adjusting RSI or moving average period parameters to suit different cycles; combine with other indicators to filter signals; set stop loss and take profit points to control risks; optimize position sizing on every trade.

## Conclusion

In general, the RSI moving average double cross oscillation strategy is a relatively stable and reliable short-term trading strategy. With proper parameter tuning and risk control, it can achieve good return on investment. The strategy is easy to understand and implement, very suitable for beginners to learn and apply quantitative trading.

||

## Overview  

The RSI moving average double cross oscillation strategy is a quantitative trading strategy that uses both the crossovers of the RSI indicator and moving averages to determine entries and exits. It utilizes the RSI indicator to judge whether the market is overbought or oversold, combined with the trend judgment of moving averages, to issue trading signals when the RSI shows extreme conditions. This can effectively filter out fake signals and improve the stability of the strategy.

## Strategy Logic

The strategy is mainly based on the combined use of the RSI indicator and moving averages. Firstly, calculate the RSI value over a certain period and set overbought/oversold lines. Secondly, calculate fast and slow moving averages. When the RSI crosses above the slow moving average, while the RSI value is below the oversold line and lower band, a buy signal is generated; when the RSI crosses below the slow moving average, while the RSI is above the overbought line and upper band, a sell signal is generated.

## Advantage Analysis

The biggest advantage of this strategy is that it utilizes both the RSI indicator to judge overbought/oversold conditions and moving averages to determine trend direction, which can effectively avoid false breakouts. In addition, the combination of RSI and BOLL channel can further filter noise to make trading signals more accurate.

## Risk Analysis

The main risks of this strategy may include: high trading frequency leading to over-trading; improper parameter settings may reduce signal accuracy. Additionally, losses may occur in range-bound markets.

## Optimization

Consider adjusting RSI or moving average period parameters to suit different cycles; combine with other indicators to filter signals; set stop loss and take profit points to control risks; optimize position sizing on every trade.

## Conclusion

In general, the RSI moving average double cross oscillation strategy is a relatively stable and reliable short-term trading strategy. With proper parameter tuning and risk control, it can achieve good return on investment. The strategy is easy to understand and implement, very suitable for beginners to learn and apply quantitative trading.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|14|RSI Length|
|v_input_2|7|Fast|
|v_input_3|2|Slow|
|v_input_4|72|RSI Overbought Level|
|v_input_5|29|RSI Oversold Level|
|v_input_6|14|Bollinger Bands Length|
|v_input_7|2|Bollinger Bands StdDev|
|v_input_float_1|3|Stop Loss (%)|
|v_input_float_2|8|Take Profit (%)|

> Source (PineScript)

```pinescript
//@version=5
strategy("RSI Moving Average Double Cross Oscillation Strategy", overlay=false, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

// Define the RSI length
rsi_length = input(title='RSI Length', defval=14)

// Define the fast and slow moving averages
Fast = input(title='Fast', defval=7)
slow = input(title='Slow', defval=2)

// Define the overbought and oversold levels for RSI
rsi_overbought = input(title='RSI Overbought Level', defval=72)
rsi_oversold = input(title='RSI Oversold Level', defval=29)

// Define the length and standard deviation of Bollinger Bands
bb_length = input(title="Bollinger Bands Length", defval=14)
bb_stddev = input(title="Bollinger Bands StdDev", defval=2)

// Calculate RSI
rsi_value = ta.rsi(close, rsi_length)

// Calculate Bollinger Bands
bb_upper = ta.sma(rsi_value, bb_length) + bb_stddev * ta.stdev(rsi_value, bb_length)
bb_lower = ta.sma(rsi_value, bb_length) - bb_stddev * ta.stdev(rsi_value, bb_length)

// Calculate fast and slow moving averages of RSI
fastMA = ta.sma(rsi_value, Fast)
slowMA = ta.sma(rsi_value, slow)

// Define the buy and sell signals
buy_signal = (ta.crossover(rsi_value, slowMA) and rsi_value < bb_lower and rsi_value < rsi_oversold) or (rsi_value < bb_lower and rsi_value < rsi_oversold)
sell_signal = (ta.crossunder(rsi_value, slowMA) and rsi_value > bb_upper and rsi_value > rsi_overbought) or (rsi_value > bb_upper and rsi_value > rsi_overbought)

// Set the market entry and exit conditions
if buy_signal
    strategy.entry("Buy", strategy.long)

if sell_signal
    strategy.close("Buy")

// Set stop loss and take profit levels
stop_loss = input.float(title='Stop Loss (%)', step=0.01, defval=3)
take_profit = input.float(title='Take Profit (%)', step=0.01, defval=8)

strategy.exit("Exit Long", "Buy", stop=close - close * stop_loss / 100, limit=close + close * take_profit / 100)

// Set the chart visualization
plot(slowMA, title='RSISMA', color=color.rgb(75, 243, 33), linewidth=1)
plot(fastMA, title='RSIFMA', color=color.rgb(75, 243, 33), linewidth=1)
plot(rsi_value, title='RSI', color=color.purple, linewidth=1)

// Mark the overbought and oversold zones on the RSI chart
hl = hline(rsi_overbought, title='Overbought', color=color.purple, linestyle=hline.style_dotted, linewidth=1)
hll = hline(rsi_oversold, title='Oversold', color=color.purple, linestyle=hline.style_dotted, linewidth=1)
```

```