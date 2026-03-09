``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
//future strategy
//strategy(title = "stub", default_qty_type = strategy.fixed, default_qty_value = 1, overlay = true, commission_type=strategy.commission.cash_per_contract,commission_value=2.05)
//stock strategy
strategy(title = "Moving-Average-Crossover-Trading-Strategy", overlay = true)
//forex strategy
//strategy(title = "stub", 
```

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|1900|Backtest Start Year|
|v_input_2|true|Backtest Start Month|
|v_input_3|true|Backtest Start Day|
|v_input_4|2018|Backtest Start Year|
|v_input_5|12|Backtest Start Month|
|v_input_6|true|Backtest Start Day|


> Source (PineScript)

``` pinescript
//@version=3
strategy(title = "Moving-Average-Crossover-Trading-Strategy", overlay = true)

// Define input parameters for the strategy arguments
var year_start_backtest1 = input(1900, title="Backtest Start Year 1")
var month_start_backtest1 = input(true, title="Backtest Start Month 1")
var day_start_backtest1 = input(true, title="Backtest Start Day 1")
var year_start_backtest2 = input(2018, title="Backtest Start Year 2")
var month_start_backtest2 = input(12, title="Backtest Start Month 2")
var day_start_backtest2 = input(true, title="Backtest Start Day 2")

// Define the EMA periods
ema_4 = ema(close, 4)
ema_8 = ema(close, 8)
ema_20 = ema(close, 20)

// Calculate the crossovers and trade signals
long_condition = crossover(ema_4, ema_8) and ema_20 > ref(ema_20[1], 1)
short_condition = crossunder(ema_4, ema_8) and ema_20 < ref(ema_20[1], 1)

// Enter long when conditions are met
if (long_condition)
    strategy.entry("Long", strategy.long)

// Exit long position if the EMA crossovers reverse or the 20-period EMA changes direction
if (crossunder(ema_4, ema_8) or ema_20 < ref(ema_20[1], 1))
    strategy.close("Long")

// Enter short when conditions are met
if (short_condition)
    strategy.entry("Short", strategy.short)

// Exit short position if the EMA crossovers reverse or the 20-period EMA changes direction
if (crossover(ema_4, ema_8) or ema_20 > ref(ema_20[1], 1))
    strategy.close("Short")
```

This script defines a Pine Script for the moving average crossover trading strategy with detailed input parameters and logic to handle long and short trades based on EMA crossovers.