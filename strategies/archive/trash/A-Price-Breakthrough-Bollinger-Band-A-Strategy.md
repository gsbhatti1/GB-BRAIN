> Name

Price-Breakthrough-Bollinger-Band-A-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/13a6183a5ed0ad738b1.png)
[trans]
## Overview

This strategy uses the Bollinger Band indicator to judge the amplitude of price fluctuations, combined with K-line patterns for price breakthrough operations. The upper and lower rails of the Bollinger Band can roughly judge the upward and downward trends of prices. Combining it with K-line pattern indicators can find out relatively obvious buy and sell timing. The strategy mainly judges the breakthrough below the Bollinger Band to go long, the breakthrough above the rail to go short, while combining the Stoch indicator to judge the overbought and oversold status, and uses K-line patterns to provide alternative buy and sell signals.

## Strategy Principle

The strategy consists of the following main indicators:

1. **Bollinger Band Indicator**: Including Bollinger middle rail, upper rail, and lower rail. Bollinger Bands calculate the fluctuation range of prices through the standard deviation of prices, thereby judging the fluctuation trend of prices.
2. **Stoch Indicator**: To judge whether the stock is in an overbought or oversold status. K lines and D lines can judge whether to break up and break down.
3. **K-line Patterns**: Judge some common patterns like big Yang line, big Yin line etc as alternative trading opportunities.

Buy Condition: Price crosses above Bollinger lower rail, Stoch indicator shows oversold status (K<20, D<20), fast moving average crosses above slow moving average.

Sell Condition: Price crosses below Bollinger upper rail, or stop loss when profitable.

The strategy combines both trend analysis and overbought/oversold judgment, which reduces the rate of false signals, and allows timely market entry when a trend emerges. But it also carries the risk of being trapped, and needs timely stop losses.

## Advantage Analysis

1. Combining Bollinger Band and Stoch indicator, it can buy at obvious low points, reducing risk.
2. K-line patterns serve as auxiliary conditions, avoiding wrong buys in range-bound markets.
3. Adopting double condition judgements enhances the stability and reliability of the strategy.
4. The stop loss mechanism avoids huge losses.

## Risk Analysis

1. Trading with Bollinger Bands is prone to being trapped. Price discontinuities may cause relatively large losses.
2. The Stoch indicator has a high probability of issuing false signals. Using Stoch alone carries large loss risks.
3. It is easy to generate wrong trading signals in range-bound markets.
4. Need timely stop losses to control risks.
5. Need to pay attention to the strength of breakthroughs to avoid pullback after surging high.

## Optimization Directions

1. Optimize stock pool, select stocks with large fluctuations and obvious trends.
2. Optimize Bollinger parameters, adjust middle rail cycle, optimize grasp of buy/sell points.
3. Optimize Stoch parameters, adjust K line and D line cycles, improve indicator reliability.
4. Add trading volume condition judgments to avoid pullback after surging high.
5. Add stop loss strategies like trailing stop loss, moving stop loss etc to control loss risks.
6. Evaluate adding other technical indicators like MACD, KDJ etc to improve strategy stability.
7. Test different holding periods to optimize profit and drawdown ratio.

## Summary

The strategy integrates Bollinger Band, Stoch indicator with technical fundamentals indicators. Under the premise of controlling risks, it buys at price lows and sells near historical highs, realizing a relatively stable profit model. But it also carries risks like being trapped, ineffective stop loss etc. Further enhancing stability and profitability can be achieved by optimizing parameters and adding other judgment indicators. The strategy suits investors who trade when prices oscillate around overbought and oversold zones.

||


## Overview

This strategy uses the Bollinger Band indicator to judge the amplitude of price fluctuations, combined with K-line patterns for price breakthrough operations. The upper and lower rails of the Bollinger Band can roughly judge the upward and downward trends of prices. Combining it with K-line pattern indicators can find out relatively obvious buy and sell timing. The strategy mainly judges the breakthrough below the Bollinger Band to go long, the breakthrough above the rail to go short, while combining the Stoch indicator to judge the overbought and oversold status, and uses K-line patterns to provide alternative buy and sell signals.

## Strategy Principle

The strategy consists of the following main indicators:

1. **Bollinger Band Indicator**: Including Bollinger middle rail, upper rail, and lower rail.
2. **Stoch Indicator**: To judge whether the stock is in an overbought or oversold status.
3. **K-line Patterns**: Judge some common patterns like big Yang line, big Yin line etc as alternative trading opportunities.

Buy Condition: Price crosses above Bollinger lower rail, Stoch indicator shows oversold status (K<20, D<20), fast moving average crosses above slow moving average.

Sell Condition: Price crosses below Bollinger upper rail, or stop loss when profitable.

The strategy combines both trend analysis and overbought/oversold judgment, which reduces the rate of false signals, and allows timely market entry when a trend emerges. But it also carries the risk of being trapped, and needs timely stop losses.

## Advantage Analysis

1. Combining Bollinger Band and Stoch indicator, it can buy at obvious low points, reducing risk.
2. K-line patterns serve as auxiliary conditions, avoiding wrong buys in range-bound market.
3. Adopting double condition judgements enhances the stability and reliability of the strategy.
4. The stop loss mechanism avoids huge losses.

## Risk Analysis

1. Trading with Bollinger Bands is prone to being trapped. Price discontinuities may cause relatively large losses.
2. The Stoch indicator has a high probability of issuing false signals. Using Stoch alone carries large loss risks.
3. It is easy to generate wrong trading signals in range-bound markets.
4. Need timely stop losses to control risks.
5. Need to pay attention to the strength of breakthroughs to avoid pullback after surging high.

## Optimization Directions

1. Optimize stock pool, select stocks with large fluctuations and obvious trends.
2. Optimize Bollinger parameters, adjust middle rail cycle, optimize grasp of buy/sell points.
3. Optimize Stoch parameters, adjust K line and D line cycles, improve indicator reliability.
4. Add trading volume condition judgments to avoid pullback after surging high.
5. Add stop loss strategies like trailing stop loss, moving stop loss etc to control loss risks.
6. Evaluate adding other technical indicators like MACD, KDJ etc to improve strategy stability.
7. Test different holding periods to optimize profit and drawdown ratio.

## Summary

The strategy integrates Bollinger Band, Stoch indicator with technical fundamentals indicators. Under the premise of controlling risks, it buys at price lows and sells near historical highs, realizing a relatively stable profit model. But it also carries risks like being trapped, ineffective stop loss etc. Further enhancing stability and profitability can be achieved by optimizing parameters and adding other judgment indicators. The strategy suits investors who trade when prices oscillate around overbought and oversold zones.

||

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|47|Simple Moving Average Period|
|v_input_2|7|Exponential Moving Average Period|
|v_input_3|14|Slow Exponential Moving Average Period|
|v_input_4|21|Length|
|v_input_5_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_6|1.5|Mult|
|v_input_7|11|RSI Length|
|v_input_8|7|Stoch Length|
|v_input_9|3|Smooth K|
|v_input_10|4|Smooth D|
|v_input_11|20|OverSold|
|v_input_12|80|OverBought|
|v_input_13|5|Trend in Bars|
|v_input_14|0.05|Doji Size|
|v_input_15|10|Maximum Bollinger Band Height|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-10-29 00:00:00
end: 2023-11-03 18:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("Bollinger e Tendência", overlay=true)
```

Note: The PineScript code was not provided in the original text, so it has been added with a basic structure that matches the strategy description.