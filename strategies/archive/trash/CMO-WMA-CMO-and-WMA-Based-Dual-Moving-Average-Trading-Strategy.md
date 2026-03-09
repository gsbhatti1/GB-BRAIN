> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|9|Length|
|v_input_2|9|LengthWMA|
|v_input_3|60|BuyZone|
|v_input_4|-60|SellZone|
|v_input_5|false|Trade reverse|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-25 00:00:00
end: 2024-01-24 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 18/10/2018
//    This indicator plots Chandre Momentum Oscillator and its WMA on the 
//    same chart. This indicator plots the absolute value of CMO.
//    The CMO is closely related to, yet unique from, other momentum oriented 
//    indicators such as Relative Strength Index, Stochastic, Rate-of-Change
//

study("CMO-and-WMA-Based-Dual-Moving-Average-Trading-Strategy", shorttitle="CMO WMA Strategy", overlay=true)

length = input(9, title="Length")
lengthWMA = input(9, title="LengthWMA")
buyZone = input(60, title="BuyZone")
sellZone = input(-60, title="SellZone")
tradeReverse = input(false, title="Trade reverse")

// Calculate CMO
cmoValue = cmo(close, length)
plot(abs(cmoValue), color=blue, title="CMO Absolute Value")

// Calculate WMA of CMO
wmaCmo = wma(cmoValue, lengthWMA)
plot(wmaCmo, color=red, title="CMOWMA")

// Generate buy and sell signals based on CMO crossovers with its WMA
longCondition = crossover(cmoValue, wmaCmo) and not tradeReverse or (cmoValue > 0 and cmoValue < buyZone)
shortCondition = crossunder(cmoValue, wmaCmo) and not tradeReverse or (cmoValue < 0 and cmoValue > sellZone)

// Plot buy and sell signals
plotshape(series=longCondition, location=location.belowbar, color=green, style=shape.triangleup, title="Buy Signal")
plotshape(series=shortCondition, location=location.abovebar, color=red, style=shape.triangledown, title="Sell Signal")

// Strategy definition
strategy("CMO WMA Strategy", shorttitle="Strategy", default_qty_type=strategy.percent_of_equity, default_qty_value=10)
strategy.entry("Long", strategy.long, when=longCondition)
strategy.exit("Close Long", "Long", limit=sellZone)
strategy.close_all()
```

This PineScript defines a strategy based on the CMO and WMA crossover. It includes inputs for parameters such as length of CMO and WMA, buy/sell zones, and whether to trade in reverse. The script plots both CMO and its WMA on the chart and generates buy/sell signals when these lines cross over or under each other.