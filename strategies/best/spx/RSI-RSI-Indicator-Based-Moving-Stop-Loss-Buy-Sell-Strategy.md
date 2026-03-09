> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|12|RSI Period|
|v_input_2|83|RSI Sell Level|
|v_input_3|5|Stop Percentage|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-17 00:00:00
end: 2024-01-16 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("RSI Buy/Sell Strategy", overlay=false)

// Input for RSI period
rsiPeriod = input(12, title="RSI Period")

// Input for RSI levels
rsiBuyLevel1 = 20
rsiBuyLevel2 = 18
rsiBuyLevel3 = 14
rsiSellLevel = input(83, title="RSI Sell Level")

// Input for stop loss percentage
stopLossPercent = input(5, title="Stop Percentage")

// Calculate RSI
rsiValue = ta.rsi(close, rsiPeriod)

// Buy Conditions: RSI below buy levels
buyCondition1 = close[1] > close and rsiValue <= rsiBuyLevel1
buyCondition2 = close[1] > close and rsiValue <= rsiBuyLevel2
buyCondition3 = close[1] > close and rsiValue <= rsiBuyLevel3

// Sell Condition: RSI above sell level
sellCondition = rsiValue >= rsiSellLevel

// Stop Loss Condition
stopLossPrice = strategy.position_avg_price * (1 - stopLossPercent / 100)

// Buy Order
if (buyCondition1 or buyCondition2 or buyCondition3)
    strategy.entry("Buy", strategy.long)

// Sell Order with Stop Loss
if (sellCondition and strategy.position_size > 0)
    if close < stopLossPrice
        strategy.exit("Stop Loss", "Buy")
    else
        strategy.close("Buy")

```
```