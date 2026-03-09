> Name

Price Fluctuation Alert

> Author

Zero

> Strategy Description

The program monitors the price fluctuation range within the specified period. If it exceeds the specified range, it will notify the designated mobile phone user by SMS. Using the SMS interface, it can be sent to multiple mobile phone numbers, separated by commas.
Please select the K-line cycle for the cycle. If the K-line cycle is 1 minute, the data within one minute will be monitored.

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|MaxRatio|1.5|Value of fluctuation (percentage)|
|LoopInterval|5|Collection interval (seconds)|
|EnableSMS|true|Enable SMS notifications|
|SMSUser|test|SMS Username|
|SMSPass|test|SMS password MD5|
|PhoneNum|111|Notification mobile number|


> Source (javascript)

``` javascript
function _N(v) {
    return Math.floor(parseFloat(v.toFixed(10)) * 1000) / 1000;
}

var LastMsg = "";
function SMSSend(msg) {
    if (msg == LastMsg) {
        return;
    }
    Log('SMS:', msg);
    LastMsg = msg;
    var ret = false;
    var phones = PhoneNum.split(',');
    for (var i = 0; i < phones.length; i++) {
        ret = HttpQuery("http://www.smsbao.com/sms?u=" + encodeURIComponent(SMSUser) + "&p=" + SMSPass.toUpperCase() + "&m=" + phones[i] + "&c=" + encodeURIComponent(msg)) == "0";
        if (ret) {
            Log("SMS notification", phones[i], "Success");
        } else {
            Log("SMS notification", phones[i], "Failure");
        }
    }
    return ret;
}

function formatDate(t) {
    var year = t.getFullYear();
    var month = t.getMonth() + 1;
    var day = t.getDate();
    var hour = t.getHours();
    var minute = t.getMinutes();
    var second = t.getSeconds();

    if (month < 10) {
        month = '0' + month;
    }
    if (day < 10) {
        day = '0' + day;
    }
    if (hour < 10) {
        hour = '0' + hour;
    }
    if (minute < 10) {
        minute = '0' + minute;
    }
    if (second < 10) {
        second = '0' + second;
    }

    return year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second;
}

function main() {
    if (exchanges.length > 1) {
        throw "Only one exchange is supported";
    }
    LoopInterval = Math.max(1, LoopInterval);
    Log('The floating percentage will be displayed as profit, and an alarm will be issued after exceeding ' + MaxRatio + '%');
    if (EnableSMS && !SMSSend('Early warning strategy started successfully')) {
        throw "SMS interface test failed";
    }
    var preRatio = 0;
    var preKRatio = 0;
    while (true) {
        var records = exchange.GetRecords();
        if (records && records.length > 0) {
            var r = records[records.length-1];
            var n = _N(((r.High - r.Low) * 100) / r.High);

            if (records.length > 1) {
                var p = records[records.length-2];
                var pn = _N(((p.High - p.Low) * 100) / p.High);
                if (pn != preKRatio) {
                    preKRatio = pn;
                    if (pn != preRatio) {
                        LogProfit(pn, 'Time:', formatDate(new Date(p.Time)), 'High:', p.High.toFixed(4), 'Low:', p.Low.toFixed(4));
                        if (EnableSMS && n >= MaxRatio) {
                            SMSSend('Current float ratio: ' + n + '%');
                        }
                    }
                }
            }
            if (n != preRatio) {
                LogProfit(n, 'Time:', formatDate(new Date(r.Time)), 'High:', r.High.toFixed(4), 'Low:', r.Low.toFixed(4));
                preRatio = n;
                if (EnableSMS && n >= MaxRatio) {
                    SMSSend('Current float ratio: ' + n + '%');
                }
            }
        }
        Sleep(LoopInterval * 1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/885

> Last Modified

2014-10-11 18:47:40