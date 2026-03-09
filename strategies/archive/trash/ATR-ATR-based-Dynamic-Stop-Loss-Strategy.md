> Name

ATR-based Dynamic Stop Loss Strategy

> Author

ChaoZhang

> Strategy Description

## Overview

This strategy uses the ATR indicator to set dynamic stop loss points and adjust stop loss positions based on price fluctuations, in order to control risks. It primarily enters long positions when 5 EMA crosses above 20 EMA, then sets stop loss and take profit levels using the ATR indicator. The stop loss position will be adjusted according to price movements to lock in more profits.

## Strategy Logic

The strategy first determines if a golden cross occurs between 5 EMA and 20 EMA to enter long positions. After entering, it calculates the ATR multiples of the entry price relative to the current price using the ATR indicator, setting the stop loss position at 1.5ATR below the entry price. As prices rise, the stop loss is gradually moved higher until a take profit level is reached if the price increases by more than 3ATR.

Specifically, the strategy defines the following variables:

- `entry_price`: Entry price
- `stop_price`: Stop loss price 
- `take_profit_price`: Take profit price
- `atr_down`: Lower ATR line
- `atr_up`: Upper ATR line
- `atr_current`: Current ATR line
- `atr_ref`: ATR value

Upon entering, it calculates `atr_ref` as the current ATR value and `atr_div` as the ATR multiples of the entry price to the current price. Then, based on `atr_div`, it sets the positions for `atr_down`, `atr_current`, and `atr_up`. The stop loss is set at 1.5ATR below the entry price.

As prices rise, by comparing the current price `avg` with `atr_up`, if `avg` crosses above `atr_up`, the strategy recalculates `atr_div` and ATR line positions to gradually raise the stop loss to increase profits.

If the price rises above 3ATR from the entry price, partial take profit is initiated to lock in profits. The `tookProfit` flag is set to true. If prices continue to rise, the stop loss position continues to be raised. When a stop loss is triggered, it checks `tookProfit`. If partial take profit was executed earlier, only the remaining position will be closed; otherwise, all positions are closed.

## Advantages

1. Using ATR indicator dynamically adjusts stop losses based on market volatility.
2. Cuts losses while allowing profits to run as prices rise.
3. Partial take profit mechanism locks in some profit and reduces risk, with continued stop loss movement to allow profits to run.

## Risks

1. ATR is not sensitive to sharp reversals or gaps.
2. EMAs cannot determine trend reversals, which may lead to entering new positions during a reversal.
3. There is a higher chance of losses after partial take profit.
4. Parameters such as 1.5ATR stop and 3ATR take profit need optimization for different products.

## Improvements

1. Consider adding other stop loss indicators like Donchian Channel to compensate for ATR lag.
2. Test different moving average configurations or include MACD to identify trend reversals.
3. Optimize partial take profit ratios and frequencies for various products.
4. Perform parameter optimization on ATR multiples for stop and take profit levels, including trailing stops.
5. Test performance during weak trends and consider disabling the strategy in such conditions.

## Summary

The overall logic of this strategy is clear and straightforward, with the use of ATR to manage stop losses being its primary strength. However, ATR has limitations like lagging signals. Adding additional stop loss and trend indicators would enhance it. Additionally, optimizing partial take profit mechanisms for different products is necessary. Overall, the strategy provides a framework for using ATR-based stop loss management but requires further refinement.

---

## Source (Pine Script)

```pinescript
//@version=5
strategy("[EKIN] ATR Exit Strategy", overlay=true, initial_capital = 1000, default_qty_value = 100, default_qty_type = strategy.percent_of_equity, calc_on_every_tick = true)

// Simple EMA tracking
fastEMA = ta.ema(close, 5)
slowEMA = ta.ema (close, 20)
atr = ta.atr(14)

// We define entry price for future reference
var float entry_price = na
// We define stop and take profit for future calculations
var float stop_price = na
var float take_profit_price = na

// We define atr limits here
var float atr_down = na
var float atr_up = na
var float atr_current = na
var float atr_ref = na

avg = (low + high) / 2

// Conditions
enterCondition = ta.crossover(fastEMA, slowEMA)
```