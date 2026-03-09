``` pinescript
/*backtest
start: 2025-01-17 00:00:00
end: 2025-02-15 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("TrinityBar", overlay=true, initial_capital=100000, 
     default_qty_type=strategy.percent_of_equity, default_qty_value=200)

//─────────────────────────────────────────────────────────────
// Current Bar Thirds Calculations
//─────────────────────────────────────────────────────────────
cur_range      = high - low
cur_lowerThird = low + cur_range / 3
cur_upperThird = high - cur_range / 3

//─────────────────────────────────────────────────────────────
// Previous Bar Thirds Calculations
//─────────────────────────────────────────────────────────────
prev_range      = high[1] - low[1]
prev_lowerThird = low[1] + prev_range / 3
prev_upperThird = high[1] - prev_range / 3

//─────────────────────────────────────────────────────────────
// Define Bullish Bar Types for Current Bar
//─────────────────────────────────────────────────────────────
is_1_3 = (open <= cur_lowerThird) and (close >= cur_upperThird)
is_2_3 = (open > cur_lowerThird) and (open < prev_upperThird) and (close >= cur_upperThird)
is_3_3 = (open >= prev_upperThird) and (close >= cur_upperThird)

//─────────────────────────────────────────────────────────────
// Define Bearish Bar Types for Current Bar
//─────────────────────────────────────────────────────────────
is_3_1 = (open <= cur_lowerThird) and (close < prev_lowerThird)
is_2_1 = (open > prev_lowerThird) and (open < prev_upperThird) and (close <= cur_lowerThird)
is_1_1 = (open >= prev_upperThird) and (close <= cur_lowerThird)

//─────────────────────────────────────────────────────────────
// Signal Generation for Buy and Sell Actions
//─────────────────────────────────────────────────────────────
buy_signal  = na
sell_signal = na

if (is_1_3 or is_2_3 or is_3_3)
    buy_signal := true
if (is_3_1 or is_2_1 or is_1_1)
    sell_signal := true

//─────────────────────────────────────────────────────────────
// Trade Execution Based on Generated Signals
//─────────────────────────────────────────────────────────────
if (sell_signal and strategy.opentrades > 0)
    strategy.close("Long")
    
if (buy_signal and strategy.openOrders == 0)
    strategy.entry("Long", direction=strategy.long)

```
```