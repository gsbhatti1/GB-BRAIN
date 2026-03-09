```markdown
Name

Convert_Record_Cycle

Author

jxc6698

Strategy Description

### Get Candlestick Data for a Specified Period

If there are any bugs or issues, feel free to leave a comment.

### Strategy Arguments


| Argument | Default | Description |
| --- | --- | --- |
| UI_NewCycleForMS | 1000*60*60*2 | Synthesis period in milliseconds |

### Source (javascript)

``` javascript
/**
*   author: jcx
*   date:   3/10/2017
*/
/**
*   Modified from XiaoXiaoMeng's "Convert Any K-line Cycle" template, supports setting any cycle size and input ticker.
*   Time settings must be integer multiples of the provided records[] period (program does not check this).
*
*   Considering that the last record in getrecords() might change:
*   1. A loop can be used in the main function from 0 to < length-1
*   2. Or, the current method in AddKLine uses timeAfOrEq(), allowing the value of the latest period to update (implicitly requires kline records to be added in chronological order).
*/

// K-line cycle synthesis extended to synthesize based on base K-lines into any period.
var cloneObj = function(obj) {                             // deep copy object function
    var str, newobj = obj.constructor === Array ? [] : {};
    if (typeof obj !== 'object') {
        return;
    } else if (JSON) {
        str = JSON.stringify(obj);                         // serialize the object
        newobj = JSON.parse(str);                          // parse back to an object
    } else {
        for (var i in obj) {
            newobj[i] = typeof obj[i] === 'object' ?
                cloneObj(obj[i]) : obj[i];
        }
    }
    return newobj;
};

/**
*   NeWCycleForMS: New cycle
*   n            : Number of candle records to be returned each time
*/
var DefaultN = 10;
function AssembleRecords(NewCycleForMS, n) {
    var self = {};
    self.NewCycleForMS = NewCycleForMS;
    self.curBars = [];       // used to store the most recent n candle objects
    n = parseInt(n);         // store the number of candles returned each time
    if (n * 1 === n)
        self.n = n;
    else
        self.n = DefaultN;

    // temporary variables
    self.tmp = {lasttime: 0};

    self.timeAf = function(time1, time2) {
        return time1 < time2;
    }
    self.timeAfOrEq = function(time1, time2) {
        return time1 <= time2;
    }
    self.inSameKLine = function(time1, time2) {
        if (parseInt(time1 / self.NewCycleForMS) === 
            parseInt(time2 / self.NewCycleForMS)) {
            return true;
        }
        return false;
    }
    self.getKlineStartTime = function(time) {
        return time - time % self.NewCycleForMS;
    }
    self.newBarObj = function(time, v) {
        var value = 0;
        value = v;
        return {                         // define a K-line structure
            Time: time,
            Open: value,
            High: value,
            Low: value,
            Close: value,
            Volume: 0
        }
    }
    self.updateNewBar = function(time, defaultvalue) {
        var barobj;
        if (self.curBars.length == 0) {
            barobj = self.newBarObj(self.getKlineStartTime(time), 
                defaultvalue);
            self.curBars.push(barobj);
        } else if (!self.inSameKLine(self.curBars[self.curBars.length - 1].Time,
            time)) {
            barobj = self.newBarObj(self.getKlineStartTime(time),
                defaultvalue);
            self.curBars.push(barobj);
        }

        if (self.curBars.length > n + 2) {
            self.curBars.shift();
        }
        return self.curBars[self.curBars.length - 1];
    }
    self.AddTicker = function(ticker) {
        var barobj;
        // ticker should be passed in time order
        barobj = self.updateNewBar(ticker.Time, ticker.Last);

        if (!self.timeAfOrEq(self.barobj[self.barobj.length - 1].Time, 
            ticker.Time)) {
            return;
        }
        if (barobj.High < ticker.High)
            barobj.High = ticker.High;
        if (barobj.Low > ticker.Low)
            barobj.Low = ticker.Low;
        barobj.Close = ticker.Last;
        //        barobj.Volume += ticker.Volume
    }
    self.AddKLine = function(klinerecord) {
        var barobj;

        // must use <=, when stepping into new record, last record may change
        if (!self.timeAfOrEq(self.tmp.lasttime,
            klinerecord.Time)) {
            return;
        }
        barobj = self.updateNewBar(klinerecord.Time, klinerecord.Open);
        self.tmp.lasttime = klinerecord.Time;

        if (barobj.High < klinerecord.High) {
            barobj.High = klinerecord.High;
        }
        if (barobj.Low > klinerecord.Low)
            barobj.Low = klinerecord.Low;
        barobj.Close = klinerecord.Close;
        barobj.Volume += klinerecord.Volumn;
    }
    self.GetKline = function() {
        var len = self.curBars.length;
        return self.curBars.slice(len - self.n);
    }

    return self;
}

// Test code
function main() {
    var records = exchange.GetRecords();
    while (!records || records.length < 24) {
        records = exchange.GetRecords();
    }
    
    // Process UI parameters, if written into your own strategy, you can refer to this
    
    var Num_UI_NewCycleForMS = 1;
    var arrayNum = UI_NewCycleForMS.split("*");
    for (var indexNum = 0; indexNum < arrayNum.length; indexNum++) {
        Num_UI_NewCycleForMS *= Number(arrayNum[indexNum]);
    }
    Log("Custom cycle in milliseconds is:", Num_UI_NewCycleForMS);
    
    // First parameter: base K-line, second parameter: the millisecond value of the desired conversion period (1000 * 60 * 20 means converting to 20 minutes)
    obj = AssembleRecords(Num_UI_NewCycleForMS, 5);      



    while(true) {
        records = _C(exchange.GetRecords);
        
        for (var i = 0; i < records.length; i++) {
            obj.AddKLine(records[i])
        }

        newrecords = obj.GetKline()
        $.PlotRecords(newrecords, 'BTC');

        // throw "stop"; // test
        Sleep(1000);
    }
}
```

### Detail

https://www.fmz.com/strategy/37678

### Last Modified

2017-03-13 16:41:10
```