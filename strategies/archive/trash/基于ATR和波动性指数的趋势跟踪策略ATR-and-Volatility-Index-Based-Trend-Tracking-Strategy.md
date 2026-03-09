> Strategy Arguments



|Argument|Default|Description|
|---|---|---|
|v_input_1|true|Max Intraday Loss(%)|
|v_input_2|0|Renko Assignment Method: ATR|Traditional|Part of Price|
|v_input_3|14|Value|
|v_input_4|0|Price Source: Close|Open / Close|High / Low|
|v_input_5|0|Use True Range instead of Volume: Auto|Always|Never|
|v_input_6|false|Oscillating|
|v_input_7|false|Normalize|
|v_input_8|14|length|
|v_input_9|false|Offset|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-12-28 00:00:00
end: 2024-01-03 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © sharatgbhat

//@version=4
strategy("ATR and CHOP-Based Trend Tracking Strategy", overlay=false, default_qty_type = strategy.percent_of_equity, default_qty_value = 10, max_lines_count = 500, max_labels_count = 500)
maxIdLossPcnt = input(1, "Max Intraday Loss(%)", type=input.float)
// strategy.risk.max_intraday_loss(maxIdLossPcnt, strategy.percent_of_equity)

method = input(defval="ATR", options=["ATR", "Traditional", "Part of Price"], title="Renko Assignment Method")
methodvalue = input(defval=14.0, type=input.float, minval=0, title="Value")
pricesource = input(defval="Close", options=["Close", "Open / Close", "High / Low"], title="Price Source")
useClose = pricesource == "Close"
useOpenClose = pricesource == "Open / Close" or useClose
useTrueRange = input(defval="Auto", options=["Always", "Auto", "Never"], title="Use True Range instead of Volume")
isOscillating = input(defval=false, type=input.bool, title="Oscillating")
normalize = input(defval=false, type=input.bool, title="Normalize")
vol = useTrueRange == "Always" or useTrueRange == "Auto" and na(volume) ? tr : volume
op =
```