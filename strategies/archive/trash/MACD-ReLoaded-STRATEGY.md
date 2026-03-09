> Name

MACD-ReLoaded-STRATEGY

> Author

ChaoZhang

> Strategy Description

A different approach to Gerald Appel's classical Moving Average Convergence Divergence.

Appel originally set MACD with exponential moving averages.
In this version, users can apply 11 different types of moving averages which they can benefit from their smoothness and vice versa sharpnesses...

Built-in moving average type is defaultly set as VAR but users can choose from 11 different moving average types like:

SMA : Simple Moving Average
EMA : Exponential Moving Average
WMA : Weighted Moving Average
DEMA : Double Exponential Moving Average
TMA : Triangular Moving Average
VAR : Variable Index Dynamic Moving Average a.k.a. VIDYA
WWMA : Welles Wilder's Moving Average
ZLEMA : Zero Lag Exponential Moving Average
TSF : True Strength Force
HULL : Hull Moving Average
TILL : Tillson T3 Moving Average

In shorter time frames backtest results show that TILL, WWMA, and VIDYA (VAR) can be used to overcome whipsaws because they have fewer signals.
In longer time frames like daily charts, WMA, Volume Weighted MACD V2, and SMA are more accurate according to backtest results.

**Backtest**
![IMG](https://www.fmz.com/upload/asset/1358cd85827a8416981.png)

> Strategy Arguments

|Argument|Default|Description|
|---|---|---|
|v_input_1_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|12|Short Moving Average Length|
|v_input_3|26|Long Moving Average Length|
|v_input_4|9|Trigger Length|
|v_input_5|0.7|TILLSON T3c1*T3e6+T3c2*T3e5+T3c3*T3e4+T3c4*T3e3 Volume Factor|
|v_input_6|true|Bar Coloring On/Off ?|
|v_input_7|0|Moving Average Type: 0.0|EMA|WMA|DEMA|TMA|VAR|WWMA|ZLEMA|TSF|HULL|TILL|
|v_input_8|9|From Month|
|v_input_9|true|From Day|
|v_input_10|2018|From Year|
|v_input_11|true|To Month|
|v_input_12|true|To Day|
|v_input_13|9999|To Year|

> Source (PineScript)

``` pinescript
/* backtest
start: 2022-04-23 00:00:00
end: 2022-05-22 23:59:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © KivancOzbilgic

// developer: Gerald Appel
// author: @kivancozbilgic

strategy("MACD ReLoaded", "MACDRe", overlay=true)
src = input(close, title="Source")
length=input(12, "Short Moving Average Length", minval=1)
length1=input(26, "Long Moving Average Length", minval=1)
length2=input(9, "Trigger Length", minval=1)
T3a1 = input(0.7, "TILLSON T3 Volume Factor", step=0.1)
barcoloring = input(title="Bar Coloring On/Off ?", type=input.bool, defval=true)

mav = input(title="Moving Average Type", defval="VAR", options=["SMA", "EMA", "WMA", "DEMA", "TMA", "VAR", "WWMA", "ZLEMA", "TSF", "HULL", "TILL"])
Var_Func(src, length)=>
    valpha=2/(length+1)
    vud1=src>src[1] ? src-src[1] : 0
    vdd1=src<src[1] ? src[1]-src : 0
    vUD=sum(vud1,9)
    vDD=sum(vdd1,9)
    vCMO=nz((vUD-vDD)/(vUD+vDD))
    VAR=0.0
    VAR:=nz(valpha*abs(vCMO)*src)+(1-valpha*abs(vCMO))*nz(VAR[1])
VAR=Var_Func(src, length)
DEMA = (2 * ema(src, length)) - (ema(ema(src, length), length) )
Wwma_Func(src, length)=>
    wwalpha = 1/ length
    WWMA = 0.0
    WWMA := wwalpha*src + (1-wwalpha)*nz(WWMA[1])
WWMA=Wwma_Func(src, length)
Zlema_Func(src, length)=>
    zxLag = length/2==round(length/2) ? length/2 : (length - 1) / 2
    zxEMAData = (src + (src - src[zxLag]))
    ZLEMA = ema(zxEMAData, length)
ZLEMA=Zlema_Func(src, length)
Tsf_Func(src, length)=>
    lrc = linreg(src, length, 0)
    lrc1 = linreg(src, length, 1)
    lrs = (lrc-lrc1)
    TSF = linreg(src, length, 0)+lrs
TSF=Tsf_Func(src, length)
HMA = wma(2 * wma(src, length / 2) - wma(src, length), round(sqrt(length)))
T3e1=ema(src, length)
T3e2=ema(T3e1, length)
T3e3=ema(T3e2, length)
T3e4=ema(T3e3, length)
T3e5=ema(T3e4, length)
T3e6=ema(T3e5, length)
T3c1=-T3a1*T3a1*T3a1
T3c2=3*T3a1*T3a1+3*T3a1*T3a1*T3a1
T3c3=-6*T3a1*T3a1-3*T3a1-3*T3a1*T3a1*T3a1
T3c4=1+3*T3a1+T3a1*T3a1*T3a1+3*T3a1*T3a1
T3=T3c1*T3e6+T3c2*T3e5+T3c3*T3e4+T3c4*T3e3

getMA(src, length) =>
    ma = 0.0
    if mav == "SMA"
        ma := sma(src, length)
        ma

    if mav == "EMA"
        ma := ema(src, length)
        ma

    if mav == "WMA"
        ma := wma(src, length)
        ma

    if mav == "DEMA"
        ma := dema(src, length)
        ma

    if mav == "TMA"
        ma := tma(src, length)
        ma

    if mav == "VAR"
        ma := var(src, length)
        ma

    if mav == "WWMA"
        ma := wwilliamsR(src, length)
        ma

    if mav == "ZLEMA"
        ma := zlema(src, length)
        ma

    if mav == "TSF"
        ma := tsf(src, length)
        ma

    if mav == "HULL"
        ma := hull(src, length)
        ma

    if mav == "TILL"
        ma := tillsonT3(src, length)
        ma

VAR = getMA(src, length2)

plot(VAR, color=barcoloring ? color.red : color.blue)
```

This completes the translation of your strategy description and source code into English. The provided Pine Script defines a customizable MACD-like strategy that supports 11 different moving average types, with specific parameters for backtesting and visualization. Adjustments or further optimizations might be necessary depending on your specific requirements.