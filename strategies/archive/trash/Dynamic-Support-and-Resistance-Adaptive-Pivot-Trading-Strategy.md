``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2025-01-08 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © felipemiransan

//@version=6
strategy("Dynamic Support and Resistance Pivot Strategy", overlay=true)

// Strategy parameters
pivot_length = input.int(2, title="Pivot Length", tooltip="Pivot size to identify peaks and troughs")
support_resistance_distance = input.float(0.4, title="Support/Resistance Distance %", tooltip="Distance to consider a support or resistance level in %")

// Stop Loss and Take Profit parameters
stop_loss_pct = input.float(10.0, title="Stop Loss %", tooltip="Stop loss percentage", minval=0.1) / 100
take_profit_pct = input.float(26.0, title="Take Profit %", tooltip="Take profit percentage", minval=0.1) / 100

// Functions to identify high and low pivots
pivot_high = ta.pivothigh(high, pivot_length, pivot_length)
pivot_low = ta.pivotlow(low, pivot_length, pivot_length)

// Storing support and resistance levels
var float resistance_level = na
var float support_level = na
var float last_pivot_high = na
var float last_pivot_low = na

// Updating support and resistance based on pivots
if (not na(pivot_high))
    resistance_level := high[pivot_length]
    last_pivot_high := high[pivot_length]

if (not na(pivot_low))
    support_level := low[pivot_length]
    last_pivot_low := low[pivot_length]

// Function to check if the current price is near a support or resistance level
is_near_resistance = (not na(resistance_level)) and (close >= resistance_level * 
```

It seems that the Pine Script was cut off. The script continues as follows:

``` pinescript
1.0 - support_resistance_distance) / 100

// Function to check if the current price is near a support level
is_near_support = (not na(support_level)) and (close <= support_level * 
1.0 + support_resistance_distance) / 100

// Long signal generation
long_entry = ta.crossover(close, pivot_low)
if (long_entry)
    strategy.entry("Long", strategy.long)

// Short signal generation
short_entry = ta.crossunder(close, pivot_high)
if (short_entry)
    strategy.entry("Short", strategy.short)

// Set stop loss and take profit
strategy.exit("Exit Long", "Long", stop=close * (1 - stop_loss_pct), limit=close * (1 + take_profit_pct))
strategy.exit("Exit Short", "Short", stop=close * (1 + stop_loss_pct), limit=close * (1 - take_profit_pct))

// Plot support and resistance levels
plot(resistance_level, color=color.red, title="Resistance Level")
plot(support_level, color=color.green, title="Support Level")

// Additional indicators for visualization (optional)
plotchar(is_near_resistance or is_near_support, char='▲', location=location.belowbar, color=color.blue, size=size.tiny)
```