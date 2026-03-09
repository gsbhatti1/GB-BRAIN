``` pinescript
/*backtest
start: 2024-01-26 00:00:00
end: 2024-02-25 00:00:00
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("3 10.0 Oscillator Profile Flagging", shorttitle="3 10.0 Oscillator Profile Flagging", overlay=false)

signalBiasValue = input(title="Signal Bias", defval=0.26)
macdBiasValue = input(title="MACD Bias", defval=0.7)
shortLookBack = input(title="Short LookBack", defval=3)
longLookBack = input(title="Long LookBack", defval=6)
takeProfit = input(title="Take Profit", defval=2)
stopLoss = input(title="Stop Loss", defval=0.7)

fast_ma = ta.sma(close, 3)
slow_ma = ta.sma(close, 10)
macd = fast_ma - slow_ma
signal = ta.sma(macd, 16)
hline(0, "Zero Line", color=color.black)

buyVolume = volume*((close-low)/(high-low))
sellVolume = volume*((high-close)/(high-low))
buyVolSlope = buyVolume - buyVolume[1]
sellVolSlope = sellVolume - sellVolume[1]
signalSlope = ( signal - signal[1] )
macdSlope = ( macd - macd[1] )
plot(macd, color=color.blue, title="Total Volume")
plot(signal, color=color.orange, title="Signal Line")
plot(macdSlope, color=color.green, title="MACD Slope")
plot(signalSlope, color=color.red, title="Signal Slope")

intrabarRange = high - low
rsi = ta.rsi(close, 14)
rsiSlope = rsi - rsi[1]
plot(rsi)

longCondition = (macd > signal and macdSlope > 0) and rsi < 70 and buyVolSlope > sellVolSlope * signalBiasValue
shortCondition = (macd < signal and macdSlope < 0) and rsi > 30 and sellVolSlope > buyVolSlope * macdBiasValue

if (longCondition)
    strategy.entry("Long", strategy.long)

if (shortCondition)
    strategy.entry("Short", strategy.short)

trailStopLoss = stopLoss * close
stopPrice = na
if (strategy.position_size > 0 and not na(stopPrice))
    strategy.exit("Profit Target Long", from_entry="Long", limit=takeProfit*close, stop=trailStopLoss)
else if (strategy.position_size < 0 and not na(stopPrice)) 
    strategy.exit("Profit Target Short", from_entry="Short", limit=-takeProfit*close, stop=-trailStopLoss)

plotshape(series=strategy.position_size > 0, title="Long Entry", location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)
plotshape(series=strategy.position_size < 0, title="Short Entry", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)

```

This script implements the Three-Factors-Model-for-Price-Oscillation-Detection strategy in Pine Script. It calculates and plots technical indicators such as moving averages, MACD, signal line, RSI, and volume-based slopes to determine entry and exit points based on the defined conditions. The stop loss and take profit are dynamically adjusted according to the trade direction.