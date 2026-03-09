``` pinescript
/*backtest
start: 2023-10-24 00:00:00
end: 2023-11-23 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
//// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © oakwhiz and tathal

//@version=4
strategy("BBPBΔ(OBV-PVT)BB", default_qty_type=strategy.percent_of_equity, default_qty_value=100)

startDate = input(title="Start Date", type=input.integer,
     defval=1, minval=1, maxval=31)
startMonth = input(title="Start Month", type=input.integer,
     defval=1, minval=1, maxval=12)
startYear = input(title="Start Year", type=input.integer,
     defval=2010, minval=1800, maxval=2100)

endDate = input(title="End Date", type=input.integer,
     defval=31, minval=1, maxval=31)
endMonth = input(title="End Month", type=input.integer,
     defval=12, minval=1, maxval=12)
endYear = input(title="End Year", type=input.integer,
     defval=2021, minval=1800, maxval=2100)

// Normalize Function
normalize(_src, _min, _max) =>
    // Normalizes series with unknown min/max using historical min/max.
    // _src      : series to rescale.
    // _min, _min: min/max values of rescaled series.
    var _historicMin =  10e10
    var _historicMax = -10e10
    _historicMin := min(nz(_src, _historicMin), _historicMin)
    _historicMax := max(nz(_src, _historicMax), _historicMax)
    _min + (_max - _min) * (_src - _historicMin) / max(_historicMax - _historicMin, 10e-10)
    

// STEP 2:
// Look if the close time of the current bar
// falls inside the date range
inDateRange = true
     
     
// Stop loss & Take Profit Section     
sl_inp = input(2.0, title='Stop Loss %')/100
tp_inp = input(4.0, title='Take Profit %')/100
 
stop_level = strategy.position_avg_price * (1 - sl_inp)
take_level = strategy.position_avg_price * (1 + tp_inp)

icreturn = false
innercandle = if (high < high[1]) and (low > low[1])
    icreturn := true

src = close

float change_src = change(src)
float i_obv = cum(change_src > 0 ? volume : change_src < 0 ? -volume : 0*volume)
float i_pvt = pvt

float result = change(i_obv - i_pvt)

float nresult = ema(normalize(result, -1, 1), 20)



length = input(20, minval=1)
mult = input(2.0, minval=0.001, maxval=50, title="StdDev")
basis = ema(nresult, length)
dev = mult * stdev(nresult, length)
upper = basis + dev
lower = basis - dev
bbr = (nresult - lower)/(upper - lower)
```