> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|14|RSI Length|
|v_input_int_2|70|Overbought Level|
|v_input_int_3|30|Oversold Level|
|v_input_int_4|20|BB Length|
|v_input_float_1|2|BB Deviation|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-04 00:00:00
end: 2024-02-03 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("RSI & Bollinger Bands Strategy", overlay=true)

// RSI settings
rsi_length = input.int(14, title="RSI Length")
overbought = input.int(70, title="Overbought Level")
oversold = input.int(30, title="Oversold Level")
rsi = ta.rsi(close, rsi_length)

// Bollinger Bands settings
length = input.int(20, title="BB Length")
mult = input.float(2.0, title="BB Deviation")
basis = ta.sma(close, length)
dev = mult * ta.stdev(close, length)
upper = basis + dev
lower = basis - dev

// Buy and sell signals
longCondition = ta.crossover(rsi, oversold) and ta.crossover(close, lower)
shortCondition = ta.crossunder(rsi, overbought) and ta.crossunder(close, upper)

// Execute trades based on buy and sell conditions
if (longCondition)
    strategy.entry("Buy", strategy.long)
if (shortCondition)
    strategy.entry("Sell", strategy.short)

// Plot buy and sell signals
plotshape(series=longCondition, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)
plotshape(series=shortCondition, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)
```

Note: The original PineScript code has been slightly adjusted to ensure it compiles and runs correctly.