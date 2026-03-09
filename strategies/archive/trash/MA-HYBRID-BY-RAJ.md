```pinescript
/*backtest
start: 2022-05-02 00:00:00
end: 2022-05-08 23:59:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
//By theraj333
// This script is designed for the NNFX Method, so it is recommended for Daily charts only. 
// Tried to implement a few VP NNFX Rules
// This script has a SSL / Baseline (you can choose between the SSL or MA), a secondary SSL for continuation trades and a third SSL for exit trades.
// Alerts added for baseline entries, SSL2 continuations, exits.
// Baseline has a Keltner Channel setting for "in zone" gray candles
// Added "Candle Size > 1 ATR" diamonds from my old script with the criteria of being within baseline ATR range.
// Credits
// Strategy causecelebre https://www.tradingview.com/u/causecelebre/
// SSL Channel ErwinBeckers https://www.tradingview.com/u/ErwinBeckers/
// Moving Averages jiehonglim https://www.tradingview.com/u/jiehonglim/
// Moving Averages everget https://www.tradingview.com/u/everget/
// "Many Moving Averages" script Fractured https://www.tradingview.com/u/Fractured/

study("MA HYBRID", overlay=true)

show_Baseline = input(title="Show Baseline", type=input.bool, defval=true)
show_SSL1 = input(title="Show SSL1", type=input.bool, defval=false)
show_atr = input(title="Show ATR bands", type=input.bool, defval=true)

//ATR
atrlen = input(14, "ATR Period")
mult = input(1, "ATR Multi", step=0.1)
smoothing = input(title="ATR Smoothing", defval="WMA", options=["RMA", "SMA", "EMA", "WMA"])

ma_function(source, atrlen) =>
    if smoothing == "RMA"
        rma(source, atrlen)
    else
        if smoothing == "SMA"
            sma(source, atrlen)
        else
            if smoothing == "EMA"
                ema(source, atrlen)
            else
                wma(source, atrlen)

atr_slen = ma_function(tr(true), atrlen)

////ATR Up/Low Bands
upper_band = atr_slen * mult + close
lower_band = close - atr_slen * mult

////BASELINE / SSL1 / SSL2 / EXIT MOVING AVERAGE VALUES
maType = input(title="SSL1 / Baseline Type", type=input.string, defval="HMA", options=["SMA","EMA","DEMA","TEMA","LSMA","WMA","MF","VAMA","TMA","HMA", "JMA", "Kijun v2", "EDSMA","McGinley"])
len = input(title="SSL1 / Baseline Length", defval=60)

SSL2Type = input(title="SSL2 / Continuation Type", type=input.string, defval="JMA", options=["SMA","EMA","DEMA","TEMA","WMA","MF","VAMA","TMA","HMA", "JMA","McGinley"])
len2 = input(title="SSL 2 Length", defval=5)
//
SSL3Type = input(title="EXIT Type", type=input.string, defval="HMA", options=["DEMA","TEMA","LSMA","VAMA","TMA","HMA","JMA", "Kijun v2", "McGinley", "MF"])
len3 = input(title="EXIT Length", defval=15)
src = input(title="Source", type=input.source, defval=close)

//
tema(src, len) =>
    ema1 = ema(src, len)
    ema2 = ema(ema1, len)
    ema3 = ema(ema2, len)
    (3 * ema1) - (3 * ema2) + ema3
kidiv = input(defval=1,maxval=4,  title="Kijun MOD Divider")

jurik_phase = input(title="* Jurik (JMA) Only - Phase", type=input.integer, defval=3)
jurik_power = input(title="* Jurik (JMA) Only - Power", type=input.integer, defval=1)
volatility_lookback = input(10, title="* Volatility Adjusted (VAMA) Only - Volatility lookback length")
//MF
beta = input(0.8,minval=0,maxval=1,step=0.1,  title="Modular Filter, General Filter Only - Beta")
feedback = input(false, title="Modular Filter Only - Feedback")
z = input(0.5,title="Modular Filter Only - Feedback Weighting",step=0.1, minval=0, maxval=1)
//EDSMA
ssfLength = input(title="EDSMA - Super Smoother Filter Length", type=input.integer, minval=1, defval=20)
ssfPoles = input(title="EDSMA - Super Smoother Filter Poles", type=input.integer, defval=2, options=[2, 3])

//----

//EDSMA
get2PoleSSF(src, length) =>
    PI = 2 * asin(1)
    arg = sqrt(2) * PI / length
    a1 = exp(-arg)
    b1 = 2 * a1 * cos(arg)
    c2 = b1
    c3 = -pow(a1, 2)
    c1 = 1 - c2 - c3
    
    ssf = 0.0
    ssf := c1 * src + c2 * nz(ssf[1]) + c3 * nz(ssf[2]))

get3PoleSSF(src, length) =>
    PI = 2 * asin(1)

    arg = PI / length
    a1 = exp(-arg)
    b1 = 2 * a1 * cos(1.738 * arg)
    c1 = pow(a1, 2)

    coef2 = b1 + c1
    coef3 = -(c1 + b1 * c1)
    coef4 = pow(c1, 2)
    coef1 = 1 - coef2 - coef3 - coef4

    ssf = 0.0
    ssf := coef1 * src +
```