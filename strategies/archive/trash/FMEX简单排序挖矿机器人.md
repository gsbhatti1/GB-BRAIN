> Name

FMEX Simple Sorting Mining Robot

> Author

Little Grass

> Strategy Description

For specific reference: https://www.fmz.com/digest-topic/5843

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|Intervel|2|Sleep time|
|Amount|10|Order volume|
|CoverProfit|-10|Close profit threshold|
|ProfitTime|60|Interval for printing profits|
|Url|https://api.fmextest.net|API base address|


> Source (javascript)

``` javascript
exchange.SetBase(Url)
if(exchange.GetName() != 'Futures_FMex'){
    throw 'This strategy only supports FMEX Futures'
}

var account = null;
var depth = null;
var pos = {direction: 'empty', price: 0, amount: 0, unrealised_profit: 0};

// Official mining coefficient, can be set according to needs, such as increasing the larger the farther from the order book, reducing transaction risk
var factors = [1/4, 1/40, 1/40,1/40,1/40,1/50,1/50,1/50,1/50,1/50,1/100,1/100,1/100,1/100,1/100];
var total_efficiency = 0; // Total efficiency
var avg_efficiency = 0;
var avg_num = 0;

var ordersInfo = {buy:[], sell:[]}; // id:0, price:0, amount:0}
var coverInfo = {buyId:0, buyPrice:0, sellId:0, sellPrice:0};
var depthInfo = [];
var lastProfitTime = 0; // Control profit printing time
var lastRestTime = Date.now();   // Scheduled reset of the strategy
var lastLogStatusTime = 0;
var lastPeriod = 0;
var today = _D().slice(8,11);

updateAccount();

var total_back = 0;
if(_G('total_back')){
    total_back = _G('total_back');
}else{
    _G('total_back', total_back);
}
var init_value = 0;
if(_G('init_value')){
    init_value = _G('init_value');
}else{
    init_value = _N(account.Info.data.BTC[0] + account.Info.data.BTC[1] + account.Info.data.BTC[2], 6);
    Log('First start of the strategy, initial total value: ', init_value);
    _G('init_value', init_value);
}

function updateDepth(){
    var data = exchange.GetDepth();
    if(data){
        depth = data;
    }else{
        Log('Error getting depth');
    }
}

function updateAccount(){
    var data = exchange.GetAccount();
    if(data){
        account = data;
    }else{
        Log('Error getting account');
    }
}

function updatePosition(){
    var data = exchange.GetPosition();
    if(data){
        if(data.length > 0){
            if(data[0].Info.direction != pos.direction || data[0].Info.quantity != pos.amount){
                Log('Position change: ', pos.direction + ' ' + pos.amount + ' -> ' + data[0].Info.direction + ' ' + data[0].Info.quantity);
            }
            pos = {direction: data[0].Info.direction, price: data[0].Info.entry_price, amount: data[0].Info.quantity, unrealised_profit: data[0].Info.unrealized_pnl};
        }else{
            if(pos.amount){
                Log('Position change: ', pos.direction + ' ' + pos.amount + ' -> ' + 'empty');
            }
            pos = {direction: 'empty', price: 0, amount: 0, unrealised_profit: 0};
        }
    }else{
        Log('Error getting position');
    }
}

function calcDepth(){ 
    depthInfo = []; // price amount efficent ratio  
    var ask_price = depth.Asks[0].Price;
    var bid_price = depth.Bids[0].Price;
    total_efficiency = 0;
    for(var i=0;i<15;i++){
        var factor = factors[i];
        total_efficiency += 1000000 * (Amount * 2 / (depth.Asks[i].Amount + depth.Bids[i].Amount)) * factor * 0.5 / 288;
        while(ask_price <= depth.Asks[i].Price){ // Considering unoccupied depth positions
            var my_ask_amount = _.findWhere(ordersInfo.sell, {price: ask_price}) ? _.findWhere(ordersInfo.sell, {price: ask_price}).amount : 0; // Excluding own orders' interference
            var ask_amount = ask_price == depth.Asks[i].Price ? Math.max(depth.Asks[i].Amount - my_ask_amount, 0) : 0;
            depthInfo.push({side: 'sell', pos: i+1, price: ask_price, amount: ask_amount, factor: factor, my_amount: 0, e: 0, r: 0});
            ask_price += 0.5;
        }
    }
    for(var i=0;i<15;i++){
        var factor = factors[i];
        total_efficiency += 1000000 * (Amount * 2 / (depth.Asks[i].Amount + depth.Bids[i].Amount)) * factor * 0.5 / 288;
        while(bid_price >= depth.Bids[i].Price){
            var my_bid_amount = _.findWhere(ordersInfo.buy, {price: bid_price}) ? _.findWhere(ordersInfo.buy, {price: bid_price}).amount : 0;
            var bid_amount = bid_price == depth.Bids[i].Price ? Math.max(depth.Bids[i].Amount - my_bid_amount, 0) : 0;
            depthInfo.push({side: 'buy', pos: i+1, price: bid_price, amount: bid_amount, factor: factor, my_amount: 0, e: 0, r: 0});
            bid_price -= 0.5;
        }
    }
}

function calcAmount(){
    var total_amount = Amount;
    var per_amount = _N(Amount / 100, 0);
    var max_id = 0;
    while(total_amount >= per_amount){
        var max_e = 0;
        for(var i=0;i<30;i++){
            if(depthInfo[i].amount == 0){
                depthInfo[i].my_amount = per_amount;
            }else{
                depthInfo[i].e = depthInfo[i].factor * depthInfo[i].amount / Math.pow(depthInfo[i].my_amount + per_amount + depthInfo[i].amount, 2);
                max_id = depthInfo[i].e > max_e ? i : max_id;
                max_e = depthInfo[i].e > max_e ? depthInfo[i].e : max_e;
            }
        }
        depthInfo[max_id].my_amount += per_amount;     
        total_amount -= per_amount;
    }
}

function makeOrders(){
    var e = 0;
    var new_orders = {buy:[], sell:[]};
    for(var i=0;i<30;i++){
        if(depthInfo[i].my_amount > 0){
            var find = _.findWhere(ordersInfo[depthInfo[i].side], {price: depthInfo[i].price});
            // Log(find);
            var now_amount = find ? find.amount : 0;
            var now_id = find ? find.id : 0;
            if(Math.abs(now_amount - depthInfo[i].my_amount) > 2.1 * Amount / 100 || depthInfo[i].amount == 0){ // Need to place a new order
                if(now_id){
                    exchange.CancelOrder(now_id, find);
                    find.id = 0;
                }
                if(depthInfo[i].my_amount > 0){
                    exchange.SetDirection(depthInfo[i].side);
                    
                    var id = exchange[depthInfo[i].side == 'buy' ? 'Buy' : 'Sell'](depthInfo[i].price, depthInfo[i].my_amount);
                    if(id){ 
                        new_orders[depthInfo[i].side].push({price: depthInfo[i].price, amount: depthInfo[i].my_amount, id: id});
                    }
                }
            }else{
                now_id = find ? find.id : 0;
                if(now_id){
                    new_orders[depthInfo[i].side].push(find);
                }
```