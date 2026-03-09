``` pinescript
/*backtest
start: 2020-09-13 00:00:00
end: 2023-09-19 00:00:00
period: 3d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("SuperTrend Long Strategy", overlay=true, initial_capital=50000, currency=currency.USD, default_qty_type=strategy.cash, default_qty_value=50000)

Periods = input(title="ATR Period", type=input.integer, defval=10)
src = input(hl2, title="Source")
Multiplier = input(title="ATR Multiplier", type=input.float, step=0.1, defval=3.0)
changeATR = input(title="Change ATR Calculation Method ?", type=input.bool, defval=true)
showsignals = input(title="Show Buy/Sell Signals ?", type=input.bool, defval=false)
highlighting = input(title="Highlighter On/Off ?", type=input.bool, defval=true)
barcoloring = input(title="Bar Coloring On/Off ?", type=input.bool, defval=true)

atr2 = sma(tr, Periods)
atr = changeATR ? atr(Periods) : atr2

up = src - (Multiplier * atr)
up1 = nz(up[1], up)
up := close[1] > up1 ? max(up, up1) : up

dn = src + (Multiplier * atr)
dn1 = nz(dn[1], dn)
dn := close[1] < dn1 ? min(dn, dn1) : dn

trend = 1
trend := nz(trend[1], trend)
trend := trend == -1 and close > dn ? 1 : trend
trend := trend == 1 and close < up ? -1 : trend

buySignal = trend == 1 and close > up
sellSignal = trend == -1 and close < dn

if (buySignal)
    strategy.entry("Buy", strategy.long)

if (sellSignal)
    strategy.exit("Sell", "Buy")

plot(showsignals ? up : na, color=green, title="Buy Signal", style=plot.style_line)
plot(showsignals ? dn : na, color=red, title="Sell Signal", style=plot.style_line)
```

Note: The code snippet was completed and adjusted to ensure it aligns with the strategy described. The missing part of the `trend` logic was added to finalize the script.