```plaintext
Name

RSI Convergence Breakout Trend Oscillation Stop Loss Strategy - Price-Drop-Buy-Strategy-in-Downtrend-with-Stop-Loss

Author

ChaoZhang

Strategy Description

![IMG](https://www.fmz.com/upload/asset/1d8d53c1b590c2490db.png)
[trans]

## Overview

This strategy uses the RSI indicator to determine potential market trend direction, combined with Bollinger Bands to identify key support and resistance areas. It looks for low absorption opportunities in trending markets to establish long positions and takes profits or cuts losses at overbought levels.

## Strategy Logic  

1. Use the RSI indicator to determine potential market trend direction. An RSI below 40 is considered an oversold area, indicating a possible bullish turn; an RSI above 50 indicates an overbought condition, suggesting a bearish turn.

2. Use Bollinger Bands to identify key support and resistance areas. The middle band of Bollinger Bands represents the moving average line of price, while the upper and lower bands form the standard deviation channel. Prices approaching the lower band indicate low absorption opportunities.

3. When RSI < 40 and prices approach the Bollinger lower band, it is determined as a low absorption long opportunity to establish a long position.

4. When RSI > 50 or profits exceed 50%, close long positions to take profits and cut losses.

## Advantage Analysis  

1. Use RSI to determine potential market trend direction, avoiding trading against the trend.

2. Identify precise entry timing by combining with Bollinger Bands to locate low absorption points.

3. Adopt a trending oscillation approach to prevent getting trapped in a position.

4. Flexible stop profit and stop loss mechanism to maximize profits.

## Risk Analysis  

1. Improper Bollinger parameters may fail to correctly identify support areas.

2. Trend breaks or false breakouts could lead to errors in overbought/oversold judgments.

3. Incorrect stop profit and stop loss point settings may result in premature exit or increased losses.

## Optimization Directions

1. Optimize Bollinger parameters for more accurate identification of support and resistance levels.

2. Incorporate other indicators like MACD and KDJ to filter false signals.

3. Dynamically optimize stop profit and stop loss algorithms to maximize profits while minimizing losses.

## Summary

This strategy determines potential trend direction using RSI, combined with Bollinger Bands to identify support areas, achieving low buy high sell. It is a typical trending oscillation strategy. With proper optimization, it can become a reliable and stable profitable quantitative trading strategy.

|| 

## Overview

This strategy uses the RSI indicator to determine the potential market trend direction, combined with Bollinger Bands to identify key support and resistance areas, and looks for low absorption opportunities in trending markets to establish long positions and take profits at overbought levels.

## Strategy Logic  

1. Use the RSI indicator to determine the potential market trend direction. An RSI below 40 is considered an oversold area where the market could turn bullish; an RSI above 50 indicates a bearish turn.

2. Use Bollinger Bands to identify key support and resistance areas. The middle band of Bollinger Bands represents the moving average line of price, while the upper and lower bands form the standard deviation channel. Prices approaching the lower band present low absorption opportunities.

3. When RSI < 40 and prices approach the Bollinger lower band, it is determined as a low absorption long opportunity to establish a long position.

4. When RSI > 50 or profits exceed 50%, close long positions to take profits and cut losses.

## Advantage Analysis  

1. Use RSI to determine potential market trend direction to avoid trading against the trend.

2. Identify precise entry timing by combining with Bollinger Bands to locate low absorption points.

3. Adopt a trending oscillation methodology to prevent getting trapped in a position.

4. Flexible stop profit and stop loss mechanism to maximize profits.

## Risk Analysis  

1. Improper Bollinger parameters may fail to correctly identify support areas.

2. Trend breaks or false breakouts could lead to errors in overbought/oversold judgments.

3. Incorrect stop profit and stop loss point settings may result in premature exit or increased losses.

## Optimization Directions

1. Optimize Bollinger parameters for more accurate identification of support and resistance levels.

2. Incorporate other indicators like MACD and KDJ to filter false signals.

3. Dynamically optimize stop profit and stop loss algorithms to maximize profits while minimizing losses.

## Summary

This strategy determines potential trend direction using RSI, combined with Bollinger Bands to identify support areas, achieving low buy high sell, which is a typical trending oscillation strategy. With proper optimization, it can become a reliable and stable profitable quantitative trading strategy.

|| 

Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|true|From Month|
|v_input_2|true|From Day|
|v_input_3|2018|From Year|
|v_input_4|true|To Month|
|v_input_5|true|To Day|
|v_input_6|9999|To Year|
|v_input_7|60|RSI Period Length|
|v_input_8|20|Bollinger Period Length|

Source (PineScript)

```pinescript
/*backtest
start: 2023-12-28 00:00:00
end: 2024-01-04 00:00:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("price drop buy in", overlay=true, initial_capital=1000, max_bars_back=24)

// === INPUT BACKTEST RANGE ===
FromMonth = input(defval = 1, title = "From Month", minval = 1, maxval = 12)
FromDay   = input(defval = 1, title = "From Day", minval = 1, maxval = 31)
FromYear  = input(defval = 2018, title = "From Year", minval = 2017)
ToMonth   = input(defval = 1, title = "To Month", minval = 1, maxval = 12)
ToDay     = input(defval = 1, title = "To Day", minval = 1, maxval = 31)
ToYear    = input(defval = 9999, title = "To Year", minval = 2017)

// === FUNCTION EXAMPLE ===
start     = timestamp(FromYear, FromMonth, FromDay, 00, 00)  // backtest start window
finish    = timestamp(ToYear, ToMonth, ToDay, 23, 59)        // backtest finish window
window()  => true // create function "within window of time"

///////////// RSI
RSIlength = input(60,title="RSI Period Length") 
RSIoverSold = 40
RSIoverBought = 50
price = close
vrsi = rsi(close, RSIlength)

smaLong = sma(close,80)
smaShort = sma(close,40)

///////////// Bollinger Bands
BBlength = input(20, minval=1,title="Bollinger Period Length")
BBmult = 2 // input(2.0, minval=0.001, maxval=50,title="Bollinger Bands Standard Deviation")
BBbasis = sma(price, BBlength)
BBdev = BBmult * stdev(price, BBlength)
BBupper = BBbasis + BBdev
BBlower = BBbasis - BBdev

longcondition = (price < BBlower and vrsi < RSIoverSold) 

    // vrsi < RSIoverSold

shortcondition = (RSIoverBought and strategy.openprofit > 50 )  or price > BBupper


if(longcondition)
    strategy.entry('buy', strategy.long, when = window())
    
if(shortcondition)
    strategy.entry('sell', strategy.short, when = window())

```

Detail

https://www.fmz.com/strategy/437773

Last Modified

2024-01-05 14:18:05
```