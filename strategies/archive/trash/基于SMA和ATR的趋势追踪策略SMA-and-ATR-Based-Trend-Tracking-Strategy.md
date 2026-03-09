```pinescript
/*backtest
start: 2024-01-16 00:00:00
end: 2024-01-16 17:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © omererkan

//@version=5
strategy(title="SMA with ATR", overlay=true)

smaLen = input.int(100, title="SMA Length")

atrLen     = input.int(10, title="ATR Length")
stopOffset = input.float(4, title="Stop Offset Multiple", step=0.25)


smaValue  = ta.sma(close, smaLen)
stopValue = ta.atr(atrLen) * stopOffset


lowerCloses = close < close[1] and 
     close[1] < close[2] and
     close[2] < close[3]

enterLong = close > smaValue and 
     lowerCloses


longStop = 0.0
longStop := if enterLong and strategy.position_size < 1
    close - stopValue
else
    math.max(close - stopValue, longStop[1])


higherCloses = close > close[1] and 
     close[1] > close[2] and
     close[2] > close[3]

enterShort = close < smaValue and 
     higherCloses


shortStop = 0.0
shortStop := if enterShort and strategy.position_size > -1
    close + stopValue
else
    math.min(close + stopValue, shortStop[1])


plot(smaValue, color=#4169e1, linewidth=2, title="SMA")

plot(strategy.position_size > 0 ? longStop : na, color=color.lime,
     style=plot.style_linebr, title="Long stop", linewidth=2)

plot(strategy.position_size < 0 ? shortStop : na, color=color.red,
     style=plot.style_linebr, title="Short stop", linewidth=2)


if enterLong
    strategy.entry("EL", strategy.long)

if enterShort
    strategy.entry("ES", strategy.short)


if strategy.position_size > 0
    strategy.exit("SL Long", from_entry="EL", stop=longStop)

if strategy.position_size < 0
    strategy.exit("SL Short", from_entry="ES", stop=shortStop)


if enterLong
    strategy.cancel("Exit Short")

if enterShort
    strategy.cancel("Exit Long")

```

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|100|SMA Length|
|v_input_int_2|10|ATR Length|
|v_input_float_1|4|Stop Offset Multiple|


> Detail

https://www.fmz.com/strategy/439260

> Last Modified

2024-01-18 16:04:51