```pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2025-01-16 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT","balance":49999}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Vitaliby

//@version=5
strategy("Vitaliby MA and RSI Strategy", overlay=true)

// Input parameters for configuration
shortMALength = input.int(9, title="Short MA Length")
longMALength = input.int(21, title="Long MA Length")
rsiLength = input.int(14, title="RSI Length")
rsiOverbought = input.int(70, title="RSI Overbought Level")
rsiOversold = input.int(30, title="RSI Oversold Level")

// Calculation of moving averages and RSI
shortMA = ta.sma(close, shortMALength)
longMA = ta.sma(close, longMALength)
rsi = ta.rsi(close, rsiLength)

// Define entry and exit conditions
longCondition = ta.crossover(shortMA, longMA) and rsi > rsiOversold
shortCondition = ta.crossunder(shortMA, longMA) and rsi < rsiOverbought

// Display signals on the chart
plotshape(series=longCondition, location=location.belowbar, color=color.green, style=shape.labelup, text="BUY", size=size.small)
plotshape(series=shortCondition, location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL", size=size.small)

// Display moving averages on the chart
plot(shortMA, color=color.blue, title="Short MA")
plot(longMA, color=color.orange, title="Long MA")
```