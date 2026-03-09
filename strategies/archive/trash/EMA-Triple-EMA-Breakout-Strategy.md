> Name

Triple-EMA-Breakout-Strategy Triple-EMA-Breakout-Strategy

> Author

ChaoZhang

> Strategy Description


[trans]

### Strategy Overview

The triple EMA moving average breakout strategy is a quantitative strategy that uses the triple exponential moving average (EMA) indicator to generate trade signals. When the price breaks through the triple EMA, a trading signal is generated, and long or short operations are performed based on the direction of the price breakthrough. This strategy is mainly used to capture short- and medium-term price trend changes.

### Strategy Principles

1. Calculate triple EMA using the formula: 3 x EMA(n) - 3 x EMA[EMA(n)] + EMA[EMA(EMA(n))]

2. Go long when the price crosses above the triple EMA

3. Go short when the price breaks below the triple EMA

4. Exit signals are generated when the price returns below or above the triple EMA again

The triple EMA iterates on a single EMA indicator, enabling faster tracking of trends and turning points while retaining the trend-following characteristics of EMAs and smoothing the curve.

When using this strategy, the effectiveness of the breakout depends on the settings of the EMA parameters. Parameters can be adjusted according to the market to obtain the best trading results.

### Strategic Advantages

- Simple and straightforward triple EMA calculation method

- Faster response to price changes

- Smoothed curves effectively filter oscillations

- Easy determination of trend direction

- Adjustable parameters adaptable to market conditions

### Risk Warnings

- Potential price following lag

- Need to beware of false breakouts

- EMA parameter settings need to be continuously optimized

- Unable to determine the length of the trend

### Summary

The triple EMA moving average breakout strategy innovatively uses the MA indicator and has unique advantages in capturing short- and medium-term trend changes. Good trading results can be achieved by adjusting parameters. This strategy is worthy of backtest verification and real-time adjustment and optimization before application.

||


### Strategy Overview

The triple EMA breakout strategy is a quantitative strategy that generates trade signals using the triple exponential moving average (EMA) indicator. It produces signals when the price breaks through the triple EMA, with long or short positions taken based on the direction of the break. The strategy mainly aims to capture medium-short term trend changes.

### Strategy Logic

1. Calculate the triple EMA using the formula: 3 x EMA(n) - 3 x EMA[EMA(n)] + EMA[EMA(EMA(n))]

2. Go long when the price breaks above the triple EMA.

3. Go short when the price breaks below the triple EMA.

4. Exit signals are generated when the price returns back below or above the triple EMA.

The triple EMA iterates on a single EMA for faster reaction to trends and turning points, retaining the trend-following nature of EMAs while smoothing the curve.

The validity of the breakout depends on EMA parameter tuning, which can be adjusted for optimal trading performance.

### Advantages of the Strategy

- Simple and direct triple EMA calculation method

- Faster response to price changes

- Smoothed curves effectively filter oscillations

- Easy trend direction identification

- Adjustable parameters adaptable to market conditions

### Risk Warnings

- Potential price following lag

- Need to beware of false breakouts

- EMA parameter optimization required

- Hard to determine the length of the trend

### Conclusion

The triple EMA breakout strategy innovatively applies the MA indicator for unique advantages in capturing medium-short term trend changes. Excellent trading results can be achieved through parameter tuning. The strategy is worth backtesting, live optimization, and integration for application.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|26|Length|
|v_input_2|false|Trade reverse|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-01-01 00:00:00
end: 2023-04-25 00:00:00
Period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
////////////////////////////////////////////////////////////////
// Copyright by HPotter v1.0 14/08/2018
// This study plots the TEMA1 indicator. TEMA1 is a triple MA (Moving Average),
// and is calculated as 3*MA - (3*MA(MA)) + (MA(MA(MA)))
//
// You can change long to short in the Input Settings
// WARNING:
// - For purpose education only
// - This script to change bars colors.
////////////////////////////////////////////////////////////////
strategy(title="TEMA1 Backtest", shorttitle="TEMA", overlay = true )
Length = input(26, minval=1)
reverse = input(false, title="Trade reverse")
xPrice = close
xEMA1 = ema(xPrice, Length)
xEMA2 = ema(xEMA1, Length)
xEMA3 = ema(xEMA2, Length)
nRes = 3 * xEMA1 - 3 * xEMA2 + xEMA3
pos = iff(close > nRes, 1,
iff(close < nRes, -1, nz(pos[1], 0)))
possig = iff(reverse and pos == 1, -1,
iff(reverse and pos == -1, 1, pos))
if (possig == 1)
strategy.entry("Long", strategy.long)
if (possig == -1)
strategy.entry("Short", strategy.short)
barcolor(possig == -1 ? red: possig == 1 ? green : blue )
```

> Detail

https://www.fmz.com/strategy/426906

> Last Modified

2023-12-01 14:58:23