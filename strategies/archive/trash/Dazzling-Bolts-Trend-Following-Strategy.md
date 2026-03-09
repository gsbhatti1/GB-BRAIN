``` pinescript
/*backtest
start: 2024-01-02 00:00:00
end: 2024-02-01 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © greenmask9

//@version=4
strategy("Dazzling Bolts", overlay=true)
//max_bars_back=3000

// 13 SMMA
len = input(10, minval=1, title="SMMA Period")
src = input(close, title="Source")
smma = 0.0
smma := na(smma[1]) ? sma(src, len) : (smma[1] * (len - 1) + src) / len

// 55 EMA
emalength = input(55, title="EMA Period")
ema = ema(close, emalength)

// 100 SMA
smalength = input(110, title="SMA Period")
sma = sma(close, smalength)

emaforce = input(title="Force trend with medium EMA", type=input.bool, defval=true)
offsetemavalue = input(defval=6)

bullbounce = smma > ema and ema > sma and low[5] > ema and low[2] < ema and close[1] > ema and (ema[offsetemavalue] > sma or not emaforce)
bearbounce = smma < ema and ema < sma and high[5] < ema and high[2] > ema and close[1] < ema and (ema[offsetemavalue] < sma or not emaforce)

plotshape(bullbounce, title="Bulls", location=location.belowbar, color=#ff33cc, transp=0, style=shape.triangleup, size=size.tiny, text="Bolts")
plotshape(bearbounce, title="Bears", location=location.abovebar, color=#ff33cc, transp=0, style=shape.triangledown, size=size.tiny, text="Bolts")

strategy.initial_capital = 50000
ordersize = floor(strategy.initial_capital / close)

longs = input(title="Test longs", type=input.bool, defval=true)
shorts = input(title="Test shorts", type=input.bool, defval=true)
atrlength = input(title="ATR length", defval=12)
```