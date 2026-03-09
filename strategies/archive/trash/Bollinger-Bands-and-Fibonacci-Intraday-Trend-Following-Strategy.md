> Source (PineScript)

``` pinescript
/*backtest
start: 2025-01-02 00:00:00
end: 2025-01-09 00:00:00
period: 10m
basePeriod: 10m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT","balance":49999}]
*/

//@version=5
strategy("Bollinger Bands and Fibonacci Intraday Strategy", overlay=true)

// Bollinger Bands settings
length = input.int(20, title="Bollinger Band Length")
src = close
mult = input.float(2.0, title="Bollinger Band Multiplier")
basis = ta.sma(src, length)
dev = mult * ta.stdev(src, length)
upper = basis + dev
lower = basis - dev

// Fibonacci retracement levels
fibRetrace1 = input.float(0.236, title="Fibonacci Level 0.236")
fibRetrace2 = input.float(0.382, title="Fibonacci Level 0.382")
fibRetrace3 = input.float(0.618, title="Fibonacci Level 0.618")

// Define the Fibonacci levels based on recent high and low
var float fibLow = na
var float fibHigh = na

if (bar_index == 0 or ta.highest(high, 20) != fibHigh or ta.lowest(low, 20) != fibLow)
    fibHigh := ta.highest(high, 20)
    fibLow := ta.lowest(low, 20)

fibLevel1 = fibLow + (fibHigh - fibLow) * fibRetrace1
fibLevel2 = fibLow + (fibHigh - fibLow) * fibRetrace2
fibLevel3 = fibLow + (fibHigh - fibLow) * fibRetrace3

// Plot Fibonacci levels on the chart
plot(fibLevel1, title="Fib 0.236", color=color.blue, linewidth=1)
plot(fibLevel2, title="Fib 0.382", color=color.green, linewidth=1)
plot(fibLevel3, title="Fib 0.618", color=color.red, linewidth=1)

// Buy and Sell conditions
buyCondition = close < lower and close > fibLevel1
sellCondition = close > upper and close < fibLevel3

// Plot Buy and Sell signals
plotshape(buyCondition, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")
plotshape(sellCondition, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

// Execute strategy
if (buyCondition)
    strategy.entry("Buy", strategy.long)

if (sellCondition)
    strategy.exit("Sell", "Buy")
```
```