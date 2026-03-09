> Name

Dual-Moving-Average-Stop-Loss-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/df890d70efbf0b2e2e.png)

[trans]

## Overview

This strategy is a stop loss strategy based on dual moving averages. It uses two moving averages, one as the main moving average, and one as the stop loss line. When the price is above the main moving average, go long. When the price is below the stop loss line, close the long position; when the price is below the main moving average, go short. When the price is above the stop loss line, close the short position. It achieves stop loss and take profit by dynamically adjusting the entry prices.

## Strategy Logic

This strategy uses the `sma` function to calculate a simple moving average of length `len` as the main moving average (`ma`). Then it calculates the long stop loss line (`el`) and the short stop loss line (`es`) based on user input percentages for long and short stop losses. The specific formulas are:

``` pinescript
el = ma + (ma * elpercent / 100)
es = ma + (ma * espercent / 100)
```

Where `elpercent` and `espercent` represent the percentage offset from the main moving average.

This gives us three lines: the main moving average (`ma`), the long stop loss line (`el`), and the short stop loss line (`es`).

The trading logic of the strategy is:

- If the closing price is above the long stop loss line (`el`), open a long position.
- If the closing price is below the short stop loss line (`es`), close the long position.
- If the closing price is below the short stop loss line (`es`), open a short position.
- If the closing price is above the long stop loss line (`el`), close the short position.

## Advantages of the Strategy

1. Using dual moving averages to set stop loss and take profit points can effectively control risks.
2. The length of the main moving average `len` and the offset percentages `elpercent` and `espercent` are customizable, allowing for adjustments based on different markets, making it highly adaptable.
3. The stop loss mechanism can cut losses in time, avoiding further financial damage.
4. The strategy logic is simple and clear, easy to understand and implement, suitable for beginners.
5. It can go both long and short, taking advantage of two-way market movements.

## Risks and Solutions

1. Backtest overfitting risk. Moving average strategies tend to fit historical data closely, leading to potentially different results in live trading. Solution is to verify the strategy's performance in complex real markets and adjust parameters accordingly.
2. Risk of stop loss being too close. If the stop loss is set very close to the main moving average, it may be triggered by short-term price fluctuations. Increase the distance between the stop loss and the main moving average to mitigate this risk.
3. Capital pressure from dual direction trading. Going both long and short requires sufficient margin. Reduce position size to control capital pressure.
4. Parameter optimization risk. Different market conditions require different parameter settings, which can be time-consuming to optimize. Machine learning techniques can assist in optimizing parameters.

## Optimization Directions

1. Consider adding more indicators to determine market trend and improve decision-making, such as volume price indicator or volatility indicator.
2. Research auto-optimization of moving average length and stop loss parameters based on market changes.
3. Add filtering on trading instruments, only trading in clearly trending markets.
4. Consider using trailing stop losses instead of fixed stop losses to adjust the stop based on real-time prices.
5. Build an evaluation system for parameter optimization to automatically find optimal parameter combinations via backtest results.

## Conclusion

The overall logic of this strategy is clear and easy to understand. It uses dual moving averages for stop loss, which can effectively control risks. The strategy has advantages like customizable parameters and adaptability but also has challenges such as backtest overfitting and setting the correct stop distance that require careful attention. With further optimization, this strategy can become an effective stop loss strategy suitable for live trading. It is a good starting point for beginners in algorithmic trading and can be continually improved through practical application to eventually form a unique trading system.

||

## Overview

This strategy is a stop loss strategy based on dual moving averages. It uses two moving averages, one as the main moving average, and one as the stop loss line. When the price is above the main moving average, go long. When the price is below the stop loss line, close the long position; when the price is below the main moving average, go short. When the price is above the stop loss line, close the short position. It achieves stop loss and take profit by dynamically adjusting the entry prices.

## Strategy Logic

This strategy uses the `sma` function to calculate a simple moving average of length `len` as the main moving average (`ma`). Then it calculates the long stop loss line (`el`) and the short stop loss line (`es`) based on user input percentages for long and short stop losses. The specific formulas are:

