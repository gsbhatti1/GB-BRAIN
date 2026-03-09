> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|D|Hlc3 Time Frame|
|v_input_2|true|Hlc3 Shift|
|v_input_3|20|Slow EMA Period|
|v_input_4|5|Length|
|v_input_5_hlc3|0|xPrice: hlc3|high|low|open|hl2|close|hlcc4|ohlc4|
|v_input_6|2.5|Fastend|
|v_input_7|20|Slowend|


> Source (PineScript)

```pinescript
/*backtest
start: 2022-12-12 00:00:00
end: 2023-12-18 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
//Heikin/Kaufman   by Marco

strategy("HLC3/Kaufman Strategy ", shorttitle="HLC3/KAU", overlay=true)
res1 = input(title="Hlc3 Time Frame", defval="D")
test = input(1, "Hlc3 Shift")
sloma = input(20, "Slow EMA Period")

//Kaufman MA
Length = input(5, minval=1)
xPrice = input(hlc3)
xvnoise = abs(xPrice - xPrice[1])
Fastend = input(2.5, step=.5)
Slowend = input(20)
nfastend = 2/(Fastend + 1)
nslowend = 2/(Slowend + 1)
nsignal = abs(xPrice - xPrice[Length])
nnoise = sum(xvnoise, Length)
nefratio = iff(nnoise != 0, nsignal / nnoise, 0)
nsmooth = pow(nefratio * (nfastend - nslowend) + nslowend, 2) 
nAMA = nz(nAMA[1]) + nsmooth * (xPrice - nz(nAMA[1]))

//Heikin Ashi Open/Close Price
//ha_t = heikinashi(tickerid)
//ha_close = request.security(ha_t, period, nAMA)
//mha_close = request.security(ha_t, res1, hlc3)
bha_close = request.security(syminfo.ticker, timeframe.period, nAMA)
bmha_close = request.security(syminfo.ticker, res1, hlc3)

//Moving Average
//fma = ema(mha_close[test], 1)
//sma = ema(ha_close, sloma)
fma = ema(bmha_close, 1)
sma = ema(bha_close, sloma)
```