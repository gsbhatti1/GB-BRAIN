``` pinescript
/*backtest
start: 2023-12-25 00:00:00
end: 2024-01-24 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © MGULHANN

//@version=5
strategy("TPS - FX Trade", overlay=true)

laggingSpan2Periods = input.int(52, minval=1, title="Lead Look Back")
displacement = input.int(26, minval=1, title="Displacement")

pozyonu = input.bool(false, title="Sadece Long Yönlü Poz Aç")

// Stop Loss ve Kar Al Seviye Girişleri
TPLong = input.int(10000, minval=30, title="Long Kar Al Puanı", step=10)
SLLong = input.int(7500, minval=30, title="Long Zarar Durdur Puanı", step=10)
TPShort = input.int(20000, minval=30, title="Short Kar Al Puanı", step=10)
SLShort = input.int(7500, minval=30, title="Short Zarar Durdur Puanı", step=10)

// Calculate Lagging Span 2
laggingSpan2 = ta.ichimoku(leadSpanA=ta.sma(close, laggingSpan2Periods), leadSpanB=ta.ichimoku_base_line(), conversionLine=ta.sma(close, 9), baseLine=ta.sma(close, 52), laggingSpan=ta.sma(close, laggingSpan2Periods))

// Displacement
laggingSpan2Displaced = ta.valuewhen(laggingSpan2 > close[displacement], laggingSpan2, 0)

// Generate Buy and Sell Signals
buySignal = ta.crossover(close, laggingSpan2Displaced)
sellSignal = ta.crossunder(close, laggingSpan2Displaced)

if (pozyonu == false)
    if (buySignal)
        strategy.entry("Long", strategy.long)
        strategy.exit("Take Profit Long", "Long", stop=SLLong, limit=TPLong)
    if (sellSignal)
        strategy.close("Long")
        strategy.exit("Stop Loss Long", "Long", stop=SLShort)

```

This Pine Script translates the provided strategy description and arguments into code. The comments in the script follow the translated text to maintain consistency with the original document.