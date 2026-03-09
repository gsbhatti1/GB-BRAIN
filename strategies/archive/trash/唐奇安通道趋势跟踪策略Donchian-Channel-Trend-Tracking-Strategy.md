> Name

Donchian-Channel-Trend-Tracking-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/129926b3079bfce9a6f.png)
[trans]

## Overview

The Donchian Channel trend tracking strategy is a trend tracking strategy based on the Donchian Channel indicator. This strategy determines the trend direction by calculating the highest high and lowest low over different periods, forming upper, lower, and middle bands to achieve trend tracking trading.

## Strategy Logic

The strategy first sets the backtesting time range, and then defines the long and short entry rules.

For long positions, open long when the price breaks above the upper band of the Donchian Channel; close long when the price breaks below the lower band.

For short positions, open short when the price breaks below the lower band of the Donchian Channel; close short when the price breaks above the upper band.

The strategy also incorporates the ATR indicator to set the stop loss exit mechanism. The ATR value multiplied by a coefficient is used as the stop loss level.

Specifically, the long stop loss is the entry price minus the ATR stop loss value; the short stop loss is the entry price plus the ATR stop loss value.

The strategy also plots the upper and lower bands of the Donchian Channel and the ATR stop loss line to form a complete trading system.

## Advantages

- Use Donchian Channel to determine trend direction, with some trend tracking capability.
- The Donchian Channel smoother parameter is adjustable, allowing parameter optimization to find the best parameter combination.
- The stop loss mechanism with ATR can effectively control risks.
- The long and short trading rules are simple and easy to understand, suitable for beginners.
- The code structure is clear and easy to understand and modify.

## Risks

- The Donchian Channel may have some whipsaw trades during range-bound price fluctuations.
- Improper ATR stop loss range setting may cause too wide or too sensitive stop loss.
- Long and short positions could be too concentrated, requiring position sizing rules.
- The strategy needs to be tested for applicability on different products, with independent parameter optimization.
- Trading costs also need to be considered, parameters may need adjustment in high-cost environments.

## Enhancement Opportunities

- Optimize the period parameters of the Donchian Channel to find the best parameter combination.
- Try different ATR coefficients to find the optimal stop loss range.
- Try introducing trailing stop loss on top of the ATR stop loss to lock in profits.
- Adjust long/short position ratio based on market conditions.
- Test parameter robustness on different products to find generic parameters.
- Study incorporating MACD and other filters to improve stability.
- Test parameter adaptiveness under different trading cost environments.

## Summary

In summary, this is a relatively simple trend tracking strategy that centers on the application of the Donchian Channel. The advantage lies in its simplicity and ease of understanding, making it suitable for learning purposes, but parameters and risks still need further optimization. With diverse enhancement techniques, the strategy stability and profitability could potentially be improved.

||


## Overview

The Donchian Channel trend tracking strategy is a trend tracking strategy based on the Donchian Channel indicator. The strategy determines the trend direction by calculating the highest high and lowest low over different periods, forming upper, lower, and middle bands to achieve trend tracking trading.

## Strategy Logic

The strategy first sets the backtesting time range, and then defines the long and short entry rules.

For long positions, open long when the price breaks above the upper band of the Donchian Channel; close long when the price breaks below the lower band.

For short positions, open short when the price breaks below the lower band of the Donchian Channel; close short when the price breaks above the upper band.

The strategy also incorporates the ATR indicator to set the stop loss exit mechanism. The ATR value multiplied by a coefficient is used as the stop loss level.

Specifically, the long stop loss is the entry price minus the ATR stop loss value; the short stop loss is the entry price plus the ATR stop loss value.

The strategy also plots the upper and lower bands of the Donchian Channel and the ATR stop loss line to form a complete trading system.

## Advantages

- Use Donchian Channel to determine trend direction, with some trend tracking capability.
- The Donchian Channel smoother parameter is adjustable, allowing parameter optimization to find the best parameter combination.
- The stop loss mechanism with ATR can effectively control risks.
- The long and short trading rules are simple and easy to understand, suitable for beginners.
- The code structure is clear and easy to understand and modify.

## Risks

- The Donchian Channel may have some whipsaw trades during range-bound price fluctuations.
- Improper ATR stop loss range setting may cause too wide or too sensitive stop loss.
- Long and short positions could be too concentrated, requiring position sizing rules.
- The strategy needs to be tested for applicability on different products, with independent parameter optimization.
- Trading costs also need to be considered, parameters may need adjustment in high-cost environments.

## Enhancement Opportunities

- Optimize the period parameters of the Donchian Channel to find the best parameter combination.
- Try different ATR coefficients to find the optimal stop loss range.
- Try introducing trailing stop loss on top of the ATR stop loss to lock in profits.
- Adjust long/short position ratio based on market conditions.
- Test parameter robustness on different products to find generic parameters.
- Study incorporating MACD and other filters to improve stability.
- Test parameter adaptiveness under different trading cost environments.

## Summary

In summary, this is a relatively simple trend tracking strategy that centers on the application of the Donchian Channel. The advantage lies in its simplicity and ease of understanding, making it suitable for learning purposes, but parameters and risks still need further optimization. With diverse enhancement techniques, the strategy stability and profitability could potentially be improved.

||


## Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|v_input_1|true|From Day|
|v_input_2|true|From Month|
|v_input_3|2017|From Year|
|v_input_4|true|To Day|
|v_input_5|true|To Month|
|v_input_6|9999|To Year|
|v_input_7|true|Can Enter Long Position|
|v_input_8|false|Can Enter Short Position|
|v_input_9|true|Show Donchian Long Channels|
|v_input_10|false|Show Donchian Short Channels|
|v_input_11|false|Enable ATR Stop Rule|
|v_input_12|20|longUpperLength|
|v_input_13|10|longLowerLength|
|v_input_14|10|shortUpperLength|
|v_input_15|20|shortLowerLength|

> Source (PineScript)

``` pinescript
/*backtest
start: 2022-10-30 00:00:00
end: 2023-11-05 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © kriswaters

//@version=4
strategy("Donchian Channels Strategy by KrisWaters", overlay=true ) 

// Date filter
FromDay   = input(defval = 1, title = "From Day", minval = 1, maxval = 31)
FromMonth = input(defval = 1, title = "From Month", minval = 1, maxval = 12)
FromYear  = input(defval = 2017, title = "From Year", minval = 1900)
ToDay     = input(defval = 1, title = "To Day", minval = 1, maxval = 31)
ToMonth   = input(defval = 1, title = "To Month", minval = 1, maxval = 12)
ToYear    = input(defval = 9999, title = "To Year", minval = 2017)

start     = timestamp(FromYear, FromMonth, FromDay, 00, 00)  // backtest start window
finish    = timestamp(ToYear, ToMonth, ToDay, 23, 59)        // backtest finish window
window()  => true // create