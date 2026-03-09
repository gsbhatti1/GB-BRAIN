> Name

Low-Scanner-Smart-Tracking-Method

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/14f33a8d7100195e3f4.png)

[trans]

## Overview

The Low Scanner Smart Tracking Method is a non-repainting Forex trading strategy. It uses a low scanner to locate low points and combines with Hull Moving Average for trade signal judgment, which can achieve a high winning rate.

## Principle Analysis 

Firstly, the strategy uses a low scanner to locate low points. The low scanner calculates the RSI values of price and volume, and compares them with the WMA curve to determine low points when RSI is lower than WMA.

Secondly, the strategy uses Hull Moving Average for trade signal judgment. It calculates two Hull MAs with different periods, and goes long when the shorter period Hull MA crosses over the longer period one, and goes short when it crosses under.

Finally, the strategy combines the low point scan signals and Hull MA signals, and only triggers Hull MA signals when the low scanner gives out low point signals, forming the entry strategy.

In this way, by identifying market low points first and then tracking the trend, it can effectively avoid wrong entry timing and improve the winning rate of the trading system.

## Advantage Analysis  

The main advantages of the Low Scanner Smart Tracking Method are:

1. Using the low scanner, it can accurately identify market low points and avoid buying at high points.
2. Hull MA is an excellent trend tracking indicator that can capture larger trends.
3. Combining low scanner and Hull MA verifies each other and filters out lots of noise and false signals.
4. Adopting a progressive stop loss exit mechanism can maximize profits and avoid pullbacks.
5. The strategy uses indicator driven logic and does not manipulate historical data, which is reliable.

## Risk Analysis

The main risks of this strategy are:

1. The low scanner may miss some low points and lose trading opportunities. Parameters can be adjusted to expand the scanning range.
2. Markets may reverse sharply, causing stop loss to be hit. Stop loss range can be relaxed reasonably and control position sizing.
3. Improper parameter settings may generate too many or too few trading signals. Parameters should be repeatedly optimized to find the best combination.
4. This strategy only applies to Forex pairs with obvious trends, not suitable for range-bound or oscillating markets.

## Optimization Directions

The strategy can be optimized in the following aspects:

1. Optimize the parameters of the low scanner to identify low points more accurately.
2. Optimize the parameters of Hull MA to track trends more precisely.
3. Add other indicator filters like MACD, KDJ to improve signal reliability.
4. Add machine learning model predictions to assist trade signal judgment.
5. Optimize the stop loss mechanism to adjust dynamically based on market volatility.
6. Optimize the position sizing strategy to adjust position size dynamically based on money management rules.

## Conclusion

The Low Scanner Smart Tracking Method is a high winning rate non-repainting Forex trading strategy. It can accurately identify market low points and enter the trend when the trend is clear, locking in profits with progressive stop loss. The strategy has large room for optimization and can be improved in many ways to become a powerful automated trading system.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|0|Strategy Direction: long|short|all|
|v_input_2|1440|min|
|v_input_3|W|tf3|
|v_input_4|60|min1|
|v_input_5|0|Timeframe: W|5|15|30|60|120|240|360|720|D|1|
|v_input_6|24|Period|
|v_input_7|true|Shift|
|v_input_8|25|len|
|v_input_9|2016|BACKTEST START YEAR|
|v_input_10|6|BACKTEST START MONTH|
|v_input_11|true|BACKTEST START DAY|
|v_input_12|2500|BACKTEST STOP YEAR|
|v_input_13|12|BACKTEST STOP MONTH|
|v_input_14|31|BACKTEST STOP DAY|
|v_input_15|25| stop loss|
|v_input_16|25| qty_percent1|
|v_input_17|25| qty_percent2|
|v_input_18|25| qty_percent3|
|v_input_19|0.5| Take profit1|
|v_input_20|true| Take profit2|
|v_input_21|1.5| Take profit3|
|v_input_22|2| Take profit4|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-10-24 00:00:00
end: 2023-10-25 00:00:00
period: 3m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// © theCrypster 2020

//@version=4
// strategy(title = "Low Scanner Forex strategy", overlay = false, pyramiding=1,initial_capital = 1000, default_qty_type= strategy.percent_of_equity, default_qty_value = 100, calc_on_order_fills=false, slippage=0,commission_type=strategy.commission.percent,commission_value=0)
strat_dir_input = input(title="Strategy Direction", defval="long", options=["long", "short", "all"])
strat_dir_value