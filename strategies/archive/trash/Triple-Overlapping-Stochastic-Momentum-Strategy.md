> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|10|%K Length|
|v_input_2|3|%K Smoothing Length|
|v_input_3|3|%K Double Smoothing Length|
|v_input_4|10|Signal Length|
|v_input_5|ema|Signal MA Type|
|v_input_6|40|Overbought Level|
|v_input_7|-40|Oversold Level|
|v_input_8|20|%K Length 2|
|v_input_9|3|%K Smoothing Length 2|
|v_input_10|3|%K Double Smoothing Length 2|
|v_input_11|10|Signal Length 2|
|v_input_12|ema|Signal MA Type 2|
|v_input_13|40|Overbought Level 2|
|v_input_14|-40|Oversold Level 2|
|v_input_15|5|%K Length 3|
|v_input_16|3|%K Smoothing Length 3|
|v_input_17|3|%K Double Smoothing Length 3|
|v_input_18|10|Signal Length 3|
|v_input_19|ema|Signal MA Type 3|
|v_input_20|40|Overbought Level 3|
|v_input_21|-40|Oversold Level 3|
|v_input_22|8|From Month|
|v_input_23|true|From Day|
|v_input_24|2018|From Year|
|v_input_25|12|To Month|
|v_input_26|31|To Day|
|v_input_27|2018|To Year|

> Source (PineScript)


```pinescript
// version=2
strategy("Triple Overlapping Stochastic Momentum Strategy", overlay=false)

q = input(10, title="%K Length 1")
r = input(3, title="%K Smoothing Length 1")
s = input(3, title="%K Double Smoothing Length 1")
nsig1 = input(10, title="Signal Length 1")
matype1 = input("ema", title="Signal MA Type 1") // possible: ema, sma, wma, trima, hma, dema, tema, zlema
overbought1 = input(40, title="Overbought Level 1", type=float)
oversold1 = input(-40, title="Oversold Level 1", type=float)

q2 = input(20, title="%K Length 2")
r2 = input(3, title="%K Smoothing Length 2")
s2 = input(3, title="%K Double Smoothing Length 2")
nsig2 = input(10, title="Signal Length 2")
matype2 = input("ema", title="Signal MA Type 2") // possible: ema, sma, wma, trima, hma, dema, tema, zlema
overbought2 = input(40, title="Overbought Level 2", type=float)
oversold2 = input(-40, title="Oversold Level 2", type=float)

q3 = input(5, title="%K Length 3")
r3 = input(3, title="%K Smoothing Length 3")
s3 = input(3, title="%K Double Smoothing Length 3")
nsig3 = input(10, title="Signal Length 3")
matype3 = input("ema", title="Signal MA Type 3") // possible: ema, sma, wma, trima, hma, dema, tema, zlema
overbought3 = input(40, title="Overbought Level 3", type=float)
oversold3 = input(-40, title="Oversold Level 3", type=float)

// Calculate SMIs
s1 = sma(sma(close - (high + low) / 2, q), r) / (0.5 * sma(sma(high - low, q), r)) * 100
s2 = sma(sma(close - (high + low) / 2, q2), r2) / (0.5 * sma(sma(high - low, q2), r2)) * 100
s3 = sma(sma(close - (high + low) / 2, q3), r3) / (0.5 * sma(sma(high - low, q3), r3)) * 100

// Signals and Conditions
signal1 = crossover(sma(s1, nsig1), matype1 == "ema" ? ema(s1, nsig1) : sma(s1, nsig1))
signal2 = crossover(sma(s2, nsig2), matype2 == "ema" ? ema(s2, nsig2) : sma(s2, nsig2))
signal3 = crossover(sma(s3, nsig3), matype3 == "ema" ? ema(s3, nsig3) : sma(s3, nsig3))

exit1 = crossunder(sma(s1, nsig1), matype1 == "ema" ? ema(s1, nsig1) : sma(s1, nsig1))
exit2 = crossunder(sma(s2, nsig2), matype2 == "ema" ? ema(s2, nsig2) : sma(s2, nsig2))
exit3 = crossunder(sma(s3, nsig3), matype3 == "ema" ? ema(s3, nsig3) : sma(s3, nsig3))

// Trading Logic
if (signal1 and signal2 and signal3)
    strategy.entry("Buy", strategy.long)

if (exit1 or exit2 or exit3)
    strategy.close("Buy")

plot(s1, color=overbought1 > s1 ? color.red : overbought1 < s1 ? color.green : na, title="SMI 1")
plot(s2, color=overbought2 > s2 ? color.red : overbought2 < s2 ? color.green : na, title="SMI 2")
plot(s3, color=overbought3 > s3 ? color.red : oversold3 < s3 ? color.green : na, title="SMI 3")

```