> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|50|length|
|v_input_2|50|smoothe|
|v_input_3|false|Trade reverse|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-04 00:00:00
end: 2024-01-31 23:59:00
symbol: ETH/USD
live: true
*/

//@version=5
strategy("Donchian Channel Width Trading Strategy", overlay=true)

// Input parameters
length = input(50, title="Length")
smoothe = input(50, title="Smoothe")
tradeReverse = input(false, title="Trade reverse", type=input.bool)

// Calculate Donchian Channel Width
highLength = ta.highest(high, length)
lowLength = ta.lowest(low, length)
donchianWidth = highLength - lowLength

// Smooth Donchian Channel Width
smaDonchianWidth = ta.sma(donchianWidth, smoothe)

// Determine trading direction based on the comparison of Donchian Channel Width and its SMA
if (donchianWidth > smaDonchianWidth and not tradeReverse)
    strategy.entry("Long", strategy.long)
else if (donchianWidth < smaDonchianWidth and not tradeReverse)
    strategy.entry("Short", strategy.short)
else if (donchianWidth < smaDonchianWidth and tradeReverse)
    strategy.entry("Long", strategy.long)
else if (donchianWidth > smaDonchianWidth and tradeReverse)
    strategy.entry("Short", strategy.short)

// Plotting
plot(donchianWidth, color=color.blue, title="Donchian Channel Width")
plot(smaDonchianWidth, color=color.red, title="Smoothed Donchian Channel Width")
```