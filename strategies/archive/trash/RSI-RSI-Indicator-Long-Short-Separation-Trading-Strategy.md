``` pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-31 23:59:59
period: 3h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Nextep

//@version=4
strategy(title="RSI top&bottom destroy", overlay=false, pyramiding=4, default_qty_value=2, default_qty_type=strategy.fixed, initial_capital=10000, currency=currency.USD)

// INPUT Settings --------------------------------------------------------------------------------------------------------------------------------------------------
len = input(title="RSI Period", minval=1, defval=13)
src = input(title="RSI Source", defval="close")

lbRshort = input(title="Short Lookback Right", defval=47)  // Short Lookback Range
lbLshort = input(title="Short Lookback Left", defval=1)    // Short Lookback Start

lbRlong = input(title="Long Lookback Right", defval=2)     // Long Lookback End
lbLlong = input(title="Long Lookback Left", defval=14)    // Long Lookback Start

maxLookback = input(title="Max of Lookback Range", minval=1, defval=400)
minLookback = input(title="Min of Lookback Range", defval=true)

takeProfitLevel = input(title="Take Profit at RSI Level", defval=75)
shortTakeProfitLevel = input(title="Take Profit for Short at RSI Level", defval=25)

longStopLossType = input(title="Long Stop Loss Type: PERC|ATR|FIB|NONE", type=input.bool, defval=false)  // Long Stop Loss Type
longStopLossValue = input(title="Long Stop Loss Value", minval=0.1, defval=14)

shortStopLossType = input(title="Short Stop Loss Type: PERC|ATR|FIB|NONE", type=input.bool, defval=false)  // Short Stop Loss Type
shortStopLossValue = input(title="Short Stop Loss Value", minval=0.1, defval=5)

plotBullish = input(title="Plot Bullish", defval=true)
plotBearish = input(title="Plot Bearish", defval=true)

atrLength = input(title="ATR Length (for Trailing stop loss)", minval=1, defval=14)  // ATR Length
atrMultiplier = input(title="ATR Multiplier (for Trailing stop loss)", minval=0.1, defval=3.5)  // ATR Multiplier

// RSI Calculation -------------------------------------------------------------------------------------------------------------------------------------------------
r = rsi(src, len)

// Finding Short Separation Signals --------------------------------------------------------------------------------------------------------------------------------
shortLow = ta.lowest(r, lbLshort)
shortHigh = ta.highest(r, lbRshort)

if (ta.low(r) < shortLow and ta.low(close) > shortHigh)
    strategy.entry("Short", strategy.short)

// Finding Long Separation Signals ---------------------------------------------------------------------------------------------------------------------------------
longLow = ta.lowest(r, lbLlong)
longHigh = ta.highest(r, lbRlong)

if (ta.high(r) > longHigh and ta.high(close) < longLow)
    strategy.entry("Long", strategy.long)

// Plotting -------------------------------------------------------------------------------------------------------------------------------------------------------
plot(takeProfitLevel, title="Take Profit Level", color=color.green, linewidth=2, style=plot.style_linebr)
plot(shortTakeProfitLevel, title="Short Take Profit Level", color=color.blue, linewidth=2, style=plot.style_linebr)

if (plotBullish)
    plotshape(series=strategy.position.entry_price("Long"), location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)
    
if (plotBearish)
    plotshape(series=strategy.position.entry_price("Short"), location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)

// Stop Loss Management --------------------------------------------------------------------------------------------------------------------------------------------
longSL = strategy.position_size > 0 ? math.max(r - longStopLossValue, r - atrMultiplier * ta.atr(atrLength)) : na
shortSL = strategy.position_size < 0 ? math.min(r + shortStopLossValue, r + atrMultiplier * ta.atr(atrLength)) : na

if (strategy.position_size > 0 and r <= longSL)
    strategy.exit("Long Exit", "Short")
    
if (strategy.position_size < 0 and r >= shortSL)
    strategy.exit("Short Exit", "Long")
```

This translated script includes all the original code blocks, numbers, and formatting as requested. The text has been translated from Chinese to English while keeping the Pine Script structure intact.