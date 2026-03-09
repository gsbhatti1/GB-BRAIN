> Name

Bybit-Arbitrage-Pin-Strategy-VWAP-BTC

> Author

Beanzi

> Strategy Description

Here begins the sharing of the original Bybit pin strategy version.
What is the main reason for this?///
 ![IMG](https://www.fmz.com/upload/asset/95a9985fc126e73d27e9.png) 
 
This is quite frustrating...
You said you would open-source it, but I got upset without knowing the situation...
I hope the elder brother doesn't do this again.
Here, I'm directly open-sourcing it.
It's not a particularly impressive strategy...

Everyone can play with it随意!
Don't waste money on my junk source code!
Just use it! Let's go!

And an ad for you~
For more ways to lose money, please follow the public account "Beanzi's Quantitative Log"
WX: wangxiaoba

(●'◡'●)

> Strategy Arguments


|Argument|Default|Description|
|---|---|---|
|start_balance|false|Initial balance|
|long_qty|true|Single long USD quantity|
|short_qty|true|Single short USD quantity|
|maxPosition|500000|Maximum order volume|
|take_profit|45|Initial take profit (USD)|
|trailing_profit|true|Trailing take profit (USD)|
|stop_loss|9|Stop loss percentage|
|long_vwap_offset|2.5|VWAP upper boundary percentage|
|short_vwap_offset|2.5|VWAP lower boundary percentage|
|GG|3|Leverage multiple (2x-7x is appropriate, higher leverage means higher risk)|
|stop_step|3600|Stop loss time to stop (s)|


> Source (javascript)

``` javascript
// User authentication (UID list + getAccount UID validation)
function user_auth() {
    user_list = [775536, 783571, 789086, 819490, 1265698, 1294567, 1299150]
    user_id = account.Info.result[0].user_id
    //Log(user_id)
    if (user_list.indexOf(user_id) == -1) {
        throw new Error('User authentication error, please contact WeChat: wangxiaoba')
    }
}

// Calculate and get VWAP and upper/lower boundaries Bybit
function VWAP() {
    // Define candlestick, calculate VWAP
    if (records.length > 1440) {
        records.splice(0, 1);
    }
    var n = records.length - 1
    //Log(n)
    var total_sum = 0.0
    var volume_sum = 0
    vwap_arr = []
    vwap_up_arr = []
    vwap_dw_arr = []
    for (var i = 0; i < n + 1; i++) {
        var high_price = records[i].High
        //Log("log high_price " + high_price)
        var low_price = records[i].Low
        var close_price = records[i].Close
        //Log("log low_price " + low_price)
        var price = (high_price + low_price + close_price) / 3
        //Log("price", price)
        var volume = records[i].Volume
        //Log("log volume " + volume)
        total_sum += price * volume
        //Log("log total_sum " + total_sum)
        volume_sum += volume
        //Log("log volume_sum " + volume_sum)
        var re = total_sum / volume_sum
        var re_up = re * (1 + long_vwap_offset / 100)
        var re_dw = re * (1 - short_vwap_offset / 100)
        vwap_arr.push(re)
        vwap_up_arr.push(re_up)
        vwap_dw_arr.push(re_dw)
        //return total_sum / volume_sum
    }
    if (vwap_arr.length > 2000) {
        vwap_arr.splice(0, 1);
    }
    if (vwap_up_arr.length > 2000) {
        vwap_up_arr.splice(0, 1);
    }
    if (vwap_dw_arr.length > 2000) {
        vwap_dw_arr.splice(0, 1);
    }
    vwap = vwap_arr[vwap_arr.length - 1]
    vwap_up = vwap_up_arr[vwap_arr.length - 1]
    vwap_dw = vwap_dw_arr[vwap_arr.length - 1]
    //Log("log vwap " + vwap, "log vwap_up " + vwap_up, "log vwap_dw " + vwap_dw)
}

// Plot lines
function PlotMA_Kline(records, isFirst) {
    $.PlotRecords(records, "K")
    if (isFirst) {
        for (var i = records.length - 1; i >= 0; i--) {
            if (vwap_arr[i] !== null) {
                $.PlotLine("vwap", vwap_arr[i], records[i].Time)
                $.PlotLine("vwap_up", vwap_up_arr[i], records[i].Time)
                $.PlotLine("vwap_dw", vwap_dw_arr[i], records[i].Time)
            }
        }
        PreBarTime = records[records.length - 1].Time
    } else {
        if (PreBarTime !== records[records.length - 1].Time) {
            $.PlotLine("vwap", vwap_arr[vwap_arr.length - 2], records[records.length - 2].Time)
            $.PlotLine("vwap_up", vwap_up_arr[vwap_up_arr.length - 2], records[records.length - 2].Time)
            $.PlotLine("vwap_dw", vwap_dw_arr[vwap_dw_arr.length - 2], records[records.length - 2].Time)
            PreBarTime = records[records.length - 1].Time
        }
        $.PlotLine("vwap", vwap_arr[vwap_arr.length - 1], records[records.length - 1].Time)
        $.PlotLine("vwap_up", vwap_up_arr[vwap_up_arr.length - 1], records[records.length - 1].Time)
        $.PlotLine("vwap_dw", vwap_dw_arr[vwap_dw_arr.length - 1], records[records.length - 1].Time)
    }
}

// Place order, buy/sell Bybit
// Define Buy
function buy(Price, Amount, dec) {
    exchange.SetDirection("buy");
    var orderId = null;
    orderId = exchange.Buy(Price, Amount, dec, '@');
    while (!orderId && typeof(orderId) != "undefined" && orderId != 0) {
        Log(orderId);
        Sleep(100);
        orderId = exchange.Buy(Price, Amount, dec, '@');

    }
    return orderId;
}

// Define Sell
function sell(Price, Amount, dec) {
    exchange.SetDirection("sell");
    var orderId = null;
    orderId = exchange.Sell(Price, Amount, dec, '@');
    while (!orderId && typeof(orderId) != "undefined" && orderId != 0) {
        Log(orderId);
        Sleep(100);
        orderId = exchange.Sell(Price, Amount, dec, '@');

    }
    return orderId;
}

// Account information
function AccountInfo() {
    // Asset information table
    var AccountTab = {
        type: "table",
        title: "Asset Information",
        cols: ["Position", "Direction", "Average Entry Price", "Current Price", "Liquidation Price", "Leverage", "Position Profit/Loss", "Initial Balance", "Total Asset", "Net Asset", "Total Profit/Loss"],
        rows: [],
    }
    AccountTab.rows.push([account.Info.result[0].size, CW, account.Info.result[0].entry_price, ticker.Last, account.Info.result[0].liq_price, account.Info.result[0].leverage, account.Info.result[0].unrealised_pnl, start_balance, account.Info.result[0].wallet_balance, jzc, pt])
    LogStatus(_D() + '   STATUS: ' + CW + '\n' +
        'Total available order volume (* leverage): ' + yue + '\n' +
        'index: ' + index + '\n' +
        'VWAP: ' + vwap + '\n' +
        'VWAP_UP: ' + vwap_up + '\n' +
        'VWAP_DW: ' + vwap_dw + '\n' +
        'N: ' + records.length + '\n' +
        'WX: wangxiaoba' + '\n' +
        '`' + JSON.stringify([AccountTab]) + '`' + '\n');
}

// Status judgment
function Status() {
    if (account.Info.result[0].side === "Buy") {
        status = PD_LONG;
        CW = "LONG";
    } else if (account.Info.result[0].side === "Sell") {
        status = PD_SHORT;
        CW = "SHORT";
    } else {
        status = idle;
        CW = "IDLE";
    }
}

// Trailing take profit initial %, trailing U
function TP() {
    var TP_first_long = account.Info.result
``` 

It looks like the `TP` function was cut off. If you need the completion of the `TP` function, please provide the rest of the code so I can finish it for you. Here is what it might look like based on the context:

```javascript
// Trailing take profit initial %, trailing U
function TP() {
    var TP_first_long = account.Info.result[0].entry_price + (account.Info.result[0].entry_price * take_profit / 100);
    var TP_current_long = vwap_up_arr[vwap_up_arr.length - 1];
    if (status === PD_LONG) {
        if (account.Info.result[0].price <= TP_current_long) {
            // Execute take profit order
        }
    }
    // Similar logic for short positions
    if (status === PD_SHORT) {
        var TP_first_short = account.Info.result[0].entry_price - (account.Info.result[0].entry_price * take_profit / 100);
        var TP_current_short = vwap_dw_arr[vwap_dw_arr.length - 1];
        if (account.Info.result[0].price >= TP_current_short) {
            // Execute take profit order
        }
    }
}
```

Please let me know if you need any further modifications or additional details!