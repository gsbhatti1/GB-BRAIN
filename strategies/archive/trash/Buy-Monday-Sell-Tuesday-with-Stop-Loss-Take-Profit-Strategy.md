```pinescript
/*backtest
start: 2022-09-12 00:00:00
end: 2023-02-17 00:00:00
Period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © processingclouds

// @description Strategy to go long at end of Monday and exit by Tuesday close, or at stop loss or take profit percentages

//@version=5
strategy("Buy Monday, Exit Tuesday", "Mon-Tue Swings", overlay=true)

// ----- Inputs: stoploss %, takeProfit %
stopLossPercentage = input.float(defval=4.0, title='StopLoss %', minval=0.1, step=0.2) / 100
takeProfit = input.float(defval=3.0, title='Take Profit %', minval=0.3, step=0.2) / 100

// ----- Exit and Entry Conditions - Check current day and session time
isLong = dayofweek == dayofweek.monday and not na(time(timeframe.period, "1400-1601"))
isExit = dayofweek == dayofweek.tuesday and not na(time(timeframe.period, "1400-1601"))

// ----- Calculate Stoploss and Take Profit values
SL = stopLossPercentage * open
TP = takeProfit * open

// ----- Main Trading Logic
if (isLong)
    strategy.entry("Long", strategy.long)
    
if (isExit or close >= SL or close <= TP)
    strategy.exit("Exit", "Long", stop=SL, limit=TP)
```

This translation preserves the original code blocks and formatting, while translating the human-readable text into English.