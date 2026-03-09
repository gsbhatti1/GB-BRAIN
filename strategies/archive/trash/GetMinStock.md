> Name

Replaces the deprecated GetMinStock function

> Author

hugo_zhou



> Source (javascript)

``` javascript
/****************
Get the minimum trading volume of different currency pairs for Huobi pro
Other platforms need to add different error parsing codes themselves
****************/

function main() {
SetErrorFilter("limit order amount error");
// Add the currency pair you want to know about
var huobipro = ["BTC_USDT","XRP_USDT","EOS_BTC","OMG_ETH"];

for(var i = 0;i<huobipro.length;i++){
exchange.IO("currency", huobipro[i]);
var ticker = exchange.GetTicker();
exchange.Buy(ticker.Sell, 0.00000001); // The amount written can only be small, and get the correct min returned by the server
var error = GetLastError();
// Huobi error code analysis, different trading platforms should have different limit order amount errors, min: `0.00000001`
if(error.indexOf("limit order amount error, min") >= 0){
var min = parseFloat(error.split(": `")[1]);
_G(exchange.GetName()+exchange.GetCurrency(),min);
}
}

// Print from database
for(var j = 0;j<huobipro.length;j++){
Log(exchange.GetName()+huobipro[j],":",_G(exchange.GetName()+huobipro[j]));
}
}
```

> Detail

https://www.fmz.com/strategy/69436

> Last Modified

2018-01-17 17:42:25