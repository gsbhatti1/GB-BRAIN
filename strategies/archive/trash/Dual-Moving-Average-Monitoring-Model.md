``` pinescript
//@version=5
strategy("Dual Moving Average Monitoring Model (by ChaoZhang)",
         overlay=true,
         initial_capital=1000,
         process_orders_on_close=true,
         default_qty_type=strategy.percent_of_equity,
         default_qty_value=30,
         commission_type=strategy.commission.percent,
         commission_value=0.1)

// Show Date Range
showDate = input(defval=true, title='Show Date Range')
timePeriod = time >= timestamp(syminfo.timezone, 2022, 1, 1, 0, 0)
notInTrade = strategy.position_size <= 0

// EMAs 
fastEMA = ta.ema(close, 8)
slowEMA = ta.ema(close, 26)

// Calculate MACD
shortEMA = ta.ema(close, 12)
macdLine = shortEMA - slowEMA
signalLine = ta.ema(macdLine, 9)
hist = macdLine - signalLine

// Entry and Exit Rules
longCondition = fastEMA > slowEMA and hist > signalLine
if (longCondition and notInTrade)
    strategy.entry("Long", strategy.long)

trailStopLoss = input.float(3, title="Trailing Long Loss (%)")
shortTrailStopLoss = input.bool(true, title="Show Date Range")

// Calculate trailing stop loss for long position
trailingStop = na
if (strategy.position_size > 0)
    trailingStop := valuewhen(notInTrade, strategy.position_avg_price * (1 - trailStopLoss / 100), 0)

// Calculate trailing stop loss for short position
shortTrailingStop = na
if (strategy.position_size < 0)
    shortTrailingStop := valuewhen(notInTrade, strategy.position_avg_price * (1 + shortTrailStopLoss / 100), 0)

// Exit when trailing stop is hit
if (notInTrade and trailingStop <= close and strategy.position_size > 0)
    strategy.exit("Long Exit", "Long")
if (shortTrailingStop >= close and strategy.position_size < 0)
    strategy.exit("Short Exit", "Long")

plotchar(showDate, title="Show Date Range", char='X', location=location.top)
```

This script implements the dual moving average monitoring model with a combination of EMAs and MACD. It includes entry and exit rules based on EMA crossovers and MACD signals, as well as trailing stop loss mechanisms to manage risk.