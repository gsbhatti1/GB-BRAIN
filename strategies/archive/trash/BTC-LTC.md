Name

BTC-LTC-Address Monitoring-SMS Notification

Author

Zero

Strategy Description

Immediate alert for new transactions

Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|Type|0|Type: BTC|LTC|
|Addr|1LuckyY9fRzcJre7aou7ZhWVXktxjjBb9S|Address|
|Interval|3|Polling interval|
|EnableSMS|false|Enable SMS notification|
|SMSUser|***|SMS Username|
|SMSPass|***|SMS Pass MD5 password|
|PhoneNum|1111|Mobile phone number for receiving text messages|


Source (javascript)

``` javascript
var LastMsg = "";
function SMSSend(msg) {
if (msg == LastMsg) {
return true;
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

function main() {
var url = "http://open.qukuai.com/address/" + Addr + "?key=2ejf4jgfNoya8Y3GnQf68e4J23HherpUh1&limit=1";
if (Type == 1) {
url += "&ltc=true";
}
varlt = "";
Log("Monitor: ", Addr, Type == 0 ? 'BTC' : 'LTC');
if (EnableSMS) {
if (!SMSSend("Policy started successfully")) {
return false;
}
}
while (true) {
try {
var res = HttpQuery(url);
if (res) {
var obj = JSON.parse(res);
if (typeof(obj.t0) !='undefined' && obj.t0.length > 0) {
if (obj.t0.toString() != lt) {
if (lt != "") {
LogProfit(obj.balance, obj.received);
if (EnableSMS) SMSSend('There is a new transaction, current balance: ' + obj.balance/100000000 + 'Total number of receipts: ' + obj.received/100000000);
}
lt = obj.t0.toString();
}
}
}
} catch(e) {
Log(e);
}
Sleep(Interval*1000);
}
}
```


Detail

https://www.fmz.com/strategy/1295

Last Modified

2014-11-07 19:41:42