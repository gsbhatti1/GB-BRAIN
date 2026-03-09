> Name

Double Bottom Reversal Mean Reversion DCA Grid Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1435b49f70c6d07d1c0.png)
[trans]
## Overview

The Double Bottom Reversal Mean Reversion DCA Grid strategy primarily applies mean reversion price and DCA strategies to gradually establish positions. It identifies reversal opportunities based on the double bottom reversal pattern. Once a reversal is triggered, multiple limit orders at different prices are placed, combining DCA to build grid positions step by step.

## Strategy Logic

The strategy first checks if there are two consecutive closing prices equal to the bottom on the candlestick chart, which is called a "double bottom." If a double bottom is detected, it considers there may be a price reversal opportunity. At this point, the strategy will set multiple limit orders around the bottom price. The prices of these orders will be calculated based on ATR and volatility, forming a grid zone. This achieves the DCA effect and allows traders to gradually build positions at different prices after the reversal.

Specifically, the ATR indicator over the recent 14 candlesticks is first obtained through `ta.atr`. Then the price volatility over the recent 5 candlesticks is calculated. They are the main parameters used to determine the grid zone. The grid contains four price levels: bottom price + volatility, bottom price + 0.75 * volatility, and so on. Once the double bottom condition triggers, four limit orders with equal size will be placed according to this formula. Unfilled orders will be cancelled after a certain number of candlesticks.

In addition, the strategy also sets a stop loss price and a take profit price. The stop loss price is set to the lowest price of the double bottom minus one tick size, while the take profit price is set to the entry price plus 5 times the ATR. These two prices will update in real-time when the position size is greater than 0.

## Advantages

The main advantages of this strategy are:

1. Using a double bottom to determine reversal improves accuracy and avoids false breaks.
2. The DCA grid allows traders to gradually build positions at different prices, lowering cost basis.
3. Dynamic ATR and volatility parameters adjust the grid and profit range based on market changes.
4. Auto stop loss effectively controls per trade loss amount.

## Risk Analysis

Major risks include:

1. Price may break through support without reversal, triggering a stop loss and causing losses. Widen stop loss distance for protection.
2. Improper DCA grid setting may lead to low fill rate. Test different parameters to ensure high fill rate.
3. Frequent take profit in volatile markets. Consider allowing wider take profit multiples.

## Optimization Directions

This strategy can be further optimized from the following directions:

1. Add trend judgment, only trade reversals along the major trend to avoid missing big trends.
2. Consider larger size for the first entry and smaller sizes for grid entries to optimize capital usage efficiency.
3. Test different parameter combinations to find the best parameters. Or design dynamic adjusting logic based on market conditions.
4. Integrate machine learning in an advanced platform to achieve automatic parameter optimization.

## Summary

The Double Bottom Reversal Mean Reversion DCA Grid Strategy integrates price patterns, moving averages, and grid trading techniques. It has accurate timing, controllable cost basis, and built-in drawdown protection mechanisms. There is still room for improvement and it is worth further research and application. Properly configured, the strategy can achieve good results in range-bound markets.

||

## Overview

The Double Bottom Reversal Mean Reversion DCA Grid strategy mainly applies mean reversion price and DCA strategies to gradually establish positions. It identifies reversal opportunities based on the double bottom reversal pattern. Once a reversal is triggered, multiple limit orders at different prices are placed, combining DCA to build grid positions step by step.

## Strategy Logic

The strategy first checks if there are two consecutive closing prices equal to the bottom on the candlestick chart, which is called a "double bottom." If a double bottom is detected, it considers there may be a price reversal opportunity. At this point, the strategy will set multiple limit orders around the bottom price. The prices of these orders will be calculated based on ATR and volatility, forming a grid zone. This achieves the DCA effect and allows traders to gradually build positions at different prices after the reversal.

