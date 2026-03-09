``` pinescript
/*backtest
start: 2022-10-18 00:00:00
end: 2023-10-24 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © lazy_capitalist

//@version=5
strategy('Linear Regression MA', overlay=true, initial_capital=10000)
datesGroup = "Date Info"
startMonth = input.int(defval = 1,    title = "Start Month",  minval = 1, maxval = 12,  group=datesGroup)
startDay   = input.int(defval = 1,    title = "Start Day",    minval = 1, maxval = 31,  group=datesGroup)
startYear  = input.int(defval = 2022, title = "Start Year",   minval = 1970,            group=datesGroup)

averagesGroup = "Averages"
lrLineInput     = input.int(defval = 55,    title = "Linear Regression Line", minval = 1, maxval = 200, group=averagesGroup)
lrMAInput      = input.int(defval = 55,    title = "Linear Regression MA",   minval = 1, maxval = 200, group=averagesGroup)
emaLength      = input.int(defval = 55,    title = "EMA Length",              minval = 1, maxval = 200, group=averagesGroup)

// Calculate linear regression line
lrLine = ta.linreg(close, lrLineInput, 0)
// Calculate moving averages
lrMA   = ta.sma(lrLine, lrMAInput)
ema    = ta.ema(close, emaLength)

longEntry = ta.crossover(ema, lrMA)
longExit  = ta.crossunder(ema, lrMA)

if (v_input_bool_1 and strategy.opentrades == 0) // Execute Long Trades
    strategy.entry("Long", strategy.long)

if (v_input_bool_3) // Execute Stop Loss
    stopLossLevel = v_input_float_2 * close / 100
    strategy.exit("Stop Loss", "Long", stop=stopLossLevel)

// Optional: Show date range on chart
plotshape(series=longEntry, location=location.belowbar, color=color.green, style=shape.labelup, text="Buy")
plotshape(series=longExit,  location=location.abovebar, color=color.red,   style=shape.labeldown, text="Sell")

// Optional: Market filter for bullish market
isBullish = input.bool(true, title="Consider Bullish Market Only")
if (isBullish)
    strategy.cancel("Long", when=strategy.opentrades > 0 and not isBullish)
```

This Pine Script translates the given Chinese text into English while preserving all code blocks and formatting.