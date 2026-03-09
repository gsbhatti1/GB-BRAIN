```pinescript
/*backtest
start: 2024-06-04 00:00:00
end: 2025-02-19 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("[RS]ZigZag Percent Reversal with Stochastic Strategy", overlay=true)

// ZigZag Settings
string percent_method = input.string(
         defval="MANUAL", 
         title="Method to use for the zigzag reversal range:", 
         options=[
             "MANUAL", 
             "ATR005 * X", "ATR010 * X", "ATR020 * X", "ATR050 * X", "ATR100 * X", "ATR250 * X"
             ]
         )

var float percent = input.float(
         defval=0.25, 
         title="Percent of last pivot price for zigzag reversal:", 
         minval=0.0, maxval=99.0
         ) / 100

float percent_multiplier = input.float(
         defval=1.0, 
         title="Multiplier to apply to ATR if applicable:"
         )
if percent_method == "ATR005 * X"
    percent := ta.atr(5) / open * percent_multiplier
if percent_method == "ATR010 * X"
    percent := ta.atr(10) / open * percent_multiplier
if percent_method == "ATR020 * X"
    percent := ta.atr(20) / open * percent_multiplier
if percent_method == "ATR050 * X"
    percent := ta.atr(50) / open * percent_multiplier
if percent_method == "ATR100 * X"
    percent := ta.atr(100) / open * percent_multiplier
if percent_method == "ATR250 * X"
    percent := ta.atr(250) / open * percent_multiplier

// Zigzag function
f_zz(_percent)=>
    // Direction
    var bool _is_direction_up = na
    var float _htrack = na
    var float _ltrack = na
    var float _pivot = na
    float _reverse_range = 0.0
    var int _real_pivot_time = na
    var int _htime = na
    var int _ltime = na
    var float _reverse_line = na
    
    if bar_index >= 1
        
        if na(_is_direction_up)
            _is_direction_up := true
        
        _reverse_range := nz(_pivot[1]) * _percent
        
        if _is_direction_up
            _ltrack := na
            _ltime := time
            
            if na(_htrack)
                if high > high[1]
                    _htrack := high
                    _htime := time
                else
                    _htrack := high[1]
                    _htime := time[1]
            else
                if high > _htrack
```