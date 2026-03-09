<!-- AUTO-TRANSLATE FAILED: the JSON object must be str, bytes or bytearray, not NoneType -->


> Name

RWI Volatility Contrarian Strategy RWI-Volatility-Contrarian-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/172c13c696da25da589.png)
[trans]
### Overview  

The RWI Volatility Contrarian Strategy calculates the RWI highs and lows over a certain period to determine whether the market is in a reversal state, thereby identifying reversal opportunities. It adopts a contrarian strategy of going short at the highs and long at the lows, aiming for profit.

### Strategy Principle

Firstly, it calculates the RWI highs and lows over a specific length period (such as 14 candles). The calculation formulas are as follows:

RWI High = (High - Lowest of N Periods Ago) / (ATR of N Periods * sqrt(N))

RWI Low = (Highest of N Periods Ago - Low) / (ATR of N Periods * sqrt(N))

Then, it calculates the difference between the RWI highs/lows and a threshold to determine if this difference is below the threshold (such as 1). If both RWI highs and lows are below the threshold, the market is considered ranging. In this case, no action is taken.

If the RWI high is significantly above the RWI low by more than the threshold, it indicates that the price is about to reverse, and one may consider going short; if the RWI low is significantly above the RWI high by more than the threshold, it also suggests a reversal and the possibility of going long. This forms a contrarian trading strategy based on RWI indicators to determine market reversal states.

### Advantage Analysis

The RWI Volatility Contrarian Strategy has several advantages:

1. Using the RWI indicator to pinpoint reversal points is precise with high winning rates.
2. Adopting contrarian strategies suits ranging markets well.
3. The strategy logic is clear and easy to understand, with flexible parameter adjustments.
4. Long and short cycles can be configured to enhance signal quality.

### Risk Analysis

The RWI Volatility Contrarian Strategy also carries certain risks:

1. Reversal signals may experience false breakouts, leading to losses.
2. Frequent reversal signals during sustained trends can result in more losses.
3. Improper settings of RWI parameters may reduce the quality of signals.
4. The RWI indicator may fail when volatility increases.

To mitigate these risks, one can adjust RWI parameters, set up filters, and limit the range of reversals accordingly.

### Optimization Directions

The strategy can be further optimized in several ways:

1. Add double time frame analysis using long and short RWI periods to improve signal quality.
2. Combine with other indicators like KD and MACD to avoid false breakouts.
3. Configure stop loss strategies to strictly control single losses.
4. Dynamically optimize RWI parameters to adapt to market changes.
5. Optimize position management by adding or reducing positions based on market conditions.

### Summary

The RWI Volatility Contrarian Strategy has a clear overall logic, using the RWI indicator to determine reversal opportunities effectively. The trading logic is robust and performs well in ranging markets. By optimizing parameters and controlling risks, this strategy can be applied more stably and efficiently.

||

### Overview  

The RWI volatility contrarian strategy calculates the RWI highs and lows over a certain period to determine whether the market is in a reversal state in order to discover reversal opportunities. It adopts a contrarian strategy, going short at the highs and long at the lows, aiming for profit.

### Strategy Principle

Firstly, it calculates the RWI highs and lows over a specific length period (such as 14 candles). The calculation formulas are as follows:

RWI High = (High - Lowest of N Periods Ago) / (ATR of N Periods * sqrt(N))

RWI Low = (Highest of N Periods Ago - Low) / (ATR of N Periods * sqrt(N))

Then, it calculates the difference between the RWI highs/lows and a threshold to determine if this difference is below the threshold (such as 1). If both RWI highs and lows are below the threshold, the market is considered ranging. In this case, no action is taken.

If the RWI high is significantly above the RWI low by more than the threshold, it indicates that the price is about to reverse, and one may consider going short; if the RWI low is significantly above the RWI high by more than the threshold, it also suggests a reversal and the possibility of going long. This forms a contrarian trading strategy based on RWI indicators to determine market reversal states.

### Advantage Analysis

The RWI volatility contrarian strategy has several advantages:

1. Using the RWI indicator to pinpoint reversal points is precise with high winning rates.
2. Adopting contrarian strategies suits ranging markets well.
3. The strategy logic is clear and easy to understand, with flexible parameter adjustments.
4. Long and short cycles can be configured to enhance signal quality.

### Risk Analysis

The RWI volatility contrarian strategy also carries certain risks:

1. Reversal signals may experience false breakouts, leading to losses.
2. Frequent reversal signals during sustained trends can result in more losses.
3. Improper settings of RWI parameters may reduce the quality of signals.
4. The RWI indicator may fail when volatility increases.

To mitigate these risks, one can adjust RWI parameters, set up filters, and limit the range of reversals accordingly.

### Optimization Directions

The strategy can be further optimized in several ways:

1. Add double time frame analysis using long and short RWI periods to improve signal quality.
2. Combine with other indicators like KD and MACD to avoid false breakouts.
3. Configure stop loss strategies to strictly control single losses.
4. Dynamically optimize RWI parameters to adapt to market changes.
5. Optimize position management by adding or reducing positions based on market conditions.

### Summary

The RWI volatility contrarian strategy has a clear overall logic, using the RWI indicator to determine reversal opportunities effectively. The trading logic is robust and performs well in ranging markets. By optimizing parameters and controlling risks, this strategy can be applied more stably and efficiently.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|Length|
|v_input_2|true|Threshold|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
// Copyright (c) 2020-present, JMOZ (1337.ltd)
strategy("RWI Strategy", overlay=false)


length = input(title="Length", type=input.integer, defval=14, minval=1)
threshold = input(title="Threshold", type=input.float, defval=1.0, step=0.1)


rwi(length, threshold) =>
    rwi_high = (high - nz(low[length])) / (atr(length) * sqrt(length))
    rwi_low = (nz(high[length]) - low) / (atr(length) * sqrt(length))
    is_rw = rwi_high < threshold and rwi_low < threshold
    [is_rw, rwi_high, rwi_low]


[is_rw, rwi_high, rwi_low] = rwi(length, threshold)


long = not is_rw and rwi_high > rwi_low
short = not is_rw and rwi_low > rwi_high


strategy.entry("Long", strategy.long, when=long)
strategy.entry("Short", strategy.short, when=short)


plot(rwi_high, title="RWI High", linewidth=1, color=is_rw?color.gray:color.blue, transp=0)
plot(rwi_low, title="RWI Low", linewidth=1, color=is_rw?color.gray:color.red, transp=0)

```

> Detail

https://www.fmz.com/strategy/440724

> Last Modified

2024-02-01 14:56:58