``` pinescript
el = ma + (ma * elpercent / 100)
es = ma + (ma * espercent / 100)
```

Where `elpercent` and `espercent` represent the percentage offset from the main moving average.

This gives us three lines: the main moving average (`ma`), the long stop loss line (`el`), and the short stop loss line (`es`).

The trading logic of the strategy is:

- If the closing price is above the long stop loss line (`el`), open a long position.
- If the closing price is below the short stop loss line (`es`), close the long position.
- If the closing price is below the short stop loss line (`es`), open a short position.
- If the closing price is above the long stop loss line (`el`), close the short position.

## Advantages of the Strategy

1. Using dual moving averages to set stop loss and take profit points can effectively control risks.
2. The length of the main moving average `len` and the offset percentages `elpercent` and `espercent` are customizable, allowing for adjustments based on different markets, making it highly adaptable.
3. The stop loss mechanism can cut losses in time, avoiding further financial damage.
4. The strategy logic is simple and clear, easy to understand and implement, suitable for beginners.
5. It can go both long and short, taking advantage of two-way market movements.

## Risks and Solutions

1. Backtest overfitting risk. Moving average strategies tend to fit historical data closely, leading to potentially different results in live trading. Solution is to verify the strategy's performance in complex real markets and adjust parameters accordingly.
2. Risk of stop loss being too close. If the stop loss is set very close to the main moving average, it may be triggered by short-term price fluctuations. Increase the distance between the stop loss and the main moving average to mitigate this risk.
3. Capital pressure from dual direction trading. Going both long and short requires sufficient margin. Reduce position size to control capital pressure.
4. Parameter optimization risk. Different market conditions require different parameter settings, which can be time-consuming to optimize. Machine learning techniques can assist in optimizing parameters.

## Optimization Directions

1. Consider adding more indicators to determine market trend and improve decision-making, such as volume price indicator or volatility indicator.
2. Research auto-optimization of moving average length and stop loss parameters based on market changes.
3. Add filtering on trading instruments, only trading in clearly trending markets.
4. Consider using trailing stop losses instead of fixed stop losses to adjust the stop based on real-time prices.
5. Build an evaluation system for parameter optimization to automatically find optimal parameter combinations via backtest results.

## Conclusion

The overall logic of this strategy is clear and easy to understand. It uses dual moving averages for stop loss, which can effectively control risks. The strategy has advantages like customizable parameters and adaptability but also has challenges such as backtest overfitting and setting the correct stop distance that require careful attention. With further optimization, this strategy can become an effective stop loss strategy suitable for live trading. It is a good starting point for beginners in algorithmic trading and can be continually improved through practical application to eventually form a unique trading system.

||

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Long|
|v_input_2|false|Short|
|v_input_3|50|len|
|v_input_4_ohlc4|0|src: ohlc4|high|low|open|hl2|hlc3|hlcc4|close|
|v_input_5|5|Shift long, %|
|v_input_6|-5|Shift short, %|
|v_input_7|true|Show lines|
|v_input_8|true|Show background|

> Source (PineScript)

``` pinescript
//@version=5
strategy("Dual-Moving-Average-Stop-Loss-Strategy", overlay=true)
len = input(50, title="Len")
src = input(close, title="Source")
elpercent = input(5, title="Long Shift, %")
espercent = input(-5, title="Short Shift, %")

ma = ta.sma(src, len)
el = ma + (ma * elpercent / 100)
es = ma + (ma * espercent / 100)

plot(ma, color=color.blue, title="Main Moving Average")
plot(el, color=color.red, title="Long Stop Loss Line")
plot(es, color=color.orange, title="Short Stop Loss Line")

longCondition = ta.crossover(close, el)
shortCondition = ta.crossunder(close, es)

if (longCondition)
    strategy.entry("Long", strategy.long)
if (strategy.opentrades > 0 and close < es)
    strategy.close("Long")
if (shortCondition)
    strategy.entry("Short", strategy.short)
if (strategy.opentrades > 0 and close > el)
    strategy.close("Short")
```