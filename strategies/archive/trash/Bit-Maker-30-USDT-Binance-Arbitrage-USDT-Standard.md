> Name

Bit-Maker-30-Arbitrage-Smart-Learning-USDT-Standard-Binance-Single-Platform

> Author

AutoBitMaker-ABM

> Strategy Description

Self-learning Grid:

Based on the traditional grid strategy approach, this self-learning grid has been optimized over a long period of live trading and backtesting data. It optimizes parameters such as entry logic, additional position timing, profit-taking positions, leverage ratio, grid spacing, among others. This achieves an intelligent dynamic addition model and profit-taking positions, which can avoid the high risks encountered in traditional grids during one-sided market conditions by using extremely low leverages to achieve good return-to-drawdown ratios.

The strategy configuration parameters are incredibly rich, with our team assigning a dedicated person to tailor unique parameter combinations based on your account's risk and reward requirements. We also have round-the-clock human and automated market surveillance.

We have developed an in-house proprietary index trading collection, where each index trading set includes multiple high-quality single trade pairs, each with its own unique weight distribution. The robot runs the self-learning grid strategy on these index sets to avoid risks associated with individual single-sided market conditions. In addition to built-in static indexes, we define dynamic indexes for our index sets using various selection models, selecting leading coins from different sectors to reduce risk further.

A single account can configure and run multiple single-asset trade pairs and index trade pairs simultaneously, effectively spreading the risk while helping you profit in various complex market conditions.

Regarding optimization and risk control:
The historical backtesting server operates 24/7, automatically testing all new data to calculate optimal parameters in real-time.
Our strategy cluster includes over 50 auxiliary servers, verifying account stop-loss conditions every two seconds to quickly exit when risks arise.

Using the Alibaba Cloud, Amazon Cloud, and Microsoft Cloud architectures, we separate management and execution nodes, forming a cluster for redundancy assurance, ensuring smooth business operations and secure funds.

Regarding trial use:
Based on your capital scale, we provide approximately 2 weeks of free trial. During this period, no commissions will be deducted.
Please do not perform any actions manually after the bot takes over your account; if it detects any manual positions, all bots will immediately exit.

Regarding commission:
This depends on your capital amount. We can discuss details after the trial phase. If you use our recommended link to create an account, we will charge a very low commission.

Contact Information:
WeChat: DuQi_SEC/autobitmaker/Shawn_gb2312/ABM_DD
Email: liuhongyu.louie@autobitmaker.com/autobitmaker_master@autobitmaker.com

Submit Trial Application via WeChat Mini Program:
![WeChat Mini Program QR Code](https://www.fmz.cn![IMG](https://www.fmz.com/upload/asset/1281e73989f891ac26aa9.jpg))

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|baseOriginalBalance|1000|Initial Balance|
|showInfo|false|Show Information|


> Source (javascript)

``` javascript
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

function updateAccountDetailChart(ObjChart) {
    var nowTime = new Date().getTime();
    var account = exchanges[0].GetAccount();
    try {
        if (account !== null && account.Info !== null && account.Info.totalMarginBalance > 0) {
            ObjChart.add([0, [nowTime, Number(account.Info.totalMarginBalance)]]);
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

function getMarginBalance() {
    var currentBalance = 0;
    var account = exchanges[0].GetAccount();
    try {
        if (account !== null && account.Info !== null && account.Info.totalMarginBalance > 0) {
            currentBalance += Number(account.Info.totalMarginBalance);
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
    if (showInfo) {
        table.rows.push([{
            body: '* 2020-09-07 之前一直人民币100万实盘运行，现策略更新，自动将合约闲置资金转入币安宝，即提高资金安全性，也可以双边获利，当合约所需保证金上涨或下降时，将自动调整两边余额。因当前FMZ无法监控币安宝余额，所以剥离10W人民币继续运行原策略以做展示。',
            colspan: 5
        }]);
    }
    table.rows.push([{
        body: 'This strategy is USDT-pegged, based on a mean reversion arbitrage strategy on Binance futures contracts, with low-risk auxiliary grid parallelism (BitMEX supports BTC-pegged).',
        colspan: 5
    }]);
    table.rows.push([{
        body: 'The main arbitrage currencies are BTC/USDT and ETH/USDT, with the grid covering all trading pairs on Binance perpetual futures contracts.',
        colspan: 5
    }]);
    for (var index in exchangeInnerArray) {
        var position = exchangeInnerArray[index].GetPosition()
        for (var indexInner in position) {
            var profit = Number(position[indexInner].Info.unRealizedProfit);
            totalProfit = totalProfit + profit
            table.rows.push([position[indexInner].Info.symbol, (position[indexInner].Type == 1 ? 'SHORT #da1b1bab' : 'LONG #1eda1bab'), position[indexInner].Price, position[indexInner].Amount, profit.toFixed(5)]);
        }
        Sleep(168);
    }
    table.rows.push([{
        body: 'TOTAL PROFIT OF CURRENT POSITION',
        colspan: 4
    }, totalProfit.toFixed(6) + ' USDT']);
    table.rows.push([{
        body: 'TOTAL PROFIT',
        colspan: 4
    }, totalProfitUSDT + ' USDT']);
    table.rows.push([{
        body: 'TOTAL PROFIT RATE',
        colspan: 4
    }, totalProfitRate + ' %']);
    LogStatus('`' + JSON.stringify(table)