> Name

ATR-RSI Combination Strategy

> Author

One knife

> Strategy Description

## ATR Indicator
Average True Range (Average True Range), referred to as the ATR indicator. It is primarily used to measure the intensity of market fluctuations and indicate the rate of change in the market, but it does not reflect price direction or trend stability. The higher the value of this indicator, the greater the possibility of a trend change; conversely, the lower the value, the smaller the possibility of a trend change.

### Calculation Method
The average true range is calculated based on the actual fluctuations of the past N days and the current day's real fluctuation. The single-day true fluctuation is determined by the maximum value among three sets of results: (the highest price of the day - the lowest price of the day), (the highest price of the day - yesterday’s closing price), and (yesterday’s closing price - the lowest price of the day), aiming to obtain the price difference within the maximum fluctuation range.

## RSI Indicator
Relative Strength Index (RSI). Technical indicators that determine future market trends by comparing the strength of buying and selling power between long and short parties over a period of time.

### Calculation Method
\[ \text{RSI} = 100 - \left( \frac{100}{1 + RS} \right) \]
Where \( RS = \frac{\text{n-day closing number of gains}}{\text{n-day closing number of decreases}} \);
Generally, RSI uses 50 as the middle line. If it is greater than 50, it is considered a long market; if it is less than 50, it is considered a short market.
An RSI value greater than 70 is considered an overbought state, suggesting that a subsequent market correction or reversal may occur. An RSI value less than 30 is considered an oversold state, indicating potential for a subsequent rise.

## Strategy Principle
ATR is used for filtering. When ATR > ATRMa (the average ATR of the past N days), it means that market volatility has begun to increase and the trend is strengthening. RSI is used to generate trading signals.

> Strategy Arguments


|Argument|Default|Description|
|---|---|---|
|rsi_period|20|RSI strength and weakness indicator calculation period|
|atr_period|14|ATR true range calculation period|
|atrma_period|20|Average true volatility and average price calculation period|
|tick_interval|60|Time interval|
|slide_price|0.3|Order sliding value|


> Source (JavaScript)

```javascript
/*backtest
start: 2021-02-11 00:00:00
end: 2022-02-10 23:59:00
Period: 15m
basePeriod: 5m
exchanges: [{"eid":"Huobi","currency":"BCH_USDT"}]
args: [["rsi_period",12],["atrma_period",18]]
*/

/*
* rsi_period: RSI strength indicator calculation period
* atr_period: ATR true range calculation period
* atrma_period: Average true volatility mean calculation period
* tick_interval: time interval
* slide_price: order sliding value
*/

// RSI operating status indicators
varRSI_NONE = 0;
varRSI_BUY = 1;
varRSI_SELL = 2;

var last_rsi_status;

// ATR active signal judgment
function isAtrActive(records) {
    let atr = TA.ATR(records, atr_period);
    let atrma = atr[atr.length - 1];
    if (atr.length > atrma_period) {
        let tmp_atr = 0;
        for (let i = atr.length - atrma_period; i < atr.length; i++) {
            tmp_atr += atr[i];
        }
        atrma = tmp_atr / atrma_period;
    } else {
        atrma = aval(atr.join("+")) / atr.length;
    }
    return atr[atr.length - 1] > atrma;
}

// Get RSI operating status
function getRsiStatus(records) {
    let rsi = TA.RSI(records, rsi_period)[records.length - 1];
    if (rsi < 30) {
        return RSI_BUY;
    } else if (rsi > 70) {
        return RSI_SELL;
    } else {
        return RSI_NONE;
    }
}

// Cancel unfilled orders
function cancelPendingOrders() {
    while (true) {
        let orders = _C(exchange.GetOrders);
        if (orders.length == 0) {
            break;
        }
        for (let i = 0; i < orders.length; i++) {
            exchange.CancelOrder(orders[i].Id);
        }
    }
}

function onTick() {
    let records = _C(exchange.GetRecords, PERIOD_M15);
    let ticker = _C(exchange.GetTicker);
    if (records == null ||
        ticker == null ||
        records.length < rsi_period ||
        records.length < atr_period) {
        return;
    }

    if (isAtrActive(records)) {
        let rsi = getRsiStatus(records);
        if (rsi != RSI_NONE) {
            let account = _C(exchange.GetAccount);
            if (rsi == RSI_BUY && last_rsi_status != RSI_BUY) {
                Log("Buy signal");
                last_rsi_status = RSI_BUY;
                cancelPendingOrders();
                if (account.Balance > 0) {
                    let price = ticker.Last + slide_price;
                    let amount = account.Balance / price * 0.99;
                    exchange.Buy(price, amount);
                }
            } else if (rsi == RSI_SELL && last_rsi_status != RSI_SELL) {
                Log("Sell signal");
                last_rsi_status = RSI_SELL;
                cancelPendingOrders();
                if (account.Stocks > 0) {
                    let price = ticker.Last - slide_price;
                    exchange.Sell(price, account.Stocks);
                }
            }
        }
    }
    last_records = records;
}

function main() {
    while (true) {
        onTick();
        Sleep(tick_interval * 1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/345036

> Last Modified

2022-02-13 17:19:57