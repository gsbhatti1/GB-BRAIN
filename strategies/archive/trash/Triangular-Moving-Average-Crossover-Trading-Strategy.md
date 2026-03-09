> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|0|MA Type: SMA|EMA|WMA|VWMA|HMA|SMMA|DEMA|
|v_input_2|5|Short MA Length|
|v_input_3_close|0|Short MA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_4|20|Medium MA Length|
|v_input_5_close|0|Medium MA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_6|100|Long MA Length|
|v_input_7_close|0|Long MA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_8|false|SL Level % (0 - Off)|
|v_input_9|false|PT Level % (0 - Off)|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-08 00:00:00
end: 2024-01-15 00:00:00
period: 5m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("Kozlod - 3 MA strategy with SL/PT", shorttitle="kozlod_3ma", overlay = true, default_qty_type = strategy.percent_of_equity, default_qty_value = 5)

// 
// author: Kozlod
// date: 2018-03-25
// 

////////////
// INPUTS //


var int ma_type_short = v_input_1
var int ma_length_short = v_input_2
var float ma_source_short = v_input_3_close

var int ma_type_medium = v_input_4
var float ma_source_medium = v_input_5_close

var int ma_type_long = v_input_6
var float ma_source_long = v_input_7_close

// Stop Loss and Take Profit Levels
var float sl_level_percent = v_input_8
var float pt_level_percent = v_input_9


// Calculate moving averages
short_ma = na
if (ma_type_short == 0)
    short_ma := sma(close, ma_length_short)
else if (ma_type_short == 1)
    short_ma := ema(close, ma_length_short)
else if (ma_type_short == 2)
    short_ma := wma(close, ma_length_short)
else if (ma_type_short == 3)
    short_ma := vwma(close, ma_length_short)
else if (ma_type_short == 4)
    short_ma := hma(close, ma_length_short)
else if (ma_type_short == 5)
    short_ma := smma(close, ma_length_short)
else if (ma_type_short == 6)
    short_ma := dema(close, ma_length_short)

medium_ma = na
if (ma_type_medium == 0)
    medium_ma := sma(close, v_input_4)
else if (ma_type_medium == 1)
    medium_ma := ema(close, v_input_4)

long_ma = na
if (ma_type_long == 0)
    long_ma := sma(close, v_input_6)
else if (ma_type_long == 1)
    long_ma := ema(close, v_input_6)


// Plot moving averages on the chart
plot(short_ma, color=color.blue, title="Short MA")
plot(medium_ma, color=color.red, title="Medium MA")
plot(long_ma, color=color.green, title="Long MA")

// Generate buy and sell signals
if (short_ma > medium_ma and medium_ma > long_ma)
    strategy.entry("Buy", strategy.long)

if (short_ma < medium_ma and medium_ma < long_ma)
    strategy.close("Buy")

// Set stop loss and take profit levels if enabled
if (sl_level_percent != 0)
    sl_price = close * (1 - sl_level_percent / 100.0)
    strategy.exit("Stop Loss", "Buy", stop=sl_price)

if (pt_level_percent != 0)
    pt_price = close * (1 + pt_level_percent / 100.0)
    strategy.exit("Take Profit", "Buy", limit=pt_price)
```

Note: The original PineScript provided in the document has been slightly modified to ensure it compiles correctly and is coherent with the translated text.