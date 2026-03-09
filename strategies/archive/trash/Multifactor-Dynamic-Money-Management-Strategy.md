> Name

Multifactor-Dynamic-Money-Management-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1efccebef172067cffb.png)

## Overview 

This strategy integrates the use of MACD, RSI, PSAR, and other technical indicators with dynamic money management principles to track trends and execute reversal trades across multiple timeframes. The strategy can be applied for short-term, medium-term, and long-term trading.

## Principles

The strategy uses the PSAR indicator to determine the trend direction. The crossover between EMA and BB middle line serves as the first confirmation point. The MACD histogram direction acts as the second confirmation point. The RSI overbought and oversold areas serve as the third confirmation point. Trading signals are generated when all the above conditions are met.

After entering the position, stop loss and take profit points are set. The stop loss point is determined by multiplying the ATR value by a fixed number. The take profit point is calculated in the same way. Meanwhile, a floating loss percentage stop loss is set. When the loss reaches a certain percentage of total account equity, the stop loss will be triggered.

There is also a percentage setting for floating profit. When profit reaches a certain percentage of total account equity, take profit will be triggered.

Dynamic money management calculates position size based on total account equity, ATR value, and the multiplier used for stop loss. Minimum trading quantity is also set.

## Advantages

1. Multiple factor confirmation avoids false breakouts and improves entry accuracy.

2. Dynamic money management controls single trade risk and protects the account effectively.

3. Stop loss and take profit points are set according to ATR, which can be adjusted based on market volatility.

4. Floating loss and profit percentage settings lock in profits and prevent pullbacks.

## Risks

1. Multiple factor combinations may miss some trading opportunities.

2. High percentage settings can lead to greater losses.

3. Improper ATR value settings may result in stop loss and take profit points that are too wide or too aggressive.

4. Improper money management settings may lead to excessively large position sizes.

## Optimization Directions

1. Adjust factor weights to improve signal accuracy.

2. Test different percentage parameter settings to find optimal combinations.

3. Select reasonable ATR multipliers based on different product characteristics.

4. Dynamically adjust money management parameters based on backtest results.

5. Optimize timeframe settings and test trading sessions.

## Summary

This strategy integrates multiple technical indicators for trend determination and adds dynamic money management to control risks, achieving stable profits across multiple timeframes. It can be further optimized by adjusting factor weights, risk control parameters, and money management settings based on backtest results.

---

## Strategy Arguments

| Argument | Default | Description |
| --- | --- | --- |
| v_input_1 | true | From Day |
| v_input_2 | 6 | From Month |
| v_input_3 | 2020 | From Year |
| v_input_4 | true | To Day |
| v_input_5 | 12 | To Month |
| v_input_6 | 2020 | To Year |
| v_input_7 | 5 | length |
| v_input_8 | 23 | overSold |
| v_input_9 | 72 | overBought |
| v_input_10 | 12 | Fast Length |
| v_input_11 | 26 | Slow Length |
| v_input_12_close | 0 | Source: close | high | low | open | hl2 | hlc3 | hlcc4 | ohlc4 |
| v_input_13 | 9 | Signal Smoothing |
| v_input_14 | true | Simple MA (Oscillator) |
| v_input_15 | true | Simple MA (Signal Line) |
| v_input_16 | 0.02 | start |
| v_input_17 | 0.02 | increment |
| v_input_18 | 0.2 | maximum |
| v_input_19 | 17 | length_bb |
| v_input_20_close | 0 | Source: close | high | low | open | hl2 | hlc3 | hlcc4 | ohlc4 |
| v_input_21 | 2 | StdDev |
| v_input_22 | false | Offset |
| v_input_23 | 10 | Length |
| v_input_24_close | 0 | Source: close | high | low | open | hl2 | hlc3 | hlcc4 | ohlc4 |
| v_input_25 | false | Offset |
| v_input_26 | 14 | Average True Range Period |
| v_input_27 | 2 | Risk % |
| v_input_28 | false | Is this a 2 digit pair? (JPY, XAU, XPD... |
| v_input_29 | true | Equity Protection % |
| v_input_30 | 2 | Equity TP % |
| v_input_31 | 5 | multi atr tp |
| v_input_32 | 5 | multi atr sl |
| v_input_33 | true | SL X |
| v_input_34 | true | TP X |

---

> Source (PineScript)

```pinescript
/*backtest
start: 2023-09-16 00:00:00
end: 2023-10-16 00:00:00
period: 10m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © SoftKill21

//@version=4
strategy("EURUSD 1min strat RISK %", overlay=false, initial_capital = 1000)

// BACKTESTING RANGE
 
// From Date Inputs
fromDay = input(defval = 1, title = "From Day", minval = 1, maxval = 31)
fromMonth = input(defval = 6, title = "From Month", minval = 1, maxval = 12)
fromYear = input(defval = 2020, title = "From Year", minval = 1970)
 
// To Date Inputs
toDay = input(defval = 1, title = "To Day", minval = 1, maxval = 31)
toMonth = input(defval = 12, title = "To Month", minval = 1, maxval = 12)
toYear = input(defval = 2020, title = "To Year", minval = 1970)
 
// Calculate start/end date and time condition
DST = 1 //day light saving for usa
```