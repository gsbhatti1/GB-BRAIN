> Name

MACD Indicator Cross-Period Trading Strategy MACD-Cross-Period-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

This strategy uses MACD on higher timeframes (e.g., daily) for trend bias and trades on lower timeframes (e.g., 5-min) for execution. The cross-period approach aims to improve the reliability of basic MACD strategies.

Strategy Logic:

1. Calculate MACD on a higher timeframe to determine overall trend direction.
2. Enter trades on a lower timeframe when MACD crosses the signal line.
3. Add MFI overbought/oversold signals for additional entry confirmation.
4. Use stop and take profit levels for risk management.
5. Optimize parameters for greater stability.

Advantages:

1. Cross-period analysis filters short-term noise.
2. MFI helps avoid false signals and improves accuracy.
3. Stop loss/take profit mechanisms control single trade risks.

Risks:

1. Cross-period operations lag, potentially missing best entries.
2. Both MACD and MFI can give false signals, require caution.
3. Strict risk management needed to offset whipsaw risks.

In summary, this approach uses cross-period MACD for trend bias and MFI for filtering, trading on lower timeframes for stability. But lag issues remain so prudent trading is still required.

||

This strategy uses MACD on higher timeframes (e.g., daily) for trend bias and trades on lower timeframes (e.g., 5-min) for execution. The cross-period approach aims to improve the reliability of basic MACD strategies.

Strategy Logic:

1. Calculate MACD on a higher timeframe for overall trend direction.
2. Enter trades on a lower timeframe when MACD crosses the signal line.
3. Add MFI overbought/oversold signals for additional entry confirmation.
4. Use stop and take profit levels for risk management.
5. Optimize parameters for greater stability.

Advantages:

1. Cross-period analysis filters short-term noise.
2. MFI helps avoid false signals and improves accuracy.
3. Stop loss/take profit mechanisms control single trade risks.

Risks:

1. Cross-period operations lag, potentially missing best entries.
2. Both MACD and MFI can give false signals, require caution.
3. Strict risk management needed to offset whipsaw risks.

In summary, this approach uses cross-period MACD for trend bias and MFI for filtering, trading on lower timeframes for stability. But lag issues remain so prudent trading is still required.

---

> Strategy Arguments

|Argument|Default|Description|
|---|---|---|
|v_input_14|true|Highlight Oversold/Overbought?|
|v_input_18|8|Fixed SL (%)|
|v_input_25|false|Min ATR|
|v_input_1|5|(?Strategy)Resolution|
|v_input_2|19|Period|
|v_input_3||Open Long Comment|
|v_input_4||Close Long Comment|
|v_input_5|7|(?MACD)Fast Length|
|v_input_6|23|Slow Length|
|v_input_7|10|Signal Smoothing|
|v_input_8_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_9|false|Simple MA(Oscillator)|
|v_input_10|false|Simple MA(Signal Line)|
|v_input_11|15|(?MFI)length|
|v_input_12|12|lower|
|v_input_13|80|upper|
|v_input_15|true|(?Trailing Profit)Enable Trailing|
|v_input_16|4|Long TP (%)|
|v_input_17|0.5|TTP Dev %%|
|v_input_19|false|(?Filters)Show Data|
|v_input_20|false|Use Trend|
|v_input_21|3|Trend EMA|
|v_input_22|false|Use RSI|
|v_input_23|34|RSI Length|
|v_input_24|50|Buy Below RSI Filter|
|v_input_26|2018|(?Backtest)Fr Year|
|v_input_27|true|Fr Month|
|v_input_28|true|Fr Day|
|v_input_29|9999|To Year|
|v_input_30|12|To Month|
|v_input_31|31|To Day|

---

> Source (PineScript)

