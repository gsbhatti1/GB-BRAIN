> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|2017|Backtest Start Year|
|v_input_2|true|Backtest Start Month|
|v_input_3|true|Backtest Start Day|
|v_input_4|2019|Backtest Stop Year|
|v_input_5|12|Backtest Stop Month|
|v_input_6|31|Backtest Stop Day|
|v_input_7|true|smoothK|
|v_input_8|7|smoothD|
|v_input_9|5|lengthRSI|
|v_input_10|7|lengthStoch|
|v_input_11_close|0|RSI Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_12|14|roclength|
|v_input_13|2|pcntChange|
|v_input_14|2|Stop Loss %|
|v_input_15|9|Take Profit %|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-10-02 00:00:00
end: 2023-11-01 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Sto2", overlay=false, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=100, commission_type=strategy.commission.percent, commission_value=0.0)

/////////////// Time Frame ///////////////
testStartYear = input(2017, "Backtest Start Year") 
testStartMonth = input(1, "Backtest Start Month")
testStartDay = input(1, "Backtest Start Day")
testPeriodStart = timestamp(testStartYear,testStartMonth,testStartDay, 0, 0)

testStopYear = input(2019, "Backtest Stop Year")
testStopMonth = input(12, "Backtest Stop Month")
testStopDay = input(31, "Backtest Stop Day")
testPeriodStop = timestamp(testStopYear,testStopMonth,testStopDay, 23, 59)

var float highestPrice = na
var float lowestPrice = na

// Calculate Stochastic RSI
smoothK = input(7, "smoothK")
smoothD = input(7, "smoothD")
lengthRSI = input(5, "lengthRSI")
lengthStoch = input(7, "lengthStoch")

hlc3 = close + high + low
hlc3 /= 3

stochK = ta.stoch(hlc3, lengthRSI, smoothK)
stochD = ta.sma(stochK, smoothD)

// Calculate Price Rate of Change
roclength = input(14, "roclength")
pcntChange = input(2, "pcntChange")

roc = ta.roc(hlc3, roclength)

// Define conditions for entering long and short positions
longCondition = stochK > stochD and roc > pcntChange
shortCondition = stochK < stochD and roc < -pcntChange

if (longCondition)
    strategy.entry("Long", strategy.long)
    highestPrice := high
    lowestPrice := low

if (shortCondition)
    strategy.entry("Short", strategy.short)
    lowestPrice := low
    highestPrice := high

// Update stop loss and take profit levels
stopLossPercent = input(2, "Stop Loss %")
takeProfitPercent = input(9, "Take Profit %")

if (highestPrice != na)
    strategy.exit("Take Profit Long", "Long", stop=highestPrice * (1 + takeProfitPercent / 100), limit=highestPrice * (1 - stopLossPercent / 100))

if (lowestPrice != na)
    strategy.exit("Take Profit Short", "Short", stop=lowestPrice * (1 - takeProfitPercent / 100), limit=lowestPrice * (1 + stopLossPercent / 100))

// Plot indicators
plot(stochK, title="Stochastic K", color=color.blue)
plot(stochD, title="Stochastic D", color=color.red)
plot(roc, title="ROC", color=color.green)
```

This PineScript code defines the "Sto2" strategy based on the provided description. It calculates Stochastic RSI and Price Rate of Change indicators and uses them to enter long and short positions. The strategy also includes stop loss and take profit levels based on the highest and lowest prices observed during the trades.