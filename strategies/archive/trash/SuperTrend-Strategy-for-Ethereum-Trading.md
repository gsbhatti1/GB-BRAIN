```pinescript
/*backtest
start: 2023-01-01 00:00:00
end: 2024-01-07 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4 
strategy("SuperTrend Strategy", 
     overlay=true, 
     initial_capital=2e3, 
     process_orders_on_close=true, 
     commission_type=strategy.commission.percent, 
     commission_value=0.1 
     ) 
  
length = input(title="ATR Period", type=input.integer, defval=21) 
mult = input(title="ATR Multiplier", type=input.float, step=.25, defval=6.2) 
wicks = input(title="Take Wicks into Account ?", type=input.bool, defval=false) 
  
useDate = input(title="Start from Specific Date ?", defval=false) 
yearStart = input(title="Start Year", defval=2019) 
monthStart = input(title="Start Month", minval=1, maxval=12, defval=1) 
dayStart = input(title="Start Day", minval=1, maxval=31, defval=1) 
  
startTime = timestamp(yearStart, monthStart, dayStart, 0, 0) 
startFrom = useDate ? time(timeframe.period) >= startTime : true 
  
atr = mult * ta.atr(length) 
  
longStop = hl2 - atr 
longStopPrev = nz(longStop[1], longStop) 
longStop := (wicks ? low[1] : close[1]) > longStopPrev ? math.max(longStop, longStopPrev) : longStop 
  
shortStop = hl2 + atr 
shortStopPrev = nz(shortStop[1], shortStop) 
shortStop := (wicks ? high[1] : close[1]) < shortStopPrev ? math.min(shortStop, shortStopPrev) : shortStop 
  
dir = 1 
dir := nz(dir[1], dir) 
dir := dir == -1 and (wicks ? high : close) > shortStopPrev ? 1 : dir == 1 and (wicks ? low : close) < longStopPrev ? -1 : dir 
  
longColor = color.green 
shortColor = color.red 
  
plot(dir == 1 ? longStop : na, title="Long Stop", styl
```