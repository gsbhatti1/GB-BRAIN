> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|20|Period|
|v_input_2|1.5|Standard Deviation|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-18 00:00:00
end: 2023-12-18 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy(title="Bollinger Bands Momentum Breakout Strategy", overlay=true)

// Input parameters
length = input(20, title="Period")
mult = input(1.5, title="Standard Deviation")

// Calculate Bollinger Bands
src = close
basis = sma(src, length)
dev = mult * stdev(src, length)
upperband = basis + dev
lowerband = basis - dev

// Plot Bollinger Bands on chart
plot(basis, color=color.gray)
plot(upperband, color=color.red)
plot(lowerband, color=color.green)

// Buy and Sell conditions
longCondition = crossover(close, upperband)
shortCondition = crossunder(close, lowerband)

if (longCondition)
    strategy.entry("Long", strategy.long)

if (shortCondition)
    strategy.exit(id="Short", from_entry="Long", limit=lowerband)

// Optional: Plot exit prices for better visualization
plot(strategy.close_price, color=color.blue, title="Close Price")
```

This PineScript code implements the Bollinger Bands Momentum Breakout Strategy as described. It uses the specified period and standard deviation to calculate the Bollinger Bands, and triggers buy (`long`) or sell (`short`) signals based on price crossing the upper and lower bands respectively.