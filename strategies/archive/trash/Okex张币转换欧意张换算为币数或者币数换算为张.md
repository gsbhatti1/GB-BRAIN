```markdown
Name

Okex Zhang Coin Conversion European and Italian Zhangs are converted into coins or coins are converted into Zhangs

Author

Exodus[strategy ghostwriting]

Strategy Description

As in the title:
![IMG](https://www.fmz.com/upload/asset/1f4d7d7de4354276de970.png)
![IMG](https://www.fmz.com/upload/asset/1f448a3f706ccc2712c15.png)
![IMG](https://www.fmz.com/upload/asset/1f43c354a217fb6575477.png)
![IMG](https://www.fmz.com/upload/asset/1f4073ba260e47fcc5a3c.png)

By the way, I will undertake the ghostwriting of strategies.


Source (javascript)

``` javascript
//test module
//The link can be initiated by any exchange, just pass in the corresponding currency pair name, price, quantity, etc.
function main() {

let currency=_C(exchange.GetCurrency);//Currency pair name

let curPrice=_C(exchange.GetTicker).Last;//Current price

let atz=AmountToZhang(currency,curPrice,1);//How many coins are equal to one currency?

let zta=ZhangToAmount(currency,curPrice,1);//How many coins is one piece worth?


Log(currency+"1 currency is equal to "+atz+" Zhang,","1 currency is equal to "+zta+" currency");

}

//Coin transfer
//currency represents the name of the currency pair, px represents the price at conversion, sz represents the number of coins, and the number of coins is calculated based on the number of coins (leverage is not calculated)
function AmountToZhang(currency,px,sz){

//ok The trading pair format when requested by the exchange is ETH-USDT-SWAP, not ETH_USDT, so please note that the underscore in instId must be converted to -, which is a minus sign
let instId=currency.replace("_","-")+"-SWAP";


let str="https://www.okx.com/api/v5/public/convert-contract-coin?"+"instId="+instId+"&px="+px+"&sz="+sz;
let ret=JSON.parse(HttpQuery(str));

Log("Coin transfer HTTP link"+str,"Return result:"+JSON.stringify(ret));


return ret.data[0].sz;//Return how many coins correspond to one coin

}

//Zhang transfer coins, indicating how many coins one corresponds to
//currency represents the name of the currency pair, px represents the price during conversion, sz represents the number of coins, and the number of coins is obtained by passing in the number of coins (leverage is not calculated)
function ZhangToAmount(currency,px,sz){
//ok The trading pair format when requested by the exchange is ETH-USDT-SWAP, not ETH_USDT, so please note that the underscore in instId must be converted to -, which is a minus sign
let instId=currency.replace("_","-")+"-SWAP";

let str="https://www.okx.com/api/v5/public/convert-contract-coin?"+"type=2&instId="+instId+"&px="+px+"&sz="+sz;
let ret=JSON.parse(HttpQuery(str));

Log("Zhang Zhuanbi Http link"+str,"Return result:"+JSON.stringify(ret));


return ret.data[0].sz;//Note that the result does not calculate leverage. For example, if one piece of BCH is OK, the corresponding number of coins is 10. If you want to place an order for coins with the same amount of margin on other exchanges, you must calculate the leverage, that is, place 10/20 (leverage), 0.5 coins.

}
```


Detail

https://www.fmz.com/strategy/387901

Last Modified

2022-10-29 18:47:50
```