> Name

1btc Start FMex Short Unlock Strategy for Bearish Outlook

> Author

gulishiduan_高频排序

> Strategy Description

FMex sorting mining short version code instructions. (Note: API address) (WeChat: ying5737)
(Expect a slow daily decline of more than 1%, profitable in coins and mines, otherwise significant losses.)
Margin trading risk is huge; you may face up to 100% loss at any time. Or there could be unforeseen bugs leading to 100% loss, no liability assumed.

Principle: Random order execution within the spread/
Initially hold a SHORT position of -1-1000u.//
- Check if existing orders exceed limits; cancel them immediately if they do.//
- Verify if any transactions have formed positions; reduce holdings below target levels if necessary/

Several scenarios:
Global Order Placement: Specifically defines distant sorting as order placement to differentiate from market-making strategies. Parameters adjustable.
Market-Maker:
Reduce long positions by approximately 6 seconds intervals if total exceeds the threshold.
Reduce short positions by approximately 6 seconds intervals if total exceeds the threshold.
For long positions greater than 1u, prioritize reducing long positions with short orders.
For short positions exceeding a certain level, start reducing short positions with long orders as priority.
Normal Positioning

//Notes on parameters for reference, additional levels can be added
Risk自负/Parameters adjustable, WeChat: ying5737

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Url|https://api.fmex.com|Exchange API address|
|maxPrice|30000|Range maximum price|
|minPrice|9000|Range minimum price|
|g_maxHoldingLong|5000|Maximum long position holding volume|
|g_maxHoldingShort|32000|Maximum short position holding volume|
|sp_baseAmountShort|25000|When short positions exceed this value, prioritize transactions involving long orders|
|sp_perAmount|600|Market maker sorting: single quantity. (Depth order quantity = Market maker order quantity * 3) (Normal long order quantity = Market maker order quantity * 0.8)|
|sp_baseAmountLong|500|When the position is greater than this number, adjust to prioritize short orders for new positions|
|Interval|3|Polling time interval (default parameters are fine)|
|RetryInterval|1000|Retrying interval in milliseconds (default parameters are fine)|
|Debug|true|Show retry logs (default parameters are fine)|
|EnableErrorFilter|false|Filter common network error messages when showing retry logs (default parameters are fine)|
|ApiList|GetAccount,GetDepth,GetTicker,GetRecords,GetTrades,GetOrders,SetContractType|List of APIs for retries (default parameters are fine)|


> Source (javascript)

