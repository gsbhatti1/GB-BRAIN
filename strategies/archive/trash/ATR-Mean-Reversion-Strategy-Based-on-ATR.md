> Strategy Arguments



|Argument|Default|Description|
|---|---|---|
|v_input_1|timestamp(01 Apr 2000 13:30 +0000)|Backtest Start Time|
|v_input_2|14|(?Stop loss)Length of ATR for trailing stop loss|
|v_input_3|2|ATR Multiplier for trailing stop loss|
|v_input_4|14|(?Hypothesis testing)Length of ATR (fast) for diversion test|
|v_input_5|28|Length of ATR (slow) for diversion test|
|v_input_float_1|1.645|Reliability factor|
|v_input_6|14|(?Trend prediction)Length of drift|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-10-16 00:00:00
end: 2023-10-16 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © DojiEmoji

//@version=5
strategy("Mean Reversion (ATR) Strategy v2 [KL]", overlay=true, pyramiding=1)
var string ENUM_LONG = "Long"
var string GROUP_TEST = "Hypothesis testing"
var string GROUP_TSL = "Stop loss"
var string GROUP_TREND = "Trend prediction"

backtest_timeframe_start = input(defval=timestamp("01 Apr 2000 13:30 +0000"), title="Backtest Start Time")
within_timeframe = true

// TSL: calculate the stop loss price. {
ATR_TSL      = ta.atr(input(14, title="Length of ATR for trailing stop loss", group=GROUP_TSL)) * input(2.0, title="ATR Multiplier for trailing stop loss", group=GROUP_TSL)
TSL_source   = low
TSL_line_color  = color.green
TSL_transp      = 100
var float stop_loss_price = 0

if strategy.position_size == 0 or not within_timeframe
    TSL_line_color := color.black
    stop_loss_price := TSL_source - ATR_TSL
else if strategy.position_size > 0
    stop_loss_price := math.max(stop_loss_price, TSL_source - ATR_TSL)
    TSL_transp := 0

plot(stop_loss_price, color=color.new(TSL_line_color, TSL_transp))
// } end of "TSL" block

// Entry variables {
// ATR diversion test via Hypothesis testing (2-tailed):
//     H0 : atr_fast equals atr_slow
//     Ha : reject H0 if z_stat is above critical value, say reliability factor of 1.96 for a 95% confidence interval
len_fast    = input(14, title="Length of ATR (fast) for diversion test", group=GROUP_TEST)
atr_fast    = ta.atr(len_fast)
std_error   = ta.stdev(ta.tr, len_fast) / math.pow(len_fast, 0.5) // Standard Error (SE) = std / sq root(sample size)

atr_slow    = ta.atr(input(28, title="Length of ATR (slow) for diversion test", group=GROUP_TEST))
test_stat   = (atr_fast - atr_slow) / std_error
reject_H0   = math.abs(test_stat) > input.float(1.645)
if reject_H0 and strategy.position_size == 0
    strategy.entry("Long", strategy.long)
// } end of "Entry" block

// Trend prediction {
drift       = ta.sma(log(ta.close), input(14, title="Length of drift"))
bullish     = drift > ta.previous(drift)
if bullish and strategy.position_size == 0
    strategy.entry("Long", strategy.long)
// } end of "Trend Prediction" block

```