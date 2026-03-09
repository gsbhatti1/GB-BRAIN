> Name

bitfinex margin trading

> Author

7 meters





> Source (javascript)

``` javascript
var bitfinexIndex = 0;
var basecurrency;
var quotecurrency;

function init(){
    for(var i = 0; i < exchanges.length; i++){
        if(exchanges[i].GetName() == "Bitfinex"){
            bitfinexIndex = i;
        }
    }
    var st = exchanges[bitfinexIndex].GetCurrency().split("_");
    basecurrency = st[0];
    quotecurrency = st[1];
}

$.bitfinexSell = function(price, amount){
    var message = "symbol=" + basecurrency + quotecurrency + "&amount=" + amount.toString() + "&price=" + price.toString() + "&side=sell&type=limit";
    id = exchanges[bitfinexIndex].IO("api", "POST", "/v1/order/new", message);
    return id.order_id;
}

$.bitfinexBuy = function(price, amount){
    var message = "symbol=" + basecurrency + quotecurrency + "&amount=" + amount.toString() + "&price=" + price.toString() + "&side=buy&type=fill-or-kill";
    var id = exchanges[bitfinexIndex].IO("api", "POST", "/v1/order/new", message);
    return id.order_id;
}

$.bitfinexGetPosition = function(){
    var position = exchanges[bitfinexIndex].IO("api", "POST", "/v1/positions");
    return position;
}

//Just use exchange.GetOrder(id) directly, no need to call the template
$.bitfinexGetOrder = function(order_id){
    var order = exchanges[bitfinexIndex].IO("api", "POST", "/v1/order/status", "order_id=" + parseInt(order_id));
    return order;
}

//You can cancel the order directly using exchange.CancelOrder(id) without calling the template
$.bitfinexCancelOrder = function(order_id){
    //var result = exchanges[bitfinexIndex].IO("api", "POST", "/v1/order/cancel", "order_id=" + parseInt(order_id));
    //return order;
}

//Return the total amount of USD that can be traded in the margin wallet (the virtual currency will be converted into US dollars and added to the calculation)
$.marginBalance = function(){
    var balance = exchanges[bitfinexIndex].IO("api", "POST", "/v1/margin_infos");
    return balance[0].tradable_balance;
}
```

> Detail

https://www.fmz.com/strategy/57333

> Last Modified

2017-12-02 22:04:28