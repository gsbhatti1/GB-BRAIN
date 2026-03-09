> Name

1btc Start FMex Bull Unlock Strategy Post-Market Bullish Outlook

> Author

gulishiduan_高频排序

> Strategy Description

**FMex Sorting Mining Bull Version Code Usage Instructions**

// Margin trading carries significant risk; you may face a 100% loss at any time. There might be unforeseen bugs leading to a 100% loss, for which we are not responsible.
// (If considering holding short or experiencing volatility, adjust the parameters and code positions accordingly.)
// Currently, the maximum position is calculated based on转向计算), it's recommended to maintain between 0.5-3 times this amount. For example, with a leverage of 3x on 0.1B, the adjusted position will be approximately 2700u, and the maximum position could be up to 3200u. If using 10x leverage, the adjusted position would be around 9000u, and the maximum position 10000u. Adjustments can be made for trade volumes between 300-500u.
// Live trading address: https://api.fmex.com Test network: https://api.fmextest.net// Note: Manually open a long position first at 1u-1000u.
// (Contact us on WeChat: ying5737)
**Strategy Principle:**

![](http://https://wx1.sinaimg.cn/mw690/c5775633ly1gaajdxk8a8j20u10f4dhx.jpg)
For reference only
https://wx1.sinaimg.cn/mw690/c5775633ly1gaajdxk8a8j20u10f4dhx.jpg

Random order placement for the market/Default strategy favors holding a bullish position/
Note: First manually open a long position at 1u-1000u.//
**- Detect if existing orders exceed the limit; cancel them immediately if they do.**
**- Check if an order has formed a position, and reduce it to below the predefined position size if it exceeds xxu.**

**Several Order Scenarios:**

**Global Orders:**
Specifically defined as far-end sorting orders for distinguishing from market-making strategies. Parameters are adjustable, currently around 8 levels.

**Market Makers (Near-End Market Orders):**
Maximum bullish positions can be customized; if exceeding this position, reduce it approximately every 6 seconds until below the custom parameter.
Maximum bearish positions can also be customized; if exceeding this position, reduce it approximately every 6 seconds until below the custom parameter.
Exceeding long positions triggers a reduction in long positions strategy with short orders as the main focus: resulting in bearish positions.
Exceeding 1u of bearish positions triggers a reduction in bearish positions strategy with long orders as the primary focus:极易成交多单
Normal position (random fill for bullish orders based on market fluctuations)

**// Remarks and descriptions within parameters are provided for reference, additional levels can be added** as follows:

``` javascript
order = createOrderPrice({
    symbol: "BTCUSD_P",
    type: "LIMIT",
    direction: "SHORT", // Choose between long or short
    post_only: true,
    price: lastPrice + 5.5, // Adjustible by multiples of 0.5 or its multiples
    quantity: sp_perAmount,
    affiliate_code: "9y40d8"
})
```

******
Risk自负/Parameters are adjustable; contact us on WeChat: ying5737
**Optimization Directions:** Incorporate moving averages or candlestick comparisons to determine direction, optimize levels, and add custom trade volumes, etc.******

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Url|https://api.fmex.com|Exchange API address, change to: https://api.fmex.com for the production version|
|maxPrice|30000|Range maximum price|
|minPrice|9000|Range minimum price|
|g_maxHoldingLong|21000|Maximum long position amount|
|g_maxHoldingShort|5000|Maximum short position amount|
|sp_baseAmountLong|18000|Position control: limit for converting to a short position from a long position|
|sp_baseAmountShort|600|Position control: reduce short positions if the bearish position is too large|
|sp_perAmount|800|Market maker order amount. (Depth level orders = market maker orders * 3) (Normal short orders = market maker orders * 0.6)|
|Interval|3|Polling time interval (default parameters can be used)|
|RetryInterval|5000|Retrying interval (milliseconds). Default parameters can be used|
|Debug|true|Show retry logs (default parameters can be used)|
|EnableErrorFilter|false|Hide common network error messages in retry logs (default parameters can be used)|
|ApiList|GetAccount, GetDepth, GetTicker, GetRecords, GetTrades, GetOrders, SetContractType|List of APIs for error handling. Default parameters can be used|

> Source Code (JavaScript)

``` javascript
// Margin trading carries significant risk; you may face a 100% loss at any time. There might be unforeseen bugs leading to a 100% loss, for which we are not responsible. The leverage used in this strategy is relatively small, so it can be safely experienced.
// Note: Default near-end market orders do not start (leave space for manual liquidation), long version starts with a long position of 1u-1000u, short version starts with a short position of 1u-1000u to activate the near-end market order functionality
var eName = exchange.GetName();
if (eName == "Futures_FMex") {
    exchange.IO("extend", '{"POST/v3/contracts/orders$":{"affiliate_code":"9y40d8"}}');
} else if (eName == "FCoin") {
    exchange.IO("extend", '{"POST/v2/orders$":{"affiliate_code":"9y40d8"}}');
}
exchange.IO("base", Url); // (Contact us on WeChat:) The strategy is for personal use only; contact us before any commercial distribution.
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
    resultData = exchange.IO("api", "POST", "/v3/contracts/orders/" + id + "/cancel");//+ id 
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
    resultData = _C(exchange.IO,"api", "GET", "/candles/" + resolution + "/" + symbol);
    return resultData.data;
}
function underElephant(ticker) {
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
}
```