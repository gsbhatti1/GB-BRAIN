> Name

Swing Points Breakouts-Long-term-strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/177c877e47160fc0587.png)
[trans]
### Overview

The Swing Points Breakouts strategy is a long-term trend fluctuation strategy based on identifying swing highs and lows. The strategy enters long positions when the price breaks above the highest price in the most recent specified period, and enters short positions when the price breaks below the lowest price in the most recent specified period.

### Strategy Logic

The strategy identifies the highest and lowest prices in the most recent N bars based on input parameters. It determines the entry and exit based on the direction parameter. When going long, it enters long positions with an OCO stop order when the price breaks above the swing high. When going short, it enters short positions with an OCO stop order when the price breaks below the swing low.

In addition, the strategy sets stop losses. After opening long positions, the stop loss is set near the recent lowest price. After opening short positions, the stop loss is set near the most recent highest price. This effectively avoids huge losses in a trending market.

### Advantage Analysis

The biggest advantage of this strategy is that it captures key fluctuations around swing highs and lows and profits accordingly. Setting stop losses also effectively controls risks.

Specifically the advantages are:

1. The strategy logic is clear, with entries and exits based on swing high/low breakouts.
2. It utilizes swing highs/lows to identify reversal opportunities, a classic technical analysis approach.
3. There are stop losses set to control risks and avoid huge losses in trending markets.
4. The code has clear structure and is easy to understand and modify.
5. Parameters can be adjusted to optimize the strategy, like tuning the swing high/low period.

### Risk Analysis

The main risk of this strategy comes from inaccurate swing high/low identification leading to wrong trades. The specific risks include:

1. False breakout of swing highs/lows resulting in wrong entries.
2. Huge stop loss hit near the breakout points.
3. Trending symbols tend to need huge costs determining swing points.
4. Improper parameter tuning also affects strategy performance.

The solutions include:

1. Optimizing parameters like swing high/low period.
2. Increasing stop loss distance.
3. Avoiding using it on trending symbols.
4. Adopting machine learning to dynamically optimize parameters.

### Optimization Directions

The strategy can be optimized in the following directions:

1. Dynamic optimization of swing high/low periods instead of fixed values to avoid overfitting.
2. Introducing dynamic stop loss/take profit based on ATR and volatility.
3. Combining multiple time frames, using higher TFs to define trend and lower TFs for entry.
4. Incorporating machine learning models to predict potential swing points and improve performance.
5. Optimizing the stop loss algorithms to avoid unnecessary hits while keeping effective stop loss.

### Conclusion

The Swing Points Breakouts strategy is a practical long-term quantitative strategy overall. By capturing reversal opportunities around swing points and setting stop losses to control risks, it ensures profits while also controlling drawdowns. With flexible parameter tuning and clear logic, it is a recommended strategy paradigm worth utilizing. Further improvements can be made by introducing dynamic optimization and machine learning.

||

### Overview

The Swing Points Breakouts strategy is a long-term trend fluctuation strategy based on identifying swing highs and lows. The strategy enters long positions when the price breaks above the highest price in the most recent specified period, and enters short positions when the price breaks below the lowest price in the most recent specified period.

### Strategy Logic

The strategy defines the most recent N bar's highest price and lowest price as the swing high and swing low through input parameters. It determines the entry and exit based on the direction parameter. When going long, it enters long positions with an OCO stop order when the price breaks above the swing high. When going short, it enters short positions with an OCO stop order when the price breaks below the swing low.

In addition, the strategy sets up stop losses. After opening long positions, the stop loss is set near the recent lowest price. After opening short positions, the stop loss is set near the most recent highest price. This effectively avoids huge losses in a trending market.

### Advantage Analysis

The biggest advantage of this strategy is that it captures key fluctuations around swing highs and lows and profits accordingly. Setting stop losses also effectively controls risks.

Specifically the advantages are:

1. The strategy logic is clear, with entries and exits based on swing high/low breakouts.
2. It utilizes swing highs/lows to identify reversal opportunities, a classic technical analysis approach.
3. There are stop losses set to control risks and avoid huge losses in trending markets.
4. The code has clear structure and is easy to understand and modify.
5. Parameters can be adjusted to optimize the strategy, like tuning the swing high/low period.

### Risk Analysis

The main risk of this strategy comes from inaccurate swing high/low identification leading to wrong trades. The specific risks include:

1. False breakout of swing highs/lows resulting in wrong entries.
2. Huge stop loss hit near the breakout points.
3. Trending symbols tend to need huge costs determining swing points.
4. Improper parameter tuning also affects strategy performance.

The solutions include:

1. Optimizing parameters like swing high/low period.
2. Increasing stop loss distance.
3. Avoiding using it on trending symbols.
4. Adopting machine learning to dynamically optimize parameters.

### Optimization Directions

The strategy can be optimized in the following directions:

1. Dynamic optimization of swing high/low periods instead of fixed values to avoid overfitting.
2. Introducing dynamic stop loss/take profit based on ATR and volatility.
3. Combining multiple time frames, using higher TFs to define trend and lower TFs for entry.
4. Incorporating machine learning models to predict potential swing points and improve performance.
5. Optimizing the stop loss algorithms to avoid unnecessary hits while keeping effective stop loss.

### Conclusion

The Swing Points Breakouts strategy is a practical long-term quantitative strategy overall. By capturing reversal opportunities around swing points and setting stop losses to control risks, it ensures profits while also controlling drawdowns. With flexible parameter tuning and clear logic, it is a recommended strategy paradigm worth utilizing. Further improvements can be made by introducing dynamic optimization and machine learning.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|false|Strategy Direction|
|v_input_2|true|Use Swing Lo/Hi Stop Loss & Take Profit|
|v_input_3|10|Swing Low Lookback|
|v_input_4|10|Swing High Lookback|
|v_input_5|false|Reverse Trades|
|v_input_6|false|SL Expander|


> Source (PineScript)

```pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-31 23:59:59
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © tweakerID

// Long term strategy for managing a Crypto investment with Swing Trades of more than 1 day. The strategy buys with a 
// stop order at the Swing High price (green line) and sells with a stop order at the Swing Low price (red line). 
// The direction of the strategy can be adjusted in the Inputs panel.

//@version=4
strategy("Swing Points Breakouts", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=100, initial_capital=10000, commission_value=0.04)

direction = input(0, title = "Strategy Direction", type=input.integer, minval=