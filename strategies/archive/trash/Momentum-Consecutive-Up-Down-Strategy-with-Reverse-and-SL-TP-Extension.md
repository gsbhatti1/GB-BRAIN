> Name

Consecutive-Up-Down-Strategy-with-Reverse-and-SL-TP-Extension

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/fbc6cc394fa0f5770d.png)

[trans]

## Overview

This strategy is an extension of the built-in consecutive up/down bars strategy on TradingView. It has flexible direction settings that allow reverse trading. Additionally, it integrates various stop loss methods such as swing high/low points, ATR stop, and strategy stop, along with corresponding take profit settings. This makes the strategy better at risk management while maintaining the original trading signals.

## Strategy Logic

The strategy primarily uses consecutive up or down bars to generate buy and sell signals. Users can configure the number of consecutive up bars required for a buy signal and the number of consecutive down bars needed for a sell signal.

Additionally, reverse trade functionality is added. By enabling it, the original buy signals become sell signals, and vice versa, thus completing the trade reversal.

For entries and exits, direct position reversal is supported to reduce the time with no position.

In terms of stop loss and take profit, swing high/low points, ATR stop, and strategy stop are provided for choice. The stop loss method will combine with the position direction to select a swing low or high as an aggressive stop or use ATR to dynamically determine the stop price. Take profit settings are based on the entry price, setting a fixed distance.

If trailing stop is enabled, the strategy can increase the stop distance when losing and decrease it when profiting, achieving automatic trailing.

## Advantage Analysis

The biggest advantage of this strategy lies in its flexibility, allowing it to adapt to different market conditions:

1. Buy/sell filter parameters can be set for both trending and ranging markets.
2. Reverse trade allows direction selection as needed.
3. Direct position reversal reduces the time with no position.
4. Multiple stop loss methods are available; choose according to needs.
5. Trailing stop is enabled for automatic risk management.

## Risk Analysis

The main risks include too many consecutive bars potentially leading to missed trading opportunities and overly aggressive stop losses causing larger losses. Recommendations include:

1. Adjust the up/down bar quantity moderately, not too aggressively.
2. Test different stop loss methods and choose the most suitable one.
3. Use trailing stops cautiously to avoid excessive losses.

## Optimization Directions

There is room for further optimization:

1. Dynamically adjust up/down bars based on ATR or volatility.
2. Test stop loss/profit ratios under different holding periods.
3. Add open price filters to avoid false breakouts.
4. Integrate other indicators to improve signal quality.

## Conclusion

This strategy provides beneficial extensions to the base strategy, enhancing risk control and offering more flexible trading options. It is an effective momentum strategy that can be optimized and traded live easily.

||

## Overview

This strategy is an extension of the built-in consecutive up/down bars strategy on TradingView. It has flexible direction settings that allow reverse trading. Additionally, it integrates various stop loss methods such as swing high/low points, ATR stop, and strategy stop, along with corresponding take profit settings. This makes the strategy better at risk management while maintaining the original trading signals.

## Strategy Logic

The strategy primarily uses consecutive up or down bars to generate buy and sell signals. Users can configure the number of consecutive up bars required for a buy signal and the number of consecutive down bars needed for a sell signal.

Additionally, reverse trade functionality is added. By enabling it, the original buy signals become sell signals, and vice versa, thus completing the trade reversal.

For entries and exits, direct position reversal is supported to reduce the time with no position.

In terms of stop loss and take profit, swing high/low points, ATR stop, and strategy stop are provided for choice. The stop loss method will combine with the position direction to select a swing low or high as an aggressive stop or use ATR to dynamically determine the stop price. Take profit settings are based on the entry price, setting a fixed distance.

If trailing stop is enabled, the strategy can increase the stop distance when losing and decrease it when profiting, achieving automatic trailing.

## Advantage Analysis

The biggest advantage of this strategy lies in its flexibility, allowing it to adapt to different market conditions:

1. Buy/sell filter parameters can be set for both trending and ranging markets.
2. Reverse trade allows direction selection as needed.
3. Direct position reversal reduces the time with no position.
4. Multiple stop loss methods are available; choose according to needs.
5. Trailing stop is enabled for automatic risk management.

## Risk Analysis

The main risks include too many consecutive bars potentially leading to missed trading opportunities and overly aggressive stop losses causing larger losses. Recommendations include:

1. Adjust the up/down bar quantity moderately, not too aggressively.
2. Test different stop loss methods and choose the most suitable one.
3. Use trailing stops cautiously to avoid excessive losses.

## Optimization Directions

There is room for further optimization:

1. Dynamically adjust up/down bars based on ATR or volatility.
2. Test stop loss/profit ratios under different holding periods.
3. Add open price filters to avoid false breakouts.
4. Integrate other indicators to improve signal quality.

## Conclusion

This strategy provides beneficial extensions to the base strategy, enhancing risk control and offering more flexible trading options. It is an effective momentum strategy that can be optimized and traded live easily.

||

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|false|Strategy Direction|
|v_input_2|true|-----------------Strategy Inputs-------------------|
|v_input_3|3|consecutiveBarsUp|
|v_input_4|4|consecutiveBarsDown|
|v_input_5|true|-----------------General Inputs-------------------|
|v_input_6|true|Use Stop Loss and Take Profit|
|v_input_7|0|Type Of Stop: ATR Stop|Swing Lo/Hi|Strategy Stop|
|v_input_8|10|Swing Point Lookback|
|v_input_9|2|Swing Point SL Perc Increment|
|v_input_10|14|ATR Length|
|v_input_11|5|ATR Multiple|
|v_input_12|5|Take Profit Risk Reward Ratio|
|v_input_13|true|Trailing Stop|
|v_input_14|true|Allow Direct Position Reverse|
|v_input_15|false|Reverse Trades|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-01-07 00:00:00
end: 2023-08-30 05:20:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// Extension of the built-in strategy by TradingView. The strategy buys after an X amount of
// consecutive bullish bars and viceversa for selling. This logic can be reversed and a Stop Loss
// with Take Profit can be added. There's also an option to adapt the SL into a Trailing Stop.

//@version=4
strategy("Consecutive Up/Down Strategy with Reverse", 
     overlay=true, 
     default_qty_type=strategy.percent_of_equity, 
     default_qty_value=100, 
     initial_capital=10000, 
     commission_value=0.04, 
     calc_on_every_tick=false, 
     slippage=0)

direction = input(0, title = "Strategy Direction", type=input.integer, minval=-1, maxval=1)
strategy.risk.allow_entry_in(direction == 0 ? strategy.direction.all : (direction < 0 ? strategy.direction.short : strategy.direction.long))

/////////////////////// STRATEGY INPUTS ////////////////////////////////////////
title1=input(true, "-----------------Strategy Inputs-------------------")  

consecutiveBarsUp = input(3)
consecutiveBarsDown = input(4)

/////////////////////// BACKTESTER /////////////////////////////////////////////
title2=input(true, "-----------------General Inputs-------------------")  

// Backtester General Inputs
i_S