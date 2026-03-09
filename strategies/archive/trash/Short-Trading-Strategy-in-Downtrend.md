---
### Overview

This strategy takes advantage of a downtrend by building short positions gradually based on moving average and RSI indicators. It aims for profit in falling markets.

### Strategy Logic

When the close price is below the 100-day simple moving average (SMA) and the RSI is greater than 30, enter a short position. Then set the stop loss above the entry price by more than 3%, and take profit below the entry price by less than 2%. The wider stop loss allows for greater volatility tolerance to avoid unnecessary stops. Close the position when the price surpasses the stop loss or falls below the take profit.

On the Coinrule platform, set multiple sequential sell orders to build a position gradually. When the downtrend persists, increase the position size. Setting a time interval between orders also helps in controlling overall position size.

Each trade is connected with both a stop loss order and a take profit order. The percentages are optimized for mid-cap coins. You can adjust them based on specific coin. As it trades along with the trend, the stop loss and take profit ratio like 1:1.5 could work well.

Stop loss at 3% above entry price  
Take profit at 2% below entry price  
A slightly larger stop loss tolerates more volatility.

### Advantage Analysis

- The moving average (MA) judges trend direction well, allowing timely capture of a downtrend
- The RSI filter avoids blindly entering short positions
- Gradual position building controls risk maximally with a better risk-reward ratio
- Stop loss and take profit ensure each trade has the necessary endurance

### Risk Analysis

- A sharp V-shaped reversal could lead to significant losses  
- Need to closely monitor price movements and adjust stop loss and take profit levels
- Leverage should be reasonable to control position size
- Pausing the strategy in choppy markets avoids unnecessary losses

### Optimization Directions 

- Test different parameters for the moving average indicator
- Test RSI combinations with different parameters
- Adjust stop loss and take profit ratios to optimize risk-reward
- Test different time intervals between orders to control position size

### Summary

This strategy effectively captures a downtrend based on MA and RSI. Gradual position building controls risk while stop loss and take profit ensure endurance for each trade. Further optimizing the risk-reward ratio by adjusting the stop loss/take profit parameters can yield better results. There is room for improvements in parameter settings and risk control, but overall it is a solid short-term short strategy.

---

## Overview

This strategy takes advantage of downtrends by building short positions gradually based on moving average (MA) and Relative Strength Index (RSI) indicators. It aims to profit from falling markets.

## Strategy Logic

When the close price is below the 100-day simple moving average and RSI is greater than 30, go short. Then set a stop loss above the entry price by more than 3%, and take profit below the entry price by less than 2%. The wider stop loss allows for greater volatility tolerance to avoid unnecessary stops. Close the position when the price surpasses the stop loss or falls below the take profit.

On the Coinrule platform, set multiple sequential sell orders to build a position gradually. When the downtrend persists, increase the position size. Setting a time interval between orders also helps in controlling overall position size.

Each trade is connected with both a stop loss order and a take profit order. The percentages are optimized for mid-cap coins. You can adjust them based on specific coin. As it trades along with the trend, the stop loss and take profit ratio like 1:1.5 could work well.

Stop loss at 3% above entry price  
Take profit at 2% below entry price  
A slightly larger stop loss tolerates more volatility.

## Advantage Analysis

- The moving average (MA) judges trend direction well, allowing timely capture of downtrends
- The RSI filter avoids blindly going short
- Gradual position building controls risk maximally with a better risk-reward ratio
- Stop loss and take profit ensure each trade has the necessary endurance

## Risk Analysis

- A sharp V-shaped reversal could lead to significant losses  
- Need to closely monitor price movements and adjust stop loss and take profit levels
- Leverage should be reasonable to control position size
- Pausing the strategy in choppy markets avoids unnecessary losses

## Optimization Directions 

- Test different parameters for the moving average indicator
- Test RSI combinations with different parameters
- Adjust stop loss and take profit ratios to optimize risk-reward
- Test different time intervals between orders to control position size

## Summary

This strategy effectively captures downtrends based on MA and RSI. Gradual position building controls risk while stop loss and take profit ensure endurance for each trade. Further optimizing the risk-reward ratio by adjusting the stop loss/take profit parameters can yield better results. There is room for improvements in parameter settings and risk control, but overall it is a solid short-term short strategy.

---

### Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|v_input_1|true|From Month|
|v_input_2|10|From Day|
|v_input_3|2019|From Year|
|v_input_4|true|Thru Month|
|v_input_5|true|Thru Day|
|v_input_6|2112|Thru Year|
|v_input_7|true|Show Date Range|
|v_input_8|50|MASignal|
|v_input_9|14|RSI period|

### Source (PineScript)

```pinescript
/*backtest
start: 2022-10-31 00:00:00
end: 2023-11-06 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Coinrule

//@version=4
strategy(shorttitle='Short In Downtrend', title='Short In Downtrend Below MA100', overlay=true, initial_capital = 1000, process_orders_on_close=true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100)

// Backtest dates
fromMonth = input(defval = 1, title = "From Month", type = input.integer, minval = 1, maxval = 12)
fromDay   = input(defval = 10, title = "From Day", type = input.integer, minval = 1, maxval = 31)
fromYear  = input(defval = 2019, title = "From Year", type = input.integer, minval = 1970)
thruMonth = input(defval = 1, title = "Thru Month", type = input.integer, minval = 1, maxval = 12)
thruDay   = input(defval = 1, title = "Thru Day", type = input.integer, minval = 1, maxval = 31)
thruYear  = input(defval = 2112, title = "Thru Year", type = input.integer, minval = 1970)

showDate  = input(defval = true, title = "Show Date Range", type = input.bool)

start     = timestamp(fromYear, fromMonth, fromDay, 00, 00)        // backtest start window
finish    = timestamp(thruYear, thruMonth, thruDay, 23, 59)        // backtest finish window
window()  => true       // create function "within window of time"

// MA inputs and calculations
inSignal=input(50, title='MASignal')

MA= sma(close, inSignal)

// RSI inputs and calculations
lengthRSI = input(14, title = 'RSI period', minval=1)
RSI = rsi(close, lengthRSI)


// Entry 
strategy.entry(id="short", long = false, when = close < MA and RSI > 30)

// Exit
shortStopPrice  = strategy.position_avg_price * (1 + 0.03)
shortTakeProfit = strategy.position_avg_price * (1 - 0.02)

strategy.close("short", when = close > shortStopPrice or close < shortTakeProfit and window())


plot(MA, color=color.purple, linewidth=2)
```

### Detail

https://www.fmz.com/strategy/431428

### Last Modified

2023-11-07 17:06:59