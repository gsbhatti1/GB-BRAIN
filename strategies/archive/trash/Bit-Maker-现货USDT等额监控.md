> Name

Bit-Maker-Real-Time USDT Equal Monitoring

> Author

AutoBitMaker-ABM

> Strategy Description

**AutoBitMaker** officially launches a risk-free arbitrage strategy.
The principle of the strategy is to use spot and contract hedging. This process can also be done manually, but compared to manual operations, the BOT will capture the profit margins of all trading pairs in the market every day, with hundreds of transactions. This further releases your hands and reduces market risks.

The current code only monitors accounts; the source code is publicly disclosed, allowing users to check or utilize it themselves.
Monitor the USDT value of spot trading.

We are **AutoBitMaker**, abbreviated as **ABM Capital**. Please carefully verify our team name, WeChat ID, to distinguish us from imitations.
For now, we only communicate with domestic customers via WeChat and email; other methods like QQ will not be used.

The **ABM Team** currently offers three types of strategies:
* Futures Trading
* Spot Trading
* Arbitrage Trading

Our self-developed adaptive grid strategy is based on traditional grid strategy concepts but has been optimized through extensive real-time trading and backtest data. It features a smart dynamic rebalancing model and profit-taking positions, avoiding the high risks faced by traditional grids during one-sided markets with minimal position sizes to achieve good risk-adjusted returns.

The strategy configuration parameters are extremely rich; our team will allocate dedicated personnel to tailor unique parameter combinations for your account based on your risk and return requirements. We offer around-the-clock human and automated market monitoring.

We self-develop proprietary indexes, where each index includes multiple high-quality trading pairs with distinct weight distributions. Robots run adaptive grid strategies on these index sets, mitigating risks associated with single trading pairs experiencing one-sided markets.
In addition to the built-in static indexes, we define dynamic indexes for our index sets based on various selection models, selecting leading coins from different sectors further lowering risk.

A single account can simultaneously configure and run multiple single-asset and index-based trading pairs, both diversifying risks while aiding in profit-making under complex market conditions.

Currently, the team's strategy server cluster consists of 80 machines, with an additional 50 support servers. At an average rate of two checks per second, we quickly identify stop-loss conditions to exit positions swiftly when risk arises.

Utilizing a hybrid cloud architecture on Alibaba Cloud, Amazon Web Services, and Microsoft Azure, we separate management nodes from execution nodes, forming a cluster for redundancy assurance, ensuring smooth business operations and fund safety efficiently.

For trial use:
Based on your capital scale, we provide about 2 weeks of free running. During the trial phase, no commission will be charged.
Do not perform any operations when the Bot takes over your account; upon detecting any manual positions, all Bots will immediately exit.

Regarding commissions:
This depends on your capital size. We can discuss this after the trial run. If you sign up using our recommended link, we will charge a very low commission.

Contact Information:
1. Available for face-to-face talks nationwide
2. WeChat: DuQi_SEC/autobitmaker/autobitmaker_001/Shawn_gb2312/ABM_DD 
3. Email: liuhongyu.louie@autobitmaker.com/autobitmaker_master@autobitmaker.com

* Special Note (WeChat ID autobitmaker001 is not us! Nor do we call ourselves makebit! The correct WeChat ID is autobitmaker_001)

