> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_float_1|2|Gamma|
|v_input_float_2|8|Sigma|
|v_input_float_3|0.0833|T|
|v_input_float_4|5|k|
|v_input_float_5|0.5|M|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-03-01 00:00:00
end: 2024-03-31 23:59:59
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Khaled Tamim's Avellaneda-Stoikov Strategy", overlay=true)

// Avellaneda-Stoikov model logic
avellanedaStoikov(src, gamma, sigma, T, k, M) =>
    midPrice = (src + src[1]) / 2
    sqrtTerm = gamma * sigma * sigma * T
    // Add 0.1% fee to bid and ask quotes
    fee = 0.001 // 0.1% fee
    bidQuote = midPrice - k * sqrtTerm - (midPrice * fee)
    askQuote = midPrice + k * sqrtTerm + (midPrice * fee)
    longCondition = src < bidQuote - M
    shortCondition = src > askQuote + M
    [bidQuote, askQuote]

// Define strategy parameters
gamma = input.float(2, title="Gamma")
sigma = input.float(8, title="Sigma")
T = input.float(0.0833, title="T")
k = input.float(5, title="k")
M = input.float(0.5, title="M")

// Calculate signals
[bidQuote, askQuote] = avellanedaStoikov(close, gamma, sigma, T, k, M)
longCondition = close < bidQuote - M
shortCondition = close > askQuote + M

// Plot signals
plotshape(series=longCondition ? low : na, title="Buy Signal", location=belowbar, color=color.green, style=shape.triangleup, size=size.small)
plotshape(series=shortCondition ? high : na, title="Sell Signal", location=abovebar, color=color.red, style=shape.triangledown, size=size.small)
```

This PineScript code defines the Khaled Tamim's Avellaneda-Stoikov strategy with the specified parameters and logic. It calculates buy and sell signals based on the Avellaneda-Stoikov model while considering transaction costs. The strategy plots buy and sell signals using triangle shapes to visualize trading opportunities.