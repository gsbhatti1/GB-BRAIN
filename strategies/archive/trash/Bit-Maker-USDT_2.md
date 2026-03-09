---

### Name

Bit-Maker-Spot USDT Equivalence Monitoring

### Author

AutoBitMaker-ABM

### Strategy Description

**AutoBitMaker** has now officially launched a risk-free arbitrage strategy.
The principle of the strategy is to hedge spot and futures, which can also be completed manually.
However, compared to manual operations, the BOT will capture profit margins for all trading pairs in the market every day, with hundreds of transactions. This further frees your hands, reducing the risks in the market.

The current code only monitors accounts; the source code is publicly disclosed, and everyone can check or use it if they wish.
Monitor the USDT value of spot trading.

We are **AutoBitMaker**, abbreviated as **ABM Capital**. Please carefully verify our team name, WeChat ID to distinguish authenticity.
For now, we communicate with domestic customers only through WeChat and Email; other methods such as QQ will not be used.

The **ABM Team** currently offers three types of strategies:
- Futures Trading
- Spot Trading
- Arbitrage Trading

Our self-developed learning grid strategy is based on the traditional grid strategy concept. After long-term practical testing and backtesting, we have optimized dozens of parameters such as opening logic, entry timing, take-profit positions, leverage ratios, grid spacing, etc., to achieve intelligent dynamic grid models and take-profit positions. This model can avoid high risks associated with single-sided market conditions in traditional grids by using extremely low leverage to achieve good risk-adjusted returns.

The strategy configuration is very rich; our team will assign a dedicated person to customize unique parameter combinations based on your account's risk and return requirements, providing 24/7 manual and automated market monitoring.

We have developed a proprietary index trading collection. Each index includes multiple high-quality single-trading pairs with unique weight ratios. Robots run the learning grid strategy on these index collections, mitigating risks associated with single trading pairs experiencing single-sided conditions.
In addition to built-in static indices, we define dynamic indices for our indices based on various selection models of coins, selecting leading cryptocurrencies in each sector to further reduce risk.

Single accounts can simultaneously configure and operate multiple single-coin trading pairs and index trading pairs, effectively spreading risks while helping you profit in a wide variety of market conditions.

Currently, the team's strategy server cluster consists of 80 machines, with an additional 50 support servers. The system checks the stop-loss conditions for your account every second on average to quickly exit when risk arises.

Using Alibaba Cloud, Amazon Web Services (AWS), and Microsoft Azure architectures, we separate management from execution nodes, forming a cluster to ensure redundancy and secure, efficient operation of our services and capital safety.

### Tryout:
Based on your capital scale, we provide a 2-week trial run. During the trial period, no commissions will be deducted.
Please do not make any operations after the bot takes over your account; all bots will exit if they detect any manually entered positions.

### Commission:
This depends on your capital volume. We can discuss this in detail after the trial phase. If you use our recommended link to create an account, we will charge a very low commission rate.

### Contact Information:
1. Available for face-to-face meetings nationwide
2. WeChat: DuQi_SEC/autobitmaker/autobitmaker_001/Shawn_gb2312/ABM_DD 
3. Email: liuhongyu.louie@autobitmaker.com/autobitmaker_master@autobitmaker.com

* Special Note (WeChat ID autobitmaker001 is not us! We are also not makebit! The correct one is WeChat ID autobitmaker_001)

### Tryout Application via WeChat Mini-Program:
![WeChat Mini-Program Code](https://www.fmz.cn![IMG](https://www.fmz.com/upload/asset/1281e73989f891ac26aa9.jpg))

---

### Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|baseOriginalBalance|10000|Base original balance|

### Source (JavaScript)

```javascript
// exchanges[0] is spot

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
        body: 'This strategy is USDT-based, low-risk smart dynamic parameter grid for spot trading',
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
                    if (Number((Number(obj.free) + Number(obj.locked))) > 0) {
                        table.rows.push([obj.asset, obj.type, priceMap[obj.asset + 'USDT'], Number(obj.free) + Number(obj.locked), (Number(priceMap[obj.asset + 'USDT']) * (Number(obj.free) + Number(obj.locked))).toFixed(6)]);
                    }
                }
            }
        }
    } catch (err) {
        Log('ERROR ' + account + ',' + err)
    }
}
```