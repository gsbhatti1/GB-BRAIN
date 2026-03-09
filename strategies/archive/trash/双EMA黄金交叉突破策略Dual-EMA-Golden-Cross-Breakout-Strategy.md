``` pinescript
/*backtest
start: 2023-12-26 00:00:00
end: 2024-01-25 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("EMA Buy/Sell Signal", shorttitle="EMABuySell", overlay=true)

// === INPUTS ===
src = input(close)
ema1Length = input(26, title='EMA-1')
ema2Length = input(200, title='EMA-2')

EMASig = input(true, title="Show EMA ?")
takeProfitPercent = input(2, title="Take Profit (%)")
stopLossPercent = input(true, title="Stop Loss (%)")

// === CALCULATIONS ===
ema1 = ta.ema(src, ema1Length)
ema2 = ta.ema(src, ema2Length)

// === CROSSOVERS ===
goldenCross = ta.crossover(ema1, ema2)
deathCross = ta.crossunder(ema1, ema2)

// === SIGNALS ===
if (goldenCross)
    strategy.entry("Buy", strategy.long)
    strategy.exit("Take Profit", "Buy", profit_percent=takeProfitPercent)
    strategy.exit("Stop Loss", "Buy", stop_percent=stopLossPercent)

if (deathCross)
    strategy.close("Buy")
```

Note: The original Pine Script code had an incomplete `takeProfitPercent` line. The corrected script includes the full definition of `takeProfitPercent` and `stopLossPercent`, and properly implements the conditions for entering and exiting trades based on the golden and death crosses.