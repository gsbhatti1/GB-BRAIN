> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|(?AstroHub Vortex Strategy)Length|
|v_input_2|true|Multiplier|
|v_input_3|0.5|Threshold|
|v_input_4|20|EMA Length|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This work is licensed under a Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) https://creativecommons.org/licenses/by-nc-sa/4.0/
// © AstroHub

//@version=5
strategy("Vortex Strategy [AstroHub]", shorttitle="VS [AstroHub]", overlay=true)

// Vortex Indicator Settings
length = input(14, title="Length", group ="AstroHub Vortex Strategy", tooltip="Number of bars used in the Vortex Indicator calculation. Higher values may result in smoother but slower responses to price changes.")
mult = input(1.0, title="Multiplier", group ="AstroHub Vortex Strategy", tooltip="Multiplier for the Vortex Indicator calculation. Adjust to fine-tune the sensitivity of the indicator to price movements.")
threshold = input(0.5, title="Threshold",group ="AstroHub Vortex Strategy",  tooltip="Threshold level for determining the trend. Higher values increase the likelihood of a trend change being identified.")
emaLength = input(20, title="EMA Length", group ="AstroHub Vortex Strategy", tooltip="Length of the Exponential Moving Average (EMA) used in the strategy. A longer EMA may provide a smoother trend indication.")

// Calculate Vortex Indicator components
a = math.abs(close - close[1])
b = close - ta.sma(close, length)
shl = ta.ema(b, length)
svl = ta.ema(a, length)

// Determine trend direction
upTrend = shl > svl
downTrend = shl < svl

// Define Buy and Sell signals
buySignal = ta.crossover(shl, svl) and close > ta.ema(close, emaLength) and (upTrend != upTrend[1])
sellSignal = ta.crossunder(shl, svl) and close < ta.ema(close, emaLength) and (downTrend != downTrend[1])

// Execute strategy based on signals
strategy.entry("Sell", strategy.short, when=buySignal)
strategy.entry("Buy", strategy.long, when=sellSignal)

// Background color base
```