> Name

EMA-Oscillator-Trend-Following-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/8f0d3f4af156e3c55a.png)
[trans]


## Overview

This strategy uses the EMA indicator to identify stock price trends and combines standard deviation calculations to generate buy/sell signals, implementing a trend-following trading strategy. The main idea is to calculate the difference between the current price and EMA, setting thresholds for buying.

## Strategy Logic

The strategy first calculates the difference `v` between the close price and an EMA of length `ema_length`. Then it calculates the standard deviation `dev` of `v` over `ema_length` periods. Next, it determines the direction coefficient `k`, with `k = 1` indicating a buy on an uptrend and `k = -1` indicating a buy on a downtrend. The buy signal threshold `dev_limit` is calculated by multiplying `k` with `dev` and then with a limit factor. A buy signal is triggered when `v` crosses over `dev_limit`. The exit signal is generated when `v` re-crosses the zero axis.

The strategy provides two modes:

1. Buy on Downtrend, triggering a long position when `v` crosses below negative `dev_limit`, to follow a downtrend.
2. Buy on Uptrend, triggering a long position when `v` crosses above positive `dev_limit`, to follow an uptrend.

In summary, the strategy dynamically calculates the standard deviation of the difference between price and EMA to set thresholds for buying, with the factor controlling the sensitivity of buy signals. The `ema_length` parameter determines the EMA period, while the `buy_mode` controls the direction of the order.

## Advantage Analysis

The advantages of this strategy include:

1. Using EMA to identify trend directions effectively by smoothing prices.
2. Dynamically setting thresholds based on standard deviation adapts better than fixed thresholds.
3. Two buy modes allow following both uptrends and downtrends.
4. The factor provides flexibility in tuning the sensitivity of buy signals. `ema_length` allows optimizing the EMA period.
5. The logic is simple and easy to understand and modify.
6. Position sizing can be configured flexibly for aggressive trend following.

## Risk Analysis

The strategy also faces several risks:

1. EMA has lag, potentially missing trend turning points.
2. Relying on parameter optimization; improper settings may lead to oversensitivity or undersensitivity.
3. Trend following exposes significant risk if the trend reverses.
4. Frequent long/short switches can increase trading frequency.
5. Frequent signals in ranging markets can increase transaction costs.

To mitigate these risks, consider adding stop loss strategies, optimizing parameters, and implementing filters to avoid overtrading.

## Optimization Directions

The strategy can be optimized by:

1. Testing different EMA periods to find the optimal length.
2. Testing different factor values to determine the best sensitivity.
3. Optimizing position sizing strategies, such as pyramiding.
4. Adding filters to avoid wrong trades in choppy markets.
5. Incorporating stop loss mechanisms to control single trade losses.
6. Separately optimizing parameters for the two buy modes.
7. Researching trend reversal signals to stop trend following.

## Conclusion

This strategy identifies trends using EMA and generates dynamic threshold orders to follow trends. The logic is simple and clear, allowing flexible position sizing for aggressive trend chasing. However, it has risks that need addressing through parameter optimization and stop loss strategies. It serves as a good example of learning indicator combination and parameter tuning.

||

## Overview

This strategy uses the EMA indicator to identify price trends and combines standard deviation to calculate buy/sell signals for trend following trading. The main idea is to compute the difference between the close price and EMA, set a threshold to trigger orders.

## Strategy Logic

The strategy first calculates the difference `v` between the close price and an EMA of length `ema_length`. Then it calculates the standard deviation `dev` of `v` over `ema_length` periods. Next it determines the direction coefficient `k`, with `k=1` for long positions and `k=-1` for short positions. The buy signal threshold `dev_limit` is calculated by multiplying `k` with `dev` and then with a limit factor. When `v` crosses over `dev_limit`, a buy signal is triggered. The exit signal is when `v` re-crosses the zero axis.

The strategy provides two modes:

1. Buy short, go long when `v` crosses below negative `dev_limit`, to follow a downtrend.
2. Buy long, go long when `v` crosses above positive `dev_limit`, to follow an uptrend.

In summary, the strategy dynamically calculates the standard deviation of the difference between price and EMA to set thresholds for buying, with the factor controlling the sensitivity of buy signals. The `ema_length` parameter determines the EMA period, while the `buy_mode` controls the order direction.

## Advantage Analysis

The advantages of this strategy include:

1. Using EMA identifies trend directions well by smoothing prices.
2. Dynamic threshold based on standard deviation adapts better than fixed thresholds.
3. Two buy modes allow following uptrends or downtrends.
4. The factor provides flexibility in tuning buy sensitivity. `ema_length` allows optimizing the EMA period.
5. The logic is simple and easy to understand and modify.
6. Position sizing can be configured flexibly for aggressive trend following.

## Risk Analysis

The risks of the strategy include:

1. EMA has lag, potentially missing trend turning points.
2. Relying on parameter optimization; improper settings may lead to oversensitivity or undersensitivity.
3. Trend following exposes significant risk if the trend reverses.
4. Frequent long/short switches can increase trading frequency.
5. Frequent signals in ranging markets can increase transaction costs.

To address these risks, consider adding stop loss strategies, optimizing parameters, and implementing filters to avoid overtrading.

## Optimization Directions

The strategy can be optimized by:

1. Testing different EMA periods to find the optimal length.
2. Testing different factor values to determine the best sensitivity.
3. Optimizing position sizing strategies, such as pyramiding.
4. Adding filters to avoid wrong trades in choppy markets.
5. Incorporating stop loss mechanisms to control single trade losses.
6. Separately optimizing parameters for the two buy modes.
7. Researching trend reversal signals to stop trend following.

## Conclusion

The strategy identifies trends with EMA and generates dynamic threshold orders to follow trends. The logic is simple and clear, allowing flexible position sizing for aggressive trend chasing. However, it has risks that need addressing through parameter optimization and stop loss strategies. It serves as a good example of learning indicator combination and parameter tuning.

||

## Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|200|Period|
|v_input_float_1|1.7|Factor|
|v_input_string_1|0|Model: Buy on enter to OverSell|Buy on enter to OverBuy|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-10-06 00:00:00
end: 2023-11-05 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Azzrael

// Based on EMA and EMA Oscilator https://www.tradingview.com/script/qM9wm0PW-EMA-Oscilator-Azzrael/

// (EMA - close) + Std Dev + Factor = detecting oversell/overbuy
// Long only!
// Pyramiding - sometimes, depends on ...
// There 2 enter strategies in one script 
// 1 - Classic, buy on entering to OverSell zone (more profitable ~> 70%)
// 2 - Crazy, buy on entering to OverBuy zone (catching trend and pyramiding, more net profit)
// Exit - crossing zero of (EMA - close)

//@version=5
strategy("STR:EMA Oscilator [Azzrael]", overlay=false, 
 margin_long=100, 
 margin_short=100, 
 currency=currency.USD,
 default_qty_type=strategy.percent_of_equity,
 default_qty_value=30,
 pyramiding=3)

entry_name="Buy"

ema_length = input.int(200, "Period", minval=2, step=10)
limit = input.float(1.7, "Factor", minval=1, step=0.1, maxval=10)
dno = input.string(defva