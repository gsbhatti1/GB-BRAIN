> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Long|
|v_input_2|true|Short|
|v_input_3|100|Lot|
|v_input_4|3|length|
|v_input_5|2|fast|
|v_input_6|30|slow|
|v_input_7_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_8|0|Type: Trend|Crossing|
|v_input_9|1900|From Year|
|v_input_10|2100|To Year|
|v_input_11|true|From Month|
|v_input_12|12|To Month|
|v_input_13|true|From day|
|v_input_14|31|To day|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-12-06 00:00:00
end: 2023-12-12 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//Noro
//2019

//@version=3
strategy(title = "Noro's KAMA Strategy", shorttitle="KAMA str", overlay=true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, pyramiding = 0)

//Settings
needlong = input(true, defval = true, title = "Long")
needshort = input(true, defval = true, title = "Short")
capital = input(100, defval = 100, minval = 1, maxval = 10000, title = "Lot")
length = input(3, minval = 1) 
fast = input(2, minval = 1)
slow = input(30, minval = 1)
src = input(title = "Source",  defval = close)
type = input(defval = "Trend", options = ["Trend", "Crossing"], title = "Type")
fromyear = input(1900, defval = 1900)
toyear = input(2100, defval = 2100)
frommonth = input(true, defval = true, title = "From Month")
tomonth = input(12, defval = 12)
fromday = input(true, defval = true, title = "From day")
today = input(31, defval = 31)

// Kaufman's Adaptive Moving Average
kama = ta.kama(src, length, fast, slow)

// Determine long/short positions
if (type == "Trend" and kama[1] < kama and close > kama)
    strategy.entry("Long", strategy.long, when = needlong)
if (type == "Trend" and kama[1] > kama and close < kama)
    strategy.close("Long", when = needshort)
if (type == "Crossing" and close > kama)
    strategy.entry("Long", strategy.long, when = needlong)
if (type == "Crossing" and close < kama)
    strategy.close("Long", when = needshort)
```

This translation preserves the original code and formatting while translating the human-readable text.