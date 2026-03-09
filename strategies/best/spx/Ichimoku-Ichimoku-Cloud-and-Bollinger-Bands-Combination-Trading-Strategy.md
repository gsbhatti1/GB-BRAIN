``` pinescript
/*backtest
start: 2023-12-19 00:00:00
end: 2023-12-26 00:00:00
period: 10m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Coinrule

//@version=5
strategy("Ichimoku Cloud and Bollinger Bands",
         overlay=true,
         initial_capital=1000,
         process_orders_on_close=true,
         default_qty_type=strategy.percent_of_equity,
         default_qty_value=30,
         commission_type=strategy.commission.percent,
         commission_value=0.1)

showDate = input(defval=true, title='Show Date Range')
timePeriod = true
notInTrade = strategy.position_size <= 0


//Ichimoku Cloud
//Inputs
ts_bars = input.int(9, minval=1, title="Tenkan-Sen Bars")
ks_bars = input.int(26, minval=1, title="Kijun-Sen Bars")
ssb_bars = input.int(52, minval=1, title="Senkou-Span B Bars")
cs_offset = input.int(26, minval=1, title="Chikou-Span Offset")
ss_offset = input.int(26, minval=1, title="Senkou-Span Offset")
long_entry = input(true, title="Long Entry")
short_entry = input(true, title="Short Entry")

middle(len) => math.avg(ta.lowest(len), ta.highest(len))

// Components of Ichimoku Cloud
tenkan = middle(ts_bars)
kijun = middle(ks_bars)
senkouA = math.avg(tenkan, kijun)
senkouB = middle(ssb_bars)

// Bollinger Bands
lengthBB = input.int(20, minval=1, title="Length")
stdDev = input.float(2.0, title="StdDev")
src = input(close, title="Source")

upperBand = ta.sma(src, lengthBB) + stdDev * ta.stdev(src, lengthBB)
lowerBand = ta.sma(src, lengthBB) - stdDev * ta.stdev(src, lengthBB)

// Conditions
bullishSignal = notInTrade and tenkan > kijun and cs_offset < senkouA and src > upperBand
bearishSignal = notInTrade and tenkan < kijun and cs_offset > senkouB and src < lowerBand

if (bullishSignal)
    strategy.entry("Long", strategy.long)

if (bearishSignal)
    strategy.exit("Short", from_entry="Long")

// Plotting
plot(notInTrade ? na : close, title="Close Price", color=color.gray, linewidth=1)
plot(notInTrade ? na : tenkan, title="Tenkan-Sen", color=color.blue, linewidth=2)
plot(notInTrade ? na : kijun, title="Kijun-Sen", color=color.orange, linewidth=2)
plot(notInTrade ? na : senkouA, title="Senkou Span A", color=color.green, linewidth=1)
plot(notInTrade ? na : senkouB, title="Senkou Span B", color=color.red, linewidth=1)
fill(area(hline(0, "Zero Line"), upperBand), color=color.blue, transp=90)
fill(area(hline(0, "Zero Line"), lowerBand), color=color.red, transp=90)
plot(notInTrade ? na : src > upperBand ? upperBand : na, title="Upper Band", color=color.blue)
plot(notInTrade ? na : src < lowerBand ? lowerBand : na, title="Lower Band", color=color.red)

```