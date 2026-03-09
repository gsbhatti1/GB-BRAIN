---
## Overview

This strategy uses moving average, ATR, Bollinger Bands for trend judgment and breakout trading, combined with force index for timing, belonging to the breakout class of strategies.

## Strategy Logic

1. Calculate middle, upper, and lower lines of Bollinger Bands. The middle line is the simple moving average (sma) of the close price; the upper and lower are the middle line ± standard deviation (stdDev).

2. Calculate fast and slow ATR. The fast ATR has a period of 20, while the slow ATR has a period of 50.

3. Calculate force index XFORCE, which is the cumulative product of volume * (close - previous close). Then calculate the fast and slow exponential moving averages (EMA) of XFORCE.

4. Determine long signal: when the fast XFORCE crosses above the slow XFORCE, and fast ATR > slow ATR, and closing price > opening price.

5. Determine short signal: when the fast XFORCE crosses below the slow XFORCE, and fast ATR > slow ATR, and closing price < opening price.

6. Execute long position when a long signal is triggered; execute short position when a short signal is triggered.

## Advantage Analysis

1. Moving averages provide trend judgment, while Bollinger Bands indicate breakout points.
2. The ATR indicator measures market volatility, enabling volatility trading.
3. The force index determines the direction of force, facilitating force-based breakouts.
4. Combining multiple indicators offers a more comprehensive analysis.
5. Clear and simple rules are easy to understand and implement.
6. Backtest results show good performance with stable profits.

## Risk Analysis

1. Improper Bollinger Bands width settings can generate false signals.
2. Incorrect ATR parameter settings may fail to capture market volatility.
3. The force index has limited effectiveness, unable to determine true trend reversals.
4. Adjusting parameters and weights for multiple indicators is challenging.
5. Breakout signals may be inaccurate; divergence could occur.
6. Drawdowns can be substantial, which can be managed through stop-loss mechanisms.

## Optimization Directions

1. Optimize Bollinger Bands parameters for different time frames and instruments.
2. Fine-tune ATR parameters to better capture volatility.
3. Integrate trend indicators such as MACD for validation purposes.
4. Implement stop-loss strategies like trailing stops to control drawdowns.
5. Utilize AI algorithms to identify reversal signals.
6. Combine multiple timeframes for a more holistic judgment, reducing the chances of false signals.

## Summary

This strategy integrates moving averages, ATR, Bollinger Bands, and force index to form a comprehensive breakout trading system. Further improvements through parameter optimization, adding trend filters, stop-loss strategies, and AI algorithms can enhance stability and profitability. However, no strategy is perfect; continuous optimizations based on backtest results are necessary to adapt to changing market conditions.

---

## Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|v_input_1|3|Fast|
|v_input_2|20|Slow|
|v_input_3|20|ATR Fast|
|v_input_4|50|ATR Slow|
|v_input_5|20|Length|
|v_input_6|2|multiplier|
|v_input_7_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|

## Source (PineScript)

```pinescript
//@version=2
strategy("yuthavithi volatility based force trade scalper strategy", overlay=true)

fast = input(3, minval=1, title="Fast")
slow = input(20, minval=1, title="Slow")
atrFast = input(20, minval=1, title="ATR Fast")
atrSlow = input(50, minval=1, title="ATR Slow")

len = input(20, minval=1, title="Length")
multiplier = input(2, minval=1, title="Multiplier")
src = input(close, title="Source")
bbMid = sma(src, len)
plot(bbMid, color=blue)

atrFastVal = atr(atrFast)
atrSlowVal = atr(atrSlow)
stdOut = stdev(close, len)
bbUpper = bbMid + stdOut * multiplier
bbLower = bbMid - stdOut * multiplier
plot(bbUpper, color=(atrFastVal > atrSlowVal ? red : silver))
plot(bbLower, color=(atrFastVal > atrSlowVal ? red : silver))

force = volume * (close - nz(close[1]))
xforce = cum(force)
xforceFast = ema(xforce, fast)
xforceSlow = ema(xforce, slow)

bearish = ((xforceFast < xforceSlow) and (atrFastVal > atrSlowVal)) and ((xforceFast[1] > xforceSlow[1]) or (atrFastVal[1] < atrSlowVal[1])) and (close < open)
bullish = ((xforceFast > xforceSlow) and (atrFastVal > atrSlowVal)) and ((xforceFast[1] < xforceSlow[1]) or (atrFastVal[1] < atrSlowVal[1])) and (close > open)

if (bullish)
    strategy.entry("Buy", strategy.long)

if (bearish)
    strategy.entry("Sell", strategy.short)
```

## Detail

https://www.fmz.com/strategy/430261

## Last Modified

2023-10-26 16:17:17
---