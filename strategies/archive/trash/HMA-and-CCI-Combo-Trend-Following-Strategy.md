```plaintext
Name

HMA-and-CCI-Combo-Trend-Following-Strategy

Author

ChaoZhang

Strategy Description

This strategy uses a combination of HMA and CCI indicators to achieve trend judgment and tracking transactions. Specifically, go long when the HMA breaks upward and the CCI indicator crosses above the lower band; go short when the HMA breaks downward and the CCI indicator crosses below the upper band. The conditions for closing the position are that HMA breaks back in the opposite direction or CCI re-enters the threshold range.

The advantage of this strategy is using HMA to determine the trend direction, and CCI to confirm the timing of the trend start, which can effectively reduce erroneous transactions caused by gaps and pullbacks. However, both HMA and CCI indicators have hysteresis and may miss the best entry point. At the same time, the CCI indicator has weak ability to judge complex market conditions.

In general, the combined trend following strategy of HMA and CCI can achieve good results in the stage when the trend is obvious. However, you still need to pay attention to the stop loss setting during the real offer process, and stop the loss in time to avoid losses caused by LIBR. Only when the parameters are optimized in place can this strategy be applied for a long time.

This strategy combines HMA and CCI to identify and trade trends. Specifically, it goes long when HMA breaks upwards and CCI crosses above lower band, and goes short when HMA breaks downwards and CCI crosses below upper band. Exits occur when HMA breaks back in opposite direction, or CCI re-enters threshold range.

The advantage of this strategy is using HMA to determine trend direction, and CCI to confirm trend start, effectively reducing whipsaws and pullback errors. However, both HMA and CCI have lagging issues, potentially missing optimal entry points. Also, CCI has limited capabilities in complex market situations.

In summary, the HMA and CCI combo trend following strategy can produce decent results during strong trending phases. But in live trading, attention is still needed on stop loss to cut losses from LIQR events. Only with proper parameter optimization can this strategy be applied successfully in the long run.
```

Source (PineScript)

```pinescript
/*backtest
start: 2023-08-11 00:00:00
end: 2023-09-10 00:00:00
Period: 3h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("HMA+CCI strategy", overlay=true)

src = input(close)
hmaLen = input(21)
cciLen = input(10)
cciLower = input(-50)
cciUpper = input(50)
cciLowerExit = input(-100)
cciUpperExit = input(100)
hmaExit = input(false)
cciExit = input(true)
//rciLower = input(-60)
//rciUpper = input(60)

// Backtest
fromyear = input(2017, defval = 2018, minval = 1900, maxval = 2100, title = "From Year")
toyear = input(2100, defval = 2100, minval = 1900, maxval = 2100, title = "To Year")
frommonth = input(01, defval = 01, minval = 01, maxval = 12, title = "From Month")
tomonth = input(12, defval = 12, minval = 01, maxval = 12, title = "To Month")
fromday = input(21, defval = 01, minval = 01, maxval = 31, title = "From day")
today = input(31, defval = 31, minval = 01, maxval = 31, title = "To day")

leverage = input(100)

term = (time > timestamp(fromyear, frommonth, fromday, 00, 00) and time < timestamp(toyear, tomonth, today, 23, 59))

ord(seq, idx, itv) =>
    p = seq[idx]
    o = 1
    for i = 0 to itv - 1
        if p < seq[i]
            o := o + 1
    o

d(itv) =>
    sum = 0.0
    for i = 0 to itv - 1
        sum := sum + pow((i + 1) - ord(src, i, itv), 2)
    sum

rci(itv) => (1.0 - 6.0 * d(itv) / (itv * (itv * itv - 1.0))) * 100.0

hullma = wma(2*wma(src, hmaLen/2)-wma(src, hmaLen), round(sqrt(hmaLen)))
cci = cci(close, cciLen)
plot(hullma, color=hullma[1]>hullma?red:green, linewidth=4)
longCondition = hullma[1] < hullma and crossover(cci, cciLower) // rci < -60 // crossover(cci, cciLower)
shortCondition = hullma[1] > hullma and crossunder(cci, cciUpper) // rci > 60
exitLong1 = hmaExit ? hullma[1] > hullma : false
exitLong2 = cciExit ? cci > cciUpperExit : false
exitShort1 = hmaExit ? hullma[1] < hullma : false
exitShort2 = cciExit ? cci < cciLowerExit : false

if (longCondition and term)
    strategy.entry("Long", strategy.long )
if (shortCondition and term)
    strategy.entry("Short", strategy.short)

if strategy.position_size > 0 and term
    if (exitLong1 or exitLong2)
        strategy.close_all()
if strategy.position_size < 0 and term
    if (exitShort1 or exitShort2)
        strategy.close_all()
```

Detail

https://www.fmz.com/strategy/426363

Last Modified

2023-09-11 15:02:37
```