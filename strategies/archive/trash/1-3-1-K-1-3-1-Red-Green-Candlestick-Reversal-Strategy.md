> Name

1-3-1 Red-Green Candlestick Reversal Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/491225d47e40fa480f.png)

[trans]

## Overview

The 1-3-1 Red-Green Candlestick Reversal Strategy is a trading strategy that generates buy and sell signals based on candlestick patterns. It looks for buying opportunities when 1 red candlestick is reversed by 3 subsequent green candlesticks.

## Principles

The core logic of this strategy is:

1. Check if the current candlestick is a red candle, i.e., the close price is lower than the open price
2. Check if the previous 3 candlesticks are green candles, i.e., close price is higher than open price
3. Check if the last green candle's close price is higher than the previous 2 green candles
4. If the above conditions are met, go long at the close of the red candle
5. Set stop loss at the lowest price of the red candle
6. Set take profit at entry price plus the distance from entry to stop loss

With this strategy, we can buy when the red candle is reversed, because the subsequent trend is likely to be upwards. Stop loss and take profit are set to control risk and lock in profits.

## Advantage Analysis

The 1-3-1 Red-Green Reversal Strategy has the following advantages:

1. Simple and clear logic, easy to understand and implement
2. Utilizes candlestick pattern features without relying on indicators, avoiding overoptimization problems
3. Has clear entry and exit rules for objective execution
4. Sets stop loss and take profit to control risk/reward of each trade
5. Good backtest results, likely to translate well to live trading

## Risk Analysis

Some risks to note for this strategy:

1. Candlestick patterns cannot perfectly predict future moves, some uncertainty exists
2. Only one entry, may have lower win rate due to stock specifics  
3. No consideration of market trend, risk holding during sustained downtrend
4. Does not account for trading costs and slippage, actual performance may be worse

Solutions:

1. Consider combining with MA etc to filter signals and improve entry success rate
2. Adjust position sizing, scale in across multiple entries 
3. Dynamically adjust stop loss based on market conditions or pause trading
4. Test different stop loss/take profit ratios
5. Test actual performance including trading costs

## Optimization Directions

Some ways this strategy can be optimized:

1. Market index filtering - filter signals based on short/medium term market trend, go long in uptrend and stop trading in downtrend

2. Volume confirmation - only go long if green candle volumes increase 

3. Optimize stop loss/take profit ratios - test different ratios to find optimal parameters

4. Position sizing optimization - scale in across multiple entries to reduce single trade risk

5. Add more filters - e.g. MA, volatility etc to ensure high probability entry

6. Machine learning on big data - collect lots of historical data and train optimal parameter thresholds via ML

## Conclusion

The 1-3-1 Red-Green Reversal Strategy is overall a simple and practical short term trading strategy. It has clear entry and exit rules and good backtest results. With some optimization measures, it can become a reliable quant trading strategy. Risk management is also important to manage capital properly.

||

## Overview 

The 1-3-1 Red-Green Candlestick Reversal Strategy is a trading strategy that generates buy and sell signals based on candlestick patterns. It looks for buying opportunities when 1 red candlestick is reversed by 3 subsequent green candlesticks.

## Principles

The core logic of this strategy is:

1. Check if the current candlestick is a red candle, i.e., the close price is lower than the open price
2. Check if the previous 3 candlesticks are green candles, i.e., close price is higher than open price
3. Check if the last green candle's close price is higher than the previous 2 green candles
4. If the above conditions are met, go long at the close of the red candle 
5. Set stop loss at the lowest price of the red candle
6. Set take profit at entry price plus the distance from entry to stop loss

With this strategy, we can buy when the red candle is reversed, because the subsequent trend is likely to be upwards. Stop loss and take profit are set to control risk and lock in profits.

## Advantage Analysis

The 1-3-1 Red-Green Reversal Strategy has the following advantages:

1. Simple and clear logic, easy to understand and implement
2. Utilizes candlestick pattern features without relying on indicators, avoiding overoptimization problems
3. Has clear entry and exit rules for objective execution
4. Sets stop loss and take profit to control risk/reward of each trade
5. Good backtest results, likely to translate well to live trading

## Risk Analysis

Some risks to note for this strategy:

1. Candlestick patterns cannot perfectly predict future moves, some uncertainty exists
2. Only one entry, may have lower win rate due to stock specifics  
3. No consideration of market trend, risk holding during sustained downtrend
4. Does not account for trading costs and slippage, actual performance may be worse

Solutions:

1. Consider combining with MA etc to filter signals and improve entry success rate
2. Adjust position sizing, scale in across multiple entries 
3. Dynamically adjust stop loss based on market conditions or pause trading
4. Test different stop loss/take profit ratios
5. Test actual performance including trading costs

## Optimization Directions

Some ways this strategy can be optimized:

1. Market index filtering - filter signals based on short/medium term market trend, go long in uptrend and stop trading in downtrend

2. Volume confirmation - only go long if green candle volumes increase 

3. Optimize stop loss/take profit ratios - test different ratios to find optimal parameters

4. Position sizing optimization - scale in across multiple entries to reduce single trade risk

5. Add more filters - e.g. MA, volatility etc to ensure high probability entry

6. Machine learning on big data - collect lots of historical data and train optimal parameter thresholds via ML

## Conclusion

The 1-3-1 Red-Green Reversal Strategy is overall a simple and practical short term trading strategy. It has clear entry and exit rules and good backtest results. With some optimization measures, it can become a reliable quant trading strategy. Risk management is also important to manage capital properly.

||

```pinescript
/*backtest
start: 2023-09-26 00:00:00
end: 2023-10-26 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
//by Genma01
strategy("1-3-1 Red-Green Candlestick Reversal Strategy", overlay=true, default_qty_type = strategy.percent_of_equity,  default_qty_value = 100)

// Define parameters
var float stopLossPrice = na
var float takeProfitPrice = na
var float stopLossPriceD = na

// Check conditions
redCandle = close[3] < open[3] and low[3] < low[2] and low[3] < low[1] and low[3] < low[0]
greenCandles = close > open and close[1] > open[1] and close[2] > open[2]
higherClose = close > close[1] and close[1] > close[2]

// Calculate stop loss
if (redCandle and greenCandles and higherClose) and strategy.position_size == 0
    stopLossPrice := low[3]

// Calculate take profit
if not na(stopLossPrice) and strategy.position_size == 0
    takeProfitPrice := close + (close - stopLossPrice)

// Enter long position
if redCandle and greenCandles and higherClose and strategy.position_size == 0
    strategy.entry("Long", strategy.long)

// Exit from position
if not na(stopLossPrice) and strategy.position_size > 0
    strategy.exit("Take Profit/Stop Loss", stop=stopLossPrice, limit=takeProfitPrice)

if strategy.position_size == 0
    stopLossPriceD
```