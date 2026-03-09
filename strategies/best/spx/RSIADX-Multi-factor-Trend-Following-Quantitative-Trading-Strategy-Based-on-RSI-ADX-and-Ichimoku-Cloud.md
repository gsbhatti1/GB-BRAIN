``` pinescript
/*backtest
start: 2023-05-11 00:00:00
end: 2024-05-16 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Multi-factor Trend Following Strategy Based on RSI, ADX and Ichimoku Cloud", overlay=true, margin_long=100, margin_short=100)

// ADX, RSI ve Ichimoku tanımları
[diPlus, diMinus, adx] = ta.dmi(14, 14)
rsiPeriod = 14
rsi = ta.rsi(close, rsiPeriod)
tenkanPeriod = 9
kijunPeriod = 26
senkouSpanBPeriod = 52
displacement = 26
tenkan = ta.sma((high + low) / 2, tenkanPeriod)
kijun = ta.sma((high + low) / 2, kijunPeriod)
senkouSpanA = (tenkan + kijun) / 2
senkouSpanB = ta.sma((high + low) / 2, senkouSpanBPeriod)

// Ichimoku Bulutu koşulları
priceAboveCloud = close > ta.valuewhen(bar_index, math.max(senkouSpanA, senkouSpanB), displacement)
priceBelowCloud = close < ta.valuewhen(bar_index, math.min(senkouSpanA, senkouSpanB), displacement)

// İşlem Koşulları
adxCondition = adx > 20
rsiConditionLong = rsi < ta.sma(rsi, 14) and priceAboveCloud
rsiConditionShort = rsi > ta.sma(rsi, 14) and priceBelowCloud

if (adxCondition and rsiConditionLong)
    strategy.entry("Long", strategy.long)

if (adxCondition and rsiConditionShort)
    strategy.entry("Short", strategy.short)

// Stop-Loss ve Take-Profit
stopLoss = 50 * syminfo.mintick
takeProfit = 100 * syminfo.mintick

strategy.exit("Long Exit", "Long", stop=stopLoss, limit=takeProfit)
strategy.exit("Short Exit", "Short", stop=stopLoss, limit=takeProfit)

// Grafik Üzerinde Ekrana Çizim
plot(adx, title="ADX", color=color.blue)
plot(rsi, title="RSI", color=color.red)
plot(senkouSpanA, title="Senkou Span A", color=color.green, style=plot.style_linebr)
plot(senkouSpanB, title="Senkou Span B", color=color.orange, style=plot.style_linebr)
```

This Pine Script code translates and modifies the original script to include logic based on the given strategy description. The `ADX`, `RSI`, and `Ichimoku Cloud` conditions are implemented as described in the text, along with entry/exit criteria and basic stop-loss/take-profit mechanisms.