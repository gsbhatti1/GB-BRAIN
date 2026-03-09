``` pinescript
/*backtest
start: 2024-02-21 00:00:00
end: 2025-02-18 08:00:00
period: 2d
basePeriod: 2d
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=5
strategy("Chande Momentum Oscillator + Bollinger Bands Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// Bollinger Bands Parameters
bbLength = input.int(20, title="Bollinger Bands Length")
bbStdDev = input.float(2.0, title="Bollinger Bands Std Dev")
basis = ta.sma(close, bbLength)
upper = basis + bbStdDev * ta.stdev(close, bbLength)
lower = basis - bbStdDev * ta.stdev(close, bbLength)

// Chande Momentum Oscillator Parameters
cmoLength = input.int(14, title="CMO Length")
cmoOverbought = input.float(50, title="CMO Overbought Level")
cmoOversold = input.float(-50, title="CMO Oversold Level")
cmo = ta.cmo(close, cmoLength)

// Plot Bollinger Bands
plot(basis, color=color.blue, title="Bollinger Bands Middle")
plot(upper, color=color.red, title="Bollinger Bands Upper")
plot(lower, color=color.green, title="Bollinger Bands Lower")

// Trading Signal Generation
longCondition = ta.crossover(close, lower) and cmo < cmoOversold
shortCondition = ta.crossunder(close, upper) and cmo > cmoOverbought

// Execute Trades
if (longCondition)
    strategy.entry("Long", strategy.long)
if (shortCondition)
    strategy.entry("Short", strategy.short)

// Exit Mechanism
exitConditionLong = ta.crossunder(close, basis)
exitConditionShort = ta.crossover(close, basis)
if (exitConditionLong)
    strategy.close("Long")
if (exitConditionShort)
    strategy.close("Short")
```

This Pine Script implements the strategy described, using Bollinger Bands and CMO to generate and execute trading signals. The script includes the necessary parameters and conditions to define when to enter and exit trades based on the strategy's rules.