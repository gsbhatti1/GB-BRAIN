> Name

Zero-Lag-EMA-Trend-Following-Strategy

> Author

ChaoZhang

> Strategy Description

## Overview

This is a typical trend-following strategy. It uses fast and slow Zero-Lag EMA to determine the trend direction, and incorporates mechanisms like trailing stop, take profit, and pyramiding to follow trends.

## Strategy Logic  

1. Calculate fast and slow Zero-Lag EMA using different smooth periods.
2. Generate long signal when fast EMA crosses above slow EMA; generate short signal when fast EMA crosses below slow EMA.
3. Set trailing stop line after entry to track the highest/lowest price for risk control.
4. Take profit when price reaches a certain percentage for profit-taking.
5. Use open counts for pyramiding similar to compound interest.

## Advantage Analysis

1. Zero-Lag EMA has less lag in responding to trend changes.
2. Dual EMA strategy is simple and intuitive for directional judgment.
3. Stop loss and take profit settings effectively control single trade loss.
4. Pyramiding mechanism allows more profits when the trend extends.

## Risk Analysis 

1. Improper parameter settings may cause overly aggressive or conservative stop loss/take profit.
2. Wrong trend indicators may miss trend change opportunities.
3. Pyramiding can amplify total loss if the trend reverses.
4. Parameters need tuning for different products to avoid overfitting.

## Improvement Directions 

1. Test different EMA periods to find better parameter combinations.
2. Optimize stop/take ratios to balance profitability and risk control.
3. Adjust pyramiding logic to limit maximum open count per direction.
4. Add other technical indicators for entry filtering to improve signal quality.
5. Disable trading during specific hours to avoid times prone to incorrect signals.
6. Test parameters separately on different products to improve robustness.

## Summary

The strategy shows overall stable performance with decent risk-adjusted returns. It can be further enhanced through parameter optimization and auxiliary filtration methods. However, one should also be wary of potential signal errors in certain market conditions. Overall, this strategy framework is sound and has the potential to become a consistently profitable trend-following strategy after continuous refinement.

||

## Overview

This is a typical trend following strategy. It uses fast and slow Zero-Lag EMA to determine the trend direction and incorporates mechanisms like trailing stop, take profit, and pyramiding to follow trends.

## Strategy Logic  

1. Calculate fast and slow Zero-Lag EMA using different smooth periods.
2. Long signal generated when fast EMA crosses above slow EMA; short signal generated when fast EMA crosses below slow EMA.
3. Set trailing stop line after entry to track highest/lowest price for risk control.
4. Take profit when price reaches certain percentage for profit-taking.
5. Use open counts for pyramiding similar to compound interest.

## Advantage Analysis

1. Zero-Lag EMA has less lag in responding to trend changes.
2. Dual EMA strategy is simple and intuitive for directional judgment.
3. Stop loss and take profit settings effectively control single trade loss.
4. Pyramiding mechanism allows more profits when the trend extends.

## Risk Analysis 

1. Improper parameter settings may cause overly aggressive or conservative stop loss/take profit.
2. Wrong trend indicators may miss trend change opportunities.
3. Pyramiding can amplify total loss if the trend reverses.
4. Parameters need tuning for different products to avoid overfitting.

## Improvement Directions 

1. Test different EMA periods to find better parameter combinations.
2. Optimize stop/take ratios to balance profitability and risk control.
3. Adjust pyramiding logic to limit maximum open count per direction.
4. Add other technical indicators for entry filtering to improve signal quality.
5. Disable trading during specific hours to avoid times prone to incorrect signals.
6. Test parameters separately on different products to improve robustness.

## Summary

The strategy shows overall stable performance with decent risk-adjusted returns. It can be further enhanced through parameter optimization and auxiliary filtration methods. However, one should also be wary of potential signal errors in certain market conditions. Overall, this strategy framework is sound and has the potential to become a consistently profitable trend-following strategy after continuous refinement.

---

## Strategy Arguments

|Argument|Default|Description|
|---|---|---|
|v_input_1|2018|Backtest Start Year|
|v_input_2|3|Backtest Start Month|
|v_input_3|true|Backtest Start Day|
|v_input_4|77777777|Backtest Stop Year|
|v_input_5|11|Backtest Stop Month|
|v_input_6|15|Backtest Stop Day|
|v_input_7_close|0|ZeroLag EMA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_8|8|ZeroLag EMA Fast Length|
|v_input_9|21|ZeroLag EMA Slow Length|
|v_input_10|false|Longs Only|
|v_input_11|false|Shorts Only|
|v_input_12|false|Flip the Opens|
|v_input_13|true|Pyramiding less than|
|v_input_14|false|Pyramiding equal to|
|v_input_15|1000000|Pyramiding greater than|
|v_input_16|false|Trailing Stop|
|v_input_17|1300|Activate Trailing Stop Price (%). Divided by 100 (1 = 0.01%)|
|v_input_18|400|Trailing Stop (%). Divided by 100 (1 = 0.01%)|
|v_input_19|true|Take Profit|
|v_input_20|300|Take Profit (%). Divided by 100 (1 = 0.01%)|
|v_input_21|false|Stop Loss|
|v_input_22|750|Stop Loss (%). Divided by 100 (1 = 0.01%)|
|v_input_23|34|Lookback Period|
|v_input_24|30|Resolution|
|v_input_25|7|Number of Fibonacci Volatility Deviations|

---

## Source (PineScript)

```pinescript
//@version=3
// Learn more about Autoview and how you can automate strategies like this one here: https://autoview.with.pink/
strategy("MP ZeroLag EMA", "MP 0 Strat", overlay=true, pyramiding=0, initial_capital=100000, currency=currency.USD, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, commission_type=strategy.commission.percent, commission_value=0.1)
 
//bgcolor ( color=black, transp=40, title='Blackground', editable=true)
 
///////////////////////////////////////////////
//* Backtesting Period Selector | Component *//
///////////////////////////////////////////////
 
testStartYear = input(2018, "Backtest Start Year")
testStartMonth = input(3, "Backtest Start Month")
testStartDay = input(1, "Backtest Start Day")
testPeriodStart = timestamp(testStartYear,testStartMonth,testStartDay,00,00)
 
testStopYear = input(77777777, "Backtest Stop Year")
testStopMonth = input(11, "Backtest Stop Month")
testStopDay = input(15, "Backtest Stop Day")
testPeriodStop = timestamp(testStopYear,testStopMonth,testStopDay,0,0)
 
testPeriod() => true
 
/////////////////////////////////////
//* Put your strategy logic below *//
/////////////////////////////////////
 
// === INPUTS ===
zlmaSource      = input(defval = close, title = "ZeroLag EMA Source")
zlmaFastLength  = input(defval = 8, title = "ZeroLag EMA Fast Length")
zlmaSlowLength  = input(defval = 21, title = "ZeroLag EMA Slow Length")

// === /INPUTS ===
 
// === SERIES SETUP ===
// Fast ZeroLag EMA
zema1=ema(zlmaSource, zlmaFastLength)
zema2=ema(zema1, zlmaFastLength)
c1=zema1-zema2
zlemaFast=zema1+c1
 
// Slow ZeroLag EMA
zema3=ema(zlmaSource, zlmaSlowLength)
zema4=ema(zema3