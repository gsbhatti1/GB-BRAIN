``` javascript
//Arguments:
//1. StartPrice
//2. EndPrice
//3. MinOrderCoinSize

// noinspection SillyAssignmentJS
CoinSymbol = CoinSymbol;
// noinspection SillyAssignmentJS
StartPrice = StartPrice;
// noinspection SillyAssignmentJS
EndPrice = EndPrice;
// noinspection SillyAssignmentJS
StartPositionRate = StartPositionRate; //0.3
// noinspection SillyAssignmentJS
EndPositionRate = EndPositionRate; //0.7
// noinspection SillyAssignmentJS
GridPercentage = GridPercentage; //0.05
// noinspection SillyAssignmentJS
MinOrderAmount = MinOrderAmount;
// noinspection SillyAssignmentJS
Reset = Reset;

let varA = (EndPositionRate - StartPositionRate) / (StartPrice - EndPrice);
let varB = EndPositionRate - StartPrice * varA;
let buyVarA = varA / (1 - GridPercentage / 100);
let sellVarA = varA / (1 + GridPercentage / 100);

function getPositionRate(varA, price) {
    if (price < StartPrice) {
        price = StartPrice;
    }
    if (price > EndPrice) {
        price = EndPrice;
    }
    return varA * price + varB;
}

function getAmounts(coinSize, currency, currentPrice, minOrderCoinSize) {
    let buyPrice = currentPrice - 5;
    let buyPositionRate = getPositionRate(buyVarA, buyPrice);
    let buyCoin = buyPositionRate * (coinSize * buyPrice + currency) / buyPrice - coinSize;
    buyCoin = buyCoin > minOrderCoinSize ? buyCoin : minOrderCoinSize;
    let sellPrice = currentPrice + 5;
    let sellPositionRate = getPositionRate(sellVarA, sellPrice);
    let sellCoin = sellPositionRate * (coinSize * sellPrice + currency) / sellPrice - coinSize;
    sellCoin = sellCoin < -minOrderCoinSize ? sellCoin : -minOrderCoinSize;
    return [buyCoin, sellCoin];
}

function getPrice(coinSize, currency, amount) {
    let varA = amount < 0 ? sellVarA : buyVarA;
    // Log("(" + (coinSize + amount) + " * y) / (" + coinSize + " * y + " + currency + ") = " + varA + " * y + " + varB);
    // ((coinSize + amount) * y) / (coinSize * y + currency) = varA * y + varB;
    // Log("(" + (coinSize + amount) + " * y)  = " + (varA * coinSize) + " * y^ + " + ((varA * currency) + (varB * coinSize)) + " * y + " + (varB * currency));
    //((coinSize + amount) * y)  = varA * coinSize * y^ + ((varA * currency) + (varB * coinSize)) * y + (varB * currency)
    // Log("y^2 + " + (((varA * currency) + (varB * coinSize) - (coinSize + amount)) / (varA * coinSize)) + " * y  =  " + (-(varB * currency) / (varA * coinSize)));
    // y^ + (((varA * currency) + (varB * coinSize) - (coinSize + amount))/(varA * coinSize)) * y  =  -(varB * currency)/(varA * coinSize)
    let k = (varA * currency + varB * coinSize - coinSize - amount) / (2 * varA * coinSize);
    let l = Math.sqrt(-((varB * currency) / (varA * coinSize)) + Math.pow(k, 2));
    let p1 = -l - k;
    let p2 = l - k;
    let price;
    if (p1 > 0 && p2 > 0) {
        price = amount < 0 ? Math.max(p1, p2) : Math.min(p1, p2);
    } else {
        price = Math.max(p1, p2);
    }

    let z = (coinSize + amount) * price / (coinSize * price + currency);
    let z1 = varA * StartPrice + varB;
    let z2 = varA * EndPrice + varB;
    if (z > z1) {
        price = z1 * currency / (coinSize + amount - z1 * coinSize)
    } else if (z < z2) {
        price = z2 * currency / (coinSize + amount - z2 * coinSize)
    }
    return parseInt(price);
}

let pricesChart = Chart([ // This chart in JavaScript is an object. Before using the Chart function, we need to declare a configuration variable for the chart.
    {
        __isStock: true, // Mark whether it's a regular chart. You can change this to false and run to see the difference.
        tooltip: {
            xDateFormat: '%Y-%m-%d %H:%M:%S, %A'
        }, // Range selector
        title: {
            text: 'Profit Analysis Chart'
        }, // Title
        rangeSelector: { // Selecting a range
            buttons: [{
                type: 'hour',
                count: 1,
                text: '1h'
            }, {
                type: 'hour',
                count: 3,
                text: '3h'
            }, {
                type: 'hour',
                count: 8,
                text: '8h'
            }, {
                type: 'all',
                text: 'All'
            }],
            selected: 0,
            inputEnabled: false
        },
        xAxis: {
            type: 'datetime'
        }, // X-axis, the current type is : time.
        yAxis: { // Y-axis, default values adjust according to data size.
            title: {
                text: 'Profit'
            }, // Title
            opposite: false, // Whether to enable the right Y-axis
        },
        series: [ // Data series, this property stores various data series (lines, candlestick charts, labels, etc.)
            {
                name: "Zero",
                id: "Zero",
                dashStyle: 'shortdash',
                data: []
            }, {
                name: "Strategy Profit",
                id: "Strategy Profit",
                data: []
            }, {
                name: "Spot Profit",
                id: "Spot Profit",
                data: []
            }
        ]
    }]);

function GetOrders() {
    let ordersResp = exchange.IO("api", "GET", "/v2/private/order", "symbol=" + CoinSymbol + "USD");
    if (!ordersResp || ordersResp.ret_code !== 0) {
        return false;
    }
    let orderIds = [];
    for (let i = 0; i < ordersResp.result.length; i++) {
        orderIds.push(ordersResp.result[i].order_id);
    }
    return orderIds;
}

function GetFilledOrder(orderId) {
    let orderResp = exchange.IO("api", "GET", "/v2/private/order", "symbol=" + CoinSymbol + "USD&order_id=" + orderId);
    if (!orderResp || orderResp.ret_code !== 0 || orderResp.result.order_status !== "Filled") {
        return false;
    }
    let amount = orderResp.result.qty;
    amount = orderResp.result.side === "Sell" ? -amount : amount;
    return [orderResp.result.price, amount];
}

function sell(price, amount) {
    let createOrderResp = exchange.IO("api", "POST", "/v2/private/order",
```