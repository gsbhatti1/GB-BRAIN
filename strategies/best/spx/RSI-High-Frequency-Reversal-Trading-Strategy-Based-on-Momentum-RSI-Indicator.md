> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|RSI Period|
|v_input_2|true|Standard Deviation Multiplier|
|v_input_3|1.5|Exhaustion Multiplier|
|v_input_4|8|Profit Target (ticks)|
|v_input_5|32|Stop Loss (ticks)|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-03-01 00:00:00
end: 2024-03-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("MCOTs Intuition Strategy", overlay=true, default_qty_type=strategy.fixed, default_qty_value=1, initial_capital=50000, calc_on_every_tick=true)

// Input for RSI period
rsiPeriod = input(14, title="RSI Period")
// Input for standard deviation multiplier
stdDevMultiplier = input(1.0, title="Standard Deviation Multiplier")
// Input for exhaustion detection
exhaustionMultiplier = input(1.5, title="Exhaustion Multiplier")
// Input for profit target and stop loss in ticks
profitTargetTicks = input(8, title="Profit Target (ticks)")
stopLossTicks = input(32, title="Stop Loss (ticks)")

// Calculate RSI
rsiValue = ta.rsi(close, rsiPeriod)
// Calculate standard deviation of RSI changes
rsiStdDev = ta.stdev(ta.change(rsiValue), rsiPeriod)
// Calculate momentum
momentum = ta.change(rsiValue)

// Conditions for entering long position
if (ta.crossover(momentum, stdDevMultiplier * rsiStdDev) and (momentum > 0))
    strategy.entry("Long", strategy.long)
    
// Conditions for entering short position
if (ta.crossunder(momentum, -stdDevMultiplier * rsiStdDev) and (momentum < 0))
    strategy.entry("Short", strategy.short)

// Exit conditions based on stop loss and profit target ticks
strategy.exit("Exit Long", "Long", stop=-(stopLossTicks), limit=(close + profitTargetTicks))
strategy.exit("Exit Short", "Short", stop=(stopLossTicks), limit=(close - profitTargetTicks))

// Plot RSI for visualization
plot(rsiValue, color=color.blue)
```

This Pine Script defines the high-frequency reversal trading strategy based on the Momentum RSI indicator. The script includes inputs for setting the RSI period, standard deviation multiplier, exhaustion factor, and profit/stop loss levels. It also specifies conditions to enter long or short positions based on the calculated momentum and exits trades using limit and stop orders.