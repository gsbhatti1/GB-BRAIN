``` markdown
---
**Name:** TradingView下单机器人11

**Author:** 夏天不打你

**Strategy Description:** 
This is a self-used TradingView order bot with the following features:
1. Supports order placement on Huobi, OKEx, and Binance for both coin-based quarter contracts and USDT perpetual contracts.
2. Supports both single-order and compound-order modes.
3. Supports limit order with counteroffer spread and market order.
4. Supports concurrent order placement in multiple threads.
5. Comprehensive data statistics.
6. All data is locally saved and recoverable.

**This order bot requires server-side use. Download from:**
Link: [Download](https://pan.baidu.com/s/1RK08Ht4cAOAwTSb6X2TA4A)
Extract Code: 3qo6

**Usage:**
Send order commands via TV script as follows:
```
order_message2 = 'TradingView:order:ticker=OKEX:ETHUSDT' + ' levelRate=' + tostring(level_rate) + ' price=' + tostring(order_price) + ' size=' + tostring(order_size) + ' type=1' + ' robot=' + tostring(order_robot)
strategy.entry(id = "long", long = true, comment="做多", alert_message = order_message2)
```
`levelRate` represents the leverage multiplier, `price` represents the price, and `size` represents the number of contracts. `order_robot` is the number of the bot created by the inventor.
The main points to note are the values of `type`. `1` indicates long open, `2` indicates short open, `3` indicates long close, `4` indicates short close, `5` indicates long close and short open, and `6` indicates short close and long open.
The above code should be **inserted into the script of the TV strategy** at the point where an order needs to be placed.

Create an alert in the strategy, and fill in the webhook address with the IP address of the server running the server, and the message with `{{strategy.order.alert_message}}`. Other parameters can be set to default.

**Strategy Arguments:**

|Argument|Default|Description|
|----|----|----|
|Interval|1000|(?Basic Settings) Program execution cycle (ms)|
|Currency|ETH_USDT|Trading pair|
|MarginLevel|4|Leverage|
|IsUseHuobiOrder|false|Use Huobi USDT perpetual contract order|
|IsUseBinanceOrder|true|Whether to use Binance USDT perpetual contract order|
|UseQuarter|false|Use quarter contract|
|IsMarketOrder|true|Market order|
|UseOrderSync|false|(?Advanced Settings) Use multi-thread order placement|
|UseOpponentOrder|false|Use counteroffer order|
|OpponentSlip|0.01|Counteroffer order spread|
|OpponentOrderTime|600|Maximum hanging time for counteroffer order (s)|
|UseSameTicker|false|Use the same trading market|
|InitAsset|1,2,3,4,5,6,7,8,9,10|Initial assets|
|OrderSize|1,2,3,4,5,6,7,8,9,10|Order size|
|UseMutiOrderSize|false|Use different order sizes (fixed size)|
|UseAutoAdjustOrderSize|false|Automatically calculate order size|
|ThePercentOfAssetToOrder|0.5|Percentage of assets used for order|
|UseAllInOrder|false|Full position mode (compound interest)|
|UseLimitMaxOrderAmount|false|Whether to limit order amount|
|LimitMaxOrderAmount|1400|Maximum order amount (USDT)|
|EnablePlot|true|Enable chart drawing|
|KPeriod|60|Chart period (min)|
|PricePrecision|5|(?Order Settings) Price precision|
|AmountPrecision|false|Quantity precision|
|OneSizeInCurrentCoin|true|One contract represents the number of coins in U position|
|QuarterOneSizeValue|10|One contract represents the USDT value in coin position|
|UseAutoTransfer|true|(?Automatic Transfer) Use automatic transfer|
|UseCertainAmountTransfer|true|Fixed transfer|
|AccountMaxBalance|1100|Automatically transfer 100U when assets exceed *U|
|UseProfitToTransfer|false|Transfer based on profit (double transfer)|
|ProfitPercentToTransfer|90|Double transfer profit percentage|

**Buttons:**

|Button|Default|Description|
|----|----|----|
|LogPrint|Fixed some bugs.|Output logs|
|SaveLocalData|false|Save data to local|
|ClearLocalData|-1|Clear local data|
|ClearLog|true|Clear log information|
|LogStatusRefreshTime|5|Status bar update interval (s)|
|SetStrategyRunTime|1627747200|Set the start timestamp of the strategy (s)|
|SetUserStartTime|0,1627747200|Set user start time|
|SetUserInitAsset|0,1000|Set user initial assets|
|AdjustOrderSize|-1|Automatically adjust order size|
|ManualOrder|-1,longopen,1|Manual order|

**Source (JavaScript):**

``` javascript
/*
Order Bot 1.1
Version: 1.1
Author: summer
Date: 2021.9.9
Additions:
1. Multiple accounts with different order sizes
2. Counteroffer limit order (short positions still use market order to close)
3. Quarter contract backtesting statistics
4. Multiple accounts profit and loss statistics
5. Account data localization
6. Table display of status information
7. Multi-thread order placement
8. Add manual order interaction
9. Fix issue with incorrect profit statistics
*/

