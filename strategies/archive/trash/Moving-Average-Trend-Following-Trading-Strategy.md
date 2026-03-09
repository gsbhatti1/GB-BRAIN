``` pinescript
/*backtest
start: 2023-12-03 00:00:00
end: 2023-12-10 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
strategy("Moving-Average-Trend-Following-Trading-Strategy", default_qty_type = strategy.percent_of_equity, default_qty_value = 100, currency="USD", initial_capital=662, overlay=false)

l = input(defval=170, title="Length for indicator")
s = input(title="Length of summation", defval=18)
a = sma(close, l)
r = roc(close, l)
k = close - a
sum = 0
for i = 0 to s
    sum := sum + k[i]
//plot(a, color=yellow, linewidth=2, transp=0)
//bc = iff( sum > 0, white, teal)
//plot(sum, color=bc, transp=20, linewidth=3, style=columns)
//plot(sma(sum, 3), color=white)
//hline(0)

inpTakeProfit = input(defval=0, title="Take Profit", minval=0)
inpStopLoss = input(defval=0, title="Stop Loss", minval=0)
inpTrailStop = input(defval=0, title="Trailing Stop Loss", minval=0)
inpTrailOffset = input(defval=0, title="Trailing Stop Loss Offset", minval=0)
useTakeProfit = inpTakeProfit >= 1 ? inpTakeProfit : na
useStopLoss = inpStopLoss >= 1 ? inpStopLoss : na
useTrailStop = inpTrailStop >= 1 ? inpTrailStop : na
useTrailOffset = inpTrailOffset >= 1 ? inpTrailOffset : na

////buyEntry = crossover(source, lower)
////sellEntry = crossunder(source, upper)
if sum > 0
    strategy.entry("Long Position", strategy.long, oca_name="One-Cancels-All", comment="Enter Long")
else
    strategy.close("Long Position")

// Additional logic for trailing stop loss can be added here if needed.
```