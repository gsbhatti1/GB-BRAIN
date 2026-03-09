``` pinescript
/*backtest
start: 2024-01-21 00:00:00
end: 2024-02-20 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © exlux99

//@version=4

strategy(title="3 RSI MA movement crypto strategy", overlay=true, initial_capital = 100, default_qty_type=strategy.percent_of_equity, default_qty_value=100, commission_type=strategy.commission.percent, commission_value=0.03, pyramiding=1)

///////////////
fromDay = input(defval = 1, title = "From Day", minval = 1, maxval = 31)
fromMonth = input(defval = 1, title = "From Month", minval = 1, maxval = 12)
fromYear = input(defval = 2019, title = "From Year", minval = 1970)

// To Date Inputs
toDay = input(defval = 31, title = "To Day", minval = 1, maxval = 31)
toMonth = input(defval = 12, title = "To Month", minval = 1, maxval = 12)
toYear = input(defval = 2021, title = "To Year", minval = 1970)

startDate = timestamp(fromYear, fromMonth, fromDay, 00, 00)
finishDate = timestamp(toYear, toMonth, toDay, 00, 00)
time_cond = time >= startDate and time <= finishDate

source = input(ohlc4)

RSIFast  = rsi(source, 50)
RSINorm  = rsi(source, 75)
RSISlow = rsi(source, 100)

// plot(RSIFast, color=color.silver, style=plot.style_area, histbase=50)
// plot(RSINorm, color=#98b8be, style=plot.style_area, histbase=50)
// plot(RSISlow, color=#be9e98, style=plot.style_area, histbase=50)

// Moving Averages
smaFast  = sma(source, 5)
smaNorm  = sma(source, 30)
smaSlow  = sma(source, 50)
emaFast  = ema(source, 70)
emaNorm  = ema(source, 90)
emaSlow  = ema(source, 100)

// Buy and Sell Signals
longSignal = crossover(RSIFast, smaFast) and crossover(RSINorm, smaNorm) and crossover(RSISlow, smaSlow) and crossover(emaFast, smaFast) and crossover(emaNorm, smaNorm) and crossover(emaSlow, smaSlow)
shortSignal = crossunder(RSIFast, smaFast) and crossunder(RSINorm, smaNorm) and crossunder(RSISlow, smaSlow) and crossunder(emaFast, smaFast) and crossunder(emaNorm, smaNorm) and crossunder(emaSlow, smaSlow)

// Trade Logic
if (time_cond)
    if longSignal
        strategy.entry("Long", strategy.long)
    if shortSignal
        strategy.close("Long")
```

This Pine Script implements the described three RSI moving average bands strategy. It includes the necessary variables and logic for generating buy/sell signals based on the overlapping of RSI values with their respective moving averages, as well as the given time constraints.