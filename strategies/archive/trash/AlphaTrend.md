Name

AlphaTrend

Author

ChaoZhang

Strategy Description

AlphaTrend is a brand new indicator that I have personally derived from Trend Magic and am still developing. In Magic Trend, we encountered some issues, which Alpha Trend aims to address such as:

1. To minimize stop losses and overcome sideways market conditions.
2. To have more accurate BUY/SELL signals during trending market conditions.
3. To have significant support and resistance levels.
4. To bring together indicators from different categories that are compatible with each other and make a meaningful combination regarding momentum, trend, volatility, volume, and trailing stop loss.

According to these purposes, Alpha Trend:
1. Acts like a dead indicator like its ancestor Magic Trend in sideways market conditions and does not give many false signals.
2. With another line offset by 2 bars from the original one, Alpha Trend has BUY and SELL signals from their crossovers.

BUY / LONG when Alpha Trend line crosses above its 2 bars offsetted line and there is a green filling between them
SELL / SHORT when Alpha Trend line crosses below its 2 bars offsetted line and the filling would be red then.

3. Alpha Trend lines:
- act as support levels when an uptrend occurs, trailing 1*ATR (default coefficient) distance from bar's low values
- conversely act as resistance levels when a downtrend occurs, trailing 1*ATR (default coefficient) distance from bar's high values
and acting as trailing stop losses. The more Alpha Trend lines are straighter, the stronger the supports and resistances become.

4. Unlike Trend Magic which uses CCI in its calculation, Alpha Trend uses MFI as momentum, but when there is no volume data, MFI has 0 values. So, there is a button to change the calculation considering RSI after checking the relevant box to overcome this problem when there is no volume data on that chart.
Momentum: RSI and MFI
Trend: Magic Trend
Volatility: ATR,
Trailing STOP: ATR TRAILING STOP
Volume: MFI
Alpha trend is really a combination of different types...

Default values:
coefficient: 1 which is the factor of trailing ATR value
common period: 14 which is the length of ATR, MFI, and RSI

Wish you all use AlphaTrend in profitable trades.
Kıvanç Özbilgiç

**Backtest results**
![IMG](https://www.fmz.com/upload/asset/5b0e559be7c9374225.png)

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_float_1|true|Multiplier|
|v_input_1|8|Common Period|
|v_input_source_2|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_3|true|Show Signals?|
|v_input_4|false|Change calculation (no volume data)?|


> Source (PineScript)

```pinescript
/*backtest
start: 2017-08-01 00:00:00
end: 2022-05-04 23:59:00
Period: 1d
basePeriod: 1d
exchanges: [{"eid":"Bitfinex","currency":"BTC_USD"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// author © KivancOzbilgic
// developer © KivancOzbilgic
//@version=5
indicator('AlphaTrend', shorttitle='AT', overlay=true, format=format.price, precision=2, timeframe='')
coeff = input.float(1, 'Multiplier', step=0.1)
AP = input(8, 'Common Period')
ATR = ta.sma(ta.tr, AP)
src = input(close,'Source')
showsignalsk = input(title='Show Signals?', defval=true)
novolumedata = input(title='Change calculation (no volume data)?', defval=false)
upT = low - ATR * coeff
downT = high + ATR * coeff
AlphaTrend = 0.0
AlphaTrend := (novolumedata ? ta.rsi(src, AP) >= 50 : ta.mfi(hlc3, AP) >= 50) ? upT < nz(AlphaTrend[1]) ? nz(AlphaTrend[1]) : upT : downT > nz(AlphaTrend[1]) ? nz(AlphaTrend[1]) : downT

color1 = AlphaTrend > AlphaTrend[2] ? #00E60F : AlphaTrend < AlphaTrend[2] ? #80000B : AlphaTrend[1] > AlphaTrend[3] ? #00E60F : #80000B
k1 = plot(AlphaTrend, color=color.new(#0022FC, 0), linewidth=3)
k2 = plot(AlphaTrend[2], color=color.new(#FC0400, 0), linewidth=3)

buySignalk = ta.crossover(AlphaTrend, AlphaTrend[2])
sellSignalk = ta.crossunder(AlphaTrend, AlphaTrend[2])


K1 = ta.barssince(buySignalk)
K2 = ta.barssince(sellSignalk)
O1 = ta.barssince(buySignalk[1])
O2 = ta.barssince(sellSignalk[1])


//plotshape(buySignalk and showsignalsk and O1 > K2 ? AlphaTrend[2] * 0.9999 : na, title='BUY', text='BUY', location=location.absolute, style=shape.labelup, size=size.tiny, color=color.new(#0022FC, 0), textcolor=color.new(color.white, 0))

//plotshape(sellSignalk and showsignalsk and O2 > K1 ? AlphaTrend[2] * 1.0001 : na, title='SELL', text='SELL', location=location.absolute, style=shape.labeldown, size=size.tiny, color=color.new(color.maroon, 0), textcolor=color.new(color.white, 0))

if buySignalk and showsignalsk and O1 > K2
    strategy.entry("entry long", strategy.long)
else if sellSignalk and showsignalsk and O2 > K1
    strategy.entry("entry short")
```

> Detail

https://www.fmz.com/strategy/361480

> Last Modified

2022-05-06 15:49:16