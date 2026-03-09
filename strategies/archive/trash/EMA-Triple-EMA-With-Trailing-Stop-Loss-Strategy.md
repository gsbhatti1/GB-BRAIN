> Name

Triple-EMA-With-Trailing-Stop-Loss-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/10b6cf7f56f7e01b277.png)

[trans]

## Overview

This strategy implements a typical triple exponential moving average (EMA) trading system. It generates trading signals by comparing fast 5-day EMA, medium 20-day EMA and slow 50-day EMA. It also uses the current bar's close price compared to the previous bar's close to filter false signals. Additionally, it employs a trailing stop loss mechanism to lock in profits.

## Principles

When the 5-day EMA crosses above the 20-day EMA, and all three EMAs are bullish (5-day EMA > 20-day EMA > 50-day EMA), and the current bar's close is higher than the previous bar's close by a certain number of ticks, go long. When the 5-day EMA crosses below the 20-day EMA, and all three EMAs are bearish (5-day EMA < 20-day EMA < 50-day EMA), and the current bar's close is lower than the previous bar's close by a certain number of ticks, go short.

After entering a trade, if price runs beyond a certain number of ticks, a trailing stop loss will be activated to continuously adjust the stop loss based on price fluctuations, thereby locking in larger profits.

## Advantages

1. Using triple EMAs to generate signals can effectively filter market noise and identify trends. The fast EMA reflects recent changes, the medium EMA determines trend direction, and the slow EMA filters out oscillations.
   
2. Comparing the current bar's close with the previous bar's close further filters false signals and reduces unnecessary trades.

3. Implementing a trailing stop loss mechanism dynamically adjusts the stop loss based on price movements to maximize profit locking.

4. The strategy parameters can be flexibly adjusted, allowing optimization across different products and timeframes from daily bars to minute bars.

## Risks

1. Frequent EMA crossovers in ranging markets can generate excessive trades, increasing costs due to commissions and slippage.

2. Trailing stop loss may prematurely exit the trend during significant price swings.

3. The lag of EMAs might cause missing major turning points and resulting losses.

4. Parameters like EMA periods and trailing stop ticks require optimization for different products and timeframes.

## Optimization Directions

1. Incorporate other indicators such as MACD, KD to further filter trading signals.

2. Test and optimize parameters for specific products and timeframes to find the best combinations.

3. Dynamically adjust parameters through human oversight or machine learning techniques.

4. Consider disabling trailing stop loss in certain market conditions and holding a full position.

5. Replace simple trailing stop loss with more advanced automatic profit-taking mechanisms.

## Conclusion

This strategy integrates three common technical analysis tools—EMA crossover, price breakout, and trailing stop loss—into a comprehensive and robust trend-following trading system. Through parameter optimization, it can adapt to different products and timeframes and perform well in strong trending markets. However, like most technical analysis strategies, it has some typical weaknesses that need further refinement to handle various market scenarios. Overall, this strategy provides a simple and practical idea for quantitative trading by effectively demonstrating common strategy concepts.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|false|═════ Data Filtering ═════|
|v_input_2|2021|Year|
|v_input_3|false|Month (0=ALL)|
|v_input_4|100|Stop Loss (ticks)|
|v_input_5|130|Trailing S/L (ticks)|
|v_input_6|15|Buffer (ticks)|
|v_input_7|5|EMA 1|
|v_input_8|20|EMA 2|
|v_input_9|50|EMA 3|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-10-01 00:00:00
end: 2023-10-02 12:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Matt Dearden - IndoPilot
// @version=4

/////////////////////////////////////////////////////// Initial Parameters /////////////////////////////////////////////////////// 
SystemName = "Triple EMA Strategy"
ShortSystemName = "TEMA"
InitPosition = 0
InitCapital = 50000
InitCommission = 0.004 //approx value to compensate for Oanda spreads
InitPyramidMax = 0
CalcOnorderFills = true

strategy(title=SystemName, shorttitle=ShortSystemName, overlay=true, pyramiding=InitPyramidMax, 
 default_qty_type=strategy.cash, default_qty_value=InitPosition, commission_type=strategy.commission.percent, 
 commission_value=InitCommission, initial_capital=InitCapital, max_lines_count=500, 
 max_labels_count=500, process_orders_on_close=false, calc_on_every_tick=false) 

///////////////////////////////////////////////////////////// Inputs /////////////////////////////////////////////////////////////

DateFilter = input(false, "═════ Data Filtering ═════") 
InitYear = input(2021, "Year")
InitMonth = input(false, "Month (0=ALL)")
StopLossTicks = input(100, "Stop Loss (ticks)")
TrailingSLTicks = input(130, "Trailing S/L (ticks)")
BufferTicks = input(15, "Buffer (ticks)")
EMA1Period = input(5, "EMA 1")
EMA2Period = input(20, "EMA 2")
EMA3Period = input(50, "EMA 3")

// EMA Calculations
ema1 = ta.ema(close, EMA1Period)
ema2 = ta.ema(close, EMA2Period)
ema3 = ta.ema(close, EMA3Period)

// Conditions for entering long position
longCondition = ta.crossover(ema1, ema2) and (ta.cmparray(close[0], close[-1]) > StopLossTicks * BufferTicks)

// Conditions for entering short position
shortCondition = ta.crossunder(ema1, ema2) and (ta.cmparray(close[0], close[-1]) < -StopLossTicks * BufferTicks)

// Trailing stop loss logic
trailStop = strategy.position_size > 0 ? math.max(strategy.position_avg_price, ema3) : na

strategy.entry("Long", strategy.long, when=longCondition)
strategy.close("Long", when=ta.crossover(close, trailStop))

strategy.entry("Short", strategy.short, when=shortCondition)
strategy.close("Short", when=ta.crossunder(close, trailStop))
```