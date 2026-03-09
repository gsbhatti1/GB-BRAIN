``` pinescript
/* backtest
start: 2023-10-27 00:00:00
end: 2023-11-26 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
//
// study(title="Chande Kroll Stop", shorttitle="CK Stop", overlay=true)
strategy(title="Chande Kroll Stop", shorttitle="Chande Kroll Stop回測", overlay=true, initial_capital=100000, calc_on_every_tick=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)
br_red = #e91e63
Red = #f41818
n_green = #91dc16
dk_green = #004d40
lt_green = #16dc78
lt_blue = #0dbdd8
dk_blue = #0a3577
Blue = #034fed
br_orange = #f57c00
dk_orange = #e65100
dk_gray = #434651
dk_pink = #7c1df0
lt_pink = #e743f5
Purple = #5b32f3
lt_purple = #6b5797

hiP = input(9, "", inline="h")
hix = input(1, "", inline="h", step=0.1)
hiQ = input(7, "", inline="h")
loP = input(9, "", inline="h1")
lox = input(1, "", inline="h1", step=0.1)
loQ = input(5, "", inline="h1")
Xr = input(false, "反向操作:買/賣", inline="T"),
first_high_stop = highest(high, hiP) - hix * atr(hiP)
first_low_stop = lowest(low, loP) + lox * atr(loP)

stop_short = highest(first_high_stop, hiQ)
stop_long = lowest(first_low_stop, loQ)

cklow = stop_short
ckhigh = stop_long

Xdn = cklow < cklow[1] and ckhigh < ckhigh[1]
Xup = cklow > cklow[1] and ckhigh > ckhigh[1]
longcol = Xup ? lt_green : Xdn ? br_red : #2a2e39
shortcol = Xup ? lt_green : Xdn ? br_red : #2a2e39
plot(stop_long, color=longcol)
plot(stop_short, color=shortcol)

plotshape(Xup and not Xup[1], title="CK Stop Buy", text='CK', style=shape.triangleup, size=size.tiny, location=location.belowbar, color=lt_green, textcolor=lt_green, display=display.none)
plotshape(Xdn and not Xdn[1], title="CK Stop Sell", text='CK', style=shape.triangledown, size=size.tiny, location=location.abovebar, color=br_red, textcolor=br_red, display=display.none)

tl = input(true, "Sig", inline="T"), sbg = input(true, "Bgtrend", inline="T"), vbuild = "FIREHORSE XRPUSDT"
Xp = 0.0
Xp := Xdn ? -1 : Xup ? 1 : Xp[1]
Xdf = Xr ? Xup and Xp[1] == -1 : Xdn and Xp[1] == 1
Xuf = Xr ? Xdn and Xp[1] == 1 : Xup and Xp[1] == -1
FY = input(2021, "年", inline="btf")
FM = input(9, "月", inline="bfm")
FD = input(true, "日", inline="bfm")
plotshape(Xdf or Xuf ? (Xup and not Xup[1]) : na, title="CK Stop Buy & Sell", text='CK', style=shape.triangleup, size=size.tiny, location=location.belowbar, color=color.new(lt_green, 0), textcolor=color.new(lt_green, 0), display=display.none)
plotshape(Xdf or Xuf ? (Xdn and not Xdn[1]) : na, title="CK Stop Buy & Sell", text='CK', style=shape.triangledown, size=size.tiny, location=location.abovebar, color=color.new(br_red, 0), textcolor=color.new(br_red, 0), display=display.none)
```