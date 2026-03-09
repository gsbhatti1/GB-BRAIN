> Name

RSI with Fibonacci Retracement Trading Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/3d0a9a45e020b9ce0b.png)
[trans]

## Overview

This article mainly describes a trading strategy that combines the Relative Strength Index (RSI) and Fibonacci retracement levels. The strategy first calculates key Fibonacci retracement levels based on historical price dynamics over a certain period, then uses the RSI indicator to determine whether the market is overbought or oversold near these retracement levels to generate trade signals.

## Strategy Principle

The main principles behind this strategy are:

1. Use price data over a certain period (e.g., 200 bars) to calculate the median price, standard deviation, and key Fibonacci retracement levels (e.g., 0.764);
2. When prices approach upper or lower retracement levels, use the RSI indicator to determine if there is an overbought or oversold condition in that area;
3. If the RSI shows overbought or oversold signals, generate long or short trade signals around these levels;
4. Set stop loss and take profit levels to close positions when prices exceed preset levels or stop loss conditions are triggered.

This outlines the basic workflow for identifying trading opportunities using this strategy.

## Advantage Analysis

Compared to using RSI or Fibonacci alone, combining both indicators offers several advantages:

1. Double indicator filtering can reduce false signals and improve signal quality;
2. Trading near Fibonacci retracement levels is a classic technical analysis technique;  
3. Setting stop loss and take profit limits helps control the maximum potential loss per trade;
4. Parameters can be optimized for different periods or markets.

## Risk Analysis

The strategy also has some risks to consider:

1. Reversals at key levels are not guaranteed, so combine with price action patterns;
2. Single-period RSI may generate false signals from dead cat bounces; consider validation across multiple timeframes;
3. A loose stop loss setting can increase the risk of losses;
4. Wide price swings during volatile periods could trigger stops prematurely.

These risks can be managed through parameter tuning and optimizing indicator combinations.

## Optimization Directions

Further optimizations for this strategy include:

1. Adding volume indicators to avoid false breakouts with low trading volumes;  
2. Considering Bollinger Bands for signals from breakout events;
3. Building machine learning or neural network models to automatically detect high-quality trading opportunities;
4. Using genetic algorithms for automated parameter tuning and adjusting stop loss/profit levels.

## Summary

This article details a quantitative trading strategy that combines RSI and Fibonacci retracement analysis. By integrating dual indicator analysis with classic technical strategies, the approach enhances trade signal quality while managing risks. Further performance improvements can be achieved through ongoing parameter adjustments and model optimizations.

||

## Overview

This article mainly describes a trading strategy that combines the Relative Strength Index (RSI) and Fibonacci retracement levels. The strategy first calculates key Fibonacci retracement levels based on historical price dynamics over a certain period, then uses the RSI indicator to determine whether the market is overbought or oversold near these retracement levels to generate trade signals.

## Strategy Principle

The main principles behind this strategy are:

1. Use price data over a certain period (e.g., 200 bars) to calculate the median price, standard deviation, and key Fibonacci retracement levels (e.g., 0.764);
2. When prices approach upper or lower retracement levels, use the RSI indicator to determine if there is an overbought or oversold condition in that area;
3. If the RSI shows overbought or oversold signals, generate long or short trade signals around these levels;
4. Set stop loss and take profit levels to close positions when prices exceed preset levels or stop loss conditions are triggered.

This outlines the basic workflow for identifying trading opportunities using this strategy.

## Advantage Analysis

Compared to using RSI or Fibonacci alone, combining both indicators offers several advantages:

1. Double indicator filtering can reduce false signals and improve signal quality;
2. Trading near Fibonacci retracement levels is a classic technical analysis technique;  
3. Setting stop loss and take profit limits helps control the maximum potential loss per trade;
4. Parameters can be optimized for different periods or markets.

## Risk Analysis

The strategy also has some risks to consider:

1. Reversals at key levels are not guaranteed, so combine with price action patterns;
2. Single-period RSI may generate false signals from dead cat bounces; consider validation across multiple timeframes;
3. A loose stop loss setting can increase the risk of losses;
4. Wide price swings during volatile periods could trigger stops prematurely.

These risks can be managed through parameter tuning and optimizing indicator combinations.

## Optimization Directions

Further optimizations for this strategy include:

1. Adding volume indicators to avoid false breakouts with low trading volumes;  
2. Considering Bollinger Bands for signals from breakout events;
3. Building machine learning or neural network models to automatically detect high-quality trading opportunities;
4. Using genetic algorithms for automated parameter tuning and adjusting stop loss/profit levels.

## Summary

This article details a quantitative trading strategy that combines RSI and Fibonacci retracement analysis. By integrating dual indicator analysis with classic technical strategies, the approach enhances trade signal quality while managing risks. Further performance improvements can be achieved through ongoing parameter adjustments and model optimizations.

|Argument|Default|Description|
|----|----|----|
|v_input_1|1.5|SL in % of Instrum. i.e 1.5%=150pips|
|v_input_2|14|[RSI] Length|
|v_input_3|30|[RSI] Over Sold %|
|v_input_4|70|[RSI] Over Bought %|
|v_input_5|200|[Fibonacci] Length|
|v_input_6_hlc3|0|[Fibonacci] Source: hlc3|high|low|open|hl2|close|hlcc4|ohlc4|
|v_input_7|3|[Fibonacci] Multiplier|
|v_input_8|764|[Fibonacci] Level|

``` pinescript
/*backtest
start: 2023-11-26 00:00:00
end: 2023-12-26 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy(title="Gab Fib  + RSI", overlay=true, default_qty_type=strategy.cash, default_qty_value=100000, initial_capital=1000, currency=currency.USD, commission_type=strategy.commission.cash_per_order, commission_value=4)

// Inputs
timeFilter = year >= 2000

    // Stop Loss 
stop_loss = input(title="SL in % of Instrum. i.e 1.5%=150pips", minval=0, step=0.1, defval=1.5) /100
    // RSI Inputs
len = input(title="[RSI] Length", minval=0, step=1, defval=14)
overSold = input(title="[RSI] Over Sold %", defval=30)
overBought = input(title="[RSI] Over Bought %", defval=70)
    // Fibonacci Levels
length = input(title="[Fibonacci] Length", defval=200, minval=1)
src = input(hlc3, title="[Fibonacci] Source")
mult = input(title="[Fibonacci] Multiplier", defval=3.0, minval=0.001, maxval=50)
level = input(title="[Fibonacci] Level", defval=764)


// Calculate Fibonacci
basis = vwma(src, length)
dev = mult * stdev(src, length)
fu764= basis + (0.001*level*dev)
fu1= basis + (1*dev)
fd764= basis - (0.001*level*dev)
fd1= basis - (1*dev)

// Calculate RSI
vrsi = rsi(close, len)

// Calculate the Targets
targetUp = fd764
targetDown = fu764
    // Actual Targets
bought = strategy.position_size[0] > strategy.position_size[1]
exit_long = valuewhen(bought, target