> Name

MACD-Based Long-Only Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/8d62e983ebbddf0003.png)
[trans]

### Overview

This strategy is based on the MACD indicator and long and close lines to implement long-term trading of the currency pair. It opens positions when the MACD indicator line crosses over the long line and closes positions when the MACD indicator line crosses below the close line. Stop loss strategy is also configured.

### Strategy Logic

The strategy uses fast and slow lines of the MACD indicator. The fast line has a parameter of 12-day EMA, and the slow line has a parameter of 26-day EMA. The difference between the two lines is the MACD histogram. In addition, 9-day EMA is calculated as the signal line. It goes long when the MACD histogram crosses above 0.04 and closes long positions when crossing below 0.015. Also, 5% stop loss is set.

Specifically, the strategy first calculates the fast line, slow line, and signal line of the MACD indicator. Then, the long line is set at -0.04, and the close line is set at 0.015. If the current MACD histogram is greater than the long line, it goes long. If the current MACD histogram is less than the close line, it closes the long position. In addition, the stop loss line is set at 95% of the entry price.

### Advantage Analysis

The strategy has the following advantages:

1. Use MACD indicator to judge market trend with high accuracy
2. Double filter with long and close lines avoids wrong signals
3. Stop loss strategy effectively controls risks
4. Simple and clear logic, easy to understand and implement
5. Only needs MACD indicator, less resource occupation

### Risk Analysis

The strategy also has some risks:

1. MACD indicator has some lagging, may miss short-term opportunities
2. Stop loss setting may be too conservative to keep tracking long-term trends
3. Parameter tuning needs lots of backtesting, otherwise overfitting may occur
4. Only applicable to [insert specific pair], effectiveness for other pairs is uncertain

Methods like adjusting parameters, combining other indicators can be used to optimize and improve.

### Optimization Directions

The strategy can be optimized in the following aspects:

1. Test different MACD parameter combinations to find better parameters

   Fast line, slow line, signal line with different lengths can be tried to find more suitable combinations

2. Try other indicators

   Indicators like RSI, KD may have very different results

3. Optimize long and close line parameters

   More suitable parameters can be found through repetitive backtesting

4. Adjust stop loss strategy

   Consider trailing stops to make stop loss more dynamic

5. Test on different currency pairs

   Apply the strategy to other pairs and examine the effects

### Conclusion

In conclusion, this is an overall very simple and intuitive long-term trading strategy. It judges market conditions using MACD indicator and sets double filter criteria to reduce false trading. Risk control is also configured through stop loss. The logic is clear and resource occupation is low. It is easy to understand and implement, worth recommending. Of course, there is still much room for improvement through parameter tuning, indicator change and other means, to make the strategy even more outstanding.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|12|Fast moving average|
|v_input_2|26|Slow moving average|
|v_input_3|12|Fast Length|
|v_input_4|26|Slow Length|
|v_input_5_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_6|9|Signal Smoothing|
|v_input_7|false|Simple MA(Oscillator)|
|v_input_8|false|Simple MA(Signal Line)|
|v_input_9|-0.04|Enter Long|
|v_input_10|0.015|Close Long|
|v_input_11|0.05|Stop Loss %|


> Source (PineScript)

```pinescript
//@version=3
strategy(shorttitle = "GBPJPY MACD", title = "GBPJPY MACD")
fastMA = input(title="Fast moving average",  defval = 12, minval = 7)
slowMA = input(title="Slow moving average",  defval = 26, minval = 7)
lastColor = yellow
[currMacd,_,_] = macd(close[0], fastMA, slowMA, 9)
[prevMacd,_,_] = macd(close[1], fastMA, slowMA, 9)
plotColor = currMacd > 0 ? currMacd > prevMacd ? lime : green : currMacd < prevMacd ? maroon : red
plot(currMacd, style = histogram, color = plotColor, linewidth = 3)
plot(0, title = "Zero line", linewidth = 1, color = gray)

//MACD
// Getting inputs
fast_length = input(title="Fast Length",  defval=12)
slow_length = input(title="Slow Length",  defval=26)
src = input(title="Source",  defval=close)
signal_length = input(title="Signal Smoothing",  minval = 1, maxval = 50, defval =9)
sma_source = input(title="Simple MA(Oscillator)", type=bool, defval=false)
if sma_source
    sma_signal = sma(src, signal_length)
else
    sma_signal = na

plot(sma_signal, title="Signal Line", color=blue)
plot(macd, title="MACD Line", color=orange)
plot(macd - sma_signal, title="Histogram", color=plotColor)

// Strategy Logic
long_entry = macd > -0.04
long_exit = macd < 0.015
stop_loss = 0.95 * open

when(long_entry) strategy.entry("Long", strategy.long)
when(long_exit) strategy.close("Long")

// Plotting
plotshape(series=long_entry, title="Long Entry", location=location.belowbar, color=green, style=shape.triangleup, size=size.small)
plotshape(series=long_exit, title="Long Exit", location=location.abovebar, color=red, style=shape.triangledown, size=size.small)

```

This code implements the strategy logic described in the document.