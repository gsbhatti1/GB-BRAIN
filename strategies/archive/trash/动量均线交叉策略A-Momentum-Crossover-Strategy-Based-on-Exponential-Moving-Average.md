``` pinescript
/*backtest
start: 2024-01-15 00:00:00
end: 2024-01-22 00:00:00
period: 3m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
strategy("PierceMAStrat", overlay=true)

lenMA0 = input(title="Length 0", defval=2)
lenMA1 = input(title="Length 1", defval=10)
lenMA2 = input(title="Length 2", defval=20)
lenMA3 = input(title="Length3", defval=50)

emaLen0 = ema(close, lenMA0)
emaLen1 = ema(close, lenMA1)
emaLen2 = ema(close, lenMA2)
emaLen3 = ema(close, lenMA3)

ascent = if emaLen1[1] < emaLen1[0]
    true
else
    false

descent = if emaLen1[1] > emaLen1[0]
    true
else
    false

TimeSinceAscensionStart = if ascent == true
    barssince(descent == true)
else
    0

StartUp = if TimeSinceAscensionStart < 1
    true
else
    false

StartDown = if TimeSinceAscensionStart < 1
    false
else
    true

AscentBarCounter = barssince(StartUp == true)

DescentBarCounter = barssince(StartDown == true)

MaxAscent = if AscentBarCounter[1] > AscentBarCounter[0]
    AscentBarCounter[0] + 1
else
    AscentBarCounter[0]

MaxDescent = if DescentBarCounter[1] > DescentBarCounter[0]
    DescentBarCounter[0] + 1
else
    DescentBarCounter[0]

longCondition = crossover(emaLen1, emaLen2)
shortCondition = crossunder(emaLen1, emaLen2)

plotshape(series=longCondition, title="Long Entry", location=location.belowbar, color=color.green, style=shape.triangledown, size=size.small)
plotshape(series=shortCondition, title="Short Entry", location=location.abovebar, color=color.red, style=shape.triangleup, size=size.small)

if (longCondition)
    strategy.entry("Long", strategy.long)
if (shortCondition)
    strategy.exit("Short", "Long", limit=emaLen3, stop=emaLen0)
```

This script implements the described strategy in Pine Script, including the conditions for entering long and short positions based on the EMA crossover and plotting the entry points on the chart.