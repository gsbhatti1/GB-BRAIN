> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|32|r|
|v_input_2|5|s|
|v_input_3|5|u|
|v_input_4|3|SmthLen|
|v_input_5|false|Trade reverse|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-17 00:00:00
end: 2024-01-16 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version = 2
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 12/12/2016
// This is one of the techniques described by William Blau in his book "Momentum,
// Direction and Divergence" (1995). If you like to learn more, we advise you to
// read this book. His book focuses on three key aspects of trading: momentum, 
// direction and divergence. Blau, who was an electrical engineer before becoming 
// a trader, thoroughly examines the relationship between price and momentum in 
// step-by-step examples. From this grounding, he then looks at the deficiencies 
// in other oscillators and introduces some innovative techniques, including a 
// fresh twist on Stochastics. On directional issues, he analyzes the intricacies 
// of ADX and offers a unique approach to help define trending and non-trending periods.
//
// You can change long to short in the Input Settings
// Please, use it only for learning or paper trading. Do not for real trading.
////////////////////////////////////////////////////////////
strategy(title="Ergotic MDI (Mean Deviation Indicator) Backtest")
r = input(32, minval=1)
s = input(5, minval=1)
u = input(5, minval=1)
SmthLen = input(3, minval=1)
TradeReverse = input(false, title="Trade reverse")

price = close
ema_x = ema(price, r)
deviation_x = price - ema_x
ema_u = ema(deviation_x, s)
signal = ema(ema_u, u)

longCondition = crossover(signal, ema_u)
shortCondition = crossunder(signal, ema_u)

if (longCondition)
    strategy.entry("Long", strategy.long)

if (shortCondition)
    strategy.entry("Short", strategy.short)

if (TradeReverse)
    if (longCondition)
        strategy.close("Short")
    if (shortCondition)
        strategy.close("Long")
```

This Pine Script code implements the described strategy using the `ema` (Exponential Moving Average) function to calculate the `ema_x`, `ema_u`, and `signal` lines. The strategy generates long and short trading signals based on the crossovers and crossunders between the `signal` and `ema_u` lines. The `TradeReverse` input allows for toggling between long and short trades.