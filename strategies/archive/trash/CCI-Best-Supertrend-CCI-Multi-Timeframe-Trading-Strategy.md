```pinescript
/*backtest
start: 2024-01-10 00:00:00
end: 2024-01-17 00:00:00
period: 10m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
//@author=Daveatt

StrategyName = "Best Supertrend CCI Strategy"
ShortStrategyName = "Best Supertrend CCI Strategy"

strategy(title=StrategyName, shorttitle=ShortStrategyName, overlay=true )

//////////////////////////
//* COLOR CONSTANTS *//
//////////////////////////

AQUA = #00FFFFFF
BLUE = #0000FFFF
RED  = #FF0000FF
LIGHT_GRAY = #D3D3D3

// Input Definitions
sourceType = input(close, title="Source")
cciPeriod = input(28, title="CCI Period", type=input.integer)
midLinePivot = input(false, title="CCI Mid Line pivot", type=input.bool)
factor = input(3.0, title="[ST] Factor", type=input.float)
pd = input(3.0, title="[ST] PD", type=input.float)

// CCI Indicator
cci = ta.cci(sourceType, cciPeriod)

// Supertrend Calculation
up = hl2 - (factor * ta.atr(pd))
dn = hl2 + (factor * ta.atr(pd))

supertrend = na
trendUp = cci > 0 ? max(up, nz(supertrend[1], up)) : supertrend[1]
trendDown = cci < 0 ? min(dn, nz(supertrend[1], dn)) : supertrend[1]

// Direction of Supertrend
trend := cci > midLinePivot ? 1 : cci < -midLinePivot ? -1 : nz(trend[1], 1)

isLong = trend == 1
isShort = trend == -1

// Plotting
plot(isLong ? up : na, title="Supertrend Up", color=AQUA)
plot(isShort ? dn : na, title="Supertrend Down", color=RED)
hline(midLinePivot, "CCI Mid Line", lightgray)

// Entry and Exit Conditions
longCondition = isLong and not isShort
shortCondition = isShort and not isLong

if (longCondition)
    strategy.entry("Long", strategy.long)

if (shortCondition)
    strategy.entry("Short", strategy.short)

// Optional Stop Loss based on ATR
atrStopLoss = input(3.0, title="ATR Stop Loss")
stopPriceLong = close - atrStopLoss * ta.atr(pd)
stopPriceShort = close + atrStopLoss * ta.atr(pd)

if (longCondition and not isShort)
    strategy.exit("Exit Long", "Long", stop=stopPriceLong)
if (shortCondition and not isLong)
    strategy.exit("Exit Short", "Short", stop=stopPriceShort)

```

This code defines the trading strategy based on the inputs provided, calculates the Supertrend and CCI indicators, and implements entry and exit conditions. The strategy uses the default settings for demonstration purposes but can be adjusted as needed.