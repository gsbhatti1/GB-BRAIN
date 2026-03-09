> Name

RSI Dual-track Breakthrough Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/f16e56291360ffee5b.png)
[trans]

## Overview

This strategy is named "RSI Dual-track Breakthrough Strategy." It utilizes the dual tracks of the RSI indicator for judgment to achieve the goal of buy low and sell high. When the RSI indicator falls below the set lower track (default 40), it is considered as a buy signal. At this time, if RSI10 is less than RSI14, it further confirms the buy; when the RSI indicator rises above the set upper track (default 70), it is considered as a sell signal. At this time, if RSI10 is greater than RSI14, it further confirms the sell. The strategy also sets mechanisms of moving stop loss and take profit.

## Strategy Principle

The core logic of this strategy is to use the dual tracks of the RSI indicator for judgment. The RSI indicator is generally set to 14 periods, representing the strength and weakness of the stock in recent 14 days. This strategy adds RSI10 as an auxiliary judgment indicator.

When the RSI14 breaks below the 40 track, it is believed that the stock price has broken through the weak side and there may be a chance of support rebound. At this time, if RSI10 is less than RSI14, it means that the short-term trend is still downward, which can further confirm the sell signal. So when "RSI14 <= 40 and RSI10 < RSI14" is met, a buy signal is generated.

When RSI14 breaks above the 70 track, it is believed that the stock price has entered a short-term strong area and there may be a chance for a pullback adjustment. At this time, if RSI10 is greater than RSI14, it means the short-term trend continues upward, which can further confirm the buy signal. So when "RSI14 >= 70 and RSI10 > RSI14" is met, a sell signal is generated.

Thus, the combination judgment of RSI14 and RSI10 constitutes the core logic of the dual-track strategy.

## Advantages of the Strategy

1. The combination judgment of dual RSI indicators can capture trading signals more accurately.
2. The adoption of moving stop loss mechanism can cut losses timely and control maximum drawdown.
3. The setting of take profit exit mechanism allows exiting when reaching the target profit, avoiding profiteering retracement.

## Risks of the Strategy

1. RSI indicator is prone to generate false signals and losses cannot be completely avoided.
2. If stop loss point is set too close it may be taken out soon; if set too big it's hard to control risks.
3. In abnormal market conditions like gap, it may also lead to losses.

To fully utilize this strategy, RSI parameters can be adjusted properly, stop loss position should be strictly controlled, avoid over-frequent operations, and pursue steady profitability.

## Directions of Strategy Optimization

1. Consider incorporating other indicators for combination validation, such as KDJ, MACD, etc.
2. Set RSI parameters respectively based on the characteristics of different products.
3. Set dynamic stop loss based on indicators like ATR to adjust stop position timely.
4. Optimize RSI parameters automatically through machine learning techniques.

## Summary

This strategy makes judgment based on the dual-track idea of RSI and filters out some noisy signals to some extent. But no single indicator strategies can be perfect, RSI indicator is prone to mislead and should be viewed cautiously. This strategy incorporates moving stop loss and take profit mechanisms to control risks, which is essential. Future optimizations could be continued to make strategy parameters and stop loss methods more intelligent and dynamic.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|timestamp(01 Jan 2015 13:30 +0000)|Backtest Start Time|
|v_input_2|false|Exit when Risk:Reward met|
|v_input_3|3|Risk:[Reward] (i.e. 3) for exit|
|v_input_4|true|Use trailing stop loss|
|v_input_5|2|ATR multiplier for stop loss|
|v_input_6|40|RSI entry|
|v_input_7|70|RSI exit|

> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-31 00:00:00
end: 2024-01-07 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © DojiEmoji

//@version=4
strategy("[KL] RSI 14 + 10 Strategy", overlay=true)

backtest_timeframe_start = input(defval = timestamp("01 Jan 2015 13:30 +0000"), title="Backtest Start Time", type=input.time)
// backtest_timeframe_end = input(defval=timestamp("19 Mar 2021 19:30 +0000"), title="Backtest End Time", type=input.time)
TARGET_PROFIT_MODE = input(false, title="Exit when Risk:Reward met")
REWARD_RATIO = input(3, title="Risk:[Reward] (i.e. 3) for exit")

// Trailing stop loss
```