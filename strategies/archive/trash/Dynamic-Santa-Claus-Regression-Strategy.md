> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|64|length|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-01-05 00:00:00
end: 2024-01-11 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
// Creator - TradeAI
strategy('Dynamic Santa Claus Regression Strategy | TradeAI', overlay=true)

// Set the length of the moving average
length = input(64)

// Calculate the moving averages and standard deviations
x = bar_index
y = close
x_ = ta.sma(x, length)
y_ = ta.sma(y, length)
mx = ta.stdev(x, length)
my = ta.stdev(y, length)
c = ta.correlation(x, y, length)
slope = c * (my / mx)

// Calculate the parameters of the regression line
inter = y_ - slope * x_
reg = x * slope + inter

// Set the line color based on whether the regression line is moving up or down
var color lineColor = na
if (reg > reg[1] and close > open and close > high[1])
    lineColor := color.new(#d8f7ff, 0)
if (reg < reg[1] and close < open and close < low[1])
    lineColor := color.new(#ff383b, 0)

// Plot the regression line with different thicknesses
plot(reg, color=lineColor, title="Regression Line")

var color lineColorrr = na
if (reg > reg[1] and close > open and close > high[1])
    lineColorrr := color.new(#d8f7ff, 77)
if (reg < reg[1] and close < open and close < low[1])
    lineColorrr := color.new(#ff383b, 77)
plot(reg, color=lineColorrr, title="Regression Line", linewidth=5)

var color lineColorr = na
if (reg > reg[1] and close > open and close > high[1])
    lineColorr := color.new(#d8f7ff, 93)
if (reg < reg[1] and close < open and close < low[1])
    lineColorr := color.new(#ff383b, 93)
plot(reg, color=lineColorr, title="Regression Line", linewidth=20)

// Generate buy/sell signals based on the direction of the regression line
if (reg > reg[1] and close > open and close > high[1])
    strategy.entry('Buy', strategy.long)
if (reg < reg[1] and close < open and close < low[1])
    strategy.exit('Sell', from_entry='Buy')
```

This PineScript code defines the Dynamic Santa Claus Regression Strategy, including calculating the regression line based on price and bar index relationships. It also includes buy/sell signals based on the direction of the regression line and visualizes it with different thicknesses for clarity.