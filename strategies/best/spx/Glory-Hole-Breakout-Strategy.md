<!-- AUTO-TRANSLATE FAILED: the JSON object must be str, bytes or bytearray, not NoneType -->


> Name

Glory Hole Breakout Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/157be87a48d6302da71.png)

[trans]

## Overview

The Glory Hole breakout strategy is a trend-following strategy that combines moving average and ADX indicators to determine price trends and strength. It enters the market when prices break through the moving average. This simple and practical strategy can effectively track trends and has high profit potential.

## Strategy Logic

The strategy is mainly based on three indicators:

1. SMA: Simple Moving Average (SMA) to determine price trend direction.
2. ADX: Average Directional Movement Index (ADX) to measure trend strength, where higher values indicate stronger trends.
3. Glory Hole Condition: Bullish when close > open and close near low; Bearish when close < open and close near high.

The trading logic is:

1. Calculate the N-period SMA to determine the overall trend direction.
2. Calculate the M-period ADX to determine trend strength, only generating trade signals if ADX is above a certain threshold.
3. Go long when a bullish Glory Hole forms, with close > SMA and ADX > threshold.
4. Go short when a bearish Glory Hole forms, with close < SMA and ADX > threshold.
5. Exit the position using stop loss or take profit.

## Advantages

1. Combines trend direction and strength indicators for effective trend following.
2. Glory Hole condition filters out most false breakouts, improving entry quality.
3. Uses SMA instead of Exponential Moving Average (EMA) to better capture medium-to-long-term trends.
4. ADX indicator avoids trading in no-trend zones, ensuring high-probability setups.
5. Simple and clear rules make it easy to implement.

## Risks

1. SMA is a lagging indicator; early or late entries can lead to stop-loss triggers. Optimize the SMA period parameter.
2. ADX may incorrectly judge trend reversals as no-trend zones, increasing risk of false signals. Lower the ADX threshold for better risk management.
3. Despite Glory Hole filtering, tight risk management is still necessary in real trades; adjust stop loss positions appropriately.
4. The strategy lacks a balance between long and short positions, requiring manual intervention or optimization.

## Enhancement Opportunities

1. Optimize SMA and ADX parameters to find the best combination.
2. Add other trend indicators like Bollinger Bands or KDJ to improve entry quality.
3. Incorporate additional exit logic such as trend reversal or drawdown percentage to refine exits.
4. Include a long/short ratio judgment to avoid excessive one-sided trades.
5. Optimize stop loss strategies from fixed to trailing or staggered.
6. Improve risk management for better control over single trade risks.

## Summary

The Glory Hole strategy integrates SMA and ADX indicators to determine trend direction and strength, generating trading signals based on the Glory Hole condition. This simple and practical strategy effectively tracks trends and filters out noise but also has lagging trend determination and stop loss risks. Further improvements in parameter optimization, entry/exit logic, and risk management will enhance its efficiency and stability.

[/trans]

> Strategy Arguments


|Argument    |Default  |Description                                                                                      |
|------------|---------|--------------------------------------------------------------------------------------------------|
|v_input_1   |20      |SMA Period                                                                                        |
|v_input_2_close|0       |Source: close, high, low, open, hl2, hlc3, hlcc4, ohlc4                                         |
|v_input_3   |30      |ADX Tradelevel                                                                                   |
|v_input_4   |14      |ADX Smoothing                                                                                    |
|v_input_5   |14      |DI Length                                                                                        |


> Source (PineScript)

```pinescript
/*backtest
start: 2022-10-18 00:00:00
end: 2023-10-24 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
strategy("Glory Hole with SMA + ADX", overlay=true)
len = input(20, minval=1, title="SMA")
src = input(close, title="Source")
ADXlevel = input(30, minval=1, title="ADX Tradelevel")
out = sma(src, len)

//adx
adxlen = input(14, title="ADX Smoothing")
dilen = input(14, title="DI Length")
dirmov(len) =>
    up = change(high)
    down = -change(low)
    truerange = rma(tr, len)
    plus = fixnan(100 * rma(up > down and up > 0 ? up : 0, len) / truerange)
    minus = fixnan(100 * rma(down > up and down > 0 ? down : 0, len) / truerange)
    [plus, minus]

adx(dilen, adxlen) => 
    [plus, minus] = dirmov(dilen)
    sum = plus + minus
    adx = 100 * rma(abs(plus - minus) / (sum == 0 ? 1 : sum), adxlen)

sig = adx(dilen, adxlen)

plot(out, title="SMA", color=blue)

bullish = ((out < close) and (out < open) and (out > low) and (sig > ADXlevel))
bearish = ((out > close) and (out > open) and (out < high) and (sig > ADXlevel))

if (bullish)
    strategy.entry("Buy", strategy.long)

if (bearish)
    strategy.entry("Sell", strategy.short)
```

> Detail

https://www.fmz.com/strategy/430124

> Last Modified

2023-10-25 11:35:36