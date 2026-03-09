> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|2.06|Take Profit Stop Loss ratio|
|v_input_2|0.008|lowest risk per trade|
|v_input_3|0.02|highest risk per trade|
|v_input_4|33|EMA1 for pullback level Period|
|v_input_5|165|EMA2 for pullback limit Period|
|v_input_6|365|EMA3 for trend Period|
|v_input_7|true|Start Date|
|v_input_8|true|Start Month|
|v_input_9|2018|Start Year|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-20 00:00:00
end: 2023-12-20 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// created by Space Jellyfish
//@version=4

strategy("EMA pullback strategy", overlay = true, initial_capital=10000, commission_value = 0.075)

target_stop_ratio = input(title="Take Profit Stop Loss ratio", type=input.float, defval=2.06, minval=0.5, maxval=100)
riskLimit_low =  input(title="lowest risk per trade", type=input.float, defval=0.008, minval=0, maxval=100)
riskLimit_high =  input(title="highest risk per trade", type=input.float, defval=0.02, minval=0, maxval=100)

ema_pullbackLevel_period = input(title="EMA1 for pullback level Period", type=input.integer, defval=33, minval=1, maxval=10000)
ema_pullbackLimiit_period = input(title="EMA2 for pullback limit Period", type=input.integer, defval=165, minval=1, maxval=10000)
ema_trend_period = input(title="EMA3 for trend Period", type=input.integer, defval=365, minval=1, maxval=10000)

startDate = input(title="Start Date", type=input.integer, defval=1, minval=1, maxval=31)
startMonth = input(title="Start Month", type=input.integer, defval=1, maxval=12)
startYear = input(title="Start Year", type=input.integer, defval=2018, minval=2018)

// Calculate EMA
ema1 = ema(close, ema_pullbackLevel_period)
ema2 = ema(close, ema_pullbackLimiit_period)
ema3 = ema(close, ema_trend_period)

longCondition = crossover(close, ema1) and close > ema2 and low[1] < low
shortCondition = crossunder(close, ema1) and close < ema2 and high[1] > high

if (longCondition)
    strategy.entry("Long", strategy.long)
    if (close < riskLimit_low * open)
        strategy.close("Long")
    else if (close > target_stop_ratio * riskLimit_high * open)
        strategy.close("Long")

if (shortCondition)
    strategy.entry("Short", strategy.short)
    if (close > riskLimit_high * open)
        strategy.close("Short")
    else if (close < target_stop_ratio * riskLimit_low * open)
        strategy.close("Short")

// Plot EMAs on chart
plot(ema1, color=color.blue, title="EMA1")
plot(ema2, color=color.green, title="EMA2")
plot(ema3, color=color.red, title="EMA3")

// Print start date and time for debugging
if (startDate == 1 and startMonth == 1 and startYear == 2018)
    label.new(x=bar_index + 50, y=high[1], text="Strategy started on Jan 1, 2018", color=color.white, style=label.style_label_down, size=size.small)
```

This Pine Script code implements the EMA pullback strategy as described. It includes inputs for trade parameters and calculates EMAs with specified periods to generate trading signals based on crossovers and pullbacks. The script also handles take profit and stop loss conditions.