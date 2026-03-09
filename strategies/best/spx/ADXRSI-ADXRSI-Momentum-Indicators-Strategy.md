``` pinescript
/*backtest
start: 2023-11-10 00:00:00
end: 2023-12-01 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("ADXRSI Momentum Indicator Strategy", overlay=true)

// ADX Settings
adxlen = input(14, title="ADX Smoothing")
dilen  = input(14, title="DI Length")

// RSI Settings
rsiperiod = input(7, title="Periodo RSI")
oversoldLevel = input(30, title="Livello Ipervenduto")
overboughtLevel = input(70, title="Livello Ipercomprato")

// Bollinger Bands Settings
bbperiod = input(50, title="Periodo BB")
bbdev = input(2, title="Dev BB")

// Calculate ADX and DI
adx = ta.adx(dilen, adxlen)
diplus = ta.diar(dilen, adxlen)
diminus = ta.diamr(dilen, adxlen)

// RSI Calculation
rsi = ta.rsi(close, rsiperiod)

// Bollinger Bands Calculation
midband = sma(close, bbperiod)
upperband = midband + (bbdev * ta.stdev(close, bbperiod))
lowerband = midband - (bbdev * ta.stdev(close, bbperiod))

// Buy Conditions
buy_condition1 = adx > 32 and close < lowerband and rsi < oversoldLevel
buy_signal = ta.crossover(rsi, oversoldLevel)

// Sell Conditions
sell_condition1 = adx > 32 and close > upperband and rsi > overboughtLevel
sell_signal = ta.crossunder(rsi, overboughtLevel)

// Plotting
plot(adx, title="ADX", color=color.blue)
hline(oversoldLevel, "OverSold Level", color=color.red)
hline(overboughtLevel, "OverBought Level", color=color.green)
plot(lowerband, title="Lower Bollinger Band", color=color.orange)
plot(upperband, title="Upper Bollinger Band", color=color.orange)

// Strategy Execution
if (buy_signal and not buy_condition1)
    strategy.entry("Buy", strategy.long)

if (sell_signal and not sell_condition1)
    strategy.exit("Sell", "Buy")

```

Note: The Pine Script provided here is a simplified version based on the given strategy description. Please test it thoroughly before using in actual trading environments, as backtesting results may vary due to historical data limitations.