```markdown
Name

Buying-Strategy-Based-on-Historical-High-Breakout

Author

ChaoZhang

Strategy Description

[trans]


## Overview

This strategy is designed for bull markets. When the stock price breaks through the historical n-day high, a buy order is placed and a stop-loss mechanism using EMA moving average is activated. This is a trend-following strategy.

## Strategy Principle

1. Calculate the highest price in the past n days as the historical high price.
2. Buy when the current closing price exceeds the historical high price.
3. Use the x-day EMA to set the stop-loss level and exit when the price falls below the EMA.
4. The values of n and x are adjusted via parameters, with default settings of 200 days for the highest price and 90 days for the EMA.
5. The strategy logic is simple, clear, and easy to implement.

## Advantage Analysis

1. Automatically tracks trends formed by new high breakthroughs.
2. Uses EMA moving average for trailing stop-loss to lock in profits.
3. No need to predict stock prices; just follow buy signals.
4. Default parameters work well during bull market conditions.
5. The code is concise and easy to understand and modify.

## Risk Analysis

1. Significant losses can occur at the end of a bull market.
2. Improper stop-loss settings may result in premature or delayed exits.
3. Cannot predict the strength or extent of new high breakthroughs and subsequent corrections.
4. Strongly biased towards bull markets, making it unsuitable for other conditions.
5. Parameter optimization risks overfitting to historical data.

## Optimization Direction

1. Test different parameter combinations to find optimal settings.
2. Evaluate alternative stop-loss methods such as fixed ratio stops.
3. Optimize stop-loss parameters to balance frequency and risk control.
4. Add additional filters to avoid buying on noise signals.
5. Study methods for assessing the strength of buy opportunities.
6. Consider implementing profit-taking exits to lock in gains.

## Summary

This strategy implements automatic trend tracking by identifying new high breakthroughs and uses EMA moving averages to manage stop-losses. While it is effective in certain scenarios, it remains relatively simple and needs further expansion and optimization to be applicable across all market conditions.

||


## Overview

This strategy buys when the stock price breaks above the historical n-day high during a bull market, with an EMA-based stop loss. It falls under trend-following strategies.

## Strategy Logic

1. Calculate the highest price over the past n days as the historical high price.
2. Buy when the current closing price exceeds the historical high price.
3. Use x-day EMA as the stop-loss mechanism and exit when the price drops below it.
4. Values of n and x can be adjusted via parameters, defaulting to 200 days for the highest price and 90 days for the EMA.
5. The logic is simple, clear, and easy to implement.

## Advantages

1. Automatically follows trends formed by new highs.
2. EMA trailing stop-loss locks in most profits.
3. No need to predict prices; just follow buy signals.
4. Default parameters work well during bull markets.
5. Concise code that is easy to understand and modify.

## Risks

1. Significant losses are possible at the end of a bull market.
2. Improper stop-loss settings may result in premature or delayed exits.
3. Cannot predict the strength and extent of new high breakthroughs and subsequent corrections.
4. Strong bias towards bull markets, making it unsuitable for other conditions.
5. Parameter optimization risks overfitting to historical data.

## Enhancement

1. Test different parameter combinations for optimal values.
2. Evaluate alternative stop-loss methods such as fixed percentage stops.
3. Optimize stop-loss parameters to balance frequency and risk control.
4. Add filters to avoid buying on noise signals.
5. Research ways to gauge the strength of buy signals.
6. Implement profit-taking exits to lock in gains.

## Conclusion

This strategy automates trend following based on new high breakthroughs using EMA trailing stops. While it is effective in some cases, it needs further expansion and optimization to become robust across all market conditions.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|200|ATH period|
|v_input_int_2|90|ema line|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-08-20 00:00:00
end: 2023-09-19 00:00:00
Period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © gmhfund

//@version=5
strategy("ATH 200d",overlay=1)
plot(close)

bars = input.int(200, "ATH period", minval=5, maxval=2000, step=1)
range_ema = input.int(90,"ema line",minval=100,maxval=400,step=1)

ath_price = ta.highest(bars)[1]
plot(ath_price,color=color.blue)

line_ema = ta.ema(close,range_ema)
exit_condition = ta.crossunder(close,line_ema)
plot(line_ema,color=color.orange)


strategy.entry("Buy", strategy.long, 1, when = close > ath_price) // enter long by market if current open great then previous high
//strategy.close("Buy",when = close < strategy.position_avg_price*0.9 )
strategy.close("Buy",when = exit_condition )
```

> Detail

https://www.fmz.com/strategy/427388

> Last Modified

2023-09-20 15:53:26
```