``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 5h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy(title="Revolut v1.0", overlay=true)

// === GENERAL INPUTS ===
ATR = atr(3)
ema3 = ema(close, 3)
ema5 = ema(close, 5)

// === INPUT BACKTEST RANGE ===
FromMonth = input(defval = 1, title = "From Month", minval = 1, maxval = 12)
FromDay   = input(defval = 1, title = "From Day", minval = 1, maxval = 31)
FromYear  = input(defval = 2018, title = "From Year", minval = 2017)
ToMonth   = input(defval = 1, title = "To Month", minval = 1, maxval = 12)
ToDay     = input(defval = 1, title = "To Day", minval = 1, maxval = 31)
ToYear    = input(defval = 9999, title = "To Year", minval = 2017)

// === FUNCTION EXAMPLE ===
start     = timestamp(FromYear, FromMonth, FromDay, 00, 00)  // backtest start window
finish    = timestamp(ToYear, ToMonth, ToDay, 23, 59)        // backtest finish window
window()  => true// create function "within window of time"

// === ENTRY POSITION LOGIC ===
entryCondition = crossover(ema3, ema5)

// === EXIT POSITION LOGIC ===
exitLongCondition = low < (ema3 - (ATR * 2))
exitShortCondition = high > (ema3 + (ATR * 2))

// === ORDER MANAGEMENT ===
if (entryCondition)
    strategy.entry("Long", strategy.long)

if (exitLongCondition or exitShortCondition)
    strategy.close("Long")

// === PLOTTING ===
plot(ema3, title="Ema 3", color = white, linewidth = 2, transp=0)
plot(ema5, title="Ema 5", color = aqua, linewidth = 2, transp=0)
```