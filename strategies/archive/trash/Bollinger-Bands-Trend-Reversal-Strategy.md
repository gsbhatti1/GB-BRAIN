> Name

Bollinger-Bands-Trend-Reversal-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/179b736ae9513263b9a.png)

## Overview

This strategy utilizes Bollinger Bands and Moving Average to go LONG or SHORT when price approaches the upper or lower bands. It goes short when price breaks above the upper band and goes long when price breaks below the lower band. The strategy combines the advantages of both trend following and mean reversion strategies, performing well during range-bound markets.

## Logic

The strategy identifies two entry signals:

1. Long signal: When close price hits the lower band while being above EMA line, previous candle was bearish, and current candle is bullish.
2. Short signal: When close price hits the upper band while being below EMA line, previous candle was bullish, and current candle is bearish.

The stop loss uses a fixed stop loss. The stop loss level is set at the entry price plus/minus the risk/reward ratio times the distance between the entry price and the take profit level.

The take profit uses dynamic take profit. Long take profit is set at the lower band. Short take profit is set at the upper band.

## Advantages

1. Combines the strengths of both trend following and mean reversion strategies, performs well during range-bound markets.
2. Utilizes Bollinger Bands to identify overbought and oversold levels, improving accuracy of reversal signals.
3. Fixed stop loss facilitates risk management.
4. Dynamic take profit allows maximization of profits.

## Risks

1. Breakout strategies are susceptible to stop runs. Need to beware of false breakouts.
2. Frequent stop loss triggers when the market is too choppy.
3. Fixed stop loss is not adaptive to market volatility, can be too wide or too tight.
4. Poor parameter tuning of Bollinger Bands can lead to mediocre results.

## Enhancement

1. Incorporate RSI indicator to filter entry signals. For example, only go long if RSI is above 50, and only go short if RSI is below 50. This avoids bad signals.
2. Implement adaptive stop loss that adjusts the stop distance based on volatility. E.g., use ATR to set dynamic stop loss.
3. Optimize Bollinger Bands parameters to find the best parameter combinations.
4. Test different EMA periods to enhance the EMA's support/resistance effect.

## Summary

The strategy combines trend and reversal, entering overbought/oversold levels identified by Bollinger Bands. It maximizes profits through dynamic take profit. Performs well during range-bound markets. Be wary of stop runs. Fine tune parameters to optimize performance. Overall a practical and effective strategy.

||


## Overview

This strategy utilizes Bollinger Bands and Moving Average to go LONG or SHORT when price approaches the upper or lower bands. It goes short when price breaks above the upper band and goes long when price breaks below the lower band. The strategy combines the advantages of both trend following and mean reversion strategies, performing well during range-bound markets.

## Logic

The strategy identifies two entry signals:

1. Long signal: When close price hits the lower band while being above EMA line, previous candle was bearish, and current candle is bullish.
2. Short signal: When close price hits the upper band while being below EMA line, previous candle was bullish, and current candle is bearish.

The stop loss uses a fixed stop loss. The stop loss level is set at the entry price plus/minus the risk/reward ratio times the distance between the entry price and the take profit level.

The take profit uses dynamic take profit. Long take profit is set at the lower band. Short take profit is set at the upper band.

## Advantages

1. Combines the strengths of both trend following and mean reversion strategies, performs well during range-bound markets.
2. Utilizes Bollinger Bands to identify overbought and oversold levels, improving accuracy of reversal signals.
3. Fixed stop loss facilitates risk management.
4. Dynamic take profit allows maximization of profits.

## Risks

1. Breakout strategies are susceptible to stop runs. Need to beware of false breakouts.
2. Frequent stop loss triggers when the market is too choppy.
3. Fixed stop loss is not adaptive to market volatility, can be too wide or too tight.
4. Poor parameter tuning of Bollinger Bands can lead to mediocre results.

## Enhancement

1. Incorporate RSI indicator to filter entry signals. For example, only go long if RSI is above 50, and only go short if RSI is below 50. This avoids bad signals.
2. Implement adaptive stop loss that adjusts the stop distance based on volatility. E.g., use ATR to set dynamic stop loss.
3. Optimize Bollinger Bands parameters to find the best parameter combinations.
4. Test different EMA periods to enhance the EMA's support/resistance effect.

## Summary

The strategy combines trend and reversal, entering overbought/oversold levels identified by Bollinger Bands. It maximizes profits through dynamic take profit. Performs well during range-bound markets. Be wary of stop runs. Fine tune parameters to optimize performance. Overall a practical and effective strategy.

||


## Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|20|length|
|v_input_2_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_3|2|StdDev|
|v_input_4|200|EMA Input|
|v_input_5|1.5|Risk/Reward Ratio|
|v_input_6|false|Offset|


## Source (PineScript)

```pinescript
//@version=4

// Welcome to yet another script. This script was a lot easier since I was stuck for so long on the Donchian Channels one and learned so much from that one that I could use in this one
// This code should be a lot cleaner compared to the Donchian Channels, but we'll leave that up to the pro's
// This strategy has two entry signals, long = when price hits lower band, while above EMA, previous candle was bearish and current candle is bullish
// Short = when price hits upper band, while below EMA, previous candle was bullish and current candle is bearish
// Take profits are the opposite side's band(lower band for long signals, upper band for short signals). This means our take profit price will change per bar
// Our stop loss doesn't change, it's the difference between entry price and the take profit target divided by the input risk reward
// At the time of writing this, I could probably calculate that much easier by simply multiplying the opposite band by the input risk reward ratio
// Since I want to get this script out and working on the next one, I won't clean that up, I'm sorry
strategy(shorttitle="BB Trending Reverse Strategy", title="Bollinger Bands Trending Reverse Strategy", overlay=true, default_qty_type = strategy.cash, default_qty_value = 150, initial_capital = 1000, currency = currency.USD, commission_type = "percent", commission_value = 0.036)

// The built-in Bollinger Band indicator inputs and variables, added some inputs of my own and organized the code
length              = input(20, minval=1)
src                 = input(close, title="Source")
mult                = input(2.0, minval=0.001, maxval=50, title="StdDev")
emaInput            = input(title = "EMA Input", type = input.integer, defval = 200, minval = 10, maxval = 400, step = 1)
riskreward          = input(title = "Risk/Reward Ratio", type = input.float, defval = 1.50, minval = 0.01, maxval = 100, step = 0.01)
offset              = input(false, title="Offset")
```