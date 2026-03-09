``` pinescript
/*backtest
start: 2024-04-02 00:00:00
end: 2024-07-12 00:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy('TrendSync Pro (SMC)', overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=1)

// Created by Shubham Singh

// Inputs
bool show_trendlines = input.bool(true, "Show Trendlines", group="Visual Settings")
int trend_period = input(20, 'Trend Period', group="Strategy Settings")
string htf = input.timeframe("60", "Higher Timeframe", group="Strategy Settings")

// Risk Management
float sl_percent = input.float(1.0, "Stop Loss (%)", minval=0.1, maxval=10, step=0.1, group="Risk Management")
float tp_percent = input.float(2.0, "Take Profit (%)", minval=0.1, maxval=10, step=0.1, group="Risk Management")

// Created by Shubham Singh

// Trendline Detection
var line trendline = na
var float trend_value = na
var bool trend_direction_up = false  // Initialize with default value

pivot_high = ta.pivothigh(high, trend_period, trend_period)
pivot_low = ta.pivotlow(low, trend_period, trend_period)

if (barstate.islast)
    if (not na(trendline))
        line.delete(trendline)
    
    if not na(pivot_high) and not na(pivot_low)
        // Determine trend direction
        trend_direction_up := close > trend_value[1] ? true : false
        
        // Update trend value based on the latest pivot point
        if (trend_direction_up)
            trend_value := pivot_high
        else
            trend_value := pivot_low

    // Plot trendline
    if not na(trend_value) and show_trendlines
        line.new(x1=bar_index, y1=trend_value, x2=bar_index + 10 * (trend_direction_up ? htf : -htf), y2=trend_value, color=color.blue)

// Entry Logic
if (not na(trend_value))
    if trend_direction_up and close > trend_value
        strategy.entry("Long", strategy.long)
    
    if not trend_direction_up and close < trend_value
        strategy.entry("Short", strategy.short)

// Risk Management Implementation
var float entry_price = na
if (strategy.opentrades != 0)
    entry_price := strategy.opentrades.entry_price(strategy.opentrades-1, 0)

if (not na(entry_price))
    // Set Stop Loss and Take Profit
    strategy.exit("Profit Target", from_entry="Long", limit=entry_price * (1 + tp_percent / 100), stop=entry_price - sl_percent / 100)
    strategy.exit("Profit Target", from_entry="Short", limit=entry_price * (1 - tp_percent / 100), stop=entry_price + sl_percent / 100)

// Optional Dynamic Stop Loss Using ATR
atr_value = ta.atr(14)
dynamic_sl := entry_price - atr_value * (sl_percent / 100)
strategy.exit("Dynamic SL", from_entry="Long", stop=dynamic_sl)
strategy.exit("Dynamic SL", from_entry="Short", stop=dynamic_sl)

// End of Pine Script
```