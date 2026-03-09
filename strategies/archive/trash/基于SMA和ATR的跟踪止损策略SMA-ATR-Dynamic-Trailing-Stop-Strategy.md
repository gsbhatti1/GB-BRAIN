> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|200|SMA Length|
|v_input_2|14|ATR Length|
|v_input_3|true|Show SMA and ATR Bands|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-01-30 00:00:00
end: 2024-02-05 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("SMA+ATR Strategy", overlay=true)

// User inputs for SMA, ATR, and display option
smaLength = input(200, title="SMA Length")
atrLength = input(14, title="ATR Length")
showSMAandATR = input(true, title="Show SMA and ATR Bands")

// Calculation of SMA and ATR
sma = ta.sma(close, smaLength)
atr = ta.atr(atrLength)

// Buy and sell logic based on SMA and ATR
buyCondition = close > sma + atr
sellCondition = close < sma - atr

// Variable to store the entry price
var float entryPrice = na

// Buy and sell signals
if (buyCondition)
    strategy.entry("Buy", strategy.long)
    entryPrice := close // Store the entry price

if (sellCondition)
    // Only if a buy has occurred
    if not na(entryPrice)
        // Calculate performance since the buy signal
        performanceSinceBuy = ((close - entryPrice) / entryPrice) * 100
        // Display performance
        // Choose the box color based on the sign of performance
        plColor = performanceSinceBuy >= 0 ? color.green : color.red
        // Display performance in the corresponding color
        plBox = "P/L: " + str.tostring(performanceSinceBuy, "#.##") + "%"
        label.new(bar_index, high, text=plBox, color=plColor, textcolor=color.white
```

Note that the script is incomplete at the end. The `label.new` line is missing a closing parenthesis. Here is the corrected version:

``` pinescript
/*backtest
start: 2023-01-30 00:00:00
end: 2024-02-05 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("SMA+ATR Strategy", overlay=true)

// User inputs for SMA, ATR, and display option
smaLength = input(200, title="SMA Length")
atrLength = input(14, title="ATR Length")
showSMAandATR = input(true, title="Show SMA and ATR Bands")

// Calculation of SMA and ATR
sma = ta.sma(close, smaLength)
atr = ta.atr(atrLength)

// Buy and sell logic based on SMA and ATR
buyCondition = close > sma + atr
sellCondition = close < sma - atr

// Variable to store the entry price
var float entryPrice = na

// Buy and sell signals
if (buyCondition)
    strategy.entry("Buy", strategy.long)
    entryPrice := close // Store the entry price

if (sellCondition)
    // Only if a buy has occurred
    if not na(entryPrice)
        // Calculate performance since the buy signal
        performanceSinceBuy = ((close - entryPrice) / entryPrice) * 100
        // Display performance
        // Choose the box color based on the sign of performance
        plColor = performanceSinceBuy >= 0 ? color.green : color.red
        // Display performance in the corresponding color
        plBox = "P/L: " + str.tostring(performanceSinceBuy, "#.##") + "%"
        label.new(bar_index, high, text=plBox, color=plColor, textcolor=color.white)
```

This should now be fully functional.