> Name

StochRSI is consistent with okcoin

> Author

fangj





> Source (javascript)

``` javascript
function Stoch_RSI(records) {
/*
LC:=REF(CLOSE,1);
RSI:=SMA(MAX(CLOSE-LC,0),14,1)/SMA(ABS(CLOSE-LC),14,1)*100;
STOCH_RSI=STOCH_RSI:=MA(RSI-LLV(RSI,14),3)/MA(HHV(RSI,14)-LLV(RSI,14),3)*100;
STOCH_RSI_MA:SMA(STOCH_RSI,3);
*/

// Calculate RSI
var rsi = TA.RSI(records, 14);
// STOCH_RSI:=MA(RSI-LLV(RSI,14),3)/MA(HHV(RSI,14)-LLV(RSI,14),3)*100;
// Fill in blank data
var raw_stoch_rsi = [], raw_stoch_rsi_a = [], raw_stoch_rsi_b = [];
for (var i = 0; i < 14; i++) {
raw_stoch_rsi[i] = 50;
raw_stoch_rsi_a[i] = 0.5;
raw_stoch_rsi_b[i] = 1;
}
// Calculate indicators
for (i = 14; i < rsi.length; i++) {
var the_next_index = i + 1;
var first_index = the_next_index - 14;
var period_data = rsi.slice(first_index, the_next_index);
var llv = _.min(period_data);
var hhv = _.max(period_data);
var current_rsi = rsi[i];
raw_stoch_rsi_a.push(current_rsi - llv);
raw_stoch_rsi_b.push(hhv - llv);
}
// Moving average of numerator and denominator respectively
var raw_stoch_rsi_a_ma = TA.MA(raw_stoch_rsi_a, 3);
var raw_stoch_rsi_b_ma = TA.MA(raw_stoch_rsi_b, 3);
for (i = 0; i < rsi.length; i++) {
var v = raw_stoch_rsi_a_ma[i] / raw_stoch_rsi_b_ma[i] * 100;
v = isNaN(v) ? 50 : v;
raw_stoch_rsi[i] = v;
}
// moving average
var stoch_rsi_K = raw_stoch_rsi;
var stoch_rsi_D = TA.MA(stoch_rsi_K, 3);
stoch_rsi = [stoch_rsi_K, stoch_rsi_D];
return stoch_rsi;
}

var chart = { // This chart is an object in JS language. Before using the Chart function, we need to declare an object variable chart that configures the chart.
__isStock: true, // Mark whether it is a general chart. If you are interested, you can change it to false and run it to see.
tooltip: {xDateFormat: '%Y-%m-%d %H:%M:%S, %A'}, // Zoom tool
title: {text: 'K-line chart'}, // title
rangeSelector: { // Select range
buttons: [{type: 'hour', count: 1, text: '1h'}, {type: 'hour', count: 3, text: '3h'}, {
type: 'hour',
count: 8,
text: '8h'
}, {type: 'all', text: 'All'}],
selected: 0,
inputEnabled: true
},
xAxis: {type: 'datetime'}, // The horizontal axis of the coordinate axis is: x-axis, the currently set type is: time
yAxis: [{ // The vertical axis of the coordinate axis is the y-axis. The default value is adjusted with the data size.
title: {text: 'Price'}, // title
opposite: false,
height: '60%',// Whether to enable the right vertical axis
},
{ // The vertical axis of the coordinate axis is the y-axis. The default value is adjusted with the data size.
title: {text: 'stoch_rsi'}, // title
top: '65%',
height: '35%',
offset: 0,
opposite: false, // Whether to enable the right vertical axis
}],
series: [ // Data series, this attribute saves each data series (line, K-line chart, label, etc..)
{
type: 'candlestick',
name: 'price',
id: 'primary',
data: []
}, // The index is 0, and the data array stores the data of this index series.
{name: "SRSI_K", id: "SRSI_K", data: [], yAxis: 1}, // The index is 1, dashStyle is set: 'shortdash', that is, set a dash line.
{name: "SRSI_D", id: "SRSI_D", dashStyle: 'shortdash', data: [], yAxis: 1},
]
};

function main() {
exchange.SetContractType("quarter");
var ObjChart = Chart(chart); // Call the Chart function to initialize the chart.
ObjChart.reset(); // Clear
var preBarTime = 0;
while (true) {
var nowTime = new Date().getTime(); // Get the timestamp of this poll, which is a timestamp of milliseconds. Used to determine the position written to the X-axis of the chart.
var records = exchange.GetRecords(PERIOD_H1); // Get market data
var stoch_rsi = Stoch_RSI(records);
stoch_rsi_quick = stoch_rsi[0];
stoch_rsi_slow = stoch_rsi[1];

for (var i = 0; i < records.length; i++) { // Traverse records
var r_quick = stoch_rsi_quick[i];
var r_slow = stoch_rsi_slow[i];
if (isNaN(r_quick)) {
r_quick = 50;
}
if (isNaN(r_slow)) {
r_slow = 50;
}
if (records[i].Time == preBarTime) {
ObjChart.add(0, [records[i].Time, records[i].Open, records[i].High, records[i].Low, records[i].Close], -1); // Add
ObjChart.add(1, [records[i].Time, r_quick], -1);
ObjChart.add(2, [records[i].Time, r_slow], -1);
} else if (records[i].Time > preBarTime) {
preBarTime = records[i].Time;
ObjChart.add(0, [records[i].Time, records[i].Open, records[i].High, records[i].Low, records[i].Close]); // Add
ObjChart.add(1, [records[i].Time, r_quick]);
ObjChart.add(2, [records[i].Time, r_slow]);
}

}
ObjChart.update(chart); // Update the chart to display.
Sleep(2000);
}
}
```

> Detail

https://www.fmz.com/strategy/56119

> Last Modified

2017-09-26 13:04:37