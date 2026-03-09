``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("ES Stoch RSI Strategy [krypt]", overlay=true, calc_on_order_fills=true, calc_on_every_tick=true, initial_capital=10000, currency='USD')

// Backtest Range
fromMonth = input(defval = 6, title = "From Month", minval = 1)
fromDay   = input(defval = 1, title = "From Day", minval = 1)
fromYear  = input(defval = 2018, title = "From Year")
toMonth   = input(defval = 7, title = "To Month", minval = 1)
toDay     = input(defval = 30, title = "To Day", minval = 1)
toYear    = input(defval = 2018, title = "To Year")
k         = input(defval = 7, title = "K")
d         = input(defval = 2, title = "D")
rsiLen    = input(defval = 10, title = "RSI Length", minval=1)
stochLen  = input(defval = 3, title = "Stochastic Length", minval=1)
signals   = input(defval = true, title = "Buy/Sell Signals")

// Helper function to filter trades based on date
isInDateRange = fromYear <= year and (fromMonth <= month or fromMonth == month and fromDay <= dayofmonth) and (toYear >= year or (toYear == year and toMonth >= month or (toMonth == month and toDay >= dayofmonth)))
if (isInDateRange)
    // Calculate Stochastic RSI
    rsi = rsi(close, rsiLen)
    stochRSI = smoothened(stoch(rsi, k, d), 6)

    // Plot the filtered data
    plot(stochRSI, color=blue, title="Filtered Stochastic RSI")

    // Generate trading signals
    longCondition = crossover(stochRSI, stochRSIema)
    shortCondition = crossunder(stochRSI, stochRSIema)

    if (signals and longCondition)
        strategy.entry("Long", strategy.long)
    
    if (signals and shortCondition)
        strategy.close("Long")

// Plot the Stochastic RSI
stochRSIplot = input(defval=true, title="Plot Stochastic RSI")
if stochRSIplot
    plot(stoch(rsi(close, rsiLen), k, d), color=blue, title="Stochastic RSI")

```

This script translates and updates the given Pine Script to use modern Pine Script syntax (version 3) while keeping all original code blocks and formatting intact. The strategy logic has been translated from Chinese to English as requested.