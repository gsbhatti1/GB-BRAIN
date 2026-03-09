> Name

ADX Momentum Trend Strategy ADX-Momentum-Trend-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/103121df2e4eda3a4c9.png)

[trans]
## Overview

This strategy uses the ADX indicator to determine market trends, combines with DMI indicators to determine the direction of bullish or bearish forces, utilizes the slope of ADX to gauge trend strength, sets a key level for ADX to filter out non-trending markets, and uses moving averages as filters for trading signals.

## Strategy Logic

1. Calculate the ADX, DI+, and DI- indicators.
2. An ADX slope > 0 indicates an increasing trend; a key level of 23 is set to filter out non-trending markets.
3. DI+ above DI- signifies that bullish momentum outweighs bearish momentum, generating a buy signal.
4. When moving average filtering is enabled, only generate long signals when the closing price is above the moving average.
5. Close positions when ADX slope < 0, indicating a fading trend.

## Advantage Analysis

1. MA filter reduces noise trades in non-trending markets.
2. The ADX slope accurately determines the strength of trends.
3. DI indicates direction combined with ADX for strength forms a robust trend trading system.
4. Expected lower drawdown and higher profit factor than simple moving average strategies.

## Risk Analysis

1. Results vary significantly with different input parameters for ADX.
2. DMI may give false signals before the direction is clearly determined.
3. Some lag exists, reducing strategy efficiency.

## Optimization Directions

1. Optimize ADX parameter combinations to find the best settings.
2. Add stop loss strategies to limit losses on single trades.
3. Try combining other indicators to filter signals, such as RSI or Bollinger Bands.

## Summary

This strategy fully leverages the strengths of ADX in determining trends and trend strength, combined with DMI for direction analysis, forming a complete trend-following system. The MA filter effectively reduces noise. Further parameter tuning and indicator combinations can improve stability and efficiency. Overall, by incorporating trend and momentum analysis, this strategy has the potential to achieve good returns.

||

## Overview  

This strategy uses the ADX indicator to determine market trends, combines with DMI indicators to determine direction, utilizes the slope of ADX to gauge trend strength, sets a key level for ADX to filter out non-trending markets, and uses moving averages as filters for trading signals.

## Strategy Logic   

1. Calculate the ADX, DI+, and DI- indicators.  
2. An ADX slope > 0 indicates an increasing trend; a key level of 23 is set to filter out non-trending markets.
3. DI+ above DI- signifies that bullish momentum outweighs bearish momentum, generating a buy signal. 
4. When moving average filtering is enabled, only generate long signals when the closing price is above the moving average.  
5. Close positions when ADX slope < 0, indicating a fading trend.

## Advantage Analysis   

1. MA filter reduces noise trades in non-trending markets.
2. The ADX slope accurately determines the strength of trends.
3. DI indicates direction combined with ADX for strength forms a robust trend trading system.
4. Expected lower drawdown and higher profit factor than simple moving average strategies.

## Risk Analysis

1. Results vary significantly with different input parameters for ADX.
2. DMI may give false signals before the direction is clearly determined.
3. Some lag exists, reducing strategy efficiency.

## Optimization Directions  

1. Optimize ADX parameter combinations to find the best settings.
2. Add stop loss strategies to limit losses on single trades.
3. Try combining other indicators to filter signals, e.g., RSI or Bollinger Bands.

## Summary

This strategy fully leverages the strengths of ADX in determining trends and trend strength, combined with DMI for direction analysis, forming a complete trend-following system. The MA filter effectively reduces noise. Further parameter tuning and indicator combinations can improve stability and efficiency. Overall, by incorporating trend and momentum analysis, this strategy has the potential to achieve good returns.

---

## Source (Pine Script)

```pinescript
//@version=4
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © millerrh with inspiration from @9e52f12edd034d28bdd5544e7ff92e 
// The intent behind this study is to look at ADX when it has an increasing slope and is above a user-defined key level (23 default). 
// This is to identify when it is trending.
// It then looks at the DMI levels.  If D+ is above D- and the ADX is sloping upwards and above the key level, it triggers a buy condition.  Opposite for short.
// Can use a user-defined moving average to filter long/short if desired.
// NOTE: THIS IS MEANT TO BE USED IN CONJUNCTION WITH MY "ATX TRIGGER" INDICATOR FOR VISUALIZATION. MAKE SURE SETTINGS ARE THE SAME FOR BOTH.

strategy("ADX | DMI Trend", overlay=true, initial_capital=10000, currency='USD', 
   default_qty_type=strategy.percent_of_equity, default_qty_value=100, commission_type=strategy.commission.percent, commission_value=0.04)

// === BACKTEST RANGE ===
From_Year  = input(defval = 2019, title = "From Year")
From_Month = input(defval = 1, title = "From Month", minval = 1, maxval = 12)
From_Day   = input(defval = 1, title = "From Day", minval = 1, maxval = 31)
To_Year    = input(defval = 9999, title = "To Year")
To_Month   = input(defval = 1, title = "To Month", minval = 1, maxval = 12)
To_Day     = input(defval = 1, title = "To Day", minval = 1, maxval = 31)
Start      = timestamp(From_Year, From_Month, From_Day, 00, 00)  // backtest start window
Finish     = timestamp(To_Year, To_Month, To_Day, 23, 59)        // backtest finish window

// == INPUTS ==
// ADX Info
adxlen = input(14, title="ADX Smoothing")
dilen = input(14, title="DI Period")
keyLevel = input(23, title="Keylevel for ADX")
adxLookback = input(3, title="Lookback Period for Slope")

// == FILTERING ==
// Inputs
useMaFilter = input(title = "Use MA for Filtering?", type = input.bool, defval = true)
maType = input(defval="EMA", options=["EMA", "SMA"], title = "MA Type For Filtering")
maLength   = input(defval = 200, title = "MA Period for Filtering", minval = 1)

// Declare function to be able to swap out EMA/SMA
ma(maType, src, length) =>
    maType == "EMA" ? ema(src, length) : sma(src, length) //Ternary Operator (if maType equals EMA, then do ema calc, else do sma calc)
maFilter = ma(maType, close, maLength)
plot(maFilter, title = "Trend Filter MA", color = color.green, linewidth = 3, style = plot.style_line, transp = 50)

// Check to
```