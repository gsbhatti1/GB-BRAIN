```pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-18 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
//Created by Nasser mahmoodsani' all rights reserved
// E-mail : e.man4858@gmail.com

strategy("UT Bot Strategy with T/P and S/L and Trend EMA", overlay=true)

// Inputs
along = input(1, title='Key Value (Sensitivity - Long)', group="LONG")
clong = input(10, title='ATR Period (Long)', group="LONG")
h = input(true, title='Signals from Heikin Ashi Candles')
ashort = input(7, title='Key Value (Sensitivity - Short)', group="SHORT")
cshort = input(2, title='ATR Period (Short)', group="SHORT")
tradeType = input.string("Both", title="Trade Type", options=["Buy Only", "Sell Only", "Both"])
tp1_percent = input.float(0.5, title="TP1 Percentage", step=0.1, group="TP Settings") // TP1 % input
tp2_percent = input.float(1.0, title="TP2 Percentage", step=0.1, group="TP Settings") // TP2 % input
sl_percent = input.float(1.0, title="Stop Loss Percentage", step=0.1, group="TP Settings") // SL % input
sl_in_percent = input(true, title="Use Stop Loss in Percentage", group="TP Settings")
tp1_qty = input.float(0.5, title="Take Profit 1 Quantity (as % of position size)", minval=0.0, maxval=1.0, step=0.1)
tp2_qty = input.float(0.5, title="Take Profit 2 Quantity (as % of position size)", minval=0.0, maxval=1.0, step=0.1)

// Check that total quantities for TPs do not exceed 100%
if tp1_qty + tp2_qty > 1
    runtime.error("The sum of Take Profit quantities must not exceed 100%.")

// Calculate 50 EMA from 5-Minute Timeframe
trendEmaPeriod = 50
trendEma_5min = request.security(syminfo.tickerid, "5", ta.ema(close, trendEmaPeriod))
plot(trendEma_5min, title="Trend EMA (5-Min)", color=color.blue, linewidth=2)

// Calculations 
xATRlong = ta.atr(clong)
xATRshort = ta.atr(cshort)
nLosslong = along * xATRlong
nLossshort = ashort * xATRshort

src = h ? request.security(ticker.heikinashi(syminfo.tickerid), timeframe.period, close) : close

// LONG
var float xATRTrailingStoplong = na
var float stopLossLong = na
var float takeProfit1 = na
var float takeProfit2 = na

iff_1long = src > nz(xATRTrailingStoplong[1], 0) ? src - nLosslong : src + nLosslong
iff_2long = src < nz(xATRTrailingStoplong[1], 0) and src[1] < nz(xATRTrailingStoplong[1], 0) ? math.min(nz(xATRTrailingStoplong[1]), src + nLosslong) : iff_1long
xATRTrailingStoplong := src > nz(xATRTrailingStoplong[1], 0) and src[1] > nz(xATRTrailingStoplong[1], 0) ? src - nLosslong : iff_2long

// SHORT
var float xATRTrailingStopshort = na
var float stopLossShort = na
var float takeProfit3 = na
var float takeProfit4 = na

iff_1short = src < nz(xATRTrailingStopshort[1], 0) ? src + nLossshort : src - nLossshort
iff_2short = src > nz(xATRTrailingStopshort[1], 0) and src[1] > nz(xATRTrailingStopshort[1], 0) ? math.max(nz(xATRTrailingStopshort[1]), src - nLossshort) : iff_1short
xATRTrailingStopshort := src < nz(xATRTrailingStopshort[1], 0) and src[1] < nz(xATRTrailingStopshort[1], 0) ? src + nLossshort : iff_2short

// Entry Conditions
if (h and ta.crossover(src, trendEma_5min))
    if (tradeType == "Buy Only" or tradeType == "Both")
        strategy.entry("Long", strategy.long, when=iff_1long > src)
        strategy.exit("Take Profit 1 Long", from_entry="Long", limit=iff_1long)
        strategy.exit("Take Profit 2 Long", from_entry="Long", limit=iff_2long)
        strategy.exit("Stop Loss Long", from_entry="Long", stop=iff_2long)

if (h and ta.crossunder(src, trendEma_5min))
    if (tradeType == "Sell Only" or tradeType == "Both")
        strategy.entry("Short", strategy.short, when=iff_1short < src)
        strategy.exit("Take Profit 1 Short", from_entry="Short", limit=iff_1short)
        strategy.exit("Take Profit 2 Short", from_entry="Short", limit=iff_2short)
        strategy.exit("Stop Loss Short", from_entry="Short", stop=iff_2short)
```

This script now includes the short trading conditions and the corresponding take profit and stop loss exits, ensuring that both long and short trades are covered according to the specified trade type.