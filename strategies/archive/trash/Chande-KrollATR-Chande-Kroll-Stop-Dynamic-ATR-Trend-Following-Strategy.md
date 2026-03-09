``` pinescript
/*backtest
start: 2023-06-08 00:00:00
end: 2024-06-13 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Chande-Kroll Stop Dynamic ATR Trend Following Strategy", overlay=true)

// Parameters
atrLen = input(21, title="ATR Length")
atrMult = input(3.0, title="ATR Multiplier")
smaLen = input(21, title="SMA Length")
riskMultiplier = input(2.0, title="Risk Multiplier")

// Chande-Kroll Stop
var float chandeKrollStop = na
chandeKrollStop := close < ta.sma(close, atrLen) ? close - (atrLen * atrMult) : chandeKrollStop

// 21-period SMA
smaValue = ta.sma(close, smaLen)

// Strategy Logic
if (close > chandeKrollStop and close > smaValue)
    strategy.entry("Long", strategy.long)

if (close < chandeKrollStop)
    strategy.close("Long")

// Plotting
plot(chandeKrollStop, color=color.red, title="Chande-Kroll Stop")
plot(smaValue, color=color.blue, title="21-period SMA")

```

```