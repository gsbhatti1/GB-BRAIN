> Name

Adaptive-Backtest-Date-Range-Selection-Strategy-Based-on-Double-MA

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1695c14f69ad1b346e5.png)
[trans]

## Overview

The core idea of this strategy is to implement a flexible framework for selecting the backtest date range, allowing users to automatically or manually set the start and end times for backtesting based on different needs.

The strategy provides four options for date range selection through input parameters: using all history data, recent specified days, recent specified weeks, or manually specifying a date range. Based on the selected range, the strategy dynamically sets the backtest window while keeping the trading logic unchanged. This allows comparison of performance differences under various time windows.

## Strategy Principle

The strategy consists of two modules: the backtest date range selection module and the double MA trading strategy module.

### Backtest Date Range Selection Module

1. Provides four options for date range selection: all history data (ALL), recent specified days (DAYS), recent specified weeks (WEEKS), or manually specifying a date range (MANUAL).
2. Dynamically sets the backtest start and end time based on timestamp conversion of the selected range.
3. Uses the time condition `window()` function to filter candles, performing only within the selected date range.

### Double MA Trading Strategy Module

1. The fast moving average (MA) period is set as `fastMA`, default 14; the slow MA period is set as `slowMA`, default 28.
2. Long position when the fast MA crosses above the slow MA; close position when the fast MA crosses below the slow MA.
3. Plots the fast and slow MA curves.

## Analysis of Advantages

1. Flexibly selects different backtest date ranges without limitation, meeting various experimental needs.
2. Tests the effects of different period parameters within the same time frame with comparable results.
3. Easy to modify trading logic for use as a framework for other strategies.
4. The double MA strategy is simple and easy to understand, making it suitable for beginners.

## Analysis of Risks and Solutions

1. The double MA strategy can be rough and may involve frequent trading issues. Consider adding stop-loss mechanisms for optimization.
2. Manually setting the date range requires caution to avoid errors; display warning messages if necessary.
3. Long history backtesting increases testing duration; consider adding slippage or fees to reduce frequent trades.

## Directions for Strategy Optimization

1. Add stop-loss logic to lower the risk of loss.
2. Filter stocks with a stock pool by selecting highly index-related stocks, enhancing stability.
3. Add filters to remove unstable signals within certain periods to reduce unnecessary trades.
4. Test performances of different indexed stocks to find the best varieties.

## Conclusion

As a flexible and customizable framework for date range selection, this strategy can meet various testing needs of users. Combined with simple yet effective double MA trading logic, it can quickly verify and compare strategies. Follow-up optimizations like adding filters or stop-loss logic can make the strategy more practical for live trading. Overall, the strategy framework has good scalability and reference value.

||

## Overview

The core idea of this strategy is to implement a flexible framework that allows users to select different backtest date ranges based on their needs, enabling automatic or manual setting of the start and end times for backtesting.

The strategy provides four options for date range selection through input parameters: using all historical data, recent specified days, recent specified weeks, or manually specifying a date range. Based on the selected date range, the strategy dynamically sets the backtest window while keeping the trading logic unchanged. This allows comparison of performance differences under different time windows.

## Strategy Principle

The strategy consists of two modules: the backtest date range selection module and the double MA trading strategy module.

### Backtest Date Range Selection Module

1. Provides four options for date range selection: all historical data (ALL), recent specified days (DAYS), recent specified weeks (WEEKS), or manually specifying a date range (MANUAL).
2. Dynamically sets the backtest start and end time based on timestamp conversion of the selected range.
3. Uses the `window()` function to filter candles, performing only within the selected date range.

### Double MA Trading Strategy Module

1. The fast moving average (MA) period is set as `fastMA`, default 14; the slow MA period is set as `slowMA`, default 28.
2. Long position when the fast MA crosses above the slow MA; close position when the fast MA crosses below the slow MA.
3. Plots the fast and slow MA curves.

## Analysis of Advantages

1. Flexibly selects different backtest date ranges without limitation, meeting various experimental needs.
2. Tests the effects of different period parameters within the same time frame with comparable results.
3. Easy to modify trading logic for use as a framework for other strategies.
4. The double MA strategy is simple and easy to understand, making it suitable for beginners.

## Analysis of Risks and Solutions

1. The double MA strategy can be crude and may involve frequent trading issues. Consider adding stop-loss mechanisms for optimization.
2. Manually setting the date range requires caution to avoid errors; display warning messages if necessary.
3. Long history backtesting increases testing duration; consider adding slippage or fees to reduce frequent trades.

## Directions for Strategy Optimization

1. Add stop-loss logic to lower the risk of loss.
2. Filter stocks with a stock pool by selecting highly index-related stocks, enhancing stability.
3. Add filters to remove unstable signals within certain periods to reduce unnecessary trades.
4. Test performances of different indexed stocks to find the best varieties.

## Conclusion

As a flexible and customizable framework for date range selection, this strategy can meet various testing needs of users. Combined with simple yet effective double MA trading logic, it can quickly verify and compare strategies. Follow-up optimizations like adding filters or stop-loss logic can make the strategy more practical for live trading. Overall, the strategy framework has good scalability and reference value.

||

## Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|FastMA|
|v_input_2|28|SlowMA|
|v_input_3|0|Date Range: WEEKS, DAYS, ALL, MANUAL|
|v_input_4|52|# Days or Weeks|
|v_input_5|9|From Month|
|v_input_6|15|From Day|
|v_input_7|2019|From Year|
|v_input_8|12|To Month|
|v_input_9|31|To Day|
|v_input_10|9999|To Year|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-12-29 00:00:00
end: 2024-01-04 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4

strategy(title = "How To Auto Set Date Range", shorttitle = " ", overlay = true)

// Revision:        1
// Author:          @allanster 

// === INPUT MA ===
fastMA = input(defval = 14, title = "FastMA", type = input.integer, minval = 1, step = 1)
slowMA = input(defval = 28, title = "SlowMA", type = input.integer, minval = 1, step = 1)

// === INPUT BACKTEST RANGE ===
useRange     = input(defval = "WEEKS", title = "Date Range", type = input.string, confirm = false, options = ["ALL", "DAYS", "WEEKS", "MANUAL"])
nDaysOrWeeks = input(defval = 52, title = "# Days or Weeks", type = input.integer, minval = 1)
FromMonth    = input(defval = 9, title = "From Month", minval = 1, maxval = 12)
FromDay      = input(defval = 15, title = "From Day", minval = 1, maxval = 31)
FromYear     = input(defval = 2019, title = "From Year", minval = 2014)
ToMonth      = input(defval = 12, title = "To Month", minval = 1, maxval = 12)
ToDay        = input(defval = 31, title = "To Day", minval = 1, maxval = 31)
ToYear       = input(defval = 9999, title = "To Year", minval = 2014)

// === FUNCTION EXAMPLE ===
window() => true

/