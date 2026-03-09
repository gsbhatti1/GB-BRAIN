> Name

Bitcoin-Scalper-30MIN

> Author

a624587332



> Strategy Arguments



|Argument|Default|Description|
|---|---|---|
|v_input_1_high|0|src: high|close|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_19|false|Filter|
|v_input_20|3|Pullback Lookback|
|v_input_21|true|Use H.A Calculations|
|v_input_26|true|Activate leverage?|
|v_input_27|2|Max lev.|
|v_input_28|70|Volume length lever.|
|v_input_2|30|Rmi Length (Relative Momentum Index)|
|v_input_3|12|Rmi Momentum|
|v_input_4|33|Rmi oversold|
|v_input_5|70|Rmi overbought|
|v_input_6|22|Adx Length (Average Directional Index)|
|v_input_7|15|Adx Treshold|
|v_input_8|67|Rsi Length (Relative Strenght Indeks)|
|v_input_9|3|Left (Support and Resistance)|
|v_input_10|true|Right (Support and Resistance)|
|v_input_11|23|Cloud Length|
|v_input_12|2.6|Volume Multiplier|
|v_input_13|21|Volume Length|
|v_input_14|true|Scalping?|
|v_input_15|4|Scalping Length|
|v_input_16|10|Fast EMA Length|
|v_input_17|120|Medium EMA Length|
|v_input_18|500|Slow EMA Length|
|v_input_22|2|TP Long (Plotshape)|
|v_input_23|2|TP Short (Plotshape)|
|v_input_24|true|SL Plotshape?|
|v_input_25|8|% Stop loss|
|v_input_29|true|Backtest?|
|v_input_30|true|Longs|
|v_input_31|true|Shorts|
|v_input_32|100|risk|
|v_input_33|1997|start year|
|v_input_34|6|start month|
|v_input_35|true|start day|
|v_input_36|3333|stop year|
|v_input_37|12|stop month|
|v_input_38|31|stop day|
|v_input_39|0.02|TP/100|
|v_input_40|0.08|SL/100|


> Source (PineScript)

``` pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © wielkieef

//@version=4



strategy("Bitcoin Scalper [30MIN]", overlay=true, pyramiding=1, initial_capital = 10000, default_qty_type=strategy.percent_of_equity, default_qty_value = 100, calc_on_order_fills=false, slippage=0, commission_type=strategy.commission.percent, commission_value=0.04)

//SOURCE =============================================================================================================================================================================================================================================================================================================

src                 =                   input(high)

//RMI ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

RMI_len             =                   input(30, title="Rmi Length", type=input.integer, minval = 1, group="Relative Momentum Index")
mom                 =                   input(12, title="Rmi Momentum", type=input.integer, minval = 1, group="Relative Momentum Index")
RMI_os              =                   input(33, title="Rmi oversold", type=input.integer, minval = 0, group="Relative Momentum Index")
RMI_ob              =                   input(70, title="Rmi overbought", type=input.integer, minval = 0, group="Relative Momentum Index")

//ADX-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

ADX_len             =                   input(22, title="Adx Length", type=input.integer, minval = 1, group="Average Directional Index")
th                  =                   input(15, title="Adx Treshold", type=input.integer, minval = 0, group="Average Directional Index")

//RSI ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

RSI_len             =                   input(67, minval=1, group="Relative Strenght Indeks")

// Support and Resistance ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

left                =                   input(3, title="Left", group="Support and Resistance")
right               =                   input(1, title="Right", group="Support and Resistance")

// Cloud --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```