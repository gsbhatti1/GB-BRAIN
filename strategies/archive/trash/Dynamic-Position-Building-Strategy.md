> Name

Dynamic-Position-Building-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/11f92c69a06139fb365.png)
[trans]

## Overview

The main idea of this strategy is to dynamically build a position based on system signals in a bull market to control risks and obtain a lower average entry price.

## Strategy Logic

The strategy first sets the starting capital and DCA configuration percentage. At the close of each bar, it calculates an adjusted percentage based on the price change. If the price rises, it lowers the percentage; if the price falls, it increases the percentage. This allows increasing the position at lower prices. It then calculates order size based on the adjusted percentage and remaining capital. On every bar close, it places orders to build the position until the starting capital is used up.

Thus, it can control risks and get a lower average entry price during fluctuating price action. Meanwhile, it tracks the average entry price and median price to judge the current entry situation.

## Advantage Analysis

The strategy has the following advantages:

1. It can dynamically scale in the position, increasing allocation on dips and decreasing allocation on rallies to control risks.
2. It gets a lower average entry price compared to the median price, allowing more profit potential.
3. It fits ranging bull markets with volatility for better risk-reward ratios.
4. It enables presetting starting capital and DCA percentage to control position sizing risk.
5. It provides statistics on average entry price and median price for clear judgment of the entry quality.

## Risk Analysis

There are also some risks:

1. In plunging markets, it will keep adding to the position, leading to heavy losses. A stop loss can restrict the risk.
2. If the price surges rapidly, the scaling in will diminish, possibly missing much of the rally. Other LSI signals are then needed.
3. Improper parameter configuration also poses dangers. Excessive starting capital and high DCA percentage will magnify losses.

## Optimization Directions

Some ways to optimize the strategy:

1. Add stop loss logic to cease scaling in on heavy selloffs.
2. Dynamically adapt DCA percentage based on volatility or other metrics.
3. Incorporate machine learning models to forecast prices and guide scaling decisions.
4. Combine other indicators to identify market structure shifts for scaling exit points.
5. Add capital management rules to dynamically size orders based on account values.

## Conclusion

This is a very practical dynamic position scaling strategy. It flexibly adjusts the position size based on price fluctuations to achieve good average entries in bull markets, while restricting risk via configurable parameters. Combining it with other indicators or models can further improve its performance. It suits investors seeking long-term gains.

||

## Overview

The main idea of this strategy is to dynamically build a position based on system signals in a bull market to control risks and obtain a lower average entry price.

## Strategy Logic

The strategy first sets the starting capital and DCA configuration percentage. At the close of each bar, it calculates an adjusted percentage based on the price change. If the price rises, it lowers the percentage; if the price falls, it increases the percentage. This allows increasing the position at lower prices. It then calculates order size based on the adjusted percentage and remaining capital. On every bar close, it places orders to build the position until the starting capital is used up.

Thus, it can control risks and get a lower average entry price during fluctuating price action. Meanwhile, it tracks the average entry price and median price to judge the current entry situation.

## Advantage Analysis

The strategy has the following advantages:

1. It can dynamically scale in the position, increasing allocation on dips and decreasing allocation on rallies to control risks.
2. It gets a lower average entry price compared to the median price, allowing more profit potential.
3. It fits ranging bull markets with volatility for better risk-reward ratios.
4. It enables presetting starting capital and DCA percentage to control position sizing risk.
5. It provides statistics on average entry price and median price for clear judgment of the entry quality.

## Risk Analysis

There are also some risks:

1. In plunging markets, it will keep adding to the position, leading to heavy losses. A stop loss can restrict the risk.
2. If the price surges rapidly, the scaling in will diminish, possibly missing much of the rally. Other LSI signals are then needed.
3. Improper parameter configuration also poses dangers. Excessive starting capital and high DCA percentage will magnify losses.

## Optimization Directions

Some ways to optimize the strategy:

1. Add stop loss logic to cease scaling in on heavy selloffs.
2. Dynamically adapt DCA percentage based on volatility or other metrics.
3. Incorporate machine learning models to forecast prices and guide scaling decisions.
4. Combine other indicators to identify market structure shifts for scaling exit points.
5. Add capital management rules to dynamically size orders based on account values.

## Conclusion

This is a very practical dynamic position scaling strategy. It flexibly adjusts the position size based on price fluctuations to achieve good average entries in bull markets, while restricting risk via configurable parameters. Combining it with other indicators or models can further improve its performance. It suits investors seeking long-term gains.

||

## Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_float_1|5000|Starting Capital|
|v_input_int_1|10|DCA Allocation Percentage|
|v_input_1|timestamp(1 Jan 2024)|(?Backtest Time Period)Start Date|
|v_input_string_1|0|(?Table Design)Table size: Normal|Small|Tiny|Large|


> Source (PineScript)

```pinescript
/*backtest
start: 2024-01-20 00:00:00
end: 2024-02-19 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/22_0/
// © RWCS_LTD

//@version=5
strategy("DCA IN Calculator {RWCS}", overlay=true, pyramiding=999, default_qty_type=strategy.cash, initial_capital=10000, commission_value=0.02)

// User inputs
backtestStartDate = input(timestamp("1 Jan 2024"), 
     title="Start Date", group="Backtest Time Period",
     tooltip="This start date is in the time zone of the exchange " + 
     "where the chart's instrument trades. It doesn't use the time " + 
     "zone of the chart or of your computer.")
start_date = true
starting_capital = input.float(defval=5000, title="Starting Capital")
dca_allocation_percentage = input.int(defval=10, title="DCA Allocation Percentage")

// Calculate DCA allocation based on price change
price_change_percentage = ((close - close[1]) / close[1]) * 100
adjusted_allocation_percentage = close > close[1] ? dca_allocation_percentage - price_change_percentage : dca_allocation_percentage + price_change_percentage // If price action is negative, increase allocations
adjusted_allocation_percentage1 = dca_allocation_percentage - price_change_percentage // If price action is positive, reduce allocations

// Calculate order size based on adjusted allocation percentage
order_size = (adjusted_allocation_percentage / 100) * starting_capital

// Track remaining capital
var remaining_capital = starting_capital

// Long on the close of every bar
if true
    // Ensure the order size doesn't exceed 
```