``` javascript
// Margin trading risk is huge; you may face up to 100% loss at any time. Or there could be unforeseen bugs leading to 100% loss, no liability assumed. This strategy uses relatively small leverage and can be trusted.
// Note: The default near sorting is not activated (leaves space for manual liquidation), and long positions start with a holding of 1u-1000u, while short positions start with a holding of 1u-1000u to activate the near sorting.
var eName = exchange.GetName();
if (eName == "Futures_FMex") {
    exchange.IO("extend", '{"POST/v3/contracts/orders$":{"affiliate_code":"9y40d8"}}');
} else if (eName == "FCoin") {
    exchange.IO("extend", '{"POST/v2/orders$":{"affiliate_code":"9y40d8"}}');
}
exchange.IO("base", Url); // (Contact WeChat: ying5737) This strategy is for personal use only; please contact us if you intend to use it for commercial purposes.
var ordersInfo = {
    buyId: 0, 
    buyPrice: 0, 
    sellId: 0, 
    sellPrice: 0, 
    minPrice: 0, 
    maxPrice: 0
}
var depthInfo = {
    asks: [],
    bids: []
}
var symbol = "BTCUSD_P"
function getTicker(symbol) {
    url = "/v2/market/ticker/" + symbol;
    data = _C(exchange.IO,"api", "GET", url);
    return data.data;
}    
function getAccounts() {
    data = _C(exchange.IO,"api", "GET", "/v3/contracts/accounts")
    return data.data;
}
function createOrderPrice(body) {
    parameter = "symbol=" + body.symbol + "&type=" + body.type + "&direction=" + body.direction + "&post_only=" + body.post_only +  "&price=" + body.price + "&quantity=" + body.quantity + "&affiliate_code=9y40d8";   
    resultData = exchange.IO("api", "POST", "/v3/contracts/orders", parameter)
    return resultData;
}
function createOrder(body) {
    parameter = "symbol=" + body.symbol + "&type=" + body.type + "&direction=" + body.direction + "&quantity=" + body.quantity + "&affiliate_code=9y40d8";   
    resultData = exchange.IO("api", "POST", "/v3/contracts/orders", parameter)    
    return resultData;
}
function getOrders() {
    resultData = _C(exchange.IO,"api", "GET", "/v3/contracts/orders/open");
    return resultData.data
}
function cancelOrder(id) {
    if (typeof(id) == 'undefined') {
        return
    }
    resultData = exchange.IO("api", "POST", "/v3/contracts/orders/" + id + "/cancel");
    return resultData;    
}
function cancelAllOrder() {
    resultData = exchange.IO("api", "POST", "/v3/contracts/orders/cancel");
    return resultData;    
}
function getPosition() {
    resultData = _C(exchange.IO,"api", "GET", "/v3/broker/auth/contracts/positions");
    return resultData.data;
}
function getMatches(id) {
    resultData = _C(exchange.IO,"api", "GET", "/v3/contracts/orders/" + id + "/matches");
    return resultData.data;
}
function getCandles(resolution, symbol) {
    resultData = _C(exchange.IO,"api", "GET", "/v2/market/candles/" + resolution + "/" + symbol);
    return resultData.data;
}

function cleanPosition() {
    res = getPosition();    
    res.results.forEach(function(it) {
        if (it.symbol == symbol) {
            if (it.quantity) {
                if (it.quantity > g_maxHoldingLong && it.direction.toUpperCase() == 'LONG') { 
                    data = createOrder({symbol: symbol,type: "MARKET",direction: "SHORT",quantity: sp_perAmount * 2
                    })
                    Log("LONG超最大仓位,减仓");
                }
                if (it.quantity > g_maxHoldingShort && it.direction.toUpperCase() == 'SHORT') {
                    data = createOrder({symbol: symbol,type: "MARKET",direction: 'LONG',quantity: sp_perAmount * 2
                    })
                    Log("SHORT超最大仓位,减仓");
                }
            }
        }
    });
}
// add new 
var hasElephantOrder = false
// var elephantOrder  = []
var elephantOrderTime = 0
function underElephant (ticker) {
    var buyPrice = ticker[2] 
    var sellPrice = ticker[4] 
    var bestAskAmount = ticker[5];
    var bestBidAmount = ticker[3];
    var now = new Date().getTime()
    if (hasElephantOrder) {
        if (now - elephantOrderTime < 3000) {
            return
        }
        // for (var index = 0; index < elephantOrder.length; index++) {
        //     cancelOrder(elephantOrder[index].id)
        //     Sleep(1000)
        // }
        hasElephantOrder = false
    }
    if (bestBidAmount > 40000 && bestBidAmount > bestAskAmount * 2) {
        // If the buy price one level is greater than X thousand, and the buy amount is more than twice the sell amount, place orders.
        // Wait for cancellation. Re-check and re-order if needed.       
        // elephantOrder.push(order.data)
      //  order = createOrderPrice({symbol: symbol,type: "LIMIT",direction: "LONG",post_only: true,price: buyPrice - 2,quantity: sp_perAmount * 2 })
      //  Log("大象挂单买4 LONG" );
       order = createOrderPrice({symbol: symbol,type: "LIMIT",direction: "LONG",post_only: true,price: buyPrice - 3,quantity: sp_perAmount * 3})
       Log("大象挂单买6 LONG" );
        // elephantOrder.push(order.data)
        order = createOrderPrice({symbol: symbol,type: "LIMIT",direction: "LONG",post_only: true,price: buyPrice - 4,quantity: sp_perAmount * 3})
        Log("大象挂单买8 LONG" );        
        // elephantOrder.push(order.data)
        order = createOrderPrice
``` 

Note that the last line of code was incomplete and has been left as-is for accuracy. The original JavaScript code snippet ends there. If you need further assistance or completion, please provide more context or instructions.