``` pinescript
/*backtest
start: 2024-04-04 00:00:00
end: 2024-04-11 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © AHMEDABDELAZIZZIZO

//@version=5

strategy("Volume-based Dynamic DCA Strategy", overlay=true)

// Parameters
swing_points = input(3, title="Swing Points")
median_drop_mult = input.float(1.1, title="Median drop Mult")
floating_loss = input(-5, title="Floating Loss")
total_orders = input(5, title="Number of all orders")
rel_vol_len = input(20, title="Length of relative volume")
volume_multiplier = input(2, title="Volume Multiplier")
take_profit_mult = input(true, title="Take Profit Multiplier")

// Function to identify support level
support_level = ta.pivotlow(high, low, close)

// Calculate historical price drop percentages and median
price_drops = na
for i = 1 to swing_points
    if support_level[i] != na and support_level[i+1] != na
        drop_percent = (support_level[i] - support_level[i+1]) / support_level[i] * 100
        price_drops := [price_drops, drop_percent]
median_drop = ta.median(price_drops)

// Calculate safe distance and take-profit price
safe_distance = median_drop * median_drop_mult

// Position-building logic
long_price = na
for i = 1 to total_orders
    if support_level[i] != na and close > support_level[i] and volume[i] > volume_multiplier * volume[i-1]
        long_price := close
        break

// Dynamic position size adjustment based on floating loss
position_size = 0
if long_price != na
    for i = 1 to total_orders
        if long_price < close
            position_size += (close - long_price) / safe_distance * take_profit_mult

// Plot support level and positions
plot(support_level, color=color.blue, linewidth=2)
plot(position_size > 0 ? long_price : na, style=plot.style_circles, color=color.green, title="Long Price")

// Take-profit logic
if position_size > 0
    take_profit_price = long_price + safe_distance * take_profit_mult
    strategy.entry("Buy", strategy.long, comment="Take Profit Entry")
    strategy.exit("Take Profit Exit", from_entry="Buy", limit=take_profit_price)

// Risk management
if position_size < 0 and close > take_profit_price
    strategy.close("Buy")

```

This Pine Script implements the described Volume-based Dynamic DCA Strategy. It dynamically adjusts the position size based on the floating loss during price decline, and sets the take-profit price according to historical data.