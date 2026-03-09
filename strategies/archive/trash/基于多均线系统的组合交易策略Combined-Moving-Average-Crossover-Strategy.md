``` pinescript
/*backtest
start: 2022-09-13 00:00:00
end: 2023-09-19 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
//creator&compiler: Bartu Altan
//inspired by: KIVANÇ ÖZBİLGİÇ @fr3792 and @mavilim0732 on twitter
//With courtesy of Kıvanç Özbilgiç, Permission Pending

strategy("Tilson T3, Tilson T3 Fibo and MavilimW Combined Strategy Strategy",shorttitle="T3 and MavilimW Strategy", initial_capital=100,currency=currency.USD,default_qty_type=strategy.percent_of_equity,default_qty_value =75,overlay=true)
stop_loss=input(defval=3.0,title="Stop Loss %",type=input.float)*0.01
strategyt3 = input(true,"T3")
strategyt3Fibo = input(true,"T3 Fibo Cross")
strategyMav = input(true,"MavilimW")
fmal=input(3,"First Moving Average length")
smal=input(5,"Second Moving Average length")
barsSinceCloseUnderMavw = input(5,"Bars Since Close Under MAVW")
T3FiboLine = input(false, title="Show T3 Fibonacci Ratio Line?")
length1 = input(8, "T3 Length")
a1 = input(0.7, "Volume Factor")

// BEGINNING OF T3

e1 = ema((high + low + 2 * close) / 4, length1)
e2 = ema(e1, length1)
e3 = ema(e2, length1)
e4 = ema(e3, length1)
e5 = ema(e4, length1)
e6 = ema(e5, length1)
c1 = -a1 * a1 * a1
c2 = 3 * a1 * a1 + 3 * a1 * a1 * a1
c3 = -6 * a1 * a1 - 3 * a1 - 3 * a1 * a1 * a1
c4 = 1 + 3 * a1 + a1 * a1 * a1 + 3 * a1 * a1
T3 = c1 * e6 + c2 * e5 + c3 * e4 + c4 * e3

col1t3 = T3 > T3[1]
col3t3 = T3 < T3[1]
color_1 = col1t3 ? color.green : col3t3 ? color.red : color.yellow
plot(strategyt3 or strategyt3Fibo ? T3:na, color=color_1, linewidth=3, title="T3")

//T3 Fibo

length12 = input(5, "T3 Length fibo")
a12 = input(0.618, "Volume Factor fibo")

e12 = ema((high + low + 2 * close) / 4, length12)
e22 = ema(e12, length12)
e32 = ema(e22, length12)
e42 = ema(e32, length12)
e52 = ema(e42, length12)
e62 = ema(e52, length12)
c12 = -a12 * a12 * a12
c22 = 3 * a12 * a12 + 3 * a12 * a12 * a12
c32 = -6 * a12 * a12 - 3 * a12 - 3 * a12 * a12 * a12
c42 = 1 + 3 * a12 + a12 * a12 * a12 + 3 * a12 * a12
T32 = c12 * e62 + c22 * e52 + c32 * e42 + c42 * e32

col12 = T32 > T32[1]
col32 = T32 < T32[1]
color2 = col12 ? color.blue : col32 ? color.purple : color.yellow
plot(strategyt3Fibo and T3FiboLine and T32 ? T32 : na, color=color2, linewidth=2, title="T3fibo")

//End of T3 Fibo

// END OF T3


// MAVİLİMW //

tmal=fmal+smal
Fmal=smal+tmal
Ftmal=tmal+Fmal
Smal=Fmal+Ftmal

M1= wma(close, fmal)
M2= wma(M1, smal)
M3= wma(M2, tmal)
M4= wma(M3, Fmal)
M5= wma(M4, Ftmal)
MAVW= wma(M5, Smal)
col1= MAVW>MAVW[1]
col3= MAVW<MAVW[1]
colorM = col1 ? color.blue : col3 ? color.red : color.yellow
plot(strategyMav ?MAVW:na,title="MAVW",color=colorM,linewidth=2)

// END OF MAVILIMW

// Long Conditions // 

longT3single = strategyt3 and not(strategyt3Fibo) and not(strategyMav) ? cross上行交叉
```