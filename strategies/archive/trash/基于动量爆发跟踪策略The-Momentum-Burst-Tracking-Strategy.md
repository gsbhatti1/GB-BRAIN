> Name

The-Momentum-Burst-Tracking-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/bc35fb08918caf075f.png)
[trans]

## Overview

The Momentum Burst Tracking strategy identifies price breakthroughs through the percentage change in price, combined with trading volume to filter signals, aiming to capture high-probability trend breakthrough points. Once a buy signal is triggered, the strategy uses a price tracking stop loss to lock in profits and prevent excessive drawdowns.

## Strategy Principle

The main indicators used by this strategy to determine entry signals are:

1. Percentage Price Change (isFourPercentBull) - Calculate the percentage change of the closing price relative to the previous day's closing price to determine if the price has effectively broken through.
2. Ratio of Closing Price to Highest Price (HighCloseRatio) - Calculate the ratio of the closing price to the highest price to determine the strength of the price breakthrough.
3. Trading Volume (volume) - Require trading volume to be greater than the previous day to ensure a valid breakthrough.
4. 200-Day Simple Moving Average (SMA) - Require the closing price and opening price to be higher than the 200-day line to determine the trend direction.

When all of these multiple conditions are satisfied simultaneously, a buy signal is issued. Afterward, the strategy uses a price tracking stop loss to actively manage risk and lock in profits. Specifically, the calculation formula for the trailing stop loss line is:

```
trailPrice = close * (100 - trailPercent) / 100
```

Where `trailPercent` is the configurable trailing stop loss percentage. This ensures that as long as prices rise, the stop loss line will also rise to lock in profits. When prices fall back to the stop loss line, close positions to stop losses.

## Strategy Advantages

This is a typical breakout strategy with the following advantages:

1. Multi-condition filtering to ensure the validity of the breakout and avoid false breakouts.
2. Using price tracking stop loss can actively manage risk and lock in profits, minimizing drawdowns.
3. The strategy logic is simple and clear, making it easy to understand and optimize.

## Strategy Risks

The strategy also has some risks:

1. There is still a probability of failed breakouts that cannot be completely avoided, leading to potential losses.
2. Overly aggressive trailing stop loss settings may result in frequent stop losses.
3. Improper parameter settings may lead to excessive trading frequency or signal misses.

The solutions to these risks are:

1. Optimize parameters to reduce stop loss magnitude, ensuring sufficient room.
2. Relax the breakout conditions appropriately to ensure clear trends are not missed.
3. Test the strategy on different assets to assess its stability.

## Optimization Directions

Given the high frequency of stop losses in this strategy, the following directions can be further optimized:

1. Try other trailing stop loss methods, such as moving average tracking, ATR, and volatility tracking.
2. Introduce machine learning algorithms to train better-performing parameter combinations based on historical data.
3. Add auxiliary judgment conditions based on volume breakouts to ensure effectiveness.
4. Evaluate differences in parameter settings across different assets to find the best fit.

## Conclusion

The Momentum Burst Tracking Strategy is a very practical trend tracking strategy overall. It solves the problem of ineffective stop loss and profit taking in breakout strategies while still effectively controlling risk when capturing trends. With the potential for further improvement through optimization and machine learning, it is worth in-depth research and application.

||

## Overview

The Momentum Burst Tracking strategy judges price breakthroughs by calculating percentage price changes and filters signals with trading volume to implement high-probability capturing of trend breakthrough points. After triggering a buy signal, this strategy uses price tracking stop loss to lock in profits and avoid excessive drawdowns.

## Strategy Principle

The main indicators this strategy uses to determine entry signals are:

1. Percentage price change (isFourPercentBull) - Calculate the percentage change of the closing price relative to the previous day's closing price to determine if the price has effectively broken through.
2. Ratio of closing price to highest price (HighCloseRatio) - Calculate the ratio of the closing price to the highest price to determine the strength of the price breakthrough.
3. Trading volume (volume) - Require the trading volume to be greater than the previous day to ensure a valid breakthrough.
4. 200-day simple moving average (SMA) - Require the closing price and opening price to be higher than the 200-day line to determine the trend direction.

When the above multiple conditions are met at the same time, a buy signal is issued. Afterwards, the strategy uses price tracking stop loss to actively manage risk and lock in profits. Specifically, the calculation formula for the trailing stop loss line is:

```
trailPrice = close * (100 - trailPercent) / 100
```

Where `trailPercent` is the configurable trailing stop loss percentage. This ensures that as long as prices rise, the stop loss line will also rise to lock in profits. When prices fall back to the stop loss line, close positions to stop losses.

## Advantages of the Strategy

As a typical breakout strategy, it has the following advantages:

1. Multi-condition filtering ensures the validity of the breakout and avoids false breakouts.
2. Using price tracking stop loss can actively manage risk and lock in profits, minimizing drawdowns.
3. The strategy logic is simple and clear, making it easy to understand and optimize.

## Risks of the Strategy

The strategy also has some risks:

1. There is still a probability of failed breakouts that cannot be completely avoided, leading to potential losses.
2. Overly aggressive trailing stop loss settings may result in frequent stop losses.
3. Improper parameter settings may lead to excessive trading frequency or signal misses.

The solutions to the corresponding risks are:

1. Optimize parameters to reduce stop loss magnitude, ensuring sufficient room.
2. Reasonably relax the breakout conditions to ensure clear trends are not missed.
3. Test the strategy on different assets to assess its stability.

## Optimization Directions

Considering the high frequency of stop losses in this strategy, the following directions can be further optimized:

1. Try other trailing stop loss methods, such as moving average tracking, ATR, and volatility tracking.
2. Introduce machine learning algorithms to train better-performing parameter combinations based on historical data.
3. Add auxiliary judgment conditions based on volume breakouts to ensure effectiveness.
4. Evaluate differences in parameter settings across different assets to find the best fit.

## Conclusion

The Momentum Burst Tracking Strategy is a very practical trend tracking strategy overall. It solves the problem of ineffective stop loss and profit taking in breakout strategies while still effectively controlling risk when capturing trends. With the potential for further improvement through optimization and machine learning, it is worth in-depth research and application.

||

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_bool_1|false|IncludeAvgVolume?|
|v_input_1|50|VolumeLength|
|v_input_float_1|3|Trail%|
|v_input_float_2|3.8|BreakoutPercent|
|v_input_float_3|10|Max Breakout|
|v_input_float_4|70|Close to High Ratio|
|v_input_bool_3|false|Plot MA?|
|v_input_bool_2|true|(?Strategy)Custom Date Range?|
|v_input_2|timestamp(1 Jan 2019 00:00)|FromDate|
|v_input_3|timestamp(31 Dec 2023 00:00)|ToDate|
|v_input_string_1|0|Select Position Size: Contract|Percent of Equity|
|v_input_int_1|true|No of Contract|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-03-01 00:00:00
end: 2023-12-10 05:20:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © doks23

//@version=5
strategy(title = "SD:Momentum Burst", overlay=true, initial_capital=1000,commission_value = 0,sl
