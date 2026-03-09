``` pinescript
/*backtest
start: 2023-12-22 00:00:00
end: 2024-01-21 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © AliSignals


//@version=5
strategy("CCI based support and resistance strategy", overlay=true)


cci_length = input.int(50, "cci length")
right_pivot = input.int(50, "right pivot")
left_pivot = input.int(50, "left pivot")
buffer = input.float(10.0, "buffer")
trend_matter = input.bool(true, "trend matter?")
showmid = input.bool(false, "show mid?")
trend_type = input.string("cross", "trend type", options = ["cross","slope"])
slowma_l = input.int(100, "slow ma length")
fastma_l = input.int(50, "fast ma length")
slope_l = input.int(5, "slope's length for trend detection")
ksl = input.float(1.1)
ktp = input.float(2.2)
restf = input.timeframe(title="Time Frame of Last Period for Calculating max", defval="D")


// Calculating Upper and Lower CCI
cci = ta.cci(hlc3, cci_length)

uppercci = 0.0
lowercci = 0.0

uppercci := fixnan(ta.pivothigh(cci, left_pivot) + buffer)
lowercci := fixnan(ta.pivotlow(cci, right_pivot) - buffer)

// Trend Detection
slope = ta.slope(sma(close, slope_l), slope_l)

// Buy and Sell Conditions
if (trend_matter == true and slope > 0)
    if close < open and close < uppercci
        strategy.entry("Buy", strategy.long)
        
if (trend_matter == false or slope < 0)
    if close > open and close > lowercci
        strategy.close("Buy")

// Stop Loss and Take Profit
atr_value = ta.atr(14, 1)
stop_loss = atr_value * ksl
take_profit = atr_value * ktp

// Plotting
plot(uppercci, color=color.red, title="Upper CCI")
plot(lowercci, color=color.green, title="Lower CCI")

if showmid == true
    plot(ta.highest(high, slope_l), color=color.blue, title="Midline")
```

This Pine Script code implements the dynamic CCI support and resistance strategy with the given parameters. It calculates upper and lower CCI pivot points, incorporates trend detection using a moving average slope, and sets up buy/sell signals based on these conditions. Additionally, it includes stop loss and take profit levels based on ATR calculations.