> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|30|Moving Average Period|
|v_input_2|true|Use RSI Filter|
|v_input_3|true|Use ATR Filter|
|v_input_4|true|Exclude May|
|v_input_5|timestamp(2009-01-01 00:00:00)|Start Backtest|
|v_input_6|timestamp(2025-01-01 00:00:00)|End Backtest|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-03-01 00:00:00
end: 2024-03-31 23:59:59
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © muikol  

//@version=5
strategy("Turnaround Tuesday", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=100, commission_type=strategy.commission.percent, commission_value=0.035)

// Inputs for MA period, filter_1, filter_2, month filter, and testing period
ma_period = input(30, title="Moving Average Period")
use_filter_1 = input(true, title="Use RSI Filter")
use_filter_2 = input(true, title="Use ATR Filter")
use_month_filter = input(true, title="Exclude May")
start_date = input(defval=timestamp("2009-01-01 00:00:00"), title="Start Backtest")
end_date = input(defval=timestamp("2025-01-01 00:00:00"), title="End Backtest")

// Define the filter conditions
var float rsi = na
var float atr = na

if (use_filter_1 and use_filter_2 and not na(close) and not na(open) and not na(close[1]))  // Ensure all necessary data is available
    rsi := rsi(close, 3)
    atr := atr(10, close)
    
// Check if the current month is May
is_may = month(timenow) == 5

// Buy condition
buy_condition = close < ta.sma(close, ma_period) and rsi < 51 and close / atr < 0.95 and not is_may

// Sell condition
sell_condition = bar_index % 3 == 2  // Sell on Wednesday

// Apply filters and execute trades
if (start_date <= time <= end_date and use_filter_1 and use_filter_2 and use_month_filter)
    if (buy_condition)
        strategy.entry("Buy", strategy.long)
    if (sell_condition)
        strategy.close("Buy")
```

This Pine Script code defines the "Turnaround Tuesday Strategy (Weekend Filter)" as described in the strategy document. The script includes input parameters for the moving average period, RSI filter, ATR filter, and month filter, as well as the start and end dates for backtesting. The strategy logic is implemented to buy on Monday if the conditions are met and sell on Wednesday.