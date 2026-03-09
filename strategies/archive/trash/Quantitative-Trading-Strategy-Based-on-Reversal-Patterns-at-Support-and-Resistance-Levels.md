``` pinescript
/*backtest
start: 2024-05-07 00:00:00
end: 2024-06-06 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Kingcoinmilioner

//@version=5
strategy("Reversal Patterns at Support and Resistance", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

// Parameters
support_resistance_lookback = input.int(50, title="Support/Resistance Lookback Period")
reversal_tolerance = input.float(0.01, title="Reversal Tolerance (percent)", step=0.01) / 100
take_profit_percent = input.float(3, title="Take Profit (%)") / 100
stop_loss_percent = input.float(1, title="Stop Loss (%)") / 100

// Functions to identify key support and resistance levels
findSupport() =>
    ta.lowest(low, support_resistance_lookback)

findResistance() =>
    ta.highest(high, support_resistance_lookback)

// Identify reversal patterns
isHammer() =>
    body = math.abs(close - open)
    lowerWick = open > close ? open - low[1] : 0
    upperWick = close > open ? high[1] - close : 0

    hammerPattern = (body < lowerWick * reversal_tolerance) and
                    (upperWick / body < 2) and
                    (lowerWick / body < 3)
    hammerPattern

isEngulfing() =>
    previousClose = close[1]
    nextClose = close[2]

    engulfingPattern = open > previousClose and open < nextClose and
                       close < previousClose and close > nextClose
    engulfingPattern

isDoji() =>
    dojiPattern = (high - low) / 2 < body and
                  abs(open - close) / 2 < body / 4
    dojiPattern

// Main strategy logic
longCondition = isHammer() and close <= findSupport()
shortCondition = isHammer() and close >= findResistance()

if (longCondition)
    strategy.entry("Long", strategy.long, stop = findSupport())
    
if (shortCondition)
    strategy.entry("Short", strategy.short, stop = findResistance())

// Set take profit and stop loss
takeProfitPrice = strategy.position_avg_price * (1 + take_profit_percent)
stopLossPrice = strategy.position_avg_price * (1 - stop_loss_percent)

strategy.exit("Take Profit", from_entry="Long", limit=takeProfitPrice)
strategy.exit("Stop Loss", from_entry="Short", stop=stopLossPrice)
```

This script identifies trading opportunities based on hammer, engulfing, and doji patterns near support and resistance levels. It sets up long or short positions with predefined take profit and stop loss levels.