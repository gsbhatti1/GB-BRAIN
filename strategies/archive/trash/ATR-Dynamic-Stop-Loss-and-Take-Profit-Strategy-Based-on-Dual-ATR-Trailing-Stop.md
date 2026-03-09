``` pinescript
/*backtest
start: 2024-02-01 00:00:00
end: 2024-02-29
*/

//@version=5
strategy("Dynamic-Stop-Loss-and-Take-Profit-Strategy-Based-on-Dual-ATR-Trailing-Stop", overlay=true)

// Input Parameters
atrPeriod1 = input(10, title="ATR Period 1")
atrPeriod2 = input(20, title="ATR Period 2")
sensitivity1 = input(1.0, title="Key Value 1", type=input.float)
sensitivity2 = input(2.0, title="Key Value 2", type=input.float)
useHeikinAshi = input(false, title="Signals from Heikin Ashi Candles")
fromDay = input(false, title="From Day")
fromMonth = input(false, title="From Month")
fromYear = input(2024, title="From Year")
toDay = input(false, title="To Day")
toMonth = input(false, title="To Month")
toYear = input(2024, title="To Year")

// Calculate ATRs
atr1 = ta.atr(atrPeriod1)
atr2 = ta.atr(atrPeriod2)

// Calculate Stop Loss Levels
stopLossLevel1 = close - sensitivity1 * atr1
stopLossLevel2 = close - sensitivity2 * atr2

// Calculate Take Profit Level
takeProfitLevel = close + 1.65 * ta.barssince(candle_color(close, open))

// Plot Stop Loss Levels
plot(stopLossLevel1, color=color.red, title="Stop Loss 1")
plot(stopLossLevel2, color=color.blue, title="Stop Loss 2")

// Plot Take Profit Level
plot(takeProfitLevel, color=color.green, title="Take Profit Level")

// Generate Signal
if (useHeikinAshi)
    ha_close = ta.heikinashikline(close, open, high, low)
    longCondition = ta.crossover(ha_close, stopLossLevel1)
    shortCondition = ta.crossunder(ha_close, stopLossLevel2)
else
    longCondition = ta.crossover(close, stopLossLevel1)
    shortCondition = ta.crossunder(close, stopLossLevel2)

if (longCondition)
    strategy.entry("Long", strategy.long)
if (shortCondition)
    strategy.entry("Short", strategy.short)

// Exit on Take Profit
if (strategy.position_size > 0 and close >= takeProfitLevel)
    strategy.close("Long")
if (strategy.position_size < 0 and close <= takeProfitLevel)
    strategy.close("Short")

// Plot EMA for trend assistance
emaLength = 10
ema = ta.ema(close, emaLength)
plot(ema, color=color.orange, title="EMA")

// Conditional Plot for Date Range
if (fromDay and fromMonth and fromYear)
    plotshape(series=close, location=location.abovebar, color=color.red, style=shape.labelup, title="From Date", text="From Date")
if (toDay and toMonth and toYear)
    plotshape(series=close, location=location.belowbar, color=color.green, style=shape.labeldown, title="To Date", text="To Date")
```