``` pinescript
/*backtest
start: 2022-11-09 00:00:00
end: 2023-11-15 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © KivancOzbilgic


//@version=4
strategy("Trenbolone Strategy", overlay = true)
Periods = input(title="ATR Period", type=input.integer, defval=10)
src = input(hl2, title="Source")
Multiplier = input(title="ATR Multiplier", type=input.float, step=0.1, defval=3.0)
changeATR= input(title="Change ATR Calculation Method ?", type=input.bool, defval=true)
showsignals = input(title="Show Buy/Sell Signals ?", type=input.bool, defval=false)
highlighting = input(title="Highlighter On/Off ?", type=input.bool, defval=true)
barcoloring = input(title="Bar Coloring On/Off ?", type=input.bool, defval=true)
atr2 = sma(tr, Periods)
atr= changeATR ? atr(Periods) : atr
buyPrice = na
sellPrice = na
up = ta.highest(high, Periods)
down = ta.lowest(low, Periods)
buyCondition = close >= up - Multiplier * atr
sellCondition = close <= down + Multiplier * atr

if (buyCondition)
    buyPrice := close
    strategy.entry("Long", strategy.long)
    if (highlighting)
        plotshape(series=buyCondition, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.triangledown, size=size.small)
    if (barcoloring)
        bgcolor(buyCondition ? color.new(color.green, 90) : na)

if (sellCondition)
    sellPrice := close
    strategy.exit("Short", "Long")
    if (highlighting)
        plotshape(series=sellCondition, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)
    if (barcoloring)
        bgcolor(sellCondition ? color.new(color.red, 90) : na)

if (showsignals)
    label.new(x=bar_index, y=na, text="Buy", color=color.green, style=label.style_label_down, size=size.small)
    label.new(x=bar_index, y=na, text="Sell", color=color.red, style=label.style_label_up, size=size.small)
```