> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|0915-1455|Market session|
|v_input_2|true|Long Take Profit (%)|
|v_input_3|true|Short Take Profit (%)|
|v_input_4|0.5|Long Stop Loss (%)|
|v_input_5|0.5|Short Stop Loss (%)|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-10-22 00:00:00
end: 2023-11-21 00:00:00
period: 3h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © vikris
//@version=4
strategy("[VJ]First Candle Strategy", overlay = true, calc_on_every_tick = true, default_qty_type=strategy.percent_of_equity, default_qty_value=100, initial_capital=750, commission_type=strategy.commission.percent, 
     commission_value=0.02)


// ********** Strategy inputs - Start **********

// Used for intraday handling
// Session value should be from market start to the time you want to square-off 
// your intra-day positions
var session = input("0915-1455", type.session, title="Market session")

// Long take profit percentage
var take_profit_long = input(true, type=bool, title="Long Take Profit (%)")

// Short take profit percentage
var take_profit_short = input(true, type=bool, title="Short Take Profit (%)")

// Long stop loss percentage
var stop_loss_long = input(0.5, type=float, title="Long Stop Loss (%)")

// Short stop loss percentage
var stop_loss_short = input(0.5, type=float, title="Short Stop Loss (%)")

// ********** Strategy logic - Start **********

// Define the market session
var market_session = session

// Check if the current time is within the market session
if (not na(timeframe.period) and time(timeframe.period, market_session))
    // Get the first candle of the session
    var first_candle_open = request.security(syminfo.tickerid, "D", close[1], barmerge.overlap)
    
    // Determine the direction of the first candle
    var is_long = first_candle_open > open[1]
    var is_short = first_candle_open < open[1]
    
    // Enter long position
    if (is_long)
        strategy.entry("Long", strategy.long)
    
    // Enter short position
    if (is_short)
        strategy.entry("Short", strategy.short)
    
    // Exit on take profit
    if (take_profit_long and is_long)
        strategy.exit("Long TP", "Long", profit = close * take_profit_long)
    if (take_profit_short and is_short)
        strategy.exit("Short TP", "Short", profit = close * take_profit_short)
    
    // Exit on stop loss
    if (stop_loss_long and is_long)
        strategy.exit("Long SL", "Long", loss = close * stop_loss_long)
    if (stop_loss_short and is_short)
        strategy.exit("Short SL", "Short", loss = close * stop_loss_short)
```

This script defines a Pine Script for a strategy that uses the first candle of the market session to determine the direction of the trade and applies take profit and stop loss rules based on user-defined percentages.