Specifically, the ATR indicator over the recent 14 candlesticks is first obtained through `ta.atr`. Then the price volatility over the recent 5 candlesticks is calculated. They are the main parameters used to determine the grid zone. The grid contains four price levels: bottom price + volatility, bottom price + 0.75 * volatility, and so on. Once the double bottom condition triggers, four limit orders with equal size will be placed according to this formula. Unfilled orders will be cancelled after a certain number of candlesticks.

In addition, the strategy also sets a stop loss price and a take profit price. The stop loss price is set to the lowest price of the double bottom minus one tick size, while the take profit price is set to the entry price plus 5 times the ATR. These two prices will update in real-time when the position size is greater than 0.

## Advantages

The main advantages of this strategy are:

1. Using a double bottom to determine reversal improves accuracy and avoids false breaks.
2. The DCA grid allows traders to gradually build positions at different prices, lowering cost basis.
3. Dynamic ATR and volatility parameters adjust the grid and profit range based on market changes.
4. Auto stop loss effectively controls per trade loss amount.

## Risk Analysis

Major risks include:

1. Price may break through support without reversal, triggering a stop loss and causing losses. Widen stop loss distance for protection.
2. Improper DCA grid setting may lead to low fill rate. Test different parameters to ensure high fill rate.
3. Frequent take profit in volatile markets. Consider allowing wider take profit multiples.

## Optimization Directions

This strategy can be further optimized from the following directions:

1. Add trend judgment, only trade reversals along the major trend to avoid missing big trends.
2. Consider larger size for the first entry and smaller sizes for grid entries to optimize capital usage efficiency.
3. Test different parameter combinations to find the best parameters. Or design dynamic adjusting logic based on market conditions.
4. Integrate machine learning in an advanced platform to achieve automatic parameter optimization.

## Summary

The Double Bottom Reversal Mean Reversion DCA Grid Strategy integrates price patterns, moving averages, and grid trading techniques. It has accurate timing, controllable cost basis, and built-in drawdown protection mechanisms. There is still room for improvement and it is worth further research and application. Properly configured, the strategy can achieve good results in range-bound markets.

||

## Strategy Arguments

|Argument         |Default  |Description|
|-----------------|---------|-----------|
|v_input_int_1    |14       |(?Strategy Settings) ATR length for taking profit |
|v_input_int_2    |5        |ATR multiplier|
|v_input_int_3    |5        |Volatility length|
|v_input_float_1  |0.5      |Volatility multiplier|
|v_input_int_4    |4        |How many candles to wait after placing orders grid?|

## Source (PineScript)

```pinescript
/*backtest
start: 2024-02-12 00:00:00
end: 2024-02-19 00:00:00
period: 3m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © cherepanovvsb

//@version=5
strategy("Reversal (only long)", overlay=true, margin_long=1, margin_short=1,initial_capital=1000,commission_type = strategy.commission.percent,commission_value =0.1,currency='USD', process_orders_on_close=true)
plotshape(low == low[1], style=shape.triangleup, location=location.belowbar, color=color.blue, title="1 Setup")
plotshape(low == low[low[2]], style=shape.triangleup, location=location.belowbar, color=color.red, title="Triple Setup")

ATRlenght   = input.int(title="ATR length for taking profit", defval=14, group="Strategy Settings")
atr         = ta.atr(ATRlenght)
volatility  = input.float(title="Volatility length", defval=5, group="Strategy Settings")
v          = ta.stdev(close, volatility)

// Determine double bottom
doubleBottom = low == low[1] and low[1] == low[2]

// Place limit orders based on ATR and volatility
if (doubleBottom)
    for i = 0 to v_input_int_4 - 1
        priceLevel = close + i * v
        strategy.order("Grid Order " + i, strategy.long, comment="Buy at " + str.tostring(priceLevel), when=close < priceLevel)

// Set stop loss and take profit levels
stopLoss   = doubleBottom ? low[2] - 1 : na
takeProfit = close * (1 + v_input_int_2 / 100 * atr)

strategy.exit("Take Profit", from_entry="Grid Order " + i, limit=takeProfit)
strategy.exit("Stop Loss", from_entry="Grid Order " + i, stop=stopLoss)
```
[/trans]