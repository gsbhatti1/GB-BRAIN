``` pinescript
/*backtest
start: 2023-06-11 00:00:00
end: 2024-06-16 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("20 EMA and Supertrend Strategy", overlay=true)

// Inputs
emaLength = input(20, title="EMA Length")
supertrendMultiplier = input.float(3.0, title="Supertrend Multiplier")
supertrendPeriod = input(10, title="Supertrend Period")

// EMA Calculation
ema = ta.ema(close, emaLength)

// Supertrend Calculation
Periods = supertrendPeriod
src = hl2
Multiplier = supertrendMultiplier
changeATR= input.bool(true, title="Change ATR Calculation Method?")
showsignals = input.bool(true, title="Show Buy/Sell Signals?")
highlighting = input.bool(true, title="Highlighter On/Off?")
atr2 = ta.sma(ta.tr, Periods)
atr = changeATR ? ta.atr(Periods) : atr2
up = src - (Multiplier * atr)
up1 = na(up[1]) ? up : up[1]
up := close[1] > up1 ? math.max(up, up1) : up
dn =
```