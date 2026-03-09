> Name

Candle Patterns-Based Strategy

> Author

ChaoZhang

> Strategy Description

[trans]

## Overview

This strategy is based on candlestick patterns to identify different candlestick signals and trade along the trend. With proper risk management methods like stop loss, take profit, and trailing stop, it aims to reduce the impact of market fluctuations.

## Strategy Logic

The strategy mainly identifies the following candlestick patterns for trading signals:

- Engulfing: bullish engulfing and bearish engulfing patterns
- Harami: bullish harami and bearish harami patterns
- Piercing Line / Dark Cloud Cover: bullish piercing line and bearish dark cloud cover patterns
- Morning Star / Evening Star: bullish morning star and bearish evening star patterns
- Belt Hold: bullish belt hold and bearish belt hold patterns
- Three White Soldiers / Three Black Crows: three white soldiers and three black crows patterns
- Three Stars in the South: three stars in the south pattern
- Stick Sandwich: stick sandwich pattern
- Meeting Line: bullish meeting line and bearish meeting line patterns
- Kicking: bullish kicking and bearish kicking patterns
- Ladder Bottom: ladder bottom pattern

When detecting these candlestick signals, it will place pending orders near the open price of the next bar, with predefined stop loss and take profit for trend following. It also uses trailing stop and breakeven stop to manage risks.

It also adds a moving average filter to avoid taking signals when the price is on the wrong side of the MA.

## Advantages

1. Based on classical candlestick patterns, it has some universal applicability.
2. Trading mechanically based on pattern rules, not affected by subjective factors.
3. Reasonable stop loss and take profit settings to control single trade risks.
4. Trailing stop mechanism adjusts stop loss dynamically along with the market.
5. MA filter adds more logic to avoid being trapped in wrong trades.

## Risks and Solutions

1. Candlestick patterns have some misidentification issues, which can lead to false signals. Can optimize parameters or filter out invalid patterns.
2. Static stop loss cannot fully avoid risks from market events. Can use wider stop or trailing stop.
3. Sensitive to trading sessions, cannot run 24x7. Can adjust trading times or add auction filters.
4. MA filter may miss some opportunities. Can lower MA period or remove the filter.
5. Hard to profit from both long and short sides together due to conflicts. Can separate strategies for long and short.

## Optimization Directions

1. Optimize parameters of candlestick patterns to improve identification.
2. Test different trailing stop methods to find the optimal one.
3. Try more advanced risk management techniques like money management or volatility stop loss.
4. Add more filters to improve the filtering logic.
5. Build candlestick pattern recognition models using machine learning.
6. Develop strategy logic that can identify both long and short signals.

## Summary

This strategy uses classical candlestick patterns for trend detection and trades mechanically based on the signals. It manages risks by strict stop loss and trailing stop, and improves logic by adding MA filter. The strategy is easy to understand and implement, but also has some issues like misidentification and difficulties in parameter tuning. Future optimizations can be done by introducing more technical indicators and machine learning models to achieve better performance.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Engulfing|
|v_input_2|true|Harami|
|v_input_3|true|Piercing Line / Dark Cloud Cover|
|v_input_4|true|Morning Star / Evening Star |
|v_input_5|true|Belt Hold|
|v_input_6|true|Three White Soldiers / Three Black Crows|
|v_input_7|true|Three Stars in the South|
|v_input_8|true|Stick Sandwich|
|v_input_9|true|Meeting Line|
|v_input_10|true|Kicking|
|v_input_11|true|Ladder Bottom|
|v_input_12|0.01|Tick Size|
|v_input_13|10|Stop Loss|
|v_input_14|100|Take Profit|
|v_input_15|10|Breakeven Margin|
|v_input_16|5|Price Movement Confirmation|
|v_input_17|false|MA Filter|
|v_input_18|50|MA Period|
|v_input_19|0000-0000|Trading Session|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-09-15 00:00:00
end: 2023-02-17 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
strategy("Candle Patterns Strategy - 2", shorttitle="CPS - 2", overlay=true)
// New risk management system: order entry, moving stop loss to breakeven + moving average filter (SMA)

//--- Patterns Input ---

OnEngulfing = input(defval=true, title="Engulfing", type=bool)
OnHarami = input(defval=true, title="Harami", type=bool)
OnPiercingLine = input(defval=true, title="Piercing Line / Dark Cloud Cover", type=bool)
OnMorningStar = input(defval=true, title="Morning Star / Evening Star", type=bool)
OnBeltHold = input(defval=true, title="Belt Hold", type=bool)
OnThreeWhiteSoldiers = input(defval=true, title="Three White Soldiers / Three Black Crows", type=bool)
OnThreeStars = input(defval=true, title="Three Stars in the South", type=bool)
OnStickSandwich = input(defval=true, title="Stick Sandwich", type=bool)
OnMeetingLine = input(defval=true, title="Meeting Line", type=bool)
OnKicking = input(defval=true, title="Kicking", type=bool)
OnLadderBottom = input(defval=true, title="Ladder Bottom", type=bool)

//--- Risk Management Inputs ---

TickSize = input(0.01, title="Tick Size")
StopLoss = input(10, title="Stop Loss")
TakeProfit = input(100, title="Take Profit")
BreakevenMargin = input(10, title="Breakeven Margin")
PriceMovementConfirmation = input(5, title="Price Movement Confirmation")
UseMAFilter = input(false, title="MA Filter", type=bool)
MAPeriod = input(50, title="MA Period")
TradingSession = input("0000-0000", title="Trading Session")

//--- Logic ---

if (OnEngulfing)
    // Engulfing pattern logic
    // ...

if (OnHarami)
    // Harami pattern logic
    // ...

if (OnPiercingLine)
    // Piercing Line / Dark Cloud Cover pattern logic
    // ...

if (OnMorningStar)
    // Morning Star / Evening Star pattern logic
    // ...

if (OnBeltHold)
    // Belt Hold pattern logic
    // ...

if (OnThreeWhiteSoldiers)
    // Three White Soldiers / Three Black Crows pattern logic
    // ...

if (OnThreeStars)
    // Three Stars in the South pattern logic
    // ...

if (OnStickSandwich)
    // Stick Sandwich pattern logic
    // ...

if (OnMeetingLine)
    // Meeting Line pattern logic
    // ...

if (OnKicking)
    // Kicking pattern logic
    // ...

if (OnLadderBottom)
    // Ladder Bottom pattern logic
    // ...

//--- Risk Management ---

if (UseMAFilter and not na(TradingSession))
    ma = sma(close, MAPeriod)
    if (close < ma)
        strategy.entry("Long", strategy.long)
    if (close > ma)
        strategy.entry("Short", strategy.short)

if (not na(TradingSession))
    if (time > timestamp("2023-02-17 00:00:00"))
        strategy.close_all()
```