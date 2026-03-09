```pinescript
/*backtest
start: 2024-01-04 00:00:00
end: 2024-02-03 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
strategy("Forex MA Racer - SMA Performance /w ZeroLag EMA Trigger", shorttitle = "FX MA Racer (5x SMA, 2x zlEMA)", overlay=false )

// === INPUTS ===
hr0             = input(defval = true, title = "=== SERIES INPUTS ===")
smaSource       = input(defval = close, title = "SMA Source")
sma1Length      = input(defval = 10, title = "SMA 1 Length")
sma2Length      = input(defval = 20, title = "SMA 2 Length")
sma3Length      = input(defval = 50, title = "SMA 3 Length")
sma4Length      = input(defval = 100, title = "SMA 4 Length")
sma5Length      = input(defval = 200, title = "SMA 5 Length")
smaDirSpan      = input(defval = 4, title = "SMA Direction Span")
zlmaSource      = input(defval = close, title = "ZeroLag EMA Source")
zlmaFastLength  = input(defval = 9, title = "ZeroLag EMA Fast Length")
zlmaSlowLength  = input(defval = 21, title = "ZeroLag EMA Slow Length")
hr1             = input(defval = true, title = "=== PLOT TIME LIMITER ===")
useStartLimiter = input(defval = true, title = "Use Start Time Limiter?")
startYear       = input(defval = 2018, title = "Start From Year")
startMonth      = input(defval = 2, title = "Start From Month")
startDay        = input(defval = true, title = "Start From Day")
startHour       = input(defval = false, title = "Start From Hour")
startMinute     = input(defval = false, title = "Start From Minute")
trailStop       = input(defval = true, title = "=== TRAILING STOP ===")
useTrailingStop = input(defval = false, title = "Use Trailing Stop?")
trailPoints     = input(defval = 200, title = "Stop Loss Trail Points")
trailOffset     = input(defval = 400, title = "Stop Loss Trail Offset")
```

This translation keeps the code blocks and formatting intact, translating only the human-readable text as requested.