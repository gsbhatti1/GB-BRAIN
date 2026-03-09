> Name

Goblin-Town-60min-可用版

> Author

ChaoZhang



> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1_open|0|src: open|high|low|close|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|0|Longs / Shorts: Both|Longs|Shorts|
|v_input_27|15|length_|
|v_input_28|4|gamma|
|v_input_29|false|Zero-Lag|
|v_input_30|8|Rsi vwap lenght|
|v_input_31|14|  1-SMA Lenght|
|v_input_32|28|  2-SMA Lenght|
|v_input_33|55|  3-SMA Lenght|
|v_input_45|10|per2|
|v_input_46|3.5|dev2|
|v_input_47|21|per3|
|v_input_48|5|dev3|
|v_input_50|1.7|TP-2 [%]|
|v_input_51|7|SL [%]|
|v_input_52|true|Activate leverage?|
|v_input_53|3|Max lev.|
|v_input_54|50|Volume lenght lev.|
|v_input_3|false|(?ADX)  SHOW ADX Bars |
|v_input_4|0|  ADX Option: CLASSIC|MASANAKAMURA|
|v_input_5|22|  ADX Lenght|
|v_input_6|18|  ADX Treshold|
|v_input_7|false|(?Range Filter)  Show Range Filter|
|v_input_8|30|  Sampling Period|
|v_input_9|1.3|  Range Mult.|
|v_input_10|false|(?Volume BASIC)  SHOW Volume Bars |
|v_input_11|1.4|  Volume mult.|
|v_input_12|20|  Volume lenght|
|v_input_13|1.8|(?Volume BREAKOUTS)  Volume mult. Breakouts|
|v_input_14|25|  Volume lenght Breakouts|
|v_input_15|12|(?MACD)  Fast Length|
|v_input_16|19|  Slow Length|
|v_input_17|20|  Signal Smoothing|
|v_input_18|true|(?SAR)  Show Parabolic SAR|
|v_input_19|0.1|  Sar Start|
|v_input_20|0.1|  Sar Int|
|v_input_21|0.1|  Sar Max|
|v_input_22|40|(?Relative Strenght Indeks)  RSI Lenght|
|v_input_23_high|0|  RSI Source: high|close|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_24|false|(?Support and Resistance)  Show Support and Resistance levels|
|v_input_25|5|  Left|
|v_input_26|5|  Right|
|v_input_34|10|(?Relative Momentum Index)Rmi Lenght|
|v_input_35|14|Rmi Momentum|
|v_input_36|28|Rmi oversold|
|v_input_37|70|Rmi overbought|
|v_input_38|20|(?Bolinger Bands)  Bollinger Bands Length|
|v_input_39_high|0|  Bollinger Bands Source: high|close|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_40||  Timeframe 3|
|v_input_41_open|0|  Source 3: open|high|low|close|hl2|hlc3|hlcc4|ohlc4|
|v_input_42|false|  Show Bollinger Bands|
|v_input_43||  Timeframe 2|
|v_input_44_open|0|  Source 2: open|high|low|close|hl2|hlc3|hlcc4|ohlc4|
|v_input_49|0.9|(?Backtesting)TP-1 [%]|
|v_input_55|true|(?BACKTEST)Backtest|
|v_input_56|1997|start year|
|v_input_57|6|start month|
|v_input_58|true|start day|
|v_input_59|3333|stop year|
|v_input_60|12|stop month|
|v_input_61|31|stop day|


> Source (PineScript)

``` pinescript
strategy("Goblin Town [60min]", overlay = true, pyramiding=100, initial_capital = 10000, default_qty_type=strategy.percent_of_equity, default_qty_value = 50, calc_on_order_fills=false, slippage=0, commission_type=strategy.commission.percent, commission_value=0.03)

//SOURCE =============================================================================================================================================================================================================================================================================================================

src                 =                   input(open)

// POSITION ==========================================================================================================================================================================================================================================================================================================

Position            =                   input("Both",                           title= "Longs / Shorts",                                    options = ["Both","Longs","Shorts"])

is_Long             =                   Position                                                    == "SHORT" ? na : true
is_Short            =                   Position                                                    == "LONG" ? na : true

// Indicators Inputs ========================================================================================================================================================================================================================================================================================================


//ADX --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Candles_ADX         =                   input(false,                            title="  SHOW ADX Bars ",                                                                                                                  group = "ADX")
ADX_options         =                   input("CLASSIC",                   title="  ADX Option",                                       options = ["CLASSIC", "MASANAKAMURA"],                                          group = "ADX")
ADX_len             =                   input(22,                               title="  ADX Lenght",                                       type = input.integer, minval = 1,                                               group = "ADX")
th                  =                   input(18,                             title="  ADX Treshold",                                    type = input.float, minval = 0, step = 0.5,                                     group = "ADX")

// Range Filter ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

SHOW_RF             =                   input(false,                            title="  Show Range Filter",                                                                                                  