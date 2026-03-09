``` pinescript
/*backtest
start: 2024-05-01 00:00:00
end: 2024-05-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Chandelier Exit Strategy with ZLSMA and Volume Spike Detection", shorttitle="CES with ZLSMA and Volume", overlay=true, process_orders_on_close=true, calc_on_every_tick=false)
// Chandelier Exit Inputs
lengthAtr = input.int(title='ATR Period', defval=1)
mult = input.float(title='ATR Multiplier', step=0.1, defval=2.0)
useClose = input.bool(title='Use Close Price for Extremums', defval=true)
// Calculate ATR
atr = mult * ta.atr(lengthAtr)
// Calculate Long and Short Stops
longStop = (useClose ? ta.highest(close, lengthAtr) : ta.highest(high, lengthAtr)) - atr
shortStop = (useClose ? ta.lowest(close, lengthAtr) : ta.lowest(low, lengthAtr)) + atr
// ZLSMA Inputs
zlsmaLength = input.int(title='ZLSMA Period', defval=10)
zlsma = ta.sma(ta.zlsm(closingprice), zlsmaLength)
// RVOL Spike Detection Inputs
rvolThreshold = input.float(title='RVOL Threshold', step=0.1, defval=1.5)
rvol = (volume / volume[1])
isRvolSpike = vwap > ta.sma(vwap, 20) and rvol > rvolThreshold
// Strategy Logic
if (close > zlsma and isRvolSpike)
    strategy.entry("Long", strategy.long, stop=longStop)
if (close < zlsma and isRvolSpike)
    strategy.entry("Short", strategy.short, stop=shortStop)
if (close < longStop)
    strategy.close("Long")
if (close > shortStop)
    strategy.close("Short")
```

This Pine Script code defines the ZLSMA-Enhanced Chandelier Exit Strategy with Volume Spike Detection. It includes inputs for ATR period and multiplier, use of close price for extremums, ZLSMA period, and RVOL threshold. The script calculates the stop-loss levels based on the Chandelier Exit rule and uses a volume spike detection mechanism to determine entry and exit points.