> Name

Bit-Maker-Real-Time Monitoring of Total USDT Contract Balance for Spot Trading

> Author

AutoBitMaker-ABM

> Strategy Description

**AutoBitMaker** officially launches the risk-free arbitrage strategy.
The principle involves hedging between spot trading and contracts, which can also be manually completed. However, compared to manual operations, the BOT captures profit margins on all trading pairs in the market daily, executing hundreds of trades. This frees up your hands even more and reduces market risks.

We are **AutoBitMaker**, abbreviated as **ABM Capital**. Please carefully verify our team names, WeChat IDs, to distinguish authenticity.
For now, we communicate with domestic customers only via WeChat or email; other methods like QQ will not be used.

**ABM Team** currently offers three types of strategies:
- Contract Trading
- Spot Trading
- Arbitrage Trading

The current code is solely for account monitoring. The source code has been disclosed, allowing you to check or adopt it as needed.
Monitor the USDT value of both spot and USDT contracts.

Currently, our team's strategy server cluster numbers 80 machines, with over 50 supporting servers. They verify the stop-loss conditions on accounts at an average rate of two times per second, ensuring swift exits in risky situations.

We utilize a hybrid cloud architecture from Alibaba Cloud, Amazon Web Services, and Microsoft Azure, separating management nodes from execution nodes to form redundant clusters that securely and effectively support smooth business operations and fund safety.

Regarding trials:
Based on your capital scale, we offer a 2-week trial run. During the trial phase, no commission will be deducted.
Once the bot takes over your account, do not perform any manual operations; detection of any manual positions by Bots will immediately cause their exit.

Regarding commissions:
This depends on your capital volume. We can discuss details after the trial period. If you use our recommended link to open an account, we would charge a low commission rate.

Contact Information:
1. Face-to-face meetings available nationwide
2. WeChat: DuQi_SEC/autobitmaker/autobitmaker_001/Shawn_gb2312/ABM_DD 
3. Email: liuhongyu.louie@autobitmaker.com/autobitmaker_master@autobitmaker.com

* Special Note (WeChat ID autobitmaker001 is not us! We are also not makebit! The correct WeChat ID is autobitmaker_001)

Submit a trial application via the WeChat Mini Program:
![WeChat Mini Program QR Code](https://www.fmz.cn![IMG](https://www.fmz.com/upload/asset/1281e73989f891ac26aa9.jpg))

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|baseOriginalBalance|10000|Base Original Balance|


> Source (javascript)

``` javascript
//exchanges[0] is contract
//exchanges[1] is spot

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
            text: 'Collateral Ratio (%)'
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
        if (account !== null && account.Info !== null && account.Info.totalMarginBalance > 0) {
            ObjChart.add([0, [nowTime, Number(totalBalance)]]);
        }
    } catch (err) {
        Log('ERROR ' + account + ',' + err)
    }
}

function getBalance() {
    var currentBalance = 0;
    var account = exchanges[0].GetAccount();
    try {
        if (account !== null && account.Info !== null && account.Info.totalWalletBalance > 0) {
            currentBalance += Number(account.Info.totalWalletBalance);
        }
    } catch (err) {
        Log('ERROR ' + account + ',' + err)
    }
    Sleep(666);
    return Number(currentBalance).toFixed(6);
}

function getSpotBalanceInUSDT() {
    var ticker = JSON.parse(HttpQuery('https://api.binance.com/api/v1/ticker/24hr'));
    var currentBalance = 0;
    var account = exchanges[1].GetAccount();
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
        cols: ['Symbol', 'Type', 'AvgPrice', 'Position', 'Profit'],
        rows: []
    }
    table.rows.push([{
        body: 'This strategy is USDT-centric and based on mean reversion for risk-free arbitrage between Binance spot and contract trading.',
        colspan: 5
    }]);
    table.rows.push([{
        body: 'Arbitrage covers all trading pairs of perpetual contracts on Binance.',
        colspan: 5
    }]);
    var position = exchangeInnerArray[0].GetPosition()
    for (var indexInner in position) {
        var profit = Number(position[indexInner].Info.unRealizedProfit);
        totalProfit = totalProfit + profit
        table.rows.push([position[indexInner].Info.symbol, (position[indexInner].Type == 1 ? 'SHORT #da1b1bab' : 'LONG #1eda1bab'), position[indexInner].Price, position[indexInner].Amount, profit.toFixed(5)]);
    }
    Sleep(168);
    table.rows.push([{
        body: 'TOTAL PROFIT OF CURRENT POSITION',
        colspan: 4
    }]);
```