Submit a trial application via the WeChat Mini Program:
![WeChat Mini Program QR Code](https://www.fmz.cn![IMG](https://www.fmz.com/upload/asset/1281e73989f891ac26aa9.jpg))

> Strategy Arguments


|Argument|Default|Description|
|---|---|---|
|baseOriginalBalance|10000|Initial base balance|

> Source (javascript)

``` javascript
//exchanges[0] is spot

var chart = {
    __isStock: false,
    extension: {
        layout: 'single',
        col: 8,
        height: '300px'
    },
    tooltip: {
        xDateFormat: '%Y-%m-%d %H:%M:%S, %A'
    },
    title: {
        text: 'Account_Balance_Detail'
    },
    xAxis: {
        type: 'datetime'
    },
    yAxis: {
        title: {
            text: 'USDT'
        },
        opposite: false
    },
    series: []
};

function initChart() {
    chart.series.push({
        name: "Account_" + (Number(0)) + "_Detail",
        id: "Account_" + (Number(0)) + "_Detail",
        data: []
    });
}

function getChartPosition(avaliableMargin) {
    return {
        __isStock: false,
        extension: {
            layout: 'single',
            col: 4,
            height: '300px'
        },
        title: {
            text: 'Margin Ratio (%)'
        },
        series: [{
            type: 'pie',
            name: 'one',
            data: [{
                name: 'Available Margin (%)',
                y: avaliableMargin,
                color: '#dff0d8',
                sliced: true,
                selected: true
            }, {
                name: 'Occupied Margin (%)',
                y: 100 - avaliableMargin,
                color: 'rgb(217, 237, 247)',
                sliced: true,
                selected: true
            }]
        }]
    };
}

function updateAccountDetailChart(ObjChart, totalBalance) {
    var nowTime = new Date().getTime();
    var account = exchanges[0].GetAccount();
    try {
        if (account !== null && account.Info !== null && totalBalance > 0) {
            ObjChart.add([0, [nowTime, Number(totalBalance)]]);
        }
    } catch (err) {
        Log('ERROR ' + account + ',' + err)
    }
}

function getSpotBalanceInUSDT() {
    var ticker = JSON.parse(HttpQuery('https://api.binance.com/api/v1/ticker/24hr'));
    var currentBalance = 0;
    var account = exchanges[0].GetAccount();
    var priceMap = {};
    try {
        if (ticker !== null) {
            for (var index in ticker) {
                priceMap[ticker[index].symbol] = ticker[index].lastPrice;
            }
        }
        if (account !== null && account.Info !== null) {
            for (var index in account.Info.balances) {
                var obj = account.Info.balances[index];
                if (obj.asset !== 'USDT' && priceMap[obj.asset + 'USDT']) {
                    currentBalance += Number(Number(priceMap[obj.asset + 'USDT']) * Number((Number(obj.free) + Number(obj.locked))));
                }
                if (obj.asset === 'USDT') {
                    currentBalance += Number((Number(obj.free) + Number(obj.locked)));
                }
            }
        }
    } catch (err) {
        Log('ERROR ' + account + ',' + err)
    }
    Sleep(666);
    return Number(currentBalance).toFixed(6);
}

function printProfitInfo(currentBalance) {
    var profit = Number((currentBalance) - baseOriginalBalance).toFixed(5);
    var profitRate = Number((((currentBalance) - baseOriginalBalance) / baseOriginalBalance) * 100).toFixed(4);
    LogProfit(Number(profitRate), '&');
    Log('The current balance is ' + currentBalance + ', the profit is ' + profit + ', the profit rate is ' + profitRate + '%');
}

function printPositionInfo(exchangeInnerArray, totalProfitUSDT, totalProfitRate) {
    var totalProfit = 0.0
    var table = {
        type: 'table',
        title: 'POSITIONS',
        cols: ['Symbol', 'Type', 'CurrentPrice', 'Position', 'USDT Value'],
        rows: []
    }
    table.rows.push([{
        body: 'This strategy is a USDT-centric, low-risk smart dynamic parameter grid for spot trading.',
        colspan: 5
    }]);
    table.rows.push([{
        body: 'Any trading pair can be selected',
        colspan: 5
    }]);
    var ticker = JSON.parse(HttpQuery('https://api.binance.com/api/v1/ticker/24hr'));
    var account = exchanges[0].GetAccount();
    var priceMap = {};
    try {
        if (ticker !== null) {
            for (var index in ticker) {
                priceMap[ticker[index].symbol] = ticker[index].lastPrice;
            }
        }
        if (account !== null && account.Info !== null) {
            for (var index in account.Info.balances) {
                var obj = account.Info.balances[index];
                if (obj.asset !== 'USDT' && priceMap[obj.asset + 'USDT']) {
                    if (Number((Number(obj.free) + Number(obj.locked))) > 
```