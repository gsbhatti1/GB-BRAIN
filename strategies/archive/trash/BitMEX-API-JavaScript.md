> Name

BitMEX-Advanced API Functions-One-click Cancellation of Futures Batch Placement-JavaScript

> Author

FawkesPan


---

> Source (javascript)

``` javascript
/*

BitMEX Advanced API Interface for FMZ.com.

Copyright 2018 FawkesPan
Contact: i@fawkex.me / Telegram@FawkesPan

GNU General Public License v3.0

*/

function main() {
    Log(exchange.GetAccount());
}
var bulk = []
//Add batch purchase order
function BulkBuy(symbol,qty,price,type,exec) {
    Log("New Bulk order, open long "+ symbol + " " + price + " " + qty)
    var order = {};
    order.symbol = symbol;
    order.side = "Buy";
    order.orderQty = qty;
    order.price = price;
    order.ordType = type;
    order.execInst = exec;
    bulk[Object.keys(bulk).length] = order;
}
//Add bulk sell order
function BulkSell(symbol,qty,price,type,exec) {
    Log("New Bulk order, open short "+ symbol + " " + price + " " + qty)
    var order = {};
    order.symbol = symbol;
    order.side = "Sell";
    order.orderQty = qty;
    order.price = price;
    order.ordType = type;
    order.execInst = exec;
    bulk[Object.keys(bulk).length] = order;
}
//Execute batch orders
function BulkPost() {
    Log("Total Bulk orders being executed " + Object.keys(bulk).length + " orders");
    var param = "orders=" + JSON.stringify(bulk);
    bulk = [];
    exchange.IO("api", "POST", "/api/v1/order/bulk", param);
}
//Cancel all orders
function CancelPendingOrders() {
    exchange.IO("api","DELETE","/api/v1/order/all","symbol="+exchange.GetCurrency());
}
```

> Detail

https://www.fmz.com/strategy/105056

> Last Modified

2018-08-30 03:01:43