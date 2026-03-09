> Name

Multi-Indicator-Trend-Tracking-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/139ec6da5e272c29125.png)
[trans]

## Overview

This strategy is named **Multi-Indicator-Trend-Tracking-Strategy**. It utilizes multiple indicators, including Fisher Transform, Weighted Moving Average (WMA), Relative Strength Index (RSI), and On-Balance Volume (OBV) to determine the market trend direction and track trends for trading.

## Strategy Logic  

1. The Fisher Transform is used to detect price change trends and momentum. Trading signals are generated when four Fisher lines change color simultaneously.
2. WMA determines the major trend direction. RSI filters out fake signals.
3. OBV confirms the trend.

Specifically, Fisher Transform contains 1x, 2x, 4x, and 8x lines. When all four lines turn green simultaneously, a long signal is generated. When all four lines turn red simultaneously, a short signal is generated. WMA determines if the major trend is bullish or bearish. OBV confirms the trend direction. RSI filters out false signals.

## Advantage Analysis

The advantages of this strategy include:

1. Fisher Transform is momentum-sensitive; when four Fisher lines change color simultaneously, it ensures a high probability of trend reversal.
2. WMA determines the major trend to avoid trading against the trend.
3. OBV confirms the real trend and avoids false breakout in a trendless market.
4. RSI filters out false signals to ensure reliability.

By combining multiple indicators, this strategy ensures accuracy and reliability of trading signals while having the ability to track trends effectively, leading to good overall performance.

## Risk Analysis

This strategy also has certain risks:

1. Fisher lines may generate false signals if the market is in consolidation. RSI helps filter out such signals.
2. Improper WMA parameter setting may impact trend accuracy.
3. Fisher Transform does not perform well in ultra-short-term trends.
4. A waterfall decline can lead to significant losses.

To mitigate these risks, RSI parameters can be adjusted accordingly, and WMA period optimization is recommended. Stop loss mechanisms should also be set to avoid huge losses.

## Optimization Directions

This strategy can be further optimized through the following aspects:

1. Test effectiveness across different timeframes to find the optimal parameter combination.
2. Add a stop loss mechanism. Set a stop loss when loss reaches a certain level.
3. Further adjust Fisher Transform parameters based on backtest results to find the most accurate parameter combination.
4. Attempt to add other filtering indicators such as strength index, bias index, etc.
5. Test different strategies for setting position sizing.

## Conclusion

This strategy integrates Fisher Transform, WMA, OBV, and RSI to determine the market trend direction. It generates precise trading signals with strong confirmation capability, allowing effective locking in profits along the trend. With further parameter optimization, profit factor can be improved. In conclusion, through the combination of multiple indicators, this strategy effectively tracks trends with good performance.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|10|(?Fisher Transform)Len|
|v_input_int_2|true|mult1|
|v_input_int_3|2|mult2|
|v_input_int_4|4|mult3|
|v_input_int_5|8|mult4|
|v_input_int_6|14|(?Moving Averages)rsiLength|
|v_input_int_7|10|WMA Length|
|v_input_int_8|20|(?On-Balance Volume)OBV Length|
|v_input_float_1|0.1|OBV Bullish minimum value|
|v_input_float_2|-0.1|OBV Bearish minimum value|
|v_input_float_3|-0.7|(?RSI Level Filters)Reversal Down TP Filter|
|v_input_float_4|0.7|Reversal Up TP Filter|
|v_input_float_5|1.66|RSI Level Buy Filter|
|v_input_float_6|true|RSI Level Sell Filter|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-12-20 00:00:00
end: 2023-12-26 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
//author Sdover0123
strategy(title='FTR, WMA, OBV & RSI Strat', shorttitle='FTR WMA, OBV, RSI', overlay=false, default_qty_type=strategy.percent_of_equity, initial_capital = 100, default_qty_value=100, commission_value = 0.06, pyramiding = 3)
Len = input.int(10, minval=1, group="Fisher Transform")
mult1 = input.int(1, minval=1, group="Fisher Transform")
mult2 = input.int(2, minval=1, group="Fisher Transform")
mult3 = input.int(4, minval=1, group="Fisher Transform")
mult4 = input.int(8, minval=1, group="Fisher Transform")
fish(Length, timeMultiplier) =>
    var nValue1 = 0.0
    var nValue2 = 0.0
    var nFish = 0.0
    xHL2 = hl2
    xMaxH = ta.highest(xHL2, Length * timeMultiplier)
    xMinL = ta.lowest(xHL2, Length * timeMultiplier)
    nValue1 := (xMaxH - xMinL) / (xMaxH + xMinL)
    nValue2 := 0.5 * (nValue1 + 1)
    nFish := ((2 * nValue2 - 1) ^ Len) * 0.5 + 0.5
    nValue1, nValue2, nFish

// Additional code for WMA, RSI, and OBV would follow here
```