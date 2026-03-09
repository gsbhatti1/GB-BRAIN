Name

Share-ATR as an example of fault tolerance tutorial in mean calculation

Author

TradeMan

Strategy Description

In order to give back to the FMZ platform and community, share strategies & codes & ideas & templates

Introduction:
Detailed average calculation steps, taking ATR as an example.
Contains details such as indicator calls, fault tolerance for insufficient data points, and fault tolerance for unexpected data errors.
The important thing about strategy is grasping the details.

Welcome to cooperate and exchange, learn and make progress together~
v：haiyanyydss


Source (javascript)

``` javascript
var arecords = _C(exchange.GetRecords, 300);
var time = arecords[arecords.length - 1].Time;
var nowtime = time;
var atremaarr = [];
varOnoff = 0;

function main() {
    while (true) {
        // Start here and put this paragraph in the loop
        var Num = 50; // can be changed, the average value of several wires
        var records = _C(exchange.GetRecords, 300);
        var atr = TA.EMA(records, 9);
        nowtime = records[records.length - 1].Time;
        
        if (nowtime > time || Onoff == 0) {
            atr = atr.slice(atr.length - (20 + Num));
            for (var i = 0; i < (atr.length - Num); i++) { // (atr.length-Num) The length minus the period, such as 500. The first 50 is an inaccurate average. Here we take 450
                var atremTEMP = 0; // Calculate the sum, initially set to 0
                for (var j = 0; j < Num; j++) { // Sum
                    atrTEMP = atr[i + j] > 0 ? atr[i + j] : 0; // Eliminate unexpected data, the value is greater than O, the value is less than O or in other cases, the value is O
                    atremTEMP += atrTEMP;
                }
                atremaarr.push(atremTEMP / Num); // Put the average value into the array
            }
            time = nowtime;
            Onoff += 1;
            Log("Calculation:", Onoff, "Times.");
        }
        
        // Settlement here put this paragraph in the loop
        Sleep(3000);
        Log("Last root:", _N(atremaarr[atremaarr.length - 1], 2)); // Get the value
        // Log("Last second root:", _N(atremaarr[atremaarr.length-2],2))
    }
}
```

Detail

https://www.fmz.com/strategy/396764

Last Modified

2023-02-09 09:48:42