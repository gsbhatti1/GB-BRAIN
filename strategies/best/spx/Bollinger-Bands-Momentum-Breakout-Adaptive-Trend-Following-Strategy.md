``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-11 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Demo GPT - Bollinger Bands", overlay=true, initial_capital=10000, commission_type=strategy.commission.percent, commission_value=0.1, slippage=3, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

// Inputs
length = input.int(20, minval=1, title="Length")
maType = input.string("SMA", "Basis MA Type", options = ["SMA", "EMA", "SMMA (RMA)", "WMA", "VWMA"])
src = input(close, title="Source")
mult = input.float(2.0, minval=0.001, maxval=50, title="StdDev")
offset = input.int(0, "Offset", minval=-500, maxval=500)

// Date range inputs
startYear = input.int(2018, "Start Year", minval=1970, maxval=2100)
startMonth = input.int(1, "Start Month", minval=1, maxval=12)
startDay = input.int(1, "Start Day", minval=1, maxval=31)
endYear = input.int(2069, "End Year", minval=1970, maxval=2100)
endMonth = input.int(12, "End Month", minval=1, maxval=12)
endDay = input.int(31, "End Day", minval=1, maxval=31)

// Time range
startTime = timestamp("GMT+0", startYear, startMonth, startDay, 0, 0)
endTime = timestamp("GMT+0", endYear, endMonth, endDay, 23, 59)

// Moving average function
ma(source, length, _type) =>
    switch _type
        "SMA" => ta.sma(source, length)
        "EMA" => ta.ema(source, length)
        "SMMA (RMA)" => ta.smm(source, length)
        "WMA" => ta.wma(source, length)
        "VWMA" => ta.vwma(source, length)

// Bollinger Bands
middle_band = ma(src, length, maType)
upper_band = middle_band + mult * ta.stdev(src, length) * 0.5
lower_band = middle_band - mult * ta.stdev(src, length) * 0.5

// Entry and Exit Conditions
longCondition = close > upper_band + offset
if (longCondition)
    strategy.entry("Long", strategy.long)

shortCondition = close < lower_band - offset
if (shortCondition)
    strategy.close("Long")

// Plotting
plot(middle_band, color=color.blue, title="Middle Band")
plot(upper_band, color=color.red, title="Upper Band")
plot(lower_band, color=color.green, title="Lower Band")
```

This Pine Script implements the described trading strategy. The script includes input parameters for various settings and calculates Bollinger Bands with customizable moving averages. It also defines entry and exit conditions based on price breaking through upper or lower bands.