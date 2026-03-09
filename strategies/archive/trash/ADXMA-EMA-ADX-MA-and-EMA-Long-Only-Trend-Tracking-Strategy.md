``` pinescript
/*backtest
start: 2023-01-22 00:00:00
end: 2024-01-28 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("ADX, MA, and EMA Long Strategy - ADX Trending Up", shorttitle="ADX_MA_EMA_Long_UpTrend", overlay=true)
adxlen = input(14, title="ADX Smoothing")
dilen = input(14, title="DI Length")
maPeriod = input(50, title="MA Period")
emaPeriod = input(50, title="EMA Period")

dirmov(len) =>
    up = change(high)
    down = -change(low)
    plusDM = na(up) ? na : (up > down and up > 0 ? up : 0)
    minusDM = na(down) ? na : (down > up and down > 0 ? down : 0)
    truerange = rma(tr, len)
    plus = fixnan(100 * rma(plusDM, len) / truerange)
    minus = fixnan(100 * rma(minusDM, len) / truerange)
    [plus, minus]

adx(dilen, adxlen) =>
    [plus, minus] = dirmov(dilen)
    sum = plus + minus
    100 * rma(abs(plus - minus) / (sum == 0 ? 1 : sum), adxlen)

sig = adx(dilen, adxlen)
maValue = sma(close, maPeriod)
emaValue = ema(close, emaPeriod)

longCondition = sig > sig[1] and close > maValue and close > emaValue
if (longCondition)
    strategy.entry("Long", strategy.long)

exitCondition = sig < sig[1] or  close < maValue or close < emaValue
if (exitCondition)
    strategy.close("Long")

plot(maValue, color=color.blue, title="MA")
plot(emaValue, color=color.orange, title="EMA")
plot(sig, color=color.red, title="ADX")
```

This Pine Script code defines a trading strategy that uses ADX, MA, and EMA to identify upward trends. The script includes the necessary inputs for configuring the ADX smoothing period, DI length, and moving average periods. It also implements logic for entering long positions based on these indicators and provides exit conditions. The plotted lines represent the Moving Average (blue), Exponential Moving Average (orange), and ADX values (red) to visually indicate the trend direction.