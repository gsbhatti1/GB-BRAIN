> Name

Talib simple application to find three crows

> Author

Zero



> Source (javascript)

``` javascript
/*backtest
start: 2017-12-05 00:00:00
end: 2017-12-06 12:00:00
Period: 5m
exchanges: [{"eid":"OKCoin_EN","currency":"BTC"}]
*/

function main() {
while (true) {
    var r = exchange.GetRecords();
    var pos = _.indexOf(talib.CDL3BLACKCROWS(r), -100);
    // Find the three crows pattern and it was formed on the last K line
    if (pos != -1 && pos == r.length - 1) {
        Log("K-line index:", pos, r.length, "Time:", _D(r[pos].Time));
        // For the next sell order, these backtest charts will have a buy order sign
        exchange.Sell(_C(exchange.GetTicker).Buy, 0.1);
        throw "Three crows found";
    }
    Sleep(1000);
}
}
```

> Detail

https://www.fmz.com/strategy/62163

> Last Modified

2018-04-07 11:47:38