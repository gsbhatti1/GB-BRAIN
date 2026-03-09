> Name

1btc起fmex多头解锁策略后市看多

> Author

gulishiduan_高频排序

> Strategy Description

**FMex排序挖矿多头版本代码使用说明**

// Margin market risk is significant, you may face a 100% loss at any time. There may be unknown bugs leading to a 100% loss, and we are not responsible.
// (If considering holding positions or trading in an oscillating market, corresponding parameters and code levels can be flexibly modified.)
// The current maximum position size (directional calculation) is recommended within 0.5-3 times the base amount. For example, if you have 0.1B with a 3x leverage, the directional position would be approximately 2700u, and the maximum position would be 3200u. Adjusting to 10x leverage would result in a directional position of about 9000u, and the maximum position at 10000u. The order size can be adjusted between 300-500u.
// Live trading address: https://api.fmex.com Test network: https://api.fmextest.net
// Note: Manually hold long1-1000u first.
// (Contact WeChat: ying5737)
**Strategy Principle:**

![](http://https://wx1.sinaimg.cn/mw690/c5775633ly1gaajdxk8a8j20u10f4dhx.jpg)

The reference image is for your information.
https://wx1.sinaimg.cn/mw690/c5775633ly1gaajdxk8a8j20u10f4dhx.jpg

Random order placement in the market/This strategy defaults to maintaining a long position/
Note: First manually hold long1-1000u.
// - Detect if existing orders exceed boundaries; cancel them immediately if they do
// - Detect if positions have been formed by trades, and reduce holdings if they exceed xxu

**Several Order Scenarios:**

**Global Orders:**
Defined as remote orders to differentiate from market-making strategies. Parameters are adjustable, currently around 8 levels.

**Market-Making (Near-End Order Placement):**
Max long position is customizable; if it exceeds this position, approximately every 6 seconds the position will be reduced until below the custom parameter.
Max short position is also customizable; if it exceeds this position, approximately every 6 seconds the position will be reduced until below the custom parameter.
Exceeding a long position triggers the reduction of long positions strategy, with orders mainly being short: forming short positions upon trading
Exceeding a 1u short position triggers the reduction of short positions strategy, with orders mainly being long: easily trading for long positions
Normal position (random trades in the market)

**// Notes on parameter comments are for reference only; additional levels can be added as needed.**
order = createOrderPrice({
 symbol: "BTCUSD_P",
 type: "LIMIT",
 direction: "SHORT", // Choose between long and short, 'short' or 'long'
 post_only: true,
 price: lastPrice + 5.5, // Adjustable by 0.5 or multiples of 0.5
 quantity: sp_perAmount,
 affiliate_code: "9y40d8"
})

******Risk自负/Parameters can be adjusted; contact WeChat: ying5737 for optimization directions such as adding MA or candlestick comparisons to determine direction, level adjustments, and added custom order sizes.******

> Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|Url|https://api.fmex.com|Exchange API address; use the formal version: https://api.fmex.com for production.|
|maxPrice|30000|Maximum price in the range|
|minPrice|9000|Minimum price in the range|
|g_maxHoldingLong|21000|Maximum long position size|
|g_maxHoldingShort|5000|Maximum short position size|
|sp_baseAmountLong|18000|Position control: limit for converting long positions to shorts|
|sp_baseAmountShort|600|Position control: limit for reducing short positions when they exceed a certain amount|
|sp_perAmount|800|Market-making order quantity. (Depth-level orders quantity = Market-Maker orders * 3)(Normal short orders quantity = Market-Maker orders * 0.6)|
|Interval|3|Polling time (default parameters are fine)|
|RetryInterval|5000|Retrying interval in milliseconds (default parameters are fine)|
|Debug|true|Display retry logs (default parameters are fine)|
|EnableErrorFilter|false|Filter common network error messages when displaying retry logs (default parameters are fine)|
|ApiList|GetAccount, GetDepth, GetTicker, GetRecords, GetTrades, GetOrders, SetContractType|List of APIs for error handling (default parameters are fine)|


> Source Code (JavaScript)

``` javascript
// Margin market risk is significant, you may face a 100% loss at any time. There may be unknown bugs leading to a 100% loss, and we are not responsible. The leverage used in this strategy is relatively small, so it can be experienced with confidence.
// Note: Default near-end order placement does not start (leaves room for manual liquidation), the long version first holds long1u-1000u, while the short version first holds short1u-1000u to activate the near-end order placement
var eName = exchange.GetName();
if (eName == "Futures_FMex") {
    exchange.IO("extend", '{"POST/v3/contracts/orders$":{"affiliate_code":"9y40d8"}}');
} else if (eName == "FCoin") {
    exchange.IO("extend", '{"POST/v2/orders$":{"affiliate_code":"9y40d8"}}');
}
exchange.IO("base", Url); // Contact WeChat: The strategy is for personal use only. If used for commercial purposes, please contact us in advance.
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
    var ticker = getTicker(symbol); 
    var buyPrice = ticker[2] 
    var sellPrice = ticker[4] 
    var bestAskAmount = ticker[5];
    var bestBidAmount = ticker[3];
    
    if (hasElephantOrder) {
        if ((new Date().getTime() - elephantOrderTime) < 3000) {
            return
        }
        // for (var index = 0; index < elephantOrder.length; index++) {
        //     cancelOrder(elephantOrder[index].id)
        //     Sleep(1000)
        // }
        hasElephantOrder = false
    }
``` 

Please note that some placeholder variables and functions like `Sleep` might need to be defined elsewhere in your code or replaced with appropriate functions as per the platform's requirements. Also, ensure you handle API requests and responses properly for a robust implementation. Adjustments may also be necessary based on specific trading environment and security practices.