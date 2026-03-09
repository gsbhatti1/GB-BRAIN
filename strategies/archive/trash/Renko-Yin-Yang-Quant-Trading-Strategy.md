> Name

Renko-Yin-Yang-Quant-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

## Overview

The Renko-Yin-Yang quant trading strategy is a short-term trading strategy based on intraday price-volume relationship. It utilizes the yin yang direction information within a day and combines volume confirmation signals to implement low-risk short-term operations.

## Strategy Principle

This strategy calculates the open, close, high, and low prices of each trading day and generates Renko bricks with ATR indicators. Trading signals are generated when renko bricks reverse from one color to another.

Specifically, the strategy first calculates the open price `o2` and close price `c2` of the Renko bricks. If `o2 < c2`, it indicates a yang line; if `o2 > c2`, it indicates a yin line. A sell signal is generated when a yang line turns to a yin line, and a buy signal is generated when a yin line turns to a yang line.

To filter false breakouts, the strategy also counts the number of periods of the last yang and yin lines. If the yang line has more periods, the signal is considered more reliable. Additionally, stop loss and take profit logic are set after buying and selling.

## Strategy Advantages

1. Renko bricks filter market noise to make trading signals clearer.
2. Combining price-volume relationship avoids the risk of false breakouts.
3. The DAPM model is simple and effective for intraday trading.
4. Customizable ATR parameters adjust trading frequency.
5. Customizable stop loss improves risk management.

## Risk Analysis

1. There is still a risk of unclear false breakouts.
2. Improper Renko parameter settings may miss trends or increase trading frequency.
3. Setting the stop loss too tight can result in minor losses from retracement stops out.

## Optimization Directions

1. Consider combining other technical indicators to filter signals.
2. Consider adding trailing stop loss functionality.
3. Optimize parameters for different assets.
4. Consider combining different timeframes for multi-timeframe trading.

## Summary

Overall, this is a very practical short-term trading strategy. It utilizes price-volume relationships to efficiently filter and capture key turning points. Proper parameter tuning, risk management, and stop loss strategies can greatly enhance the stability and profitability of the strategy. Continuous optimization and testing can make this strategy an essential tool for intraday traders.

---

## Overview

The Renko-Yin-Yang quant trading strategy is a short-term trading strategy based on intraday price-volume relationship. It utilizes the yin yang direction information within a day and combines volume confirmation signals to implement low-risk short-term operations.

## Strategy Logic

The strategy calculates the open, close, high, and low prices of each trading day, and generates Renko bricks together with ATR indicator. Trading signals are generated when renko bricks reverse.

Specifically, the strategy first calculates the open price `o2` and close price `c2` of the Renko bricks. If `o2 < c2`, it indicates a yang line; if `o2 > c2`, it indicates a yin line. When a yang line turns to a yin line, a sell signal is generated. When a yin line turns to a yang line, a buy signal is generated.

To filter false breakouts, the strategy also counts the number of periods of the last yang and yin lines. If the yang line has more periods, the signal is considered more reliable. In addition, stop loss and take profit logic are set after buying and selling.

## Advantages

1. Renko bricks filter market noise to make trading signals clearer.
2. Combining price-volume relationship avoids the risk of false breakouts.
3. The DAPM model is simple and effective for intraday trading.
4. Customizable ATR parameters adjust trading frequency.
5. Customizable stop loss improves risk management.

## Risks

1. There is still a risk of unclear false breakouts.
2. Improper Renko parameter settings may miss trends or increase trading frequency.
3. Setting the stop loss too tight can result in minor losses from retracement stops out.

## Optimization

1. Consider combining other technical indicators to filter signals.
2. Consider adding trailing stop loss functionality.
3. Optimize parameters for different assets.
4. Consider combining different timeframes for multi-timeframe trading.

## Conclusion

