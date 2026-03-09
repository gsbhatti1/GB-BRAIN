> Name

Momentum-Oscillation-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/f1144a1d86d9d0beb5.png)

[trans]

## Overview

This strategy is based on the Bollinger Bands indicator, combined with momentum indicators, to implement a combination trading strategy of Bollinger Bands reversion and momentum breakout. When the price breaks through the middle line of the Bollinger Bands from below, it goes long; when the price breaks through the middle line from above, it goes short. It also tracks stop loss and take profit conditions based on entry price, closing positions when the target risk-reward ratio is met.

## Strategy Logic

The strategy uses the Bollinger Bands middle line `sma` as the moving average indicator, and dynamically adjusts the band width through `param mult*stdev`. When the price breaks through the middle line from below, it indicates that upward momentum has been gained, and thus the strategy goes long. When the price breaks through the middle line from above, it indicates that downward momentum has been gained, and thus the strategy goes short. After entering long/short positions, stop loss and take profit parameters are set to track profits and control risks.

Specifically, Bollinger Bands are calculated with two parameters - `length` and `mult`. `Length` determines the period of the middle line, and `mult` decides the band width. `enterLong` and `enterShort` judge the breakout timing. `exitLong` and `exitShort` calculate stop loss and take profit prices based on entry price and target percentage.

## Advantages

This strategy combines mean reversion and momentum, enabling it to capture significant trends early on. Compared to simply tracking moving averages, the added momentum judgment based on Bollinger Bands width can filter out some false breakouts. Stop loss and take profit are set directly based on entry price without manual intervention.

## Risks

- Lagging in Bollinger Bands fitting prices, may miss some moves
- Stop loss set too wide may increase loss risks
- Short signals in bull market may not turn out well

Parameters like periods, band width, and stop loss range can be optimized to make the strategy adaptable to different market conditions.

## Enhancement

- Add trading volume or volatility to avoid low volume false breakouts
- Param grid search to optimize periods, width coefficient, and stop loss percentage
- Go only long or short based on market regime
- Add Machine Learning model to determine trend direction

## Conclusion

This strategy integrates the strengths of Bollinger Bands reversion and momentum, enabling it to capture some trends early on. Through parameter tuning, it can adapt to different market stages. The direct stop loss/take profit calculation reduces manual intervention. There is still room for improvement, such as incorporating more auxiliary indicators. These will be incrementally enhanced in further research and optimization.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|20|Length|
|v_input_2|2|Multiplier|
|v_input_3|0.5|Target Percent|
|v_input_4|95|Stop Loss Percent|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-11-13 00:00:00
end: 2023-11-20 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("BURATINO", overlay=true)

// Input parameters
length = input(20, minval=1, title="Length")
mult = input(2.0, minval=0.1, maxval=5, title="Multiplier")
target_percent = input(0.5, minval=0.1, title="Target Percent")
stop_loss_percent = input(95, minval=0.1, title="Stop Loss Percent")

// Calculation of Bollinger Bands
basis = sma(close, length)
dev = mult * stdev(close, length)
upper = basis + dev
lower = basis - dev

// Reversal from below through the middle line of Bollinger Bands for long entry
enterLong = cross(close, basis) and close[1] < basis[1]

// Reversal from above through the middle line of Bollinger Bands for short entry
enterShort = cross(basis, close) and close[1] > basis[1]

// Close long position after price increase by specified percentage or decrease by specified percentage
exitLong = close >= strategy.position_avg_price * (1 + (target_percent / 100)) or close <= strategy.position_avg_price * (1 - (stop_loss_percent / 100))

// Close short position after price decrease by specified percentage or increase by specified percentage
exitShort = close <= strategy.position_avg_price * (1 - (target_percent / 100)) or close >= strategy.position_avg_price * (1 + (stop_loss_percent / 100))

// Position management and restrictions on opening opposite positions
strategy.entry("Long", strategy.long, when = enterLong and strategy.position_size == 0)
strategy.entry("Short", strategy.short, when = enterShort and strategy.position_size == 0)

strategy.close("Long", when = exitLong)
strategy.close("Short", when = exitShort)

// Visualization of Bollinger Bands
plot(basis, color=color.blue, title="Basis")
plot(upper, color=color.red, title="Upper")
plot(lower, color=color.green, title="Lower")
```

> Detail

https://www.fmz.com/strategy/432804

>