> Name

Ichimoku-Kinko-Hyo Trend Tracking Strategy Ichimoku-Kinko-Hyo-indicator-Balancing-Trend-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/17f6295720b6450caf5.png)
[trans]

## Overview

The Ichimoku Kinko Hyo balancing trend strategy is a trend-following strategy that utilizes the Ichimoku Kinko Hyo indicator. It identifies trend directions by combining multiple indicators, going long in a bull market and short in a bear market to achieve long-term capital appreciation.

## Strategy Principle

This strategy primarily relies on the Ichimoku Kinko Hyo indicator, which consists of the Tenkan-Sen (Conversion Line), Kijun-Sen (Base Line), Senkou Span A (Leading Span A), Senkou Span B (Leading Span B), and Chikou Span (Lagging Span). When price is above the cloud, it indicates a bullish trend. When price is below the cloud, it indicates a bearish trend.

Trading signals are generated based on the combination of the following conditions:

1. Tenkan-Sen crosses above Kijun-Sen as a bullish signal
2. Tenkan-Sen crosses below Kijun-Sen as a bearish signal
3. Chikou Span crossover upward as a bullish confirmation  
4. Chikou Span crossover downward as a bearish confirmation
5. RSI above 50 as a bullish indicator 
6. RSI below 50 as a bearish indicator
7. Price above the cloud indicates an upward trend  
8. Price below the cloud indicates a downward trend

It goes long when all bullish conditions are met and goes short when all bearish conditions are met.

## Advantage Analysis

This strategy combines trend following with overbought/oversold indicators, effectively identifying trend directions. The main advantages are:

1. Ichimoku Kinko Hyo can identify medium- to long-term trends, avoiding being misled by short-term market noises.
2. Incorporating RSI helps determine overbought and oversold zones, preventing missing reversal opportunities.
3. Only acts when volatility is high enough, avoiding ineffective trades.
4. Strict entry and exit rules maximize risk mitigation.

## Risk Analysis

Some risks to note for this strategy include:

1. Ichimoku Kinko Hyo has a lagging effect, possibly delaying entry timing.
2. Low frequency of trade signal occurrence with multiple condition combination, leading to insufficient number of trades.
3. No consideration around position sizing and risk management, risking over-trading.

Corresponding solutions are:

1. Shorten Ichimoku parameters to improve sensitivity.
2. Reduce strictness of entry conditions to increase trade frequency.
3. Incorporate risk management and position sizing modules to control per trade risk exposure and overall position size.

## Optimization Directions

The strategy can be improved in the following aspects:

1. Add or combine additional indicators like KDJ, MACD to diversify signal sources.
2. Optimize Ichimoku parameters to improve sensitivity.
3. Add stop loss mechanisms to lock in profits and control risks.
4. Incorporate dynamic position sizing module based on account size.
5. Add hedging modules to manage risks for long positions.

## Summary

Overall, the Balancing Trend strategy is a reliable and robust trend-following system. It addresses the key challenge in trend trading – balancing trend identification accuracy and trade generation frequency. There is still room for improvement through parameter tuning and module expansion, making it a strategy that can be applied for the long run.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|22|Tenkan-Sen Bars|
|v_input_2|60|Kijun-Sen Bars|
|v_input_3|120|Senkou Span B Bars|
|v_input_4|30|Chikou-Span Offset|
|v_input_5|30|Senkou Span Offset|
|v_input_6|true|Long Entry|
|v_input_7|true|Short Entry|
|v_input_8|2|VolLength|
|v_input_9|0.2|Volatility Target|
|v_input_10|true|From Day|
|v_input_11|true|From Month|
|v_input_12|2019|From Year|
|v_input_13|31|To Day|
|v_input_14|12|To Month|
|v_input_15|2020|To Year|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-16 00:00:00
end: 2023-11-20 08:00:00
period: 3m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Ichimoku Kinko Hyo: ETH 3h Strategy by tobuno", overlay=true)

// Inputs
ts_bars = input(22, minval=1, title="Tenkan-Sen Bars")
ks_bars = input(60, minval=1, title="Kijun-Sen Bars")
ssb_bars = input(120, minval=1, title="Senkou Span B Bars")
cs_offset = input(30, minval=1, title="Chikou-Span Offset")
ss_offset = input(30, minval=1, title="Senkou Span Offset")
long_entry = input(true, title="Long Entry")
short_entry = input(true, title="Short Entry")

// Volatility
vollength = input(defval=2, title="VolLength")
voltarget = input(defval=0.2, type=float, step=0.1, title="Volatility Target")
```