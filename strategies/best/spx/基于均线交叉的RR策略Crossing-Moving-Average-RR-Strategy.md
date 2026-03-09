> Source (PineScript)

```pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Crossing-Moving-Average-RR-Strategy", overlay=true)

// Define the moving averages
sma_30 = ta.sma(close, 30)
sma_60 = ta.sma(close, 60)
sma_200 = ta.sma(close, 200)

// Generate buy and sell signals
buy_signal = ta.crossover(sma_30, sma_200)
sell_signal = ta.crossunder(sma_30, sma_200)

// Plot the moving averages on the chart
plot(sma_30, color=color.blue, title="30-period SMA")
plot(sma_60, color=color.green, title="60-period SMA")
plot(sma_200, color=color.red, title="200-period SMA")

// Execute trades based on the signals
if (buy_signal)
    strategy.entry("Buy", strategy.long)

if (sell_signal)
    strategy.exit("Sell", "Buy")

// Position sizing and stop loss
strategy.close_on_exit(true)
```

This PineScript code implements the "Crossing-Moving-Average-RR-Strategy" as described in the strategy document. It calculates the 30-period, 60-period, and 200-period simple moving averages (SMA) and generates buy and sell signals based on their crossovers. The script also plots these moving averages on the chart and executes trades accordingly.