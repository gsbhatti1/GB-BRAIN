> Name

Bollinger-Band-Moving-Average-and-MACD-Combined-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/11a14d6bf202f063dde.png)
[trans]

## Strategy Overview

This strategy combines Bollinger Bands, moving average, and MACD to form a relatively comprehensive trading system. While judging the market trend, it can also capture some reversal opportunities.

## Strategy Name & Rationale  

The name of this strategy is "Triangle Anchoring Trend Tracking Strategy." The name highlights its use of three technical indicators—Bollinger Bands, moving average, and MACD—to determine the direction of trends and anchor entry points. 

The basic trading logic is:

1. **Judge trend direction**. Compare Bollinger Mid Band, EMA (Exponential Moving Average), and MACD zero line to determine if the market is in an uptrend or downtrend phase.

2. **Find entry opportunities**. After a trend is identified, the strategy checks if EMA crosses BB Mid Band and if MACD histogram crosses the signal line to determine entries.

3. **Set profit target and stop loss**. Once entered, fixed target and stop loss levels are preset.

## Advantage Analysis

The biggest advantage of this strategy lies in its simultaneous use of trend, moving average, and MACD tools to guide decisions. This allows for more accurate judgments of market momentum and also helps capture some reversals.

Firstly, the Bollinger Mid Band clearly reflects the current primary trend direction. The role of EMA is to track the progress of trends. Their comparison and combination enable more precise trend identification.

Secondly, Bollinger Bands themselves have strong envelope characteristics. The area around the mid band also indicates certain support/resistance levels, making EMA crossovers valuable signals.

Additionally, MACD measures the wax and wane of bullish/bearish momentum. Its absolute size represents high or low crowd emotions, also hinting potential reversals.

Finally, preset profit targets and stop losses control risk/reward for individual trades, ensuring overall stability.

## Risk Analysis

Despite the use of multiple analytical tools, main risks include:

1. **Improper Bollinger Bands parameters** failing to clearly reflect the primary trend.
2. **EMA system signals long but MACD does not clearly turn positive**, potentially allowing bearish forces to expand.
3. **Profit target/stop loss range too wide**, leading to larger single trade losses.

Main solutions are:

1. **Adjust Bollinger Bands parameters** to ensure mid band effectively reflects the main trend.
2. **Introduce more technical indicators** to judge bull/bear momentum.
3. **Evaluate historical trades and optimize profit targets/stops**.

## Optimization Directions

The strategy can be further improved in the following aspects:

1. **Introduce more indicators like KDJ, ATR** etc., to aid trend judgment and improve accuracy.
2. **Implement more sophisticated stops** like trailing stop, breakout stop etc.
3. **Assess performance across different products**. Fine-tune parameters to suit various market conditions.
4. **Test and tweak strategy based on backtest results over different timeframes and markets**.
5. **Incorporate machine learning for automatic parameter optimization and dynamic strategy update**.

## Conclusion

This strategy leverages Bollinger Bands, moving average, and MACD together. It has clear trend judgment, certain envelope characteristics, and also captures some reversals. With more auxiliary tools for judging entries/exits, it can achieve more reliable performance. Further evaluation and enhancement of this strategy are warranted and expected to produce a robust quantitative tool.

||

## Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|150|BB Length|
|v_input_2_close|0|BB Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_3|2|BB StdDev|
|v_input_4|34|EMA Length|
|v_input_5_close|0|EMA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_6|SMA|Method|
|v_input_7|5|Length|
|v_input_8|9|Fast Length|
|v_input_9|17|Slow Length|
|v_input_10_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_int_1|9|Signal Smoothing|
|v_input_string_1|0|Oscillator MA Type: EMA|SMA|
|v_input_string_2|0|Signal Line MA Type: EMA|SMA|

> Source (PineScript)

```pinescript
/*backtest
start: 2024-01-04 00:00:00
end: 2024-02-03 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Combined Strategy", overlay=true, shorttitle="Comb Strat", default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// Take Profit and Stop Loss
takeProfitTicks = 87636
stopLossTicks = 53350

// Bollinger Bands + EMA
length_bb = input(150, title="BB Length")
src_bb = input(close, title="BB Source")
mult = input(2.0, title="BB StdDev")
basis = ta.sma(src_bb, length_
```