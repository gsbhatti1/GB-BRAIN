> Name

SuperHunter - Intelligent Learning - Multi-Account Consolidated Display Edition

> Author

AutoBitMaker-ABM



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|baseOriginalBalance|1000|Base Original Balance|


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
    for (var index in exchanges) {
        chart.series.push({
            name: "Account_" + (Number(index)) + "_Detail",
            id: "Account_" + (Number(index)) + "_Detail",
            data: []
        });
    }
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
                name: 'Used Margin (%)',
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
    for (var index in exchanges) {
        var account = exchanges[index].GetAccount();
        try {
            if (account !== null && account.Info !== null && account.Info.totalMarginBalance > 0) {
                ObjChart.add([index, [nowTime, Number(account.Info.totalMarginBalance)]]);
            }
        } catch (err) {
            Log('ERROR ' + account + ',' + err)
        }
    }
}

function getBalance() {
    var currentBalance = 0;
    for (var index in exchanges) {
        var account = exchanges[index].GetAccount();
        try {
            if (account !== null && account.Info !== null && account.Info.totalWalletBalance > 0) {
                currentBalance += Number(account.Info.totalWalletBalance);
            }
        } catch (err) {
            Log('ERROR ' + account + ',' + err)
        }
        Sleep(666);
    }
    return Number(currentBalance).toFixed(6);
}

function getMarginBalance() {
    var currentBalance = 0;
    for (var index in exchanges) {
        var account = exchanges[index].GetAccount();
        try {
            if (account !== null && account.Info !== null && account.Info.totalMarginBalance > 0) {
                currentBalance += Number(account.Info.totalMarginBalance);
            }
        } catch (err) {
            Log('ERROR ' + account + ',' + err)
        }
        Sleep(666);
    }
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
        body: 'This strategy is USDT-based and is a mean reversion arbitrage strategy on Binance contracts, with low-risk auxiliary grids running in parallel (BitMEX supports BTC-based).',
        colspan: 5
    }]);
    table.rows.push([{
        body: 'The main arbitrage pairs are BTC/USDT and ETH/USDT, with the grid covering all trading pairs of Binance perpetual futures.',
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
    LogStatus('`' + JSON.stringify(table) + '`');
}

function main() {
    initChart();
    var ObjChart = Chart([chart, getChartPosition(100)]);
    while (true) {
        try {
            var currentBalance = getBalance();
            printProfitInfo(currentBalance);
            updateAccountDetailChart(ObjChart);
            for (var i = 0; i < 120; i++) {
                try {
                    var avaliableMargin = ((getMarginBalance()) / (getBalance())) * 100;
                    ObjChart.update([chart, getChartPosition(avaliableMargin)]);
                    var profit = Number((currentBalance) - baseOriginalBalance).toFixed(5);
                    var profitRate = Number((((currentBalance) - baseOriginalBalance) / baseOriginalBalance) * 100).toFixed(4);
                    printPositionInfo(exchanges, profit, profitRate);
                    Sleep(1000 * 120);
                } catch (errInner) {
                    throw errInner;
                }
            }
        } catch
```