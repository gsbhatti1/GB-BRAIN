``` pinescript
/*backtest
start: 2022-11-29 00:00:00
end: 2023-12-05 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("Weighted Quantitative Moving Average Crossover Strategy", overlay=false, max_bars_back=500, default_qty_type=strategy.percent_of_equity, commission_type=strategy.commission.percent, commission_value=0.18, default_qty_value=100)

// === INPUT BACKTEST RANGE === 
FromMonth = input(defval = 9, title = "From Month", minval = 1, maxval = 12)
FromDay   = input(defval = 1, title = "From Day", minval = 1, maxval = 31)
FromYear  = input(defval = 2018, title = "From Year", minval = 2017)
ToMonth   = input(defval = 1, title = "To Month", minval = 1, maxval = 12)
ToDay     = input(defval = 1, title = "To Day", minval = 1, maxval = 31)
ToYear    = input(defval = 9999, title = "To Year", minval = 2017)

// === FUNCTION EXAMPLE ===
start     = timestamp(FromYear, FromMonth, FromDay, 00, 00)  // backtest start window
finish    = timestamp(ToYear, ToMonth, ToDay, 23, 59)        // backtest finish window
window()  => time >= start and time <= finish ? true : false // create function "within window of time"

// === INPUT SMA === 
fastMA    = input(defval = 25, title = "FastMA", minval = 1 )
slowMA    = input(defval = 29,  title = "SlowMA", minval = 1)

Long_period = slowMA
Short_period = fastMA
Smoothing_period = input(9, minval=1)
xLongMAVolPrice = ema(volume * close, Long_period) 
xLongMAVol = ema(volume, Long_period) 
xResLong = (xLongMAVolPrice * Long_period) / (xLongMAVol * Long_period)
xShortMAVolPrice = ema(volume * close, Short_period) 
xShortMAVol = ema(volume, Short_period) 
xResShort = (xShortMAVolPrice * Short_period) / (xShortMAVol * Short_period)
xVMACD = xResShort - xResLong
xVMACDSignal = ema(xVMACD, Smoothing_period)
nRes = xVMACD - xVMACDSignal
plot(nRes*20+slowMA, color=blue, style = line )
plot(3000, color=red, style = line )

// === SERIES SETUP ===

buy  = crossover(xVMACD, xVMACDSignal)
sell = crossunder(xVMACD, xVMACDSignal)

// === ORDER MANAGEMENT ===
if (buy)
    strategy.entry("Buy", strategy.long)
if (sell)
    strategy.exit("Sell", "Buy")
```

This Pine Script code completes the trading strategy described in the Chinese document. It includes the setup for the weighted moving average calculation, plot functions, and order management for entering and exiting trades based on the crossover conditions.