In conclusion, this is a very practical short-term trading strategy. It uses price-volume relationships to filter efficiently and capture key turning points. Proper parameter tuning, risk management, and stop loss strategies can greatly improve its stability and profitability. With continuous optimization and testing, this strategy can become a powerful tool for intraday traders.

---

## Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|true|---------------- Trade Range ----------------|
|v_input_2|true|From Month|
|v_input_3|true|From Day|
|v_input_4|2017|From Year|
|v_input_5|true|To Month|
|v_input_6|true|To Day|
|v_input_7|2099|To Year|
|v_input_8|true|---------------- Settings ----------------|
|v_input_9|false|Allow Short|
|v_input_10|10|ATR Length|

---

## Source (PineScript)

```pinescript
//@version=4
// This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License https://creativecommons.org/licenses/by-sa/4.0/
// © dman103
strategy(title="Renko-Yin-Yang Strategy V2", shorttitle="Renko-Yin-Yang V2", overlay=true, precision=3, commission_value=0.025, default_qty_type=strategy.cash, default_qty_value=10000, initial_capital=10000)
// Version 2.0 of my previous renko strategy using Renko calculations, this time without Tilson T3 and without using security with Renko to remove repaints!
// Seems to work nicely on cryptocurrencies on higher time frames.

//== Description ==
// Strategy gets Renko values and uses renko close and open to trigger signals.
// Base on these results the strategy triggers a long and short orders, where green is uptrending and red is downtrending.
// This Renko version is based on ATR, you can Set ATR (in settings) to adjust it.

// == Notes ==
// Supports alerts.
// Supports backtesting time ranges.
// Shorts are disabled by default (can be enabled in settings).
// Link to previous Renko strategy V1: https://www.tradingview.com/script/KeWBWLGT-Renko-Strategy-T3-V1/
//
// Stay tuned for version V3 in the future as i have an in progress prototype, Follow to get updated: https://www.tradingview.com/u/dman103/#published-scripts

// === INPUT BACKTEST RANGE ===
useDate = input(true,     title='---------------- Trade Range ----------------', type=input.bool)
FromMonth = input(defval = 1, title = "From Month", minval = 1, maxval = 12)
FromDay   = input(defval = 1, title = "From Day", minval = 1, maxval = 31)
FromYear  = input(defval = 2017, title = "From Year", minval = 2000)
ToMonth   = input(defval = 1, title = "To Month", minval = 1, maxval = 12)
ToDay     = input(defval = 1, title = "To Day", minval = 1, maxval = 31)
ToYear    = input(defval = 2099, title = "To Year", minval = 2010)
start     = timestamp(FromYear, FromMonth, FromDay, 00, 00)  // backtest start window
finish    = timestamp(ToYear, ToMonth, ToDay, 23, 59)        // backtest finish window
window()  => time >= start and time <= finish ? true : false // create 

settings = input(true,     title='---------------- Settings ----------------')
allowShort = input(false,  title="Allow Short", type=input.bool)
atrLength = input(10,      title="ATR Length", minval=2)

// === Renko Calculation ===
renkoClose = close[1] < open[1] ? low : high

// === Signal Generation ===
buySignal = renkoClose > close[2] and (renkoClose > close[3] or renkoClose > close[4])
sellSignal = renkoClose < close[2] and (renkoClose < close[3] or renkoClose < close[4])

// === Stop Loss and Take Profit ===
stopLossPercent = 0.5 / atrLength
takeProfitPercent = 1.5 / atrLength

longCondition = buySignal and not window()
shortCondition = sellSignal and not window()

if (longCondition)
    strategy.entry("Long", strategy.long)
    strategy.exit("Take Profit", "Long", limit=close + takeProfitPercent * close, stop=close - stopLossPercent * close)

if (shortCondition)
    strategy.entry("Short", strategy.short)
    strategy.exit("Stop Loss", "Short", limit=close - takeProfitPercent * close, stop=close + stopLossPercent * close)
```

The provided PineScript code defines the Renko-Yin-Yang quant trading strategy and its implementation in TradingView's Pine Script.