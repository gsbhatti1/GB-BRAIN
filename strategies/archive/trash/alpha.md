Name

dynamic balance alpha

Author

Nakamoto aniseed


Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|threshold|0.05|Threshold|
|LoopInterval|60|Loop time|
|Minstock|0.001|Minimum trading volume|
|XPrecision|4|Quantity Precision|
|YPrecision|8|Price Precision|


Source (javascript)

``` javascript
var threshold = 0.05
var LoopInterval = 60
var Minstock = 0.001
var XPrecision = 4
var YPrecision = 8

// Cancel order function
function CancelPendingOrders() {
    Sleep(1000);
    var ret = false;
    while (true) {
        var orders = null;
        while (!(orders = exchange.GetOrders())) {
            Sleep(1000);
        }
        if (orders.length == 0) {
            return ret;
        }
        for (var j = 0; j < orders.length; j++) {
            exchange.CancelOrder(orders[j].Id);
            ret = true;
            if (j < (orders.length - 1)) {
                Sleep(1000);
            }
        }
    }
}

// Order function
function onTick() {
    var acc = _C(exchange.GetAccount); // Get account information
    var ticker = _C(exchange.GetTicker); // Get Ticker data
    var spread = ticker.Sell - ticker.Buy; // Get the bid-ask spread of Ticker data
    var diffAsset = (acc.Balance - (acc.Stocks * ticker.Sell)) / 2; // 0.5 times the difference between the account balance and the current position value
    var ratio = diffAsset / acc.Balance;
    LogStatus('ratio: ' + ratio, _D()); // Print ratio and current time
    if (Math.abs(ratio) < threshold) { // If the absolute value of ratio is less than the specified threshold
        print("spread")
        return false; // return false
    }
    if (ratio > 0) { // If ratio is greater than 0;
        var buyPrice = _N(ticker.Sell + spread, YPrecision);
        var buyAmount = _N(diffAsset / buyPrice, XPrecision);
        if (buyAmount < Minstock) { // If the order amount is less than the minimum trading volume
            return false;
        }
        exchange.Buy(buyPrice, buyAmount, diffAsset, ratio); // Buy order
    } else {
        var sellPrice = _N(ticker.Buy - spread, YPrecision); // Calculate the order price
        var sellAmount = _N(-diffAsset / sellPrice, XPrecision); // Calculate the order amount
        if (sellAmount < Minstock) {
            return false;
        }
        exchange.Sell(sellPrice, sellAmount, diffAsset, ratio); // Sell order
    }
    return true;
}

// Main function
function main() {
    // SetErrorFilter("GetRecords:|GetOrders:|GetDepth:|GetAccount|:Buy|Sell|timeout"); // Filter non-important information
    while (true) {
        if (onTick()) {
            CancelPendingOrders();
            Log(_C(exchange.GetAccount));
        }
        Sleep(LoopInterval * 1000);
    }
}
```


Detail

https://www.fmz.com/strategy/115321

Last Modified

2018-09-06 09:50:43