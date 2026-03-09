> Name

Sentiment-Based-XBT-Futures-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/a123d6024287194256.png)
[trans]

## Overview

This strategy adopts the approach of multi-cycle sentiment analysis to trade XBTUSD futures contracts. It comprehensively considers the price fluctuation range and highest and lowest prices across different cycles, and calculates the overall market sentiment through a series of weight adjustments. Buy and sell signals are generated based on the changing patterns of the sentiment value.

## Strategy Logic

1. Calculate the highest price, lowest price, average price, price fluctuation range, and other indicators across cycles from a to j (1 to 89 bars).

2. Define the standardized position of the closing price within the price range (place variable). Combine it with the price fluctuation range of each cycle to calculate the sentiment value for different cycles.

3. The sentiment values go through a series of weight (w variable) adjustments to get the overall sentiment value (sentiment). The sentiment reflects the current overall market mood.

4. Analyze the fluctuation of sentiment value. A sell signal is generated when sentiment turns from positive to negative. A buy signal is generated when sentiment turns from negative to positive.

5. Determine entry momentum and set take profit and stop loss conditions based on the absolute value of sentiment fluctuation (delta variable).

## Advantages

1. Consider sentiment across different cycles for a more comprehensive market trend judgment.

2. The weight adjustment mechanism makes the strategy more stable.

3. More precise entry timing by combining sentiment value and its fluctuation.

4. Manage risks with highest price, lowest price, take profit, and stop loss.

## Risks

1. Improper parameter settings may cause too frequent trading or missing opportunities.

2. Black swan events may invalidate the strategy logic.

3. Contract adjustments and rule changes may impact strategy performance.

4. Sentiment calculation relies on historical data. Reassessment is needed when market regime changes.

Risks can be managed by adjusting weights, trading cycles, take profit ratios, etc., to fit changing market conditions. Meanwhile, optimize capital management by strictly controlling position sizing and overall exposure.

## Optimization Directions

1. Expand analysis cycles to build a richer basis for sentiment judgment.

2. Incorporate more technical indicators for a combined approach.

3. Extract sentiment features with machine learning methods.

4. Dynamically adjust weight settings.

5. Optimize take profit and stop loss strategies.

## Conclusion

This strategy is based on the trading philosophy of sentiment analysis. It determines the current overall market mood by considering multiple cycles. The continuous sentiment changes serve as the basis for generating trading signals, assisted by price fluctuation for timing entry. This unique approach of judging market trends works well in ranging cycles. Further expanding analysis periods, adding more indicators, and optimizing can make the sentiment trading strategy more mature and stable for adapting more complex market environments.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|true|leverage|
|v_input_2|53|take profit %|
|v_input_3|7|stoploss %|
|v_input_4|0.7|level to initiate trade|
|v_input_5|false|level to close trade|
|v_input_6|0.68|level to initiate trade|
|v_input_7|false|level to close trade|
|v_input_8|1.158|weight a|
|v_input_9|1.119|weight b|
|v_input_10|1.153|weight c|
|v_input_11|1.272|weight d|
|v_input_12|1.295|weight e|
|v_input_13|1.523|weight f|
|v_input_14|1.588|weight g|
|v_input_15|2.1|weight h|
|v_input_16|1.816|weight i|
|v_input_17|2.832|weight j|


> Source (PineScript)

```pinescript
//@version=4
strategy("expected range STRATEGY", overlay=false, initial_capital=1000, precision=2)

// 2h chart BITMEX:XBTUSD
// use on low leverage 1-2x only

leverage = input(1, "leverage", step=0.5)
tp = input(53, "take profit %", step=1)
sl = input(7, "stoploss %", step=1)
stoploss = 1 - (sl / 100)
plot(stoploss)
level = input(0.7, "level to initiate trade", step=0.02)
closelevel = input(0.0, "level to close trade", step=0.02)
levelshort = input(0.68, "level to initiate trade", step=0.02)
closelevelshort = input(0.0, "level to close trade", step=0.02)

wa = input(1.158, "weight a", step=0.2)
wb = input(1.119, "weight b", step=0.2)
wc = input(1.153, "weight c", step=0.2)
wd = input(1.272, "weight d", step=0.2)
we = input(1.295, "weight e", step=0.2)
wf = input(1.523, "weight f", step=0.2)
wg = input(1.588, "weight g", step=0.2)
wh = input(2.1, "weight h", step=0.2)
wi = input(1.816, "weight i", step=0.2)
wj = input(2.832, "weight j", step=0.2)
```

