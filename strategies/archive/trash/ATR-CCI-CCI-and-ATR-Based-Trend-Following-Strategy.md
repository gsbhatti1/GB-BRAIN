``` pinescript
/*backtest
start: 2023-08-26 00:00:00
end: 2023-09-25 00:00:00
period: 3h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Trend Trader Karan", overlay=true)
res = input(title="Resolution", type=input.resolution, defval="60", confirm=true)

ProfitPerc = input(title="Take Profit (%)", type=input.float, minval=0.0, step=0.1, defval=1.4) * 0.01

stoploss = input(title="Stop Loss (%)", type=input.float, minval=0.0, step=0.1, defval=0.7) * 0.01

CCI = input(10, title="CCI")
ATR = input(2, title="ATR")
Multiplier = 1
original = false
thisCCI = cci(close, CCI)
lastCCI = nz(thisCCI[1])

calcx() =>
    bufferDn = high + Multiplier * wma(tr, ATR)
    bufferUp = low - Multiplier * wma(tr, ATR)
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
    x := thisCCI >= 0 ? bufferUp : thisCCI <= 0 ? bufferDn : x[1]
    x

tempx = calcx()
```