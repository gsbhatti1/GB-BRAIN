> Name

Bad-guy-strategy

> Author

Zer3192



> Strategy Arguments


|Argument|Default|Description|
|---|---|---|
|v_input_1_open|0|src: open|high|low|close|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|0|Longs / Shorts: Both|Longs|Shorts|
|v_input_5|5|SL [%]|
|v_input_6|false|Activate leverage?|
|v_input_7|3|Max lev.|
|v_input_8|50|Volume length leveraged|
|v_input_3|0.7|(?Backtesting) TP_L [%]|
|v_input_4|0.9|TP_S [%]|
|v_input_9|true|(?BACKTEST) Backtest|
|v_input_10|true|Longs|
|v_input_11|true|Shorts|
|v_input_12|100|risk|
|v_input_13|2000|start year|
|v_input_14|true|start month|
|v_input_15|true|start day|
|v_input_16|3333|stop year|
|v_input_17|12|stop month|
|v_input_18|31|stop day|


> Source (PineScript)


``` pinescript
/*backtest
start: 2021-05-08 00:00:00
end: 2022-05-07 23:59:00
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Binance","currency":"BTC_USDT"}]
*/
//@version=4
strategy("Bad-guy Strategy", overlay=true, pyramiding=1, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=100, calc_on_order_fills=false, slippage=0, commission_type=strategy.commission.percent, commission_value=0.04)

// SOURCE =============================================================================================================================================================================================================================================================================================================

src = input(open)

// POSITION ==========================================================================================================================================================================================================================================================================================================

Position = input("Both", title="Longs / Shorts", options=["Both","Longs","Shorts"])

is_Long  = Position == "LONG" ? true : na
is_Short = Position == "SHORT" ? true : na


ADX_options = "MASANAKAMURA"
ADX_len     = 22
th          = 19



c1                = 19
c2                = 2.5


x1         = 12
x2         = 16                                                            
x3         = 9                                                        


u          = 3.3
o          = 20

n1                 = ""
n2                 = high


v1                 = 0.5     
v2                 = 0.2
v3                 = 0.4

y          = 2.7
i          = 33                                                               


// ADX-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

calcADX(_len) =>
    up              = change(high)
	down            = -change(low)
	plusDM          = na(up)   ? na : (up > down and up > 0   ? up   : 0)
	minusDM         = na(down) ? na : (down > up and down > 0 ? down : 0)
	truerange       = rma(tr, _len)
	_plus           = fixnan(100 * rma(plusDM, _len)  / truerange)
	_minus          = fixnan(100 * rma(minusDM, _len) / truerange)
	sum             = _plus + _minus
	_adx            = 100 * rma(abs(_plus - _minus) / (sum == 0 ? 1 : sum), _len)
    [_plus,_minus,_adx]
calcADX_Masanakamura(_len) =>
    SmoothedTrueRange                   = 0.0
    SmoothedDirectionalMovementPlus     = 0.0
    SmoothedDirectionalMovementMinus    = 0.0
    TrueRange                           = max(max(high - low, abs(high - nz(close[1]))), abs(low - nz(close[1])))
    DirectionalMovementPlus             = high - nz(high[1]) > nz(low[1]) - low ? max(high - nz(high[1]), 0) : 0
```