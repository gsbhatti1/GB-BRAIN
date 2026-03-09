``` pinescript
/*backtest
start: 2024-04-01 00:00:00
end: 2024-04-30 23:59:59
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("EMA Cross Strategy with RSI Divergence, 30-Minute Trend Identification, and Price Exhaustion", overlay=true)

// Definição das médias móveis exponenciais para tendência de curto prazo (30 minutos)
EMA5_30min = ta.ema(close, 5)
EMA10_30min = ta.ema(close, 10)

// Definição das médias móveis exponenciais
EMA13 = ta.ema(close, 13)
EMA26 = ta.ema(close, 26)

// RSI com período padrão de 7
rsi = ta.rsi(close, 7)

// Detecção do cruzamento das EMAs
crossUp = ta.crossover(EMA13, EMA26)
crossDown = ta.crossunder(EMA13, EMA26)

// Detecção de divergência no RSI
bullishDivergence = ta.crossunder(close, EMA13) and ta.crossunder(rsi, 
```