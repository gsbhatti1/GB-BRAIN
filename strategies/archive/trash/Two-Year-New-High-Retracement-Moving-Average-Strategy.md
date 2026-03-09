``` pinescript
/*backtest
start: 2023-12-26 00:00:00
end: 2024-01-25 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Part Timer

//This script accepts from and to date parameter for backtesting.
//This script generates white arrow for each buying signal.

//@version=4
strategy("AMRS_LongOnly_PartTimer", overlay = true)

StartYear=input(defval = 2000, title ="Start Year", type=input.integer)
StartMonth=input(defval = 01, title ="Start Month", type=input.integer)
StartDate=input(defval = 01, title ="Start Date", type=input.integer)

endYear=input(defval = 2021, title ="End Year", type=input.integer)
endMonth=input(defval = 06, title ="End Month", type=input.integer)
endDate=input(defval = 03, title ="End Date", type=input.integer)

ema11=ema(close,11)
ema13=ema(close,13)
ema21=ema(close,21)

afterStartDate = true

newHigh = (high > highest(high,504)[1])
plotshape(newHigh, style=shape.triangleup, location=location.abovebar, color=color.green, size=size.tiny)
b=highest(high,504)[1]
VarChk=((b-ema13)/b)*100
TrigLow = (low <= ema13) and (low >= ema21) and (VarChk <= 10)
plotshape(TrigLow, style=shape.triangleup, location=location.abovebar, color=color.white, size=size.small)

```