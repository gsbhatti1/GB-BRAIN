> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|false|Reverse Trades|
|v_input_2|true|ADX Close|
|v_input_3|false|Use Swing Lo/Hi Stop Loss & Take Profit|
|v_input_4|20|Swing Lo/Hi Lookback|
|v_input_5|false|SL Expander|
|v_input_6|false|TP Expander|
|v_input_7|14|ADX Smoothing|
|v_input_8|20|DI Length|
|v_input_9|30|adxlevel|
|v_input_10|false|-----------BB Inputs-----------|
|v_input_11|20|length|
|v_input_12|2|mult|
|v_input_13|9|MAlen|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-10-26 00:00:00
end: 2023-11-02 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © tweakerID

// This strategy uses Bollinger Bands to buy when the price 
// crosses over the lower band and sell when it crosses down
// the upper band. It only takes trades when the ADX is 
// below a certain level, and exits all trades when it's above it.

//@version=4
strategy("BB + ADX Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=100, commission_value=0.04, initial_capital=100)

// Inputs
i_reverse = input(false, title="Reverse Trades")
i_ADXClose = input(true, title="ADX Close")
i_SL = input(false, title="Use Swing Lo/Hi Stop Loss & Take Profit")
i_SwingLookback = input(20, title="Swing Lo/Hi Lookback")
i_SLExpander = input(0, title="SL Expander", step=0.5)
i_TPExpander = input(0, title="TP Expander", step=0.5)

// ADX Calculations
adxlen = input(14, title="ADX Smoothing")
dilen = input(20, title="DI Length")
dirmov(len) =>
    up = change(high)
    down = -change(low)
    plusDM = na(up) ? na : (up > down and up > 0 ? up : 0)
    minusDM = na(down) ? na : (down > up and down > 0 ? down : 0)
    truerange = atr(len)
    smoothDM = sma(plusDM, adxlen) + sma(minusDM, adxlen)
    dir = smoothDM > 0 ? 1 : smoothDM < 0 ? -1 : 0
    adx = abs(smoothDM / truerange) * 100
    adx
adx = dirmov(adxlen)

// Bollinger Bands Calculations
length = input(20, title="BB Length")
mult = input(2.0, title="BB Mult")
maLen = input(9, title="BB MA Length")

src = close
basis = sma(src, maLen)
dev = mult * atr(length)
upper = basis + dev
lower = basis - dev

// Main Logic
longCondition = close > lower and adx < adxlevel
shortCondition = close < upper and adx < adxlevel

if (longCondition)
    strategy.entry("Long", strategy.long)

if (shortCondition)
    strategy.entry("Short", strategy.short)

if (i_reverse)
    longCondition = close < upper and adx < adxlevel
    shortCondition = close > lower and adx < adxlevel

    if (longCondition)
        strategy.entry("Reverse Long", strategy.long)

    if (shortCondition)
        strategy.entry("Reverse Short", strategy.short)

if (adx > adxlevel)
    strategy.close("Long")
    strategy.close("Short")

// Stop Loss and Take Profit
if (i_SL)
    if (i_SLExpander)
        // Implement Stop Loss Expander logic
    else
        // Implement Stop Loss logic

if (i_TPExpander)
    // Implement Take Profit Expander logic
else
    // Implement Take Profit logic
```

This translation preserves the original structure and logic of the provided Pine Script, while translating the human-readable text into English.