``` pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-24 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
//hk4jerry

strategy("Adaptive Grid Trading Strategy", overlay=false, pyramiding=3000, close_entries_rule="ANY", default_qty_type=strategy.cash, initial_capital=v_input_8, currency="USD", commission_type=strategy.commission.percent, commission_value=0.025)
i_autoBounds    = input(group="Grid Bounds", title="Use Auto Bounds?", defval=v_input_1, type=input.bool)                             // calculate upper and lower bound of the grid automatically? This will theoretically be less profitable, but will certainly require less attention
i_boundSrc      = input(group="Grid Bounds", title="(Auto) Bound Source", defval=v_input_2, options=["Hi & Low", "Average"])     // should bounds of the auto grid be calculated from recent High & Low, or from a Simple Moving Average
i_boundLookback = input(group="Grid Bounds", title="(Auto) Bound Lookback", defval=v_input_3, type=input.integer, maxval=500, minval=0) // when calculating auto grid bounds, how far back should we look for a High & Low, or what should the length be of our sma
i_boundDev      = input(group="Grid Bounds", title="(Auto) Bound Deviation", defval=v_input_4, type=input.float, maxval=1, minval=-1)  // if sourcing auto bounds from High & Low, this percentage will (positive) widen or (negative) narrow the bound limits. If sourcing from Average, this is the deviation
i_upperBound    = input(group="Grid Bounds", title="(Manual) Upper Boundry", defval=v_input_5, type=input.float)
i_lowerBound    = input(group="Grid Bounds", title="(Manual) Lower Boundry", defval=v_input_6, type=input.float)
i_gridQuantity  = input(group="Grid Lines", title="Grid Line Quantity", defval=v_input_7, type=input.integer, maxval=5000, minval=1)
i_startTime     = input(title="Start Time", type=input.time, defval=v_input_9)
i_endTime       = input(title="End Time", type=input.time, defval=v_input_10)

// Strategy Parameters
var float gridSpacing = na

if (i_autoBounds)
    // Auto Bound Calculation
    var high = security(tickerid, "D", ta.highest(high, i_boundLookback))
    var low  = security(tickerid, "D", ta.lowest(low, i_boundLookback))
    upperBound := i_boundSrc == "Hi & Low" ? (low * (1 + i_boundDev)) : (high * (1 - i_boundDev))
    lowerBound := i_boundSrc == "Hi & Low" ? (high * (1 - i_boundDev)) : (low * (1 + i_boundDev))
else
    upperBound := i_upperBound
    lowerBound := i_lowerBound

gridSpacing := (upperBound - lowerBound) / i_gridQuantity

// Grid Trading Logic
for j = 1 to i_gridQuantity
    var float gridPrice = na
    if (j == 1)
        gridPrice := lowerBound + gridSpacing * (j - 1)
    else
        gridPrice := lowerBound + gridSpacing * (j - 1)

    // Place Buy Order
    buyOrderID := strategy.opentrades.entry_id(strategy.opentrades.id(0))
    if (gridPrice < close and not strategy.position_size > 0)
        strategy.entry("Buy " + tostring(gridPrice), strategy.long, when=bar_index == buyOrderID - 1)

    // Place Sell Order
    sellOrderID := strategy.opentrades.entry_id(strategy.opentrades.id(2999))
    if (gridPrice > close and not strategy.position_size < 0)
        strategy.entry("Sell " + tostring(gridPrice), strategy.short, when=bar_index == sellOrderID - 1)

// Strategy Performance
plotchar(series=strategy.net_pnl, title="Net PnL", location=location.belowbar, color=color.green, style=shape.labelup, size=size.small)
```

This script implements the adaptive grid trading strategy with the given parameters and descriptions.