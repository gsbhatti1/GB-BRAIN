> Name

SSL-Hybrid

> Author

ChaoZhang

> Strategy Description

This script is designed for the NNFX Method, so it is recommended for Daily charts only.
Tried to implement a few VP NNFX Rules.
This script has a SSL / Baseline (you can choose between the SSL or MA), a secondary SSL for continuation trades and a third SSL for exit trades.
Alerts added for Baseline entries, SSL2 continuations, Exits.
Baseline has a Keltner Channel setting for "in zone" Gray Candles.
Added "Candle Size > 1 ATR" Diamonds from my old script with the criteria of being within Baseline ATR range.

**Backtest**

![IMG](https://www.fmz.com/upload/asset/16f9872d59d9fafbaaf.png)

> Strategy Arguments


|Argument|Default|Description|
|---|---|---|
|v_input_1|true|Show Baseline|
|v_input_2|false|Show SSL1|
|v_input_3|true|Show ATR bands|
|v_input_4|14|ATR Period|
|v_input_5|true|ATR Multi|
|v_input_6|0|ATR Smoothing: SMA|RMA|EMA|WMA|
|v_input_7|0|SSL1 / Baseline Type: HMA|EMA|DEMA|TEMA|LSMA|WMA|MF|VAMA|TMA|SMA|JMA|EDSMA|McGinley|
|v_input_8|60|SSL1 / Baseline Length|
|v_input_9|0|SSL2 / Continuation Type: JMA|EMA|DEMA|TEMA|WMA|MF|VAMA|TMA|HMA|SMA|McGinley|
|v_input_10|5|SSL 2 Length|
|v_input_11|0|EXIT Type: HMA|TEMA|LSMA|VAMA|TMA|DEMA|JMA|EDSMA|Kijun v2|McGinley|MF|
|v_input_12|15|EXIT Length|
|v_input_13_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_14|true|Kijun MOD Divider|
|v_input_15|3|* Jurik (JMA) Only - Phase|
|v_input_16|true|* Jurik (JMA) Only - Power|
|v_input_17|10|* Volatility Adjusted (VAMA) Only - Volatility lookback length|
|v_input_18|0.8|Modular Filter, General Filter Only - Beta|
|v_input_19|false|Modular Filter Only - Feedback|
|v_input_20|0.5|Modular Filter Only - Feedback Weighting|
|v_input_21|20|EDSMA - Super Smoother Filter Length|
|v_input_22|0|EDSMA - Super Smoother Filter Poles: 2|3|
|v_input_23|true|useTrueRange|
|v_input_24|0.2|Base Channel Multiplier|
|v_input_25|true|Color Bars|
|v_input_26|0.9|Continuation ATR Criteria|


> Source (PineScript)

```pinescript
/*backtest
start: 2022-04-16 00:00:00
end: 2022-05-15 23:59:00
period: 45m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
//By Mihkel00
// This script is designed for the NNFX Method, so it is recommended for Daily charts only. 
// Tried to implement a few VP NNFX Rules.
// This script has a SSL / Baseline (you can choose between the SSL or MA), a secondary SSL for continuation trades and a third SSL for exit trades.
// Alerts added for Baseline entries, SSL2 continuations, Exits.
// Baseline has a Keltner Channel setting for "in zone" Gray Candles.
// Added "Candle Size > 1 ATR" Diamonds from my old script with the criteria of being within Baseline ATR range.
// Credits
// Strategy causecelebre https://www.tradingview.com/u/causecelebre/
// SSL Channel ErwinBeckers https://www.tradingview.com/u/ErwinBeckers/
// Moving Averages jiehonglim https://www.tradingview.com/u/jiehonglim/
// Moving Averages  everget https://www.tradingview.com/u/everget/
// "Many Moving Averages" script  Fractured https://www.tradingview.com/u/Fractured/

study("SSL Hybrid", overlay=true)
show_Baseline = input(title="Show Baseline", type=input.bool, defval=true)
show_SSL1 = input(title="Show SSL1", type=input.bool, defval=false)
show_atr = input(title="Show ATR bands", type=input.bool, defval=true)

//ATR
atrlen = input(14, "ATR Period")
mult = input(1, "ATR Multi", step=0.1)
smoothing = input(title="ATR Smoothing", defval="SMA", options=["RMA", "SMA", "EMA", "WMA"])

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

//ATR Up/Low Bands
upper_band = atr_slen * mult + close
lower_band = close - atr_slen * mult

//BASELINE / SSL1 / SSL2 / EXIT MOVING AVERAGE VALUES
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
ssfPoles = input(title="EDSMA - Super Smoother Filter Poles", type=input.integer, options=[2,3], defval=2)

get3PoleSSF(src, length)