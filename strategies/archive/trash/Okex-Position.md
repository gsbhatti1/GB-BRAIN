> Name

The Okex exchange retrieves the specified currency position and returns the inventor's Position structure array.

> Author

Exodus[strategy ghostwriting]

> Strategy Description

Use OK requests to obtain the position information of the specified currency.

![IMG](https://www.fmz.com/upload/asset/1f4aa7f53c0199070b59b.png)

![IMG](https://www.fmz.com/upload/asset/1f554e0443b2b6d2626e4.png)

By the way, I will undertake the ghostwriting of strategies.

> Source (javascript)

``` javascript

//test module
//Request initiated by Okex exchange
function main() {
//Log(exchange.GetAccount());
exchange.SetContractType("swap");

//Multi-currency construction query list:
let currencyList="";
for(let i=0;i<exchanges.length;i++){//Traverse all exchanges that have been added
currencyList=currencyList+ exchanges[i].GetCurrency().replace("_","-")+",";//Format conversion, okx request needs to be converted from ETH_USDT to ETH-USDT format
}
currencyList=currencyList.substring(0,currencyList.length-1);//Delete the last one
Log("query list currencyList:"+currencyList);

let positions=GetAllPositionInOk(exchange,currencyList);//Get the result

for(let i=0;i<positions.length;i++){//Print the position information obtained by each exchange
The position information of Log(positions[i][0].Symbol+" is: "+JSON.stringify(positions[i]));

}

}


// Get the positions of a specific currency from the position list
function GetPositionBySymbol(positions, symbol) {
var index = -1;

if (positions && positions.length > 0) {
for (var i = 0; i < positions.length; i++) {
if (positions[i][0].Symbol == symbol) {
index = i;
break;
}
}
}

return index == -1 ? null : positions[index];
}

// Get the list of all OK positions, pass in the OK exchange and the currency list to be queried, the currencyList format is: "BTC-USDT, ETH-USDT, LTC-USDT",
//Separated by commas, up to 10 currencies are supported.
//CurrencyList passes in an empty string to get a list of all positions!
function GetAllPositionInOk(tExchange,currencyList) {
let exchange=tExchange;
if(exchange==null)
exchange=exchanges[0];
var ret = exchange.IO("api", "GET", "/api/v5/account/positions?instId"+currencyList);
var positions = [];
var i = 0;

//Log("Ok position return information"+JSON.stringify(ret));
if (!ret || !ret.data) {
return null;
}
// Get all positions
for (i = 0; i < ret.data.length; i++) {
if (ret.data[i].pos != 0 && ret.data[i].instId.endsWith("USDT-SWAP")) {
let dir=PD_LONG;
if(ret.data[i].posSide=="long")
dir=PD_LONG;
if(ret.data[i].posSide=="short")
dir=PD_SHORT;
if(ret.data[i].posSide=="net"){
dir=ret.data[i].pos>0?PD_LONG:PD_SHORT;
}

positions.push([{
Symbol: ret.data[i].instId.substring(0, ret.data[i].instId.lastIndexOf("USDT")-1) + "_USDT",
Amount: Number(Math.abs(ret.data[i].pos)),
FrozenAmount: 0,
Price: Number(ret.data[i].avgPx),
Profit: Number(ret.data[i].upl),
Type: dir,
ContractType: "swap",
Margin: Number(ret.data[i].margin),
LevelRate: Number(ret.data[i].lever)

}]);
}
}
// Merge positions of the same currency (same currency, long and short two-way positions)
if (positions. length >= 2) {
for (i = 0; i < positions.length; i++) {
for (var j = i + 1; j < positions.length; j++) {
if (positions[i][0].Symbol == positions[j][0].Symbol) {
positions[i].push(JSON.parse(JSON.stringify(positions[j][0])));
positions.splice(j, 1); // Delete the same currency
break;
}
}
}
}

return positions;
}
```

> Detail

https://www.fmz.com/strategy/388189

> Last Modified

2022-11-07 22:51:51