> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|false|Check this for 2-digit pairs (JPY, Gold, Etc)|
|v_input_2|16|SSL Period|
|v_input_3|14|ATR Period|
|v_input_4|1.5|ATR Stop Loss Factor|
|v_input_5|true|ATR Target Factor|
|v_input_6|true|Check this to use Money Management|
|v_input_7|1000|Position size (for Fixed Risk)|
|v_input_8|0.01|Risk % in Decimal Form|


> Source (Pinescript)

``` pinescript
/*backtest
start: 2023-10-23 00:00:00
end: 2023-11-22 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © comiclysm

//@version=4
strategy("SSL Backtester", overlay=false)

//--This strategy will simply test the effectiveness of the SSL using
//--money management and an ATR-derived stop loss

//--USER INPUTS

two_digit = input(false, "Check this for 2-digit pairs (JPY, Gold, Etc)")
ssl_period = input(16, "SSL Period")
atr_period = input(14, "ATR Period")
atr_stop_factor = input(1.5, "ATR Stop Loss Factor")
atr_target_factor = input(true, "ATR Target Factor")
use_mm = input(true, "Check this to use Money Management")
position_size = input(1000, "Position size (for Fixed Risk)")
risk = input(0.01, "Risk % in Decimal Form")

// Calculate SSL Channel
var float ssl_upper_band = na
var float ssl_lower_band = na
var float ssl_midline = na

if bar_index == 1
    ssl_upper_band := ta.highest(high, ssl_period)
    ssl_lower_band := ta.lowest(low, ssl_period)
    ssl_midline := (ssl_upper_band + ssl_lower_band) / 2

if close > ssl_upper_band
    ssl_upper_band := ta.highest(high, ssl_period)
    ssl_lower_band := close
    ssl_midline := (ssl_upper_band + ssl_lower_band) / 2
else if close < ssl_lower_band
    ssl_lower_band := ta.lowest(low, ssl_period)
    ssl_upper_band := close
    ssl_midline := (ssl_upper_band + ssl_lower_band) / 2

// ATR Calculation
atr = ta.atr(atr_period)

// Money Management
max_risk = position_size * risk
position_size = max_risk / (atr * atr_stop_factor)

// Stop Loss and Take Profit
if two_digit and use_mm
    stop_loss = ssl_upper_band - (atr * atr_stop_factor)
    take_profit = ssl_lower_band + (atr * atr_target_factor)
else
    stop_loss = ssl_lower_band - (atr * atr_stop_factor)
    take_profit = ssl_upper_band + (atr * atr_target_factor)

// Entry and Exit Logic
if (close > ssl_upper_band and not na(stop_loss))
    strategy.entry("Long", strategy.long, when=not na(stop_loss), comment="Entry")
    strategy.exit("Exit Long", "Long", stop=stop_loss, limit=take_profit, comment="Exit")
else if (close < ssl_lower_band and not na(stop_loss))
    strategy.entry("Short", strategy.short, when=not na(stop_loss), comment="Entry")
    strategy.exit("Exit Short", "Short", stop=stop_loss, limit=take_profit, comment="Exit")
```

This Pinescript code defines a backtesting strategy for the SSL (Sarik's SSL) channel, incorporating ATR-based stop loss and take profit levels, and money management. The strategy uses user-defined inputs to set parameters and dynamic levels for trading decisions.