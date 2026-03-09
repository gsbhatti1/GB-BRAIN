> Name

Reversal-Trading-Strategy-Based-on-Stochastic-RSI

> Author

ChaoZhang

> Strategy Description



This strategy is named “Reversal Trading Strategy Based on Stochastic RSI”. It uses the Stochastic RSI indicator to identify overbought/oversold situations, entering reverse trades when extremes reverse.

The Stochastic RSI calculates the Stochastic oscillator on RSI values, generating K and D line signals that reflect overbought/oversold conditions in the RSI itself.

The trading logic is:

1. Calculate fast RSI to capture overbought/oversold.
2. Apply a weighted moving average on RSI to derive Stochastic RSI K-line signal.
3. When K-line crosses above its moving average, a buy signal is generated. When crossing below, a sell signal is generated.
4. Reversal signals near overbought or oversold extremes hint at reversal trade opportunities.

The advantage of this strategy is using Stochastic RSI to identify reversal points. But parameter combinations need optimization, and overtrading should be prevented. Stop loss is also essential.

In conclusion, Stochastic RSI is a common and useful way to determine reversal timing. But traders still need overall trend judgment to avoid buying tops and selling bottoms in retracements.



|||


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Use Heikin Ashi Candles in Algo Calculations|
|v_input_2|true|From Month|
|v_input_3|true|From Day|
|v_input_4|2021|From Year|
|v_input_5|12|Thru Month|
|v_input_6|30|Thru Day|
|v_input_7|2021|Thru Year|
|v_input_8|true|Show Date Range|
|v_input_9_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_10|80|TopBand|
|v_input_11|20|LowBand|
|v_input_12|2|RSI Length|
|v_input_13|50|MA Length|
|v_input_14|5|RSI MA Length|
|v_input_15|0|MA Type: LRC|EMA|DEMA|TEMA|SMA|WMA|MF|VAMA|TMA|HMA|JMA|Kijun v2|EDSMA|McGinley|
|v_input_16|0|RSI MA Type: TMA|EMA|DEMA|TEMA|LRC|WMA|MF|VAMA|SMA|HMA|JMA|Kijun v2|EDSMA|McGinley|
|v_input_17|true|Kijun MOD Divider|
|v_input_18|3|* Jurik (JMA) Only - Phase|
|v_input_19|true|* Jurik (JMA) Only - Power|
|v_input_20|10|* Volatility Adjusted (VAMA) Only - Volatility lookback length|
|v_input_21|0.8|Modular Filter, General Filter Only - Beta|
|v_input_22|false|Modular Filter Only - Feedback|
|v_input_23|0.5|Modular Filter Only - Feedback Weighting|
|v_input_24|20|EDSMA - Super Smoother Filter Length|
|v_input_25|0|EDSMA - Super Smoother Filter Poles: 2|3|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-09-05 00:00:00
end: 2023-09-12 00:00:00
period: 5m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © MightyZinger
//@version=4
strategy(shorttitle="MZ SRSI",title="MightyZinger SRSI Strategy", overlay=false, pyramiding=1, calc_on_order_fills=true, calc_on_every_tick=true, default_qty_type=strategy.fixed, default_qty_value=5,commission_value=0.1)

//heiking ashi calculation
UseHAcandles    = input(true, title="Use Heikin Ashi Candles in Algo Calculations")
////
// === /INPUTS ===

// === BASE FUNCTIONS ===
haClose = UseHAcandles ? security(heikinashi(syminfo.tickerid), timeframe.period, close) : close
haOpen  = UseHAcandles ? security(heikinashi(syminfo.tickerid), timeframe.period, open) : open
haHigh  = UseHAcandles ? security(heikinashi(syminfo.tickerid), timeframe.period, high) : high
haLow   = UseHAcandles ? security(heikinashi(syminfo.tickerid), timeframe.period, low) : low


//Backtest dates
fromMonth = input(defval = 1,    title = "From Month",      type = input.integer, minval = 1, maxval = 12)
fromDay   = input(defval = 1,    title = "From Day",        type = input.integer, minval = 1, maxval = 31)
fromYear  = input(defval = 2021, title = "From Year",       type = input.integer, minval = 1970)
thruMonth = input(defval = 12,    title = "Thru Month",      type = input.integer, minval = 1, maxval = 12)
thruDay   = input(defval = 30,    title = "Thru Day",        type = input.integer, minval = 1, maxval = 31)
thruYear  = input(defval = 2021, title = "Thru Year",       type = input.integer, minval = 1970)

showDate  = input(defval = true, title = "Show Date Range", type = input.bool)

start     = timestamp(fromYear, fromMonth, fromDay, 00, 00)        // backtest start window
finish    = timestamp(thruYear, thruMonth, thruDay, 23, 59)        // backtest finish window
window()  => true       // create function "within window of time"

src = UseHAcandles ? haClose : input(close, title="Source")

TopBand = input(80, step=0.01)
LowBand = input(20, step=0.01)
lengthRSI = input(2, minval=1,title="RSI Length")
lengthMA = input(50, minval=1,title="MA Length")
lengthRSI_MA= input(5, minval=1,title="RSI MA Length")


//RSI Source
maType = input(title="MA Type", type=input.string, defval="LRC", options=["SMA","EMA","DEMA","TEMA","LRC","WMA","MF","VAMA","TMA","HMA", "JMA", "Kijun v2", "EDSMA","McGinley"])
rsiMaType = input(title="RSI MA Type", type=input.string, defval="TMA", options=["SMA","EMA","DEMA","TEMA","LRC","WMA","MF","VAMA","TMA","HMA", "JMA", "Kijun v2", "EDSMA","McGinley"])

//MA Function

//           Pre-reqs
//
tema(src, len) =>
    ema1 = ema(src, len)
    ema2 = ema(ema1, len)
    ema3 = ema(ema2, len)
    (3 * ema1) - (3 * ema2) + ema3
kidiv = input(defval=1,maxval=4,  title="Kijun MOD Divider")

jurik
```