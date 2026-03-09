``` pinescript
/*backtest
start: 2023-08-19 00:00:00
end: 2023-09-13 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
// Thanks to HPotter for the original code for Center of Gravity Backtest
strategy("CoG SSL BF ?", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=100, commission_type=strategy.commission.percent, commission_value=0.075)

/////////////// Time Frame ///////////////
_0 = input(false,  "════════ Test Period ═══════")
testStartYear = input(2017, "Backtest Start Year") 
testStartMonth = input(1, "Backtest Start Month")
testStartDay = input(1, "Backtest Start Day")
testPeriodStart = timestamp(testStartYear,testStartMonth,testStartDay, 0, 0)

testStopYear = input(2019, "Backtest Stop Year")
testStopMonth = input(12, "Backtest Stop Month")
testStopDay = input(31, "Backtest Stop Day")
testPeriodStop = timestamp(testStopYear,testStopMonth,testStopDay, 0, 0)

testPeriod() => true

/////////////// SSL Channels /////////////// 
_1 = input(false,  "═════════ SSL ══════════")
len1=input(title="SMA Length 1", defval=12)
len2=input(title="SMA Length 2", defval=13)

smaHigh = sma(high, len1)
smaLow = sma(low, len2)
sslUp = na
sslDn = na

if (close >= smaHigh and close[1] < smaHigh)
    sslUp := high
    sslDn := low
else if (close <= smaLow and close[1] > smaLow) 
    sslDn := low
    sslUp := high
sslChannel = highestbars(sslUp, 20)[0]
channelOpen = security(syminfo.tickerid, "60", sslUp[sslChannel])
channelClose = security(syminfo.tickerid, "60", sslDn[sslChannel])

/////////////// Center of Gravity (CoG) /////////////// 
_2 = input(false,  "═════════ CoG ══════════")
len=input(title="Length", defval=25)
m=input(title="%", defval=5)
rocLen=input(title="Rate of Change Length", defval=6)

cogUp = na
cogDn = na

if (close >= sum(close, len) / len and close[1] < sum(close, len) / len)
    cogUp := high
    cogDn := low
else if (close <= sum(close, -len) / (-len) and close[1] > sum(close, -len) / (-len))
    cogDn := low
    cogUp := high

cogChannel = highestbars(cogUp, 20)[0]
cogChannelOpen = security(syminfo.tickerid, "60", cogUp[cogChannel])
cogChannelClose = security(syminfo.tickerid, "60", cogDn[cogChannel])

/////////////// Stop Loss /////////////// 
_3 = input(false,  "════════ Stop Loss ═══════")
atrStopPeriod=input(title="ATR Stop Period", defval=2)
atrStopMultiplier=input(title="ATR Stop Multiplier", defval=1)

atrValue = atr(atrStopPeriod)
stopLossPrice = na

if (position_is_long)
    stopLossPrice := low[1] - atrStopMultiplier * atrValue
else if (position_is_short)
    stopLossPrice := high[1] + atrStopMultiplier * atrValue

/////////////// Strategy Logic ///////////////
longCondition = crossover(channelOpen, close) or crossunder(cogChannelClose, close)
shortCondition = crossunder(channelClose, close) or crossover(cogChannelOpen, close)

if (testPeriod())
    strategy.entry("Long", strategy.long, when=longCondition)
    strategy.exit("Stop Loss Long", from_entry="Long", stop=stopLossPrice)

if (testPeriod())
    strategy.close("Long", when=shortCondition)
```

Note: The Pine Script provided is a simplified version that integrates the core logic of the described strategy. It uses variables to control test periods and calculates both SSL channels and CoG lines, then implements basic long/short conditions based on these indicators along with dynamic stop loss rules. Adjustments might be necessary for full integration into more complex trading environments or specific backtesting requirements.