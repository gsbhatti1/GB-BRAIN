``` pinescript
/*backtest
start: 2023-05-15 00:00:00
end: 2024-05-14 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
//@author Honestcowboy
//
strategy("Triple RSI [Honestcowboy]")

  
// $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ >>
// ---------> User Inputs <----------- >>
// $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ >>

rsiLengthInput = input.int(5, minval=1, title="RSI Length", group="RSI Settings")
rsiSourceInput = input.source(close, "Source", group="RSI Settings")

// $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ >>
// ---------> VARIABLE CALCULATIONS <----------- >>
// $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ >>

up = ta.rma(math.max(ta.change(rsiSourceInput), 0), rsiLengthInput)
down = ta.rma(-math.min(ta.change(rsiSourceInput), 0), rsiLengthInput)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ >>
// ---------> CONDITIONALS <----------- >>
// $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ >>

rule1   = rsi<35
rule2   = rsi<rsi[1] and rsi[1]<rsi[2] and rsi[2]<rsi[3]
rule3   = rsi[3]<60
rule4   = close>ta.sma(close, 200)

longCondition = rule1 and rule2 and rule3 and rule4

// $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ >>
// ---------> EXIT CONDITIONS <----------- >>
// $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ >>

exitCondition = rsi>50

// $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ >>
// ---------> LOGIC EXECUTION <----------- >>
// $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ >>

if (longCondition)
    strategy.entry("Long", strategy.long)

if (exitCondition)
    strategy.exit("Exit Long", "Long")

```

This completes the translation and ensures that all code blocks, numbers, and formatting remain unchanged.