// Order settings
var _PricePrecision = PricePrecision;                           // Price precision for orders
var _AmountPrecision = AmountPrecision;                         // Quantity precision for orders
var _OneSizeInCurrentCoin = OneSizeInCurrentCoin;               // In U position, one contract represents the number of coins
var _QuarterOneSizeValue = QuarterOneSizeValue;                 // In coin position, one contract represents the USDT value

// Auto-transfer settings
var _UseAutoTransfer = UseAutoTransfer;                         // Use auto transfer
var _UseCertainAmountTransfer = UseCertainAmountTransfer;       // Fixed transfer
var _AccountMaxBalance = AccountMaxBalance;                     // Transfer 100U when assets exceed *U
var _UseProfitToTransfer = UseProfitToTransfer;                 // Transfer based on profit (double transfer)
var _ProfitPercentToTransfer = ProfitPercentToTransfer;         // Double transfer profit percentage

var _OKCoin = "Futures_OKCoin";
var _QuantitativeOrderHeader = "Quantitative:order:";
var _OrderSize = [];
var _InitAsset = [];
var _Accounts = [];
var _Positions = [];

var ProfitLocal = [];
var TotalAsset = [];
var TakeProfitCount = [];
var StopLossCount = [];
var WinRate = [];
var MaxLoss = [];
var MaxLossPercent = [];
var MaxProfit = [];
var MaxProfitPercent = [];
var ProfitPercent = [];
var _TransferAmount = [];
var _CurrentInitAssets = [];
var UserStartTime = [];
var UserDatas = [];
var StrategyRunTimeStampString = "strategy_run_time";
var StrategyDatas = { start_run_timestamp: 0, others: "" };

var _ClosePrice = 0;
var _MarginLevel = MarginLevel;

var _TradingFee = 0.0005;
var _RemainingSize = 20;            // When in full position mode, reserve a number of positions to avoid order failure due to large price fluctuations
var _IsOpponentOrder = false;

var _LogStatusRefreshTime = 10;     // Status bar update cycle in seconds
var _LastBarTime = 0;               // Latest bar time

// Save the start running time of the program, in seconds
function saveStrategyRunTime() {
    var local_data_strategy_run_time = _G(StrategyRunTimeStampString);

    if (local_data_strategy_run_time == null) {
        StrategyDatas.start_run_timestamp = Unix();
        _G(StrategyRunTimeStampString, StrategyDatas.start_run_timestamp);
    }
    else {
        StrategyDatas.start_run_timestamp = local_data_strategy_run_time;
    }
}

// Set the start running time of the program, in seconds
function setStrategyRunTime(timestamp) {
    _G(StrategyRunTimeStampString, timestamp);
    StrategyDatas.start_run_timestamp = timestamp;
}

// Calculate the number of days between two timestamps, in seconds
function getDaysFromTimeStamp(start_time, end_time) {
    if (end_time < start_time)
        return 0;
    else
        return Math.round((end_time - start_time) / (1000 * 60 * 60 * 24));
}

// Save all account data to local
function saveUserDatasToLocal() {
    Log("已把所有账户数据保存到本地.");
    for (var i = 0; i < _Accounts.length; i++) {
        _G(_Accounts[i].GetLabel(), UserDatas[i]);
    }
}

// Read user data from local
function readUserDatasFromLocal() {
    for (var i = 0; i < _Accounts.length; i++) {
        var userData = _G(_Accounts[i].GetLabel());
        if (userData) {
            UserDatas[i] = userData;
            _InitAsset[i] = userData.init_assets;
            ProfitLocal[i] = userData.profit_local;
            MaxProfitPercent[i] = userData.max_profit_percent;
            MaxLossPercent[i] = userData.max_loss_percent;
            MaxProfit[i] = userData.max_profit;
            MaxLoss[i] = userData.max_loss;
            TakeProfitCount[i] = userData.take_profit_count;
            StopLossCount[i] = userData.stop_loss_count;
            UserStartTime[i] = userData.start_time;
            _OrderSize[i] = userData.order_size;
            _TransferAmount[i] = userData.transfer_amount;
            _CurrentInitAssets[i] = userData.current_init_assets;
        }
    }
}
```
```