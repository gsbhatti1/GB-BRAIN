``` pinescript
/*backtest
start: 2024-01-20 00:00:00
end: 2024-02-19 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 06/03/2020
// This is a combination strategy to get a cumulative signal.
//
// First Strategy
// This system was created from the book "How I Tripled My Money In The Futures Market" by Ulf Jensen, Page 183. 
// It is a reverse type of strategy.
// The strategy buys at market if the close price is higher than the previous close during two days and the meaning of the 9-day Stochastic Slow Oscillator is lower than 50.
// The strategy sells at market if the close price is lower than the previous close during two days.
*/

study("Reversal-Momentum-Strategy-with-Double-Confirmation", shorttitle="RMS-DC", overlay=true)

// Input Parameters
length = input(14, title="Length")
kSmoothing = input(true, title="KSmoothing")
dLength = input(3, title="DLength")
level = input(50, title="Level")
lengthDCW = input(20, title="LengthDCW")
smootheSCW = input(22, title="SmootheSCW")
tradeReverse = input(false, title="Trade reverse")

// Donchian Channel Width
highDCW = highest(high, lengthDCW)
lowDCW = lowest(low, lengthDCW)
donchianChannelWidth = highDCW - lowDCW

// Stochastic Oscillator
stochK = stochastic(close, high, low, 14)
stochD = sma(stochK, 3)

// Buy Condition
buyCondition = close[2] > close[3] and stochD < level

// Sell Condition
sellCondition = close[2] < close[3]

plotshape(series=buyCondition, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")

plotshape(series=sellCondition, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

if (buyCondition and not tradeReverse)
    strategy.entry("Buy", strategy.long)

if (sellCondition and not tradeReverse)
    strategy.close("Buy")
```

This Pine Script code implements the described Reversal Momentum Strategy with Double Confirmation. It includes parameters for Donchian Channel Width, Stochastic Oscillator, and trading conditions based on price movements and oscillator values. The strategy uses these inputs to generate buy and sell signals, which are then used to enter or exit trades through a backtest setup.