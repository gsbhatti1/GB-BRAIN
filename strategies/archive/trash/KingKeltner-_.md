Name

KingKeltner Trend Strategy_Low Frequency

Author

ipqhjjybj


Source (javascript)

``` javascript
/*
Strategy source: vnpy
Strategy name: KingKeltner Trend Strategy
Strategy author: ipqhjjybj
Strategy description:
trend following strategy

*/

KK_Length = 11 // Number of windows to calculate the value in the channel
kkDev = 1.3 // Calculate the deviation of the channel width
trailingPrcnt = 15 // trailing stop loss
LoopInterval = 60 // Polling interval (seconds)
SlidePrice = 0.3 // sliding price (yuan)
function adjustFloat(v) {
return Math.floor(v*1000)/1000;
}

function CancelPendingOrders() {
while (true) {
var orders = null;
while (!(orders = exchange.GetOrders())) {
Sleep(Interval);
}

if (orders.length == 0) {
return;
}

for (var j = 0; j < orders.length; j++) {
exchange.CancelOrder(orders[j].Id, orders[j]);
if (j < (orders.length-1)) {
Sleep(Interval);
}
}
}
}

function GetAccount() {
var account;
while (!(account = exchange.GetAccount())) {
Sleep(Interval);
}
return account;
}

function GetTicker() {
var ticker;
while (!(ticker = exchange.GetTicker())) {
Sleep(Interval);
}
return ticker;
}

var intraTradeHigh = 0; // moving high price
var intraTradeLow = 99999999; // Mobile lowest price
var LastBuyPrice = 0; // Last purchase price
var LastSellPrice = 0; // Last selling price
var minMoney = 100; // If the funds are less than this value, no buying
var LastRecord = null; // Initialize the previous record
function onTick(exchange) {

var ticker = GetTicker();
// Buy or Sell, Cancel pending orders first
CancelPendingOrders();
var account = GetAccount();

if (true) {
var records = exchange.GetRecords();
if (!records || records.length < (KK_Length + 3)) {
return;
}
// Price not change
var newLast = records[records.length-1];
if ((!LastRecord) || (LastRecord.Time == newLast.Time && LastRecord.Close == newLast.Close)) {
LastRecord = newLast;
return;
}
LastRecord = newLast;

//Log(newLast);
var kk_ATR = TA.ATR(records, KK_Length);
var kk_Mid = TA.MA(records, KK_Length);
var kk_Up = kk_Mid[kk_Mid.length-1] + kk_ATR[kk_ATR.length-1] * kkDev;
//var kk_Down= kk_Mid - kk_ATR * kkDev

//Log("LastRecord.Close",LastRecord.Close,"kk_up",kk_Up,"intraTradeHigh",intraTradeHigh);
if( account.Stocks <= exchange.GetMinStock() ){
if(LastRecord.Close > kk_Up){
Log("start buy");
var price = ticker.Last + SlidePrice;
var amount = adjustFloat(account.Balance / price);
if (account.Balance > minMoney && amount >= exchange.GetMinStock()) {
if (exchange.Buy(price, amount, "Buy")) {
intraTradeHigh = LastRecord.High
intraTradeLow = LastRecord.Low
LastBuyPrice = LastHighPrice = price;
}
}
}
}
else if( exchange.GetMinStock() < account.Stocks ){
Log("Close",LastRecord.Close, "intraTradeHigh",intraTradeHigh ,"intraTradeHigh * ( 1 - trailingPrcnt)",intraTradeHigh * ( 1 - trailingPrcnt/100.0))
intraTradeHigh = Math.max(intraTradeHigh , LastRecord.High)
intraTradeLow = LastRecord.Low
if(LastRecord.Close < intraTradeHigh * ( 1 - trailingPrcnt/100.0)){ // Trailing Stop
Log("start sell");
var price = ticker.Last - SlidePrice;
var sellAmount = account.Stocks;
if (sellAmount > exchange.GetMinStock()) {
exchange.Sell(ticker.Last - SlidePrice, sellAmount, "Sell");
LastSellPrice = LastLowPrice = price;
}
}
}
}
}


function main() {
InitAccount = GetAccount();
Log(exchange.GetName(), exchange.GetCurrency(), InitAccount);

LoopInterval = Math.max(LoopInterval, 1);
while (true) {
onTick(exchange);
Sleep(LoopInterval*1000);
}
}
```

Detail

https://www.fmz.com/strategy/42283

Last Modified

2017-06-02 23:06:08