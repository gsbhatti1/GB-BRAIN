``` pinescript
/*backtest
start: 2023-11-23 00:00:00
end: 2023-11-30 00:00:00
period: 15m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © PresentTrading

//@version=5
// Define the strategy settings
strategy('Volatility Capture RSI-Bollinger - Strategy [presentTrading]', overlay=true)

// Define the input parameters for the indicator
priceSource  = input.source(title='Source', defval=hlc3, group='presentBollingBand') // The price source to use
lengthParam   = input.int(50, 'lengthParam', minval=1, group='presentBollingBand') // The length of the moving average
multiplier = input.float(2.7183, 'Multiplier', minval=0.1, step=.1, group='presentBollingBand') // The multiplier for the ATR
useRSI = input.bool(true, 'Use RSI for signals', group='presentBollingBand') // Boolean input to decide whether to use RSI for signals
rsiPeriod = input.int(10, 'RSI Period', minval=1, group='RSI') // The period for the RSI
smaPeriod = input.int(5, 'SMA Period', minval=1, group='SMA') // The period for the SMA
boughtRangeLevel = input.float(55, 'Bought Range Level', group='Bought/Sold Levels') // The level to enter long positions
soldRangeLevel = input.float(50, 'Sold Range Level', group='Bought/Sold Levels') // The level to enter short positions
tradeDirection = input.string('Both', title='Trade Direction', options=['Short', 'Long', 'Both'], group='Trade Direction') // The trade direction: short, long, or both

// Calculate the Bollinger Bands
bb = ta.bband(priceSource, lengthParam, multiplier)
presentBollingBand = ta.highest(bb[1], lengthParam) + (bb[1] - bb[1][1]) * (price - bb[1][1]) / (bb[1][1] - bb[1][2])

// Calculate the RSI and SMA
rsi = ta.rsi(priceSource, rsiPeriod)
sma = ta.sma(priceSource, smaPeriod)

// Generate signals
if (useRSI)
    longCondition = ta.crossover(presentBollingBand, rsi)
    shortCondition = ta.crossunder(presentBollingBand, rsi)
else
    longCondition = ta.crossover(priceSource, presentBollingBand)
    shortCondition = ta.crossunder(priceSource, presentBollingBand)

// Enter and exit trades
if (tradeDirection == 'Long')
    strategy.entry("Long", strategy.long, when=longCondition)
if (tradeDirection == 'Short')
    strategy.entry("Short", strategy.short, when=shortCondition)
if (tradeDirection == 'Both')
    strategy.entry("Long", strategy.long, when=longCondition)
    strategy.entry("Short", strategy.short, when=shortCondition)

// Exit positions
if (priceSource >= boughtRangeLevel)
    strategy.close("Long")
if (priceSource <= soldRangeLevel)
    strategy.close("Short")
```

This script defines the `Volatility Capture RSI-Bollinger` strategy with the necessary parameters and logic to generate trading signals based on the Bollinger Bands, RSI, and SMA.