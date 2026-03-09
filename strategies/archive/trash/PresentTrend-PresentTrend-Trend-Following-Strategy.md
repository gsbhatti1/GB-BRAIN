> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_string_1|0|Trade Direction: Both|Short|Long|
|v_input_source_1_hlc3|0|(?PresentTrend)Source: hlc3|high|low|open|hl2|close|hlcc4|ohlc4|
|v_input_int_1|14|Length|
|v_input_float_1|1.618|Multiplier|
|v_input_bool_1|false|Whether to use RSI or MFI|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-08-21 00:00:00
end: 2023-09-20 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © PresentTrading

//@version=5

// Define the strategy settings
strategy('PresentTrend - Strategy [presentTrading]' , overlay=true, precision=3, default_qty_type=strategy.cash,
 commission_value= 0.1, commission_type=strategy.commission.percent, slippage= 1,
 currency=currency.USD, default_qty_type = strategy.percent_of_equity, default_qty_value = 10, initial_capital= 10000)

// Define the input parameters
priceSource  = input.source(title='Source', defval=hlc3, group='PresentTrend') // The price source to use
lengthParam  = input.int(title='Length', defval=14, group='PresentTrend') // The length of the moving average
multiplier = input.float(title='Multiplier', defval=1.618, step=0.1, group='PresentTrend') // The multiplier for the ATR
indicatorChoice  = input.bool(title='Whether to use RSI or MFI', defval=false, group='PresentTrend') // Whether to use RSI or MFI

// Add a parameter for choosing Long or Short
tradeDirection = input.string(title="Trade Direction", defval="Both", options=["Long", "Short", "Both"])

// Calculate the ATR and the upT and downT values
ATR = ta.sma(ta.tr, lengthParam)
upperThreshold = low - ATR * multiplier 
lowerThreshold  = high + ATR * multiplier 

// Initialize the PresentTrend indicator
PresentTrend = 0.0

// Calculate the PresentTrend indicator
PresentTrend := (indicatorChoice ? ta.rsi(priceSource, lengthParam) >= 50 : ta.mfi(hlc3, lengthParam) >= 50) ? upperThreshold < nz(PresentTrend[1]) ? nz(PresentTrend[1]) : upperThreshold : lowerThreshold > nz(PresentTrend[1]) ? nz(PresentTrend[1]) : lowerThreshold

// Calculate the buy and sell signals
longSignal  = ta.crossover(PresentTrend, PresentTrend[2])
shortSignal  = ta.crossunder(PresentTrend, PresentTrend[2])

// Calculate the number of bars since the last buy and sell signals
barsSinceBuy = ta.barssince(longSignal)
barsSinceSell = ta.barssince(shortSignal)

// Place orders based on the buy and sell signals
if (tradeDirection == "Both" or tradeDirection == "Long")
    strategy.entry("Long", strategy.long, when=longSignal)

if (tradeDirection == "Both" or tradeDirection == "Short")
    strategy.entry("Short", strategy.short, when=shortSignal)
```

This is the translated Pine Script with the original code blocks and formatting intact.