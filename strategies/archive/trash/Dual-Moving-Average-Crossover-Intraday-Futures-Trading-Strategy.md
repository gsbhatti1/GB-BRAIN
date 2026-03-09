> Name

Dual-Moving-Average-Crossover-Intraday-Futures-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/11c185631535c2f1ddc.png)
[trans]

## Overview

This strategy employs the principle of dual moving average crossover, combined with ATR indicators to set stop loss and take profit levels. It also includes time control mechanisms to design a day trading strategy for futures contracts. The strategy is simple and easy to understand, making it suitable for beginners.

## Strategy Logic

The strategy uses 5-period and 20-period WMA moving averages crossing as entry signals. When the 5-period line breaks above the 20-period line, a long position is initiated; when the 5-period line breaks below the 20-period line, a short position is initiated. Additionally, it uses a 50-period WMA to determine the overall trend direction. Trading signals are only generated when the price breakout direction aligns with the major trend.

Moreover, ATR indicators are employed to set stop loss and take profit levels dynamically. The ATR indicator reflects market volatility. The strategy sets stop loss and take profit levels based on multiplying the ATR value by a factor (e.g., 3 times) to control per trade losses.

Finally, trading signals are restricted to US trading hours (9:00-14:30 CST) to avoid high volatility periods around market open and close, where false signals may occur easily.

## Advantage Analysis

The strategy has the following advantages:

1. Dual moving average crossover effectively captures trend reversals for timely entry.
2. Trend filtering helps filter out noise signals, avoiding contrarian trading.
3. Dynamic ATR-based stop loss and take profit levels control per trade losses.
4. Limiting trading hours avoids volatile open and close periods.
5. Simple rules that are easy to understand and implement, making it suitable for beginners.
6. Customizable parameters such as moving average periods, ATR multipliers, and trading hours can be adjusted.

## Risk Analysis

The strategy also has the following risks:

1. More frequent stop loss triggers in range-bound markets.
2. Dual moving average crossover may have some lag and miss short-term breakouts.
3. Incorrectly set ATR parameters could lead to excessive or insufficient stop losses.
4. Sole reliance on technical indicators without fundamental analysis.
5. Effectiveness depends on the correct trading symbol and timeframe.
6. The mechanical system is vulnerable to arbitrage risks.

These issues can be improved through parameter tuning, indicator combinations, and selective manual intervention.

## Optimization Directions

The strategy can be optimized in the following ways:

1. Test different moving average systems like EMA, DMA, etc.
2. Add other technical filters such as MACD or RSI.
3. Optimize ATR parameters for better stop loss/profit levels.
4. Incorporate volume indicators to identify high-quality entry signals.
5. Adjust parameters based on the specific characteristics of each trading symbol.
6. Integrate fundamental factors to avoid contrarian trades.
7. Introduce machine learning techniques like neural networks for data modeling.
8. Explore multi-timeframe combinations to uncover more trading opportunities.
9. Construct a strategy ensemble to enhance robustness.

## Conclusion

In summary, this is a simple and intuitive strategy suitable for beginners to practice live trading. However, there remains significant room for optimization through the use of additional technical indicators or machine learning methods. Adjusting parameters based on specific symbol dynamics and market conditions is also critical. This strategy provides a reference framework for beginner quantitative traders but requires continuous testing and enhancement to achieve stable profits.

|||

## Overview

This strategy utilizes the principle of dual moving average crossover, incorporates ATR indicator for stop loss and take profit, and adds trading hour control to design an intraday trading strategy suitable for futures contracts. The strategy is simple and easy to grasp, making it ideal for beginners.

## Strategy Logic

The strategy uses 5-period and 20-period WMA lines crossing as entry signals. A long position is initiated when the 5-period line breaks above the 20-period line; a short position is initiated when the 5-period line breaks below the 20-period line. Additionally, it uses a 50-period WMA to determine the overall trend direction. Trading signals are only generated when the price breakout direction aligns with the major trend.

Moreover, the strategy leverages ATR indicators to set dynamic stop loss and take profit levels. The ATR indicator reflects market volatility dynamically. The strategy sets stop loss and take profit levels based on multiplying the ATR value by a factor (e.g., 3 times) to control per trade losses.

Finally, trading signals are restricted to US trading hours (9:00-14:30 CST) to avoid high volatility periods around market open and close where false signals may occur easily.

## Advantage Analysis

The strategy has the following advantages:

1. Dual moving average crossover effectively captures trend reversals for timely entry.
2. Trend filtering helps filter out noise signals, avoiding contrarian trading.
3. Dynamic ATR-based stop loss and take profit levels control per trade losses.
4. Limiting trading hours avoids volatile open and close periods.
5. Simple rules that are easy to understand and implement, making it suitable for beginners.
6. Customizable parameters like moving average periods, ATR multipliers, and trading hours can be adjusted.

## Risk Analysis

The strategy also has the following risks:

1. More frequent stop loss triggers in range-bound markets.
2. Dual moving average crossover may have some lag and miss short-term breakouts.
3. Incorrectly set ATR parameters could lead to excessive or insufficient stop losses.
4. Relying solely on technical indicators without fundamental analysis.
5. Effectiveness depends on the correct trading symbol and timeframe.
6. The mechanical system is vulnerable to arbitrage risks.

These can be improved through parameter tuning, indicator combinations, and selective manual intervention.

## Optimization Directions

The strategy can be enhanced in the following aspects:

1. Test different moving average systems like EMA, DMA etc.
2. Add other technical filters like MACD, RSI etc.
3. Optimize ATR parameters for better stop loss/profit levels.
4. Incorporate volume indicators to find high quality entry signals.
5. Adjust parameters based on specific trading symbol characteristics.
6. Integrate fundamental factors to avoid contrarian trades.
7. Introduce machine learning components like neural networks for data modeling.
8. Explore multi-timeframe combinations for more opportunities.
9. Construct a strategy ensemble to improve stability.

## Conclusion

In summary, this is a simple and intuitive strategy suitable for beginners to practice live trading. At the same time, there remains significant room for optimization through additional technical indicators or machine learning methods. Parameter tuning based on specific symbol dynamics and market conditions is also key. The strategy provides a reference framework for beginner quantitative traders but requires continuous testing and enhancement for stable profits.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|10|ATR Period|
|v_input_2_hl2|0|Source: hl2|high|low|open|close|hlc3|hlcc4|ohlc4|
|v_input_3|3|ATR Multiplier|
|v_input_4|true|Change ATR Calculation Method ?|
|v_input_5|true|Show Buy/Sell Signals ?|
|v_input_6_close|0|Fast WMA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_7|5|Fast WMA Period|
|v_input_8_close|0|Slow WMA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_9|20|Slow WMA Period|
|v_input_10_close|0|Trend 50 Period Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_11|50|Trend 50 Period|

> Source (PineScript)

``` pinescript
/*backtest
start: 2023-10-15 00:00:00
end: 2023-11-14 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © james4392010

//@version=4

strategy(title="DayTradingFutures Cross-Strategy", overlay=true)




// === GENERAL INPUTS ===
Periods = input(title="ATR Period", type=input.integer, defval=10)
src = input(hl2, title="Source")
Multiplier = i