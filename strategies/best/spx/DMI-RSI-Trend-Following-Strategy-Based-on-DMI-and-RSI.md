```pinescript
// Uzun pozisyon açma koşullarını tanımlayalım
longCondition1 = rsiValue < rsiOversold // RSI oversold seviyesinin altındaysa
longCondition2 = adx > 20 // ADX 20'den büyükse
longCondition3 = ta.crossover(plus, minus) // +DI -DI üzerinde geçiş yapmışsa

// Kısa pozisyon açma koşullarını tanımlayalım
shortCondition1 = rsiValue > rsiOverbought // RSI overbought seviyesinin üstündeyse
shortCondition2 = adx < 20 // ADX 20'den küçükse
shortCondition3 = ta.crossunder(plus, minus) // +DI -DI altında geçiş yapmışsa

// Uzun pozisyon açma koşullarının tümünü sağlayan durumda uzun pozisyona girilir.
if (longCondition1 and longCondition2 and longCondition3)
    strategy.entry("Long Position", strategy.long)

// Kısa pozisyon açma koşullarının tümünü sağlayan durumda kısa pozisyona girilir.
if (shortCondition1 and shortCondition2 and shortCondition3)
    strategy.entry("Short Position", strategy.short)

// Hedefli stop-loss ve trailing stop-loss ayarlamak
var float trailStopPrice = na
longPos := strategy.position_size > 0
shortPos := strategy.position_size < 0

if (longPos)
    if ta.close_above(trailStopPrice, close) and not ta.valuewhen(longPos, true, 1)
        strategy.exit("Trail Stop Loss", "Long Position")
        trailStopPrice := close * (1 - trailing_stop_loss_factor)

if (shortPos)
    if ta.close_below(trailStopPrice, close) and not ta.valuewhen(shortPos, true, 1)
        strategy.exit("Trail Stop Loss", "Short Position")
        trailStopPrice := close * (1 + trailing_stop_loss_factor)
```

In this Pine Script, the conditions for entering long and short positions are defined based on the DMI and RSI indicators. The script also sets up a trailing stop-loss mechanism to lock in profits.
```pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-24 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © YingYangJPN

//@version=5
strategy("DMI and RSI Strategy", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// DMI indikatörünü tanımlayalım
lensig = input.int(14, title="ADX Smoothing", minval=1, maxval=50)
len = input.int(14, minval=1, title="DI Length")
up = ta.change(high)
down = -ta.change(low)
plusDM = na(up) ? na : (up > down and up > 0 ? up : 0)
minusDM = na(down) ? na : (down > up and down > 0 ? down : 0)
trur = ta.rma(ta.tr, len)
plus = fixnan(100 * ta.rma(plusDM, len) / trur)
minus = fixnan(100 * ta.rma(minusDM, len) / trur)
sum = plus + minus
adx = 100 * ta.rma(math.abs(plus - minus) / (sum == 0 ? 1 : sum), lensig)
trailing_stop_loss_factor = input.float(0.50, "Trailing Stop Loss Factor", step = 0.01)

// RSI indikatörünü tanımlayalım
rsiLength = input.int(14, minval=1, title="RSI Length")
rsiSource = input(close, title="RSI Source")
rsiOverbought = input.int(70, title="RSI Overbought Level")
rsiOversold = input.int(30, title="RSI Oversold Level")
rsiValue = ta.rsi(rsiSource, rsiLength)

// Uzun pozisyon açma koşullarını tanımlayalım
longCondition1 = rsiValue < rsiOversold // RSI oversold seviyesinin altındaysa
longCondition2 = adx > 20 // ADX 20'den büyükse
longCondition3 = ta.crossover(plus, minus) // +DI -DI üzerinde geçiş yapmışsa

// Kısa pozisyon açma koşullarını tanımlayalım
shortCondition1 = rsiValue > rsiOverbought // RSI overbought seviyesinin üstündeyse
shortCondition2 = adx < 20 // ADX 20'den küçükse
shortCondition3 = ta.crossunder(plus, minus) // +DI -DI altında geçiş yapmışsa

// Uzun pozisyon açma koşullarının tümünü sağlayan durumda uzun pozisyona girilir.
if (longCondition1 and longCondition2 and longCondition3)
    strategy.entry("Long Position", strategy.long)

// Kısa pozisyon açma koşullarının tümünü sağlayan durumda kısa pozisyona girilir.
if (shortCondition1 and shortCondition2 and shortCondition3)
    strategy.entry("Short Position", strategy.short)

// Hedefli stop-loss ve trailing stop-loss ayarlamak
var float trailStopPrice = na
longPos := strategy.position_size > 0
shortPos := strategy.position_size < 0

if (longPos)
    if ta.close_above(trailStopPrice, close) and not ta.valuewhen(longPos, true, 1)
        strategy.exit("Trail Stop Loss", "Long Position")
        trailStopPrice := close * (1 - trailing_stop_loss_factor)

if (shortPos)
    if ta.close_below(trailStopPrice, close) and not ta.valuewhen(shortPos, true, 1)
        strategy.exit("Trail Stop Loss", "Short Position")
        trailStopPrice := close * (1 + trailing_stop_loss_factor)
```