> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|9|Length RSI|
|v_input_2|9|Length VRSI)|
|v_input_3|5|Length MARSI|
|v_input_4|5|Length MAVRSI|
|v_input_5|true|Xlong|
|v_input_6|true|Xshort|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-02 00:00:00
end: 2024-02-01 00:00:00
period: 3h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("VRSI-MARSI Strategy", shorttitle="(V/MA)RSI Str.", overlay=false, default_qty_type=strategy.percent_of_equity, calc_on_order_fills=true, calc_on_every_tick=true, pyramiding=0, default_qty_value=5, initial_capital=100)

// RSI(close, length) and RSI(Volume, length)
src = close, len = input(9, minval=1, title="Length RSI")
src2 = volume, len2 = input(9, minval=1, title="Length VRSI")
up = rma(max(change(src), 0), len)
down = rma(-min(change(src), 0), len)
up2 = rma(max(change(src2), 0), len2)
down2 = rma(-min(change(src2), 0), len2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))
rsi2 = down2 == 0 ? 100 : up2 == 0 ? 0 : 100 - (100 / (1 + up2 / down2))

// MA(length) of RSI(close, length) and RSI(Volume, length)
len3 = input(5, minval=1, title="Length MARSI")
marsi = sma(rsi, len3)
len4 = input(5, minval=1, title="Length MAVRSI")
marsi2 = sma(rsi2, len4)

// Plot: 
// Default plot of RSI and VRSI: not visible but can be made visible
// Default plot MARSI and MAVRSI: visible
p1 = plot(rsi, linewidth=2, transp=100, color=color.yellow, title="Price RSI")
p2 = plot(marsi, linewidth=2, color=color.blue, title="MARSI")
p3 = plot(rsi2, linewidth=2, transp=100, color=color.red, title="Volume RSI")
p4 = plot(marsi2, linewidth=2, color=color.green, title="MAVRSI")
```