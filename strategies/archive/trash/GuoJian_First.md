> Name

GuoJian_First

> Author

liuguojian



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|min|0.0085|Minimum buy value|
|max|0.008534|Sell maximum value|


> Source (javascript)

``` javascript
/*backtest
start: 2018-08-27 00:00:00
end: 2018-08-28 20:00:00
Period: 1m
exchanges: [{"eid":"Huobi","currency":"LTC_BTC"}]
*/

function main() {
    Log(max);
    Log(min);
    var a = 1;
    while (true) {
        Log(exchange.GetAccount());
        var ticker = exchange.GetTicker();
        Log(ticker);
        if (ticker.High >= max) {
            //Log("Current Highest Price" + ticker.High);
            //Log("Convert all USDT to BTC");
            Log("Sell 1");
            exchange.Sell(-1, 1);
            Log(exchange.GetAccount());
        }
        if (ticker.Low <= min) {
            Log("Buy 1");
            exchange.Buy(-1, 1);
            Log(exchange.GetAccount());
            break;
        }
        a++;
        Sleep(60000); // one minute
    }
}

function onexit() {
    Log("onexit");
}

function onerror() {
    Log("onerror");
}

function init() {
    Log("init");
}
```


> Detail

https://www.fmz.com/strategy/113871

> Last Modified

2018-08-28 21:43:15