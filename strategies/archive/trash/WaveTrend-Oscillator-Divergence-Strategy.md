``` pinescript
/*backtest
start: 2023-05-22 00:00:00
end: 2024-05-27 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("PipShiesty Swagger", overlay=true)

// WaveTrend Oscillator (WT)
n1 = input.int(10, "Channel Length")
n2 = input.int(21, "Average Length")
obLevel1 = input.float(60.0, "Overbought Level 1")
obLevel2 = input.float(53.0, "Overbought Level 2")
osLevel1 = input.float(-60.0, "Oversold Level 1")
osLevel2 = input.float(-53.0, "Oversold Level 2")

ap = hlc3
esa = ta.ema(ap, n1)
d = ta.ema(math.abs(ap - esa), n1)
ci = (ap - esa) / d
wt = ta.rma(ci, n2)

// Volume Weighted Average Price (VWAP)
timeWindow = input.int(10, "Time Window")
vwap = ta.vwa(close * volume, timeWindow)

// Divergence Check
divergenceCheck(price, wt, vwap) =>
    bearishDiv = na(prevWt) or prevWt > wt and price < prevPrice
    bullishDiv = na(prevWt) or prevWt < wt and price > prevPrice
    [bearishDiv, bullishDiv]

prevWt = wt[1]
prevPrice = close[1]

// Entry Conditions
longCondition = divergenceCheck(close, wt, vwap)[1] == true and wt > obLevel2 and vwap > close
shortCondition = divergenceCheck(close, wt, vwap)[0] == true and wt < osLevel2 and vwap < close

if (longCondition)
    strategy.entry("Long", strategy.long)

if (shortCondition)
    strategy.close("Long")

// Stop-Loss
atrLength = input.int(14, "ATR Length")
stopLossMultiplier = input.float(2.0, "Stop Loss Multiplier")
stopLossLevel = wt - stopLossMultiplier * ta.atr(atrLength)

strategy.exit("Exit Long", from_entry="Long", stop=stopLossLevel)

// Position Sizing
riskPercentage = input.float(1.0, "Risk Percentage")
maxPositionSize = riskPercentage / 100 * account.margin_balance
positionSize = min(maxPositionSize, stopLossLevel - wt)
strategy.exit("Exit Long", from_entry="Long", size=positionSize)

// Background Color
bgcolor(wt > obLevel2 ? color.new(color.green, 90) : wt < osLevel2 ? color.new(color.red, 90) : na)
```

Note: This script is a continuation of the provided Pine Script and includes necessary components such as calculating the WaveTrend Oscillator (WT), Volume Weighted Average Price (VWAP), divergence check, entry conditions, stop-loss, position sizing, and background color changes. Ensure all inputs are correctly set for your specific trading needs.