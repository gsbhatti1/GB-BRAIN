``` pinescript
/*backtest
start: 2023-10-13 00:00:00
end: 2023-11-12 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
strategy("Dual-MACD Quantitative Trading Strategy", overlay=true, initial_capital=5000, default_qty_type=strategy.percent_of_equity, default_qty_value=80, pyramiding=0, calc_on_order_fills=true)

fastLength = input(10)
slowlength = input(22)
MACDLength = input(9)
fastLength2 = input(21)
slowlength2 = input(45)
MACDLength2 = input(20)
KSmoothing = input(2)
DSmoothing = input(3)
RSILength = input(7)
StochasticLength = input(8)
rsiSource = input(close, title="RSI Source")

// Calculate first MACD
ema1 = ema(close, fastLength)
ema2 = ema(close, slowlength)
macd1 = ema1 - ema2
signal1 = sma(macd1, MACDLength)
histogram1 = macd1 - signal1

// Calculate second MACD
ema3 = ema(close, fastLength2)
ema4 = ema(close, slowlength2)
macd2 = ema3 - ema4
signal2 = sma(macd2, MACDLength2)
histogram2 = macd2 - signal2

// RSI calculation
rsiVal = rsi(rsiSource, RSILength)

// Stochastic RSI calculation
stochK = stochosc(rsiVal, KSmoothing, DSmoothing)
stochD = smooth(stochK, 3)

// Buy and Sell Signals
buySignal1 = crossover(histogram1, 0)
sellSignal1 = crossunder(histogram1, 0)
confirmSell2 = inRange(stochD, 80, 100)

if (buySignal1)
    strategy.entry("Buy", strategy.long)

if (sellSignal1 or confirmSell2)
    strategy.close("Buy")

// Parameters
plot(strategy.equity, title="Equity Curve")
```