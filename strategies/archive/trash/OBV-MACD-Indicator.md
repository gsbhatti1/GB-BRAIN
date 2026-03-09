``` pinescript
/*backtest
start: 2022-04-30 00:00:00
end: 2022-05-29 23:59:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4

study("OBV MACD Indicator", overlay=false)
// MACD
src1 = close
window_len = 28

v_len = 14
price_spread = stdev(high-low, window_len)

v = cum(sign(change(src1)) * volume)
smooth = sma(v, v_len)
v_spread = stdev(v - smooth, window_len)
shadow = (v - smooth) / v_spread * price_spread

out = shadow > 0 ? high + shadow : low + shadow

// plot(out, style=line, linewidth=3, color=color)
len10=input(1,title="OBV Length ")
obvema=ema(out,len10)

//
src = obvema

type = input(defval="DEMA", title="MA Type", options=["TDEMA", "TTEMA", "TEMA", "DEMA", "EMA", "AVG", "THMA", "ZLEMA", "ZLDEMA", "ZLTEMA", "DZLEMA", "TZLEMA", "LLEMA", "NMA"])
showma = true
len = input(9, title="MA Length ")
showma1 = false
len1 = 26
showma2 =false
len2 = 52

nma(src, length1, length2) =>
    lambda = length1 / length2
    alpha = lambda * (length1 - 1) / (length1 - lambda)
    ma1 = ema(src, length1)
    ma2 = ema(ma1, length2)
    nma = (1 + alpha) * ma1 - alpha * ma2
    
dema(src, len) => 
    ma1 = ema(src, len)
    ma2 = ema(ma1, len)
    2 * ma1 - ma2

tema(src, len) => 
    ma1 = ema(src, len)
    ma2 = ema(ma1, len)
    ma3 = ema(ma2, len)
    3 * (ma1 - ma2) + ma3

tdema(src, len) => 
    ma1 = dema(src, len)
    ma2 = dema(ma1, len)
    ma3 = dema(ma2, len)
    3 * (ma1 - ma2) + ma3

ttema(src, len) => 
    ma1 = tema(src, len)
    ma2 = tema(ma1, len)
    ma3 = tema(ma2, len)
    3 * (ma1 - ma2) + ma3

tnma(src, len) => 
    ma1 = nma(src, len, 3)
    ma2 = nma(ma1, len, 3)
    ma3 = nma(ma2, len, 3)
    3 * (ma1 - ma2) + ma3

hma(src, len) => wma(2*wma(src, len/2)-wma(src, len), round(sqrt(len)))

thma(src, len) => 
    ma1 = hma(src, len)
    ma2 = hma(ma1, len)
    ma3 = hma(ma2, len)
    3 * (ma1 - ma2) + ma3

zlema(src, len) =>
	lag = round((len - 1) / 2)
	zlsrc = src + (src - src[lag])
	ema(zlsrc, len)

zldema(src, len) =>
	lag = round((len - 1) / 2)
	zlsrc = src + (src - src[lag])
	dema(zlsrc, len)
	
zltema(src, len) =>
	lag = round((len - 1) / 2)
	zlsrc = src + (src - src[lag])
	tema(zlsrc, len)
	
dzlema(src, len) => 
    ma1 = zlema(src, len)
    ma2 = zlema(ma1, len)
    2 * ma1 - ma2

tzlema(src, len) => 
    ma1 = zlema(src, len)
    ma2 = zlema(ma1, len)
    ma3 = zlema(ma2, len)
    3 * (ma1 - ma2) + ma3

llema(src, len) =>
	srcnew = 0.25*src + 0.5*src[1] + 0.25*src[2]
	ema(srcnew, len)
	
lltema(src, len) =>
	srcnew = 0.25*src + 0.5*src[1] + 0.25*src[2]
	tema(srcnew, len)

myma(src, len) => 
    if type == "EMA"
        ema(src, len)
    else
        if type == "DEMA"
            dema(src, len)
        else 
            if type == "TEMA"
                tema(src, len)
            else 
                if type == "TDEMA"
                    tdema(src, len)
                else
                    if type == "TTEMA"
                        ttema(src, len)
                    else
                        if type == "THMA"
                            thma(src, len)
                        else
                            if type == "ZLEMA"
                                zlema(src, len)
                            else
                                if type == "ZLDEMA"
                                    zldema(src, len)
                                else
                                    if type == "ZLTEMA"
                                        zltema(src, len)
                                    else
                                        if type == "DZLEMA"
                                            dzlema(src, len)
                                        else
                                            if type == "TZLEMA"
                                                tzlema(src, len)
                                            else
                                                if type == "LLEMA"
                                                    llema(src, len)
                                                else
                                                    if type == "NMA"
                                                        nma(src, len, len1)
                                                    else
                                                        avg(ttema(src, len), tdema(src, len))
        
ma = showma ? myma(src, len) : na
slow_length = input(title="MACD Slow Length", type=input.integer, defval=26)
//signal_length = input(title="MACD Signal Smoothing", type=input.integer, minval = 1, maxval = 50, defval = 9)
src12=close
plot(0, linewidth=3, color=color.black)
// Calculating MACD
slow_ma = ema(src12, slow_length)
macd = ma - slow_ma

```