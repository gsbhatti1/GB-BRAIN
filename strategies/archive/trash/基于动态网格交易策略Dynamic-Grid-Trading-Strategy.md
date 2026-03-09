> Name

Dynamic-Grid-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1a9ad639454b87242d4.png)
 [trans]

### Overview

This strategy implements grid trading by placing multiple parallel buy and sell orders within a price range. It adjusts the grid range and lines based on market fluctuations to profit.

### Strategy Logic

1. Set upper and lower bounds of the grid, which can be manually configured or automatically calculated based on recent high and low prices.
2. Calculate grid interval width according to specified number of grid lines.
3. Generate grid line prices array with corresponding quantity.
4. When price drops below a grid line, open long order below it; when price rises above a grid line, close short order above it.
5. Dynamically adjust bounds, interval width and grid line prices to adapt the strategy to market changes.

### Advantage Analysis

1. Can steadily profit in range-bound and volatile markets, regardless of trend direction.
2. Supports both manual and automatic parameter settings for strong adaptability.
3. Optimizable parameters like grid quantity, interval width, and order size for better rewards.
4. Embedded position control for lower risk.
5. Dynamic grid range adjustment enhances adaptability.

### Risk Analysis

1. Severe loss may occur in strong trending markets.
2. Improper grid quantity and position settings may amplify risk.
3. Auto-calculated grid ranges may fail in extreme price swings.

Risk Management:
1. Optimize grid parameters and strictly control total positions.
2. Close the strategy before significant price movements.
3. Judge market conditions with trend indicators, and close the strategy when necessary.

### Optimization Directions

1. Choose optimal grid quantity based on market characteristics and capital scale.
2. Test different time periods to optimize auto-calculated parameters.
3. Optimize order size calculation for more stable returns.
4. Add indicators for trend identification and set up strategy closure conditions.

### Summary

The dynamic grid trading strategy adapts to the market by adjusting grid parameters, enabling steady profits in range-bound and volatile markets. With proper position control, risk is mitigated. Optimizing grid settings and incorporating trend judgment indicators can further improve the stability of the strategy.

||

### Overview

This strategy implements grid trading by placing multiple parallel buy and sell orders within a price range. It adjusts the grid range and lines based on market fluctuations to profit.

### Strategy Logic

1. Set upper and lower bounds of the grid, which can be manually configured or automatically calculated based on recent high and low prices.
2. Calculate grid interval width according to specified number of grid lines.
3. Generate grid line prices array with corresponding quantity.
4. When price drops below a grid line, open long order below it; when price rises above a grid line, close short order above it.
5. Dynamically adjust bounds, interval width and grid line prices to adapt the strategy to market changes.

### Advantage Analysis

1. Can steadily profit in range-bound and volatile markets, regardless of trend direction.
2. Supports both manual and automatic parameter settings for strong adaptability.
3. Optimizable parameters like grid quantity, interval width, and order size for better rewards.
4. Embedded position control for lower risk.
5. Dynamic grid range adjustment enhances adaptability.

### Risk Analysis

1. Severe loss may occur in strong trending markets.
2. Improper grid quantity and position settings may amplify risk.
3. Auto-calculated grid ranges may fail in extreme price swings.

Risk Management:
1. Optimize grid parameters and strictly control total positions.
2. Close the strategy before significant price movements.
3. Judge market conditions with trend indicators, and close the strategy when necessary.

### Optimization Directions

1. Choose optimal grid quantity based on market characteristics and capital scale.
2. Test different time periods to optimize auto-calculated parameters.
3. Optimize order size calculation for more stable returns.
4. Add indicators for trend identification and set up strategy closure conditions.

### Summary

The dynamic grid trading strategy adapts to the market by adjusting grid parameters, enabling steady profits in range-bound and volatile markets. With proper position control, risk is mitigated. Optimizing grid settings and incorporating trend judgment indicators can further improve the stability of the strategy.

---

``` pinescript
/*backtest
start: 2023-12-23 00:00:00
end: 2024-01-22 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("sarasa srinivasa kumar", overlay=true, pyramiding=14, close_entries_rule="ANY", default_qty_type=strategy.cash, initial_capital=100.0, currency="USD", commission_type=strategy.commission.percent, commission_value=0.1)
i_autoBounds    = input(group="Grid Bounds", title="Use Auto Bounds?", defval=true, type=input.bool)                             // calculate upper and lower bound of the grid automatically? This will theoretically be less profitable, but will certainly require less attention
i_boundSrc      = input(group="Grid Bounds", title="(Auto) Bound Source", defval="Hi & Low", options=["Hi & Low", "Average"])     // should bounds of the auto grid be calculated from recent High & Low, or from a Simple Moving Average
i_boundLookback = input(group="Grid Bounds", title="(Auto) Bound Lookback", defval=250, type=input.integer, maxval=500, minval=0) // when calculating auto grid bounds, how far back should we look for a High & Low, or what should the length be of our sma
i_boundDev      = input(group="Grid Bounds", title="(Auto) Bound Deviation", defval=0.10, type=input.float, maxval=1, minval=-1)  // if sourcing auto bounds from High & Low, this percentage will (positive) widen or (negative) narrow the bound limits. If sourcing from Average, this is the deviation (up and down) from the sma, and cannot be negative.
i_upperBound    = input(group="Grid Bounds", title="(Auto) Upper Boundry", defval=0.285, type=input.float)                      // for manual grid bounds only. The upperbound price of your grid
i_lowerBound    = input(group="Grid Bounds", title="(Auto) Lower Boundry", defval=0.225, type=input.float)                      // for manual grid bounds only. The lowerbound price of your grid.
i_gridQty       = input(group="Grid Lines",  title="Grid Line Quantity", defval=8, maxval=15, minval=3, type=input.integer)       // how many grid lines are in your grid

f_getGridBounds(_bs, _bl, _bd, _up) =>
    if _bs == "Hi & Low"
        _up ? highest(close, _bl) * (1 + _bd) : lowest(close, _bl)  * (1 - _bd)
    else
        avg = sma(close, _bl)
        _up ? avg * (1 + _bd) : avg * (1 - _bd)

f_buildGrid(_lb, _gw, _gq) =>
```