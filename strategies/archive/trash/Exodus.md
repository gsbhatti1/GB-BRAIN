> Name

Three-Moving-Average System Exodus

> Author

Exodus[Strategy Writer]

> Strategy Description

This system is a two-way contract strategy, where positions are opened for buying or selling when certain conditions are met. The order volume equals the number of contracts; on Binance, it is in terms of BTC, and on Huobi, it is in terms of lots.
【Updated 7-31】
The parameters of this strategy are suitable for running on a 1-hour timeframe, but due to insufficient trading frequency at that level, it has been updated to the minute-level. However, manual parameter adjustments are required when using the minute-level strategy.

Below are backtest results based on an hourly cycle:
**** April 27 - July 25 ****
Initial capital: $300, Order volume: 0.04 BTC
![](https://www.fmz.com/upload/asset/1f4e9984f53d575c506c1.png)
**** January 1 - July 25 ****
Initial capital: $300, Order volume: 0.03 BTC and 0.04 BTC (the latter amount is insufficient for initial capital)
If you plan to use this in a live environment, it's recommended to backtest to determine your own order size.
![](https://www.fmz.com/upload/asset/1f47c59a9ac1f93694193.png)

Feel free to support the author if you find this useful!
![](https://www.fmz.com/upload/asset/1f4c36c1fca8b23e727c7.jpg)

> Strategy Arguments

| Argument | Default | Description |
| --- | --- | --- |
| afterEmaCrossTime | 4 | Number of candles after an EMA crossover before MACD conditions are met to allow operations |
| buyVolume | 0.016 | Trading volume (0.016 BTC) |
| stopLossRate | true | Stop-loss rate (not including leverage) |
| winLossRate | 5 | Win/loss ratio |
| period | 60 | Timeframe (minutes) |
| EMA1 | 8 | Fastest moving average cycle |
| EMA2 | 34 | Medium-speed moving average cycle |
| EMA3 | 89 | Slowest moving average cycle |
| MACD1 | 16 | MACD parameter 1 |
| MACD2 | 26 | MACD parameter 2 |
| MACD3 | 9 | MACD parameter 3 |

> Source (JavaScript)

```javascript
/* backtest
start: 2021-04-27 00:00:00
end: 2021-07-25 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT","balance":300}]
args: [["afterEmaCrossTime",4],["buyVolume",0.04],["winLossRate",5]]
*/

function GetCrossStatus(a, lastA, b, lastB) {
    let lastStatus = lastA < lastB;
    let curStatus = a < b;
    let crosssStaus = 0; //0表示没有交叉，1表示金叉，2表示死叉
    //判断金叉还是死叉,同时判断此刻大于0轴或者小于0轴,因为在此系统中要求金叉时macd>0才有意义，死叉时macd<0才有意义
    if (curStatus != lastStatus) { //状态不同时表示金叉或者死叉了
        if (a > b) {
            crosssStaus = 1; //金叉
        }
        if (a < b)
            crosssStaus = 2; //死叉
    }
    return crosssStaus;
}

var lastOpenTime;

function GetCurRecord(records) {
    return records[records.length - 1];
}

function GetCurTime(records) {
    return GetCurRecord(records).Time;
}

function GetCurPrice(records) {
    return GetCurRecord(records).Close;
}

function Open(direction) {
    let pos = exchange.GetPosition()[0];

    if (pos != null) {
        return;
    }
    let amount = buyVolume;
    if (direction == 1) { //做多
        Log("做多", amount);
        exchange.SetDirection("buy");
        exchange.Buy(-1, amount);
    }
    if (direction == 2) { //做空
        Log("做空", amount);
        exchange.SetDirection("sell");
        exchange.Sell(-1, amount);
    }
    
}

function Close(ticker, fastLine, midLine) {
    let pos = exchange.GetPosition()[0];

    if (pos == null) {
        return;
    }
    
    if (pos.Type == PD_LONG) {
        if (ticker.Last < pos.Price * (1 - stopLossRate / 100) || ticker.Last > pos.Price * (1 + (stopLossRate * winLossRate) / 100)) {
            Log("平多,开仓价为:", pos.Price, "本次盈利:", pos.Profit);
            exchange.SetDirection("closebuy");
            exchange.Sell(-1, pos.Amount);
            
        }
    }
    if (pos.Type == PD_SHORT) {
        if (ticker.Last > pos.Price * (1 + stopLossRate / 100) || ticker.Last < pos.Price * (1 - (stopLossRate * winLossRate) / 100)) {
            Log("平空,开仓价为:", pos.Price, "本次盈利:", pos.Profit);
            exchange.SetDirection("closesell");
            exchange.Buy(-1, pos.Amount);
        }
    }
}

var lastEmaCrossTime = 0;
var lastMacdCrossTime = 0;

function NearMacdCross(time) {
    //Log("MACD", time, lastMacdCrossTime, time - lastMacdCrossTime);
    return time - lastMacdCrossTime <= afterEmaCrossTime * 1000 * 3600;
}

function NearEmaCross(time) {
    //Log("EMA", time, lastMacdCrossTime, time - lastMacdCrossTime);
    return time - lastEmaCrossTime <= afterEmaCrossTime * 1000 * 3600;
}

var emaMeet = 0; //0表示不满足，1满足做多条件，2满足做空条件
var macdMeet = 0; //判断macd是否满足条件,0表示不满足，1表示做多条件满足，2表示做空条件满足

function main() {
    exchange.SetContractType("swap");
    while (1) {
        let r = exchange.GetRecords(PERIOD_M1 * period);

        //************均线EMA****************
        let emaChart8 = TA.EMA(r, EMA1);
        let emaChart34 = TA.EMA(r, EMA2);
        let emaChart89 = TA.EMA(r, EMA3);

        let ema8 = emaChart8;
        let curEma8 = ema8[emaChart8.length - 1];
        let lastEma8 = ema8[emaChart8.length - 2];

        let ema34 = emaChart34;
        let curEma34 = ema34[emaChart34.length - 1];
        let lastEma34 = ema34[emaChart34.length - 2];

        let ema89 = emaChart89;
        let curEma89 = ema89[emaChart89.length - 1];
        let lastEma89 = ema89[emaChart89.length - 2];

        //判断8均线和34均线的死叉和金叉，当金叉时如果当前实体在ema89均线以上做多，当死叉时如果实体在ema89以下时做空      
        let ticker = exchange.GetTicker();
        let low = ticker.Low;
        let high = ticker.High; // Assuming 'high' is the same as the closing price for simplicity

        if (NearEmaCross(GetCurTime(r))) {
            if (curEma8 > curEma34 && lastEma8 <= lastEma34) { // EMA8金叉
                Open(1); // 开多仓
            } else if (curEma8 < curEma34 && lastEma8 >= lastEma34) { // EMA8死叉
                Open(2); // 开空仓
            }
        }

        //************MACD****************
        let macd = MACD(r, MACD1, MACD2, MACD3);
        let curDif = macd[0][macd.length - 1];
        let lastDif = macd[0][macd.length - 2];
        let curMacd = macd[2][macd.length - 1];
        let lastMacd = macd[2][macd.length - 2];

        // 判断金叉还是死叉
        if (curDif < 0 != lastDif < 0) {
            if (curDif > 0) { // MACD金叉
                macdMeet = 1;
                Log("macd金叉", lastDif, curDif);
                lastMacdCrossTime = GetCurTime(r);
            }
            if (curDif < 0) {
                macdMeet = 2; // MACD死叉
                Log("macd死叉", lastDif, curDif);
                lastMacdCrossTime = GetCurTime(r);
            }
        }

        // 根据MACD条件平仓
        if (macdMeet == 1 && ticker.Last < 0) { // MACD金叉后价格回撤
            Close(ticker, curEma89, curEma34); // 平多仓
        } else if (macdMeet == 2 && ticker.Last > 0) { // MACD死叉后价格上涨
            Close(ticker, curEma89, curEma34); // 平空仓
        }
    }
}
``` 

Note: The logic for handling EMA crossovers and MACD conditions has been added to the `main` function. Adjustments may be needed based on specific requirements or additional context not provided in the original code snippet. Make sure to test thoroughly before using this strategy in a live environment. 

Feel free to adjust the parameters according to your preferences and backtest them extensively. If you have any further questions, please let me know! 🚀💡

*Disclaimer: The information provided is for educational purposes only and should not be considered financial advice.* 💰