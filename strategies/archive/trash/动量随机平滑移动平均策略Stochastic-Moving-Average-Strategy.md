> Name

Stochastic-Moving-Average-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/17ad863810e29fd427a.png)
[trans]
## Overview

This strategy combines Exponential Moving Average (EMA) with Stochastic Oscillator in a trend following and continuation manner, along with some cool functionalities. I designed this strategy especially for trading altcoins, but it works just as good on Bitcoin itself and some Forex pairs.

## Strategy Logic

The strategy has 4 mandatory conditions to unlock a trading signal. Find these conditions for a long trade below (works the exact other way round for shorts):

- Fast EMA must be higher than Slow EMA
- Stochastic K% line must be in overbought territory
- Stochastic K% line must cross over Stochastic D% line
- Price as to close between slow EMA and fast EMA

Once all the conditions are true, a trade will start at the opening of the next candle.

## Advantage Analysis

The strategy combines the advantages of EMA and Stochastic to effectively capture the start and continuation of trends, suitable for medium and long term operations. At the same time, the strategy provides many customizable parameters for users to adjust based on their trading style and market characteristics.

Specifically, the advantages of the strategy include:

1. EMA crossings judge trend direction and enhance signal stability and reliability
2. Stochastic judges overbought and oversold levels to find reversal opportunities
3. Combining two indicators, it has both trend following and mean reversion
4. ATR automatically calculates stop loss distance, adjusting stops based on market volatility
5. Customizable risk reward ratio to meet needs of different users
6. Provides multiple customizable parameters for users to adjust based on markets

## Risk Analysis

The main risks of this strategy come from:

1. EMA crossings may have false breaks, thus generating incorrect signals
2. Stochastic itself has lagging properties, may miss best timing for price reversals
3. A single strategy cannot fully adapt to constantly changing market environments

To mitigate above risks, we can take following measures:

1. Adjust EMA period parameters to avoid too many false signals
2. Incorporate more indicators to judge trends and support levels to ensure reliable signals
3. Define clear money management strategies to control risk exposure per trade
4. Adopt combinational strategies so different strategies can verify signals and improve stability

## Optimization Directions

The strategy can be further optimized in following aspects:

1. Add volatility based position adjustment module. Reduce size when volatility surges and increase when calms down.
2. Add judgement of higher timeframe trends to avoid counter trend operations, e.g. combining daily or weekly trends.
3. Add machine learning models to aid signal generation. Train classification models based on historical data.
4. Optimize money management modules to make stops and sizes more intelligent.

## Conclusion

This strategy integrates the pros of both trend following and mean reversion, considering both higher timeframe market environments and current price behaviors. It is an effective strategy worth real time tracking and testing. Through continuous optimization on parameters, adding trend judgement modules etc, there is still large room for performance improvement, worth pouring in more research efforts.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_bool_1|true|(?     Trade Setup)Long Trades|
|v_input_bool_2|true|Short Trades|
|v_input_float_1|true|Risk : Reward|
|v_input_bool_3|false|Risk = % Equity    |
|v_input_float_2|true|riskPrctEqui|
|v_input_bool_4|false|Risk = $ Amount   |
|v_input_float_3|1000|riskUSD|
|v_input_float_4|true|(?     Stop Loss)ATR Multiplier|
|v_input_int_1|14|ATR Lookback|
|v_input_int_2|14|(?     Stochastic)K%|
|v_input_int_3|3| D%|
|v_input_int_4|80|OB|
|v_input_int_5|20| OS|
|v_input_int_6|false|Stoch. OB/OS lookback|
|v_input_bool_5|false|All must be OB/OS|
|v_input_color_1|#00ffff|   |
|v_input_color_2|#333333|  |
|v_input_int_7|50|   |
|v_input_int_8|21|(?     Exp. Moving Average)Fast EMA     |
|v_input_int_9|50|Slow EMA     |
|v_input_color_3|#0066ff|     |
|v_input_color_4|#0000ff|     |
|v_input_bool_6|false|(?     Reference Market)Reference Market Filter|
|v_input_1|BTC_USDT:swap|Market|
|v_input_timeframe_1|30|Timeframe|
|v_input_int_10|50|EMA Length|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-18 00:00:00
end: 2023-12-18 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © L
```