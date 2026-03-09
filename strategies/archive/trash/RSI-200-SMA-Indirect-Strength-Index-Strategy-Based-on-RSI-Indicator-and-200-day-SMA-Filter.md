> Name

Indirect-Strength-Index-Strategy-Based-on-RSI-Indicator-and-200-day-SMA-Filter

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1b091ed5e4a648e54f7.png)
[trans]

## Overview

This strategy mainly uses the Relative Strength Index (RSI) indicator to judge overbought and oversold situations, and employs a 200-day Simple Moving Average (SMA) filter as the main price trend filter. Based on determining the trend direction, it utilizes the RSI indicator to find better entry and exit points, achieving profitability. Compared with using the RSI indicator alone, this strategy increases trend judgment and can more accurately grasp market trends, allowing for higher returns in bull markets by chasing rises and selling declines, while doing the opposite in bear markets.

## Strategy Principle 

The strategy consists mainly of two parts: the RSI indicator and the 200-day SMA filter.

The RSI indicator section mainly judges whether the price has entered the overbought or oversold zone. Its calculation formula is:

```pinescript
RSI = 100 - 100 / (1 + Average gain of up days in RSI / Average loss of down days in RSI)
```

According to empirical parameters, when RSI < 30, it is oversold; when >70, it is overbought.

The 200-day SMA filter mainly judges the overall market trend direction. When the price is above the 200-day SMA, it is a bull market, otherwise it is a bear market.

Based on these two judgments, the strategy has the following entry and exit logic:

- Long entry: RSI < 45 and Close price > 200-day SMA
- Long exit: RSI > 75 and Close price > 200-day SMA  
- Short entry: RSI > 65 and Close price < 200-day SMA
- Short exit: RSI < 25 and Close price < 200-day SMA

Thus, the strategy uses the precise judgment of the RSI indicator to find better entry and exit points in the overall trend and thereby achieve higher returns.

## Advantage Analysis

The biggest advantage of this strategy is using the combination of the RSI indicator and 200-day SMA filter to make the strategy more stable and precise:

1. The 200-day SMA effectively judges the overall market trend, avoiding misjudgments from a single RSI indicator.
2. The RSI indicator can find better entry and exit points within the overall market trend.
3. The strategy operation is simple and easy to implement.

In addition, the strategy also has the following advantages:

1. Applicable to various products including stock indices, cryptocurrencies, and precious metals.
2. High capital utilization efficiency.
3. Can cautiously add a stop loss to effectively control single losses.

## Risk Analysis

The strategy also has some risks:

1. Sudden adjustments in the overall market may lead to greater losses.
2. There is some degree of lag in RSI and SMA indicators.
3. High trading frequency leads to higher trading costs.

To control these risks, the following measures can be taken:

1. Adjust position sizing appropriately to guard against impacts of unexpected events.
2. Optimize RSI and SMA parameters to reduce lag probability.
3. Adjust trading frequency appropriately to reduce trading costs.

## Optimization Directions

The strategy can be optimized in the following aspects:

1. Dynamically adjust RSI parameters based on market volatility.
2. Test whether other moving average indicators like EMA can bring better results.
3. Increase automatic stop loss mechanism.
4. Add position sizing module to dynamically adjust positions based on capital.
5. Optimize entry and exit logic to test if better returns can be achieved.

## Conclusion

The overall performance of this strategy is good, with the advantages of accurate judgment, simple operation, and wide applicability. After adding stop loss and position sizing, it can be carefully run in live trading. Follow-up aspects like parameter optimization, stop loss optimization, and position sizing can further enhance the strategy.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|---|---|---|
|v_input_int_1|14|RSI length|
|v_input_int_2|200|SMA length|
|v_input_float_1|5|stop loss|


> Source (PineScript)

```pinescript
// This work is licensed under a Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) https://creativecommons.org/licenses/by-nc-sa/4.0/
// © LuxAlgo

//@version=5
strategy("Relative Strength Index Extremes with 200-Day Moving Average Filter", overlay=true, pyramiding=1, initial_capital=10000, default_qty_type=s
```