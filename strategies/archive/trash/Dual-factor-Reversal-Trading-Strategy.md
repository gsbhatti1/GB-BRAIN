> Strategy Arguments



|Argument|Default|Description|
|---|---|---|
|v_input_1|14|Length|
|v_input_2|true|KSmoothing|
|v_input_3|3|DLength|
|v_input_4|50|Level|
|v_input_5|20|LengthETT|
|v_input_6|0.5|Delta|
|v_input_7|false|Trigger|
|v_input_8|false|Trade reverse|


> Source (PineScript)

``` pinescript
//backtest
start: 2023-11-26 00:00:00
end: 2023-12-26 00:00

//@version=5
strategy("Dual-factor-Reversal-Trading-Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

length = input(14, title="Length")
ksmooth = input(True, title="KSmoothing")
dlength = input(3, title="DLength")
level = input(50, title="Level")
lengthett = input(20, title="LengthETT")
delta = input(0.5, title="Delta")
trigger = input(False, title="Trigger")
trade_reverse = input(False, title="Trade reverse")

// Price Reversal Logic
var float prev_close_1 = na
var float prev_close_2 = na

if not na(prev_close_1) and not na(prev_close_2)
    if close[1] > prev_close_1 and close < prev_close_2 and sma(close, 9) < level
        strategy.entry("Buy", strategy.long)
        
    if close[1] < prev_close_1 and close > prev_close_2 and ema(close, 9) > level
        strategy.close("Buy")

// Update previous closes
prev_close_2 := prev_close_1
prev_close_1 := close

// ETT Logic
var float trend = na
var int direction = na

if not na(trend)
    if (trend < 0 and close > open + delta * typical_price) or (trend > 0 and close < open - delta * typical_price)
        strategy.close("Buy")
        
// Calculate ETT direction
tt = ta.rsi(close, lengthett)
if tt[1] < tt and not na(trend)
    direction := if (direction == 0) 1 else (1 + direction)
else if tt[1] > tt and not na(trend)
    direction := if (direction == 0) -1 else (-1 + direction)

// Set trend
trend := direction

// Trade Logic
if trigger and trade_reverse
    strategy.close("Buy")
```