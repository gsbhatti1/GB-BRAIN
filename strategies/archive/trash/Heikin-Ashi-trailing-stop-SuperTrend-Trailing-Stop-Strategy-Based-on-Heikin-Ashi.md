``` pinescript
/*backtest
start: 2024-01-06 00:00:00
end: 2024-02-05 00:00:00
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © ringashish

//@version=4
strategy("sa-strategy with HTF-TSL", overlay=true)


Pd = input(title="ATR Period", type=input.integer, defval=4)
Factor = input(title="ATR Multiplier", type=input.float, step=0.1, defval=2)
ST= supertrend(Factor, Pd)

heikinashi_close = security(heikinashi(syminfo.tickerid), timeframe.period, close)
heikinashi_low = security(heikinashi(syminfo.tickerid), timeframe.period, low)
heikinashi_open = security(heikinashi(syminfo.tickerid), timeframe.period, open)
heikinashi_high = security(heikinashi(syminfo.tickerid), timeframe.period, high)

heikinashi_close30 = security(heikinashi(syminfo.tickerid), "30", close)
//res1 = input("30", type=input.resolution, title="higher Timeframe")


//CCI TSL

res = input("240",type=input.resolution,title = "Higher Time Frame")
CCI = input(20)
ATR = input(5)
Multiplier=input(1,title='ATR Multiplier')
original=input(false,title='original coloring')
thisCCI = cci(close, CCI)
lastCCI = nz(thisCCI[1])


calcx()=> 
    bufferDn= high + Multiplier * sma(tr,ATR)
    bufferUp= low - Multiplier * sma(tr,ATR)
    if (thisCCI >= 0 and lastCCI < 0) 
        bufferUp := bufferDn[1]
    if (thisCCI <= 0 and lastCCI > 0) 
        bufferDn := bufferUp[1]

    if (thisCCI >= 0)
        if (bufferUp < bufferUp[1])
            bufferUp := bufferUp[1]
    else
        if (thisCCI <= 0)
            if (bufferDn > bufferDn[1])
                bufferDn := bufferDn[1]

   
    x = 0.0
    x := thisCCI >= 0 ?bufferUp:thisCCI <= 0 ?bufferDn:x[1]
    x

tempx = calcx()

calcswap() =>
    swap = 0.0
    swap := tempx>tempx[1]?1:tempx<tempx[1]?-1:swap[1]
    swap

tempswap = calcswap()

swap2=tempswap==1?color.blue:color.orange
swap3=thisCCI >=0 ?color.blue:color.orange
swap4=original?swap3:swap2

//display current timeframe's Trend

plot(tempx,"CTF",color=swap4,transp=0,linewidth=2, style = plot.style_stepline)
```