> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|0|What trades should be taken:: LONG|SHORT|BOTH|NONE|
|v_input_2|true|---------------- Fast Moving Average (BLUE)----------------|
|v_input_3|0|First Slow moving average: EMA|SMA|WMA|HMA|JMA|KAMA|TMA|VAMA|SMMA|DEMA|VMA|WWMA|EMA_NO_LAG|TSF|ALMA|
|v_input_4||First Time Frame|
|v_input_5|6|First MA Length|
|v_input_6|true|---------------- Slow Moving Average (YELLOW)----------------|
|v_input_7|0|Second Fast moving average: JMA|EMA|WMA|HMA|SMA|KAMA|TMA|VAMA|SMMA|DEMA|VMA|WWMA|EMA_NO_LAG|TSF|ALMA|
|v_input_8||Second time frame|
|v_input_9|14|Second MA length|
|v_input_10|true|---------------- Other Settings ----------------|
|v_input_11|2|Line Width|
|v_input_12|50|Color Transparency|
|v_input_13|blue|color_fast|
|v_input_14|yellow|color_slow|
|v_input_15|true|Fill Color|
|v_input_16|true|---------------- Indicators Settings ----------------|
|v_input_17|0.85|Alma Offset (only for ALMA)|
|v_input_18|12|Volatility lookback (only for VAMA)|
|v_input_19|1.25|KAMA's alpha (only for KAMA)|
|v_input_20|false|----- Add Stop Loss / Take profit -----|
|v_input_21|2.5|Stop Loss %|
|v_input_22|5|Take Profit %|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-01-28 00:00:00
end: 2024-02-03 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License https://creativecommons.org/licenses/by-sa/4.0/
// © dman103
// A moving averages SandBox strategy where you can experiment using two different moving averages (like KAMA, ALMA, HMA, JMA, VAMA and more) on different time frames to generate BUY and SELL signals, when they cross.
// Great sandbox for experimenting with different moving averages and different time frames.

// == How to use ==
// We select two types of moving averages on two different time frames:
//
// First is the FAST moving average that should be at the same time frame or higher.
// Second is the SLOW moving average that should be on the same time frame or higher.
// When FAST moving average crosses over the SLOW moving average, we have a BUY signal (for LONG).
// When FAST moving average crosses under the SLOW moving average, we have a SELL signal (for SHORT).

// WARNING: Using a low
```