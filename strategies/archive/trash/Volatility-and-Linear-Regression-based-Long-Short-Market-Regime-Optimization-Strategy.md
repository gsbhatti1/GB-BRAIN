``` pinescript
/*backtest
start: 2023-05-22 00:00:00
end: 2024-05-27 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © tmalvao

//@version=5
strategy("Regime de Mercado com Regressão e Volatilidade Otimizado", overlay=true)

// Parâmetros para otimização
upperThreshold = input.float(1.0, title="Upper Threshold")
lowerThreshold = input.float(-1.0, title="Lower Threshold")
length = input.int(50, title="Length", minval=1)

// Indicadores de volatilidade
atrLength = input.int(14, title="ATR Length")
atrMult = input.float(2.0, title="ATR Multiplier")
atr = ta.atr(atrLength)
volatility = atr * atrMult

// Calculando a regressão linear usando função incorporada
intercept = ta.linreg(close, length, 0)
slope = ta.linreg(close, length, 1) - ta.linreg(close, length, 0)

// Sinal de compra e venda
buySignal = slope > upperThreshold and close > intercept + volatility
sellSignal = slope < lowerThreshold and close < intercept - volatility

// Entrando e saindo das posições
if (buySignal)
    strategy.entry("Long", strategy.long) // Inicia posição longa

// Adicionar lógica para sair da posição longa aqui
```