``` pinescript
/*backtest
start: 2022-12-10 00:00:00
end: 2023-06-16 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy(title = "Double Moving Average Crossover Strategy", shorttitle = "DMAC Strategy", overlay = true, pyramiding = 0, default_qty_type = strategy.cash, default_qty_value = 1000, commission_value = 0.0675, initial_capital = 1000, currency = currency.USD, calc_on_order_fills = true, calc_on_every_tick = true)

maFastSource   = input(defval = ohlc4, title = "Fast MA Source")
maFastLength   = input(defval = 15, title = "Fast MA Period", minval = 1)
maSlowSource   = input(defval = ohlc4, title = "Slow MA Source")
maSlowLength   = input(defval = 21, title = "Slow MA Period", minval = 1)

tradeInvert     = input(defval = false, title = "Invert Trade Direction?")
inpTakeProfit   = input(defval = 100, title = "Take Profit percentage(0.1%)", minval = 0)
inpStopLoss     = input(defval = 100, title = "Stop Loss", minval = 0)
trailStopLossOffset = input(defval = false, title = "Trailing Stop Loss Offset")
useStartTimeLimiter   = input(defval = true, title = "Use Start Time Limiter?")
startYear         = input(defval = 2018, title = "Start From Year", minval = 1970)
startMonth        = input(defval = 5, title = "Start From Month", minval = 1, maxval = 12)
startDay          = input(defval = true, title = "Start From Day")
startHour         = input(defval = false, title = "Start From Hour")
startMinute       = input(defval = false, title = "Start From Minute")

if useStartTimeLimiter
    startCondition = time >= timestamp(year(startYear), month(startMonth), dayofmonth(startDay), hour(startHour == true ? 9 : 0), minute(startMinute == true ? 30 : 0))
else
    startCondition = true

if (startCondition)
    if crossover(maFastSource, maSlowSource)
        strategy.entry("Long", strategy.long)
    else if crossunder(maFastSource, maSlowSource)
        strategy.entry("Short", strategy.short)

    strategy.exit("Take Profit/Stop Loss", "Long", profit = inpTakeProfit / 1000, loss = inpStopLoss / 1000)
    
    if (trailStopLossOffset)
        strategy.exit("Trailing Stop Loss", "Long", loss = trailStopLossOffset / 1000)

```
```