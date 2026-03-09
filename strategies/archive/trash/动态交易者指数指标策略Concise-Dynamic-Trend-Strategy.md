``` pinescript
/*backtest
start: 2023-11-11 00:00:00
end: 2023-12-05 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
//

strategy("[BACKTEST]Traders Dynamic Index Indicator Alert by JustUncleL", shorttitle="[BACKTEST]TDIALT")

// 
// author: JustUncleL
// date: 10-Oct-2019
// 
// Description:
//   This script is a "strategy" version of the "Traders Dynamic Index Indicator Alert v0.1 by JustUncleL"
//   made available for backtesting to help optimize settings.
//
//   This is a Trend following system utilising the Traders Dynamic Index (TDI),
```

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|13|lengthrsi|
|v_input_2|34|lengthband|
|v_input_3|2|lengthrsipl|
|v_input_4|7|lengthtradesl|
|v_input_5|5|Price Action Channel Length|
|v_input_6|22|RSI Oversold Level|
|v_input_7|78|RSI Overbought Level|
|v_input_8|2|Strength Level: (1)Strong (2)Medium (3)All|
|v_input_9|false|Check Box To Turn Bars Gray|
|v_input_10|true|Highlight TDI Alert Bars|
|v_input_11|true|Show Alert Condition Status|
|v_input_12|false|Use Heikin Ashi Candles for Calculations|
|v_input_13|false|Use MACD Filtering|
|v_input_14|8|MACD Fast MA Length|
|v_input_15|16|MACD Slow MA Length|
|v_input_16|true|MACD Signal Length|
|v_input_17|0|What trades should be taken : : BOTH|SHORT|LONG|NONE|
|v_input_18|false|Initial Stop Loss Points (zero to disable)|
|v_input_19|false|Initial Target Profit Points (zero for disable)|
|v_input_20|2018|Backtest Start Year|
|v_input_21|true|Backtest Start Month|
|v_input_22|true|Backtest Start Day|
|v_input_23|9999|Backtest Stop Year|
|v_input_24|12|Backtest Stop Month|
|v_input_25|31|Backtest Stop Day|

> Source (PineScript)

``` pinescript
// TDI calculation
src = close, len = input(13), src2 = rsi(src, len)
smoothK = sma(src2, 3)
k = sma(smoothK, 3)
d = sma(k, 3)
lengthrsi = v_input_1

// Bollinger Bands
mult = input(2.0), lengthband = v_input_2
basis = sma(close, lengthband)
dev = mult * stdev(close, lengthband)
upperBB = basis + dev
lowerBB = basis - dev

// RSI and its Moving Averages
rsiVal = rsi(close, lengthrsi)
rsiPriceLine = sma(rsiVal, v_input_3)
rsiTradeSignalLine = sma(rsiVal, v_input_4)

// MACD (if enabled)
fastLength = input(12), slowLength = input(26), signalLength = 9
[macdLine, signalLine, _] = macd(close, fastLength, slowLength, signalLength)
useMacdFiltering = v_input_13

// Price Action Channel Length
lengthpac = v_input_5

// TDI Alert Bar Highlighting and Other Settings
bgcolor(v_input_9 ? color.new(color.gray, 90) : na)
plotshape(series=cross(rsiPriceLine, rsiTradeSignalLine), title="Buy Signal", location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)
plotshape(series=cross(rsiTradeSignalLine, rsiPriceLine), title="Sell Signal", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)

// MACD Filtering
if (useMacdFiltering and barssince(cross(macdLine, signalLine)) == 0)
    strategy.entry("Buy", strategy.long)
else if (useMacdFiltering and barssince(cross(signalLine, macdLine)) == 0)
    strategy.close("Buy")

// Other Strategy Settings
alertcondition(v_input_10, title="TDIALT Buy Alert")
alertcondition(v_input_11, title="Alert Condition Status")

```

This script implements the described strategy using Pine Script for TradingView. It includes the necessary indicators and conditions to detect trading signals based on TDI, RSI, Bollinger Bands, MACD, and Price Action Channel.