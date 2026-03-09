``` pinescript
takeProfitType = input.string(title="Take Profit Type", defval="0", options=["1 Take Profit", "2 Take Profits", "3 Take Profits"])

// HMA Inputs
hmaLength = input.int(title="HMA Length", defval=50)
hma = ta.hma(close, hmaLength)

// --- Strategy Logic ---

// Baseline Cross Qualifier
if (pbcqEnabled)
    pbcqCondition = ta.crossover(close, baseline) or ta.crossunder(close, baseline)
    pbcqCondition = pbcqCondition and (close[pbcqBarsAgo] < baseline[pbcqBarsAgo])

// Volatility Filter
volatilityFilter = ta.atr(atrLength) * multiplier

// Take Profit Levels
tpLevel1 = na
tpLevel2 = na
tpLevel3 = na
if (takeProfitType == "1 Take Profit")
    tpLevel1 := close * (1 + 0.01 * 10)
elseif (takeProfitType == "2 Take Profits")
    tpLevel1 := close * (1 + 0.01 * 10)
    tpLevel2 := close * (1 + 0.01 * 20)
elseif (takeProfitType == "3 Take Profits")
    tpLevel1 := close * (1 + 0.01 * 10)
    tpLevel2 := close * (1 + 0.01 * 20)
    tpLevel3 := close * (1 + 0.01 * 30)

// Buy Condition
longCondition = ta.crossover(close, baseline) and (close > baseline + volatilityFilter) and (hma > hma[-1])
if (longCondition)
    strategy.entry("Long", strategy.long)

// Sell Condition
shortCondition = ta.crossunder(close, baseline) and (close < baseline - volatilityFilter) and (hma < hma[-1])
if (shortCondition)
    strategy.entry("Short", strategy.short)

// Stop Loss
strategy.exit("Long SL", "Long", stop=baseline - volatilityFilter)
strategy.exit("Short SL", "Short", stop=baseline + volatilityFilter)
```

This Pine Script defines the parameters and logic for the strategy described, including the use of moving averages, ATR volatility filtering, and HMA trend bias to generate trading signals and manage take profits and stop losses.