```pinescript
//@version=4
strategy("Customizable HTF MACD Strategy v1.5", overlay=false, pyramiding=0, commission_type=strategy.commission.percent, commission_value=0.08, default_qty_type = strategy.percent_of_account)

// (c) Wunderbit Trading
// Modified by Mauricio Zuniga - Trade at your own risk
// This script was originally shared on the Wunderbit website as a free open source script for the community.
//
// WHAT THIS SCRIPT DOES:
//   This is a scalping script originally intended to be used on altorightmic bot trading.
//   This strategy is based on the trend-following momentum indicator. It includes the Money Flow index as an additional point for entry.
//
// HOW IT DOES IT:
//   It uses a combination of MACD and MFI indicators to create entry signals.  Parameters for each indicator have been surfaced for user configurability.
//   Take profits are fixed, but stop loss uses ATR configuration to minimize losses and close profitably.
//
// HOW IS MY VERSION ORIGINAL:
//   I started trying to deploy this script myself in my algorithmic trading but ran into some issues which I have tried to address in this version.
//   Delayed Signals: The script has been refactored to use a time frame drop down.  The higher time frame can be run on a faster chart (recommended on one minute chart for fastest signal confirmation and relay to algotrading platform).
//   Repainting Issues: All indicators have been recoded to use the security function that checks to see if the current calculation is in realtime, if it is, then it uses the previous bar for calculation.
//   If you are still experiencing repainting issues based on intended (or non-intended use), please provide a report with screenshot and explanation so I can try to address.
//   Filtering:  I have added to additional filters an ABOVE EMA Filter and a BELOW RSI Filter (both can be turned on and off)
//   Customizable Long and Close Messages: This allows someone to use the script for algorithmic trading without having to alter code. It also means you can use one indicator for all of your different alerts required for your bots.
//
// HOW TO USE IT:
//   Find a pair with high volatility - I have found it works particularly well with 3L and 3S tokens for crypto although the limitation is that configurations I have found to work typically have low R/R ratio, but very high win rate and profit factor.
//   Ideally set one minute chart for bots, but you can use other charts for manual trading. The signal will be delayed by one bar but I have found configurations that still test well.
//   Select a time frame in configuration for your indicator calculations.
//   I like to use 5 and 15 minutes for scalping scenarios, but I am interested in hearing back from other community members.
//   Optimize your indicator without filters (trendFilter and RSI Filter)
//   Use the TrendFilter and RSI Filter to further refine your signals for entry.

var float maOsc = na
if (v_input_9 == true)
    maOsc := ta.sma(close, v_input_5)

var float maSig = na
if (v_input_10 == true)
    maSig := ta.sma(macdline, v_input_7)

var float mfiVal = na
mfiVal := ta.mfi(v_input_11, v_input_12, v_input_13)

longCondition = ta.crossover(macdline, signal_line) and (mfiVal > 80 or v_input_9 == false)
if longCondition
    strategy.entry("Long", strategy.long)
    
shortCondition = ta.crossunder(macdline, signal_line) and (mfiVal < 20 or v_input_10 == false)
if shortCondition
    strategy.entry("Short", strategy.short)

var float takeProfitLevel = na
takeProfitLevel := v_input_16 / 100 * close

var float stopLossLevel = na
stopLossLevel := ta.atr(14) * v_input_18 / 100

if (v_input_15 == true)
    strategy.exit("Long Exit", "Long", limit=takeProfitLevel, stop=stopLossLevel)
else
    strategy.close("Long", when=(strategy.position_avg_price + takeProfitLevel < close and strategy.position_avg_price - stopLossLevel > close))
    
if (v_input_15 == true)
    strategy.exit("Short Exit", "Short", limit=takeProfitLevel, stop=stopLossLevel)
else
    strategy.close("Short", when=(strategy.position_avg_price - takeProfitLevel > close and strategy.position_avg_price + stopLossLevel < close))

// Additional Filters
var float emaFilter = na
if (v_input_20 == true)
    emaFilter := ta.ema(close, v_input_21)

var float rsiFilter = na
if (v_input_22 == true)
    rsiFilter := ta.rsi(close, v_input_23) > v_input_24

// Customizable Long and Close Messages
strategy.comment(v_input_3)
strategy.close("Long", comment=v_input_4)

```

This script is designed to be customized for various trading scenarios and provides a flexible approach to leveraging MACD and MFI indicators in conjunction with stop and take profit levels.