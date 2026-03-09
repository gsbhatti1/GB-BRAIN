> Name

STC-MA-ATR Integrated Trend Trading Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/550f6d2fc5464ca01e.png)

[trans]

## Overview

This strategy integrates the technical indicators STC, Moving Average MA, and Average True Range ATR to judge trends and implement relatively stable trend tracking trading.

## Strategy Principle 

1. The STC indicator judges trend reversals. It utilizes the fast line minus the slow line, then processes secondary smoothing, forming consistent trend signals. A buying signal is generated when the indicator crosses above 0 axis, and a selling signal when it crosses below 0 axis.

2. Moving Average MA judges trend direction. When stock price crosses above MA, it signals an uptrend, giving a long position holding signal. When price crosses below MA, it signals a downtrend, giving a short position holding signal.

3. ATR indicator sets stop loss and take profit points. ATR can dynamically adjust stop loss and take profit levels based on market volatility. It also acts as a trading direction signal itself, rising in an uptrend and falling in a downtrend.

4. The strategy uses STC signals primarily for entry timing, with MA as auxiliary trend judgment, and ATR for stop loss and take profit. When STC gives a buy signal, if MA is also showing an uptrend and ATR is rising, it opens a long position; when STC gives a sell signal, if MA shows a downtrend and ATR is falling, it opens a short position.

## Advantage Analysis

1. The strategy combines multiple indicators to judge trends and reversal points, improving the accuracy of trading signals.

2. STC can capture reversal signals and avoid being trapped in trends. MA filters uncertain reversal signals, ensuring following the main trend.

3. ATR sets dynamic stop loss and take profit based on market volatility, avoiding huge losses. And it acts as an auxiliary signal for trend judgment.

4. The combination of multiple indicators forms strong trend tracking ability. Historical backtests show relatively stable profitability.

## Risk Analysis

1. STC has time lag, which may miss the optimal timing for price reversal.

2. MA tends to lag during violent price swings, which may generate wrong signals.

3. ATR stop loss may be hit in seconds. The ATR multiplier should be loosened, or temporarily disabled during big trends.

4. More indicators mean more chances of hitting stop loss. Parameters should be adjusted to avoid unnecessary stop loss.

## Optimization Directions

1. Adjust STC parameters to find faster responsive combinations for reversal.

2. Optimize MA period parameter for better trend tracking.

3. Test impacts of different ATR multiples.

4. Try replacing STC with other indicators for a better match.

5. Introduce machine learning algorithms for multi-parameter auto optimization.

6. Consider large cycle trends and distinguish different stages.

## Summary

The STC-MA-ATR strategy integrates three indicators to capture trend reversal points, achieving stable trend tracking trading. Indicator combinations filter false signals and control risks with stop loss/take profit mechanisms, providing strong robustness and stability. Further improvements can be achieved through parameter optimization and algorithm introduction. Overall, it is a reliable and moderate strategy choice.

||

## Overview

This strategy combines the technical indicators STC, Moving Average MA, and Average True Range ATR to judge trends and implement relatively stable trend tracking trading.

## Strategy Principle 

1. The STC indicator judges trend reversals. It utilizes the fast line minus the slow line, then processes secondary smoothing, forming consistent trend signals. A buying signal is generated when the indicator crosses above 0 axis, and a selling signal when it crosses below 0 axis.

2. Moving Average MA judges trend direction. When stock price crosses above MA, it signals an uptrend, giving a long position holding signal. When price crosses below MA, it signals a downtrend, giving a short position holding signal.

3. ATR indicator sets stop loss and take profit points. ATR can dynamically adjust stop loss and take profit levels based on market volatility. It also acts as a trading direction signal itself, rising in an uptrend and falling in a downtrend.

4. The strategy uses STC signals primarily for entry timing, with MA as auxiliary trend judgment, and ATR for stop loss and take profit. When STC gives a buy signal, if MA is also showing an uptrend and ATR is rising, it opens a long position; when STC gives a sell signal, if MA shows a downtrend and ATR is falling, it opens a short position.

## Advantage Analysis

1. The strategy combines multiple indicators to judge trends and reversal points, improving the accuracy of trading signals.

2. STC can capture reversal signals and avoid being trapped in trends. MA filters uncertain reversal signals, ensuring following the main trend.

3. ATR sets dynamic stop loss and take profit based on market volatility, avoiding huge losses. And it acts as an auxiliary signal for trend judgment.

4. The combination of multiple indicators forms strong trend tracking ability. Historical backtests show relatively stable profitability.

## Risk Analysis

1. STC has time lag, which may miss the optimal timing for price reversal.

2. MA tends to lag during violent price swings, which may generate wrong signals.

3. ATR stop loss may be hit in seconds. The ATR multiplier should be loosened, or temporarily disabled during big trends.

4. More indicators mean more chances of hitting stop loss. Parameters should be adjusted to avoid unnecessary stop loss.

## Optimization Directions

1. Adjust STC parameters to find faster responsive combinations for reversal.

2. Optimize MA period parameter for better trend tracking.

3. Test impacts of different ATR multiples.

4. Try replacing STC with other indicators for a better match.

5. Introduce machine learning algorithms for multi-parameter auto optimization.

6. Consider large cycle trends and distinguish different stages.

## Summary

The STC-MA-ATR strategy integrates three indicators to capture trend reversal points, achieving stable trend tracking trading. Indicator combinations filter false signals and control risks with stop loss/take profit mechanisms, providing strong robustness and stability. Further improvements can be achieved through parameter optimization and algorithm introduction. Overall, it is a reliable and moderate strategy choice.

||

## Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_9|true|Close position when ATR changes color|
|v_input_1|12|(?STC)Length|
|v_input_2|26|FastLength|
|v_input_3|50|SlowLength|
|v_input_4|5|(?ATR Stops)nATRPeriod|
|v_input_5|3.5|nATRMultip|
|v_input_6|200|(?Moving Average)MA Length|
|v_input_7|2|(?Strategy)Take Profit ATR Multiplier|
|v_input_8|true|Stop Loss ATR Multiplier|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-09-16 00:00:00
end: 2023-10-16 00:00:00
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Romedius

//@version=5
strategy("My Strategy", overlay=true, margin_long=100, margin_short=100)

// STC
EEEEEE = input(12, "Length", group="STC")
BBBB = input(26, "FastLength", group="STC")
BBBBB = input(50, "SlowLength", group="STC")

AAAA(BBB, BBBB, BBBBB) =>
    fastMA = ta.ema(BBB, BBBB)
    slowMA = ta.ema(BBB, BBBBB)
    AAAA = fastMA - slowMA
    AAAA

AAAAA(EEEEEE, BBBB, BBBBB) => 
    //AAA = input(0.5)
    var AAA = 0.5
    var CCCCC = 0.0
    var DDD = 0.0
    var DDDDDD = 0.0
    var EEEEE = 0.0
    BBBBBB = AAAA(close, BBBB, BBBBB)     
    CCC = ta.lowest(BBBBBB, EEEEEE)
    CCCC = ta.highest(BBBBBB, EEEEEE) - CCC    
    CCCCC := (CCCC > 0 ? ((BBBBBB - CCC) / CCCC) * 100 : nz(CCCCC[1])) 
    DDD := (na(DDD[1]) ? CCCCC : DDD[1] + (AAA * (CCCCC - DDD[1]))) 
    DDDD = ta.lowest(DDD, EEEEEE) 
    DDDDD = ta.highest(DDD,