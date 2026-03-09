> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|500|Contribution (USD)|
|v_input_2|20|Bollinger (Period)|
|v_input_3|2|Deviations (Float)|
|v_input_4|14|RSI (Period)|


> Source (PineScript)

``` pinescript
//@version=5
strategy("Momentum Bollinger Bands Dual Moving Average DCA Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=0.5, initial_capital=10000)

// Inputs
contribution = input(500, title="Contribution (USD)")
bollinger_period = input(20, title="Bollinger (Period)")
deviations = input(2.0, title="Deviations (Float)", type=input.float)
rsi_period = input(14, title="RSI (Period)")

// Bollinger Bands
src = close
lengthBB = bollinger_period
stdDev = deviations
bBands = ta.bband(src, lengthBB, stdDev)

// RSI
rsi_length = rsi_period
rsi_value = ta.rsi(close, rsi_length)

// Buy Conditions
longCondition = ta.crossunder(bBands[1], bBands) and ta.valuewhen(ta.crossover(rsi_value, 50), true, 0)
if (longCondition)
    strategy.entry("Buy", strategy.long, comment="Buy Signal")
```

This PineScript code implements the described Momentum Bollinger Bands Dual Moving Average DCA strategy. It uses Bollinger Bands and RSI to determine buy signals based on specific conditions.