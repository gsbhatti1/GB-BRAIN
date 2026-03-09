``` pinescript
/*backtest
start: 2024-05-17 00:00:00
end: 2024-06-16 00:00:00
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Cruce de Medias con Filtros de RSI y Estocástico", overlay=true)

// Definir parámetros de las medias móviles
fast_length = input(20, title="Periodo de Media Rápida")
slow_length = input(50, title="Periodo de Media Lenta")

// Calcular medias móviles
fast_ma = ta.sma(close, fast_length)
slow_ma = ta.sma(close, slow_length)

// Añadir filtro RSI
rsi_length = input(7, title="Periodo del RSI")
rsi = ta.rsi(close, rsi_length)
rsi_overbought = input(70, title="RSI de Sobreyacimiento")
rsi_oversold = input(30, title="RSI de Sobreventa")
rsi_filter = rsi > rsi_overbought and rsi < rsi_oversold

// Añadir filtro Estocástico
stoch_k = ta.stoch(close, high, low, 5)
stoch_d = ta.stoch(close, high, low, 5, 3, 3)
stoch_filter = stoch_k > 20 and stoch_d > 20

// Generar señales de compra y venta
long_condition = ta.crossover(fast_ma, slow_ma) and rsi_filter and stoch_filter
short_condition = ta.crossunder(fast_ma, slow_ma) and rsi_filter and stoch_filter

// Definir niveles de stop-loss y take-profit
atr_length = input(14, title="Periodo de ATR")
atr = ta.atr(atr_length)
long_stop = ta.lowest(low, 1) - atr
long_take_profit = ta.highest(high, 1) + 2 * atr
short_stop = ta.highest(high, 1) + atr
short_take_profit = ta.lowest(low, 1) - 2 * atr

// Implementar las señales
if (long_condition)
    strategy.entry("Long", strategy.long)
    strategy.exit("Take Profit Long", "Long", stop=long_stop, limit=long_take_profit)
if (short_condition)
    strategy.entry("Short", strategy.short)
    strategy.exit("Take Profit Short", "Short", stop=short_stop, limit=short_take_profit)

// Plotear las líneas de media móvil, RSI y Estocástico
plot(fast_ma, color=color.blue, title="Media Rápida")
plot(slow_ma, color=color.red, title="Media Lenta")
hline(rsi_overbought, "Rsi Sobreyacimiento", color=color.red)
hline(rsi_oversold, "Rsi Sobreventa", color=color.green)
plot(stoch_k, color=color.orange, title="K Stochastic")
plot(stoch_d, color=color.purple, title="D Stochastic")
```