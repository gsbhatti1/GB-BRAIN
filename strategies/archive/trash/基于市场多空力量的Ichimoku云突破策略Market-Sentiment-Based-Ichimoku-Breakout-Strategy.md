> Name

Market-Sentiment-Based-Ichimoku-Breakout-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/11a0bb50187e9a54be7.png)
[trans]
## Overview

This is a trend-following strategy that integrates the configuration of the Ichimoku Cloud indicator to determine market sentiment and identify potential breakout opportunities. Key components include an Ichimoku Cloud-based trend filtering framework, ATR stop-loss, percentage stop-loss, and an optional profit-taking mechanism.

## Strategy Logic

There are two core components - Ichimoku Cloud signals to determine bullish/bearish momentum and strength burst signals to capture potential breakouts.

For trend signals, it requires the Conversion Line to cross above the Base Line to indicate an uptrend, the Lagging Span above the price bars indicating strong momentum, and the price breaking the Ichimoku Cloud's top band.

The strength burst signals for additional entry opportunities require the price breaking through Cloud's recent lows and highs for ultra strength and the Conversion Line and Base Line agreeing on bullish sentiment.

Long entries are triggered when either signal fires. Exits will trail stops based on ATR, percentage, or Ichimoku rules to lock in profits.

## Advantage Analysis

The biggest advantage comes from using the Ichimoku Cloud for both trend and momentum analysis, making signals more accurate than single indicators like moving averages. 

The risk management from ATR/percentage trailing stops also keeps loss per trade small. The optional profit-taking mechanism further enhances reward consistency.

## Risk Analysis

The primary risk comes from the lag in the Ichimoku Cloud itself. Additionally, strength signals also increase the risk of momentum chasing.

To address the lagging risk, optimize the Cloud's faster settings. For the momentum risk, tighter trailing stops can react more quickly to reversals.

## Optimization Directions

Possible improvements include:

1. Testing on more market data to assess robustness and adaptability.
2. Optimizing Ichimoku Cloud parameters to better fit specific market conditions.
3. Trying machine learning algorithms like LSTM to assist in signal rating.
4. Adding volume analysis to avoid the risk of buying into a trap.

## Conclusion

This Ichimoku system effectively gauges market sentiment for trend trading. The balanced focus on catching momentum and managing risk also makes it practical. Although there is room for improvement, it is overall a solid trend-following framework.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_string_1|0|(?Strategy settings)Trail Source: Lows/Highs|Close|Open|
|v_input_string_2|0|Trail Method: ATR|Percent|Ichi exit|
|v_input_float_1|10|Trail Percent|
|v_input_int_1|7|Lookback|
|v_input_int_2|14|ATR Period|
|v_input_float_2|true|ATR Multiplier|
|v_input_bool_1|false|Add Ichimoku exit|
|v_input_bool_2|false|Use Take Profit|
|v_input_float_3|5|Take Profit Percentage|
|v_input_int_3|9|(?Ichimoku settings)Conversion Line Length|
|v_input_int_4|26|Base Line Length|
|v_input_int_5|52|Leading Span B Length|
|v_input_int_6|26|Lagging Span|
|v_input_int_7|26|Delta|


> Source (PineScript)

```pinescript
/*backtest
start: 2024-01-04 00:00:00
end: 2024-02-03 00:00:00
period: 3h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © mikul_se
//@version=5
strategy("mikul's Ichimoku Cloud Strategy v 2.0", shorttitle="mikul's Ichi strat", overlay=true, margin_long=100, margin_short=100, default_qty_type = strategy.percent_of_equity, default_qty_value = 100)

// Strategy settings
strategySettingsGroup = "Strategy settings"
trailSource         = input.string(title="Trail Source", defval="Lows/Highs", options=["Lows/Highs", "Close", "Open"], confirm=true, group=strategySettingsGroup)
trailMethod         = input.string(title="Trail Method", defval="ATR", options=["ATR", "Percent", "Ichi exit"], confirm=true, tooltip="Ichi rules means it follows the rules of the Ichimoku cloud for exiting the trade.", group=strategySettingsGroup)
trailPercent        = input.float(title="Trail Percent", defval=10, minval=0.1, confirm=true, group=strategySettingsGroup)
swingLookback       = input.int(title="Lookback", defval=7, confirm=true, group=strategySettingsGroup)
atrPeriod           = input.int(title="ATR Period", defval=14, confirm=true, group=strategySettingsGroup)
atrMultiplier       = input.float(title="ATR Multiplier", defval=1.0, confirm=true, group=strategySettingsGroup)
addIchiExit         = input.bool(false, "Add Ichimoku exit", "You can use this to add Ichimoku cloud exit signals on top of Percent or ATR", group=strategySettingsGroup)
useTakeProfit       = input.bool(false, "Use Take Profit", confirm=true, group=strategySettingsGroup)
takeProfitPercent   = input.float(title="Take Profit Percentage", defval=5, minval=0.1, confirm=true, group=strategySettingsGroup)

// Ichimoku settings
ichimokuSettingsGroup = "Ichimoku settings"
conversionPeriods       = input.int(9, minval=1, title="Conversion Line Length", group=ichimokuSettingsGroup)
basePeriods             = input.int(26, minval=1, title="Base Line Length", group=ichimokuSettingsGroup)
leadingSpanBPeriods     = input.int(52, minval=1, title="Leading Span B Length", group=ichimokuSettingsGroup)
laggingSpan             = input.int(26, minval=1, title="Lagging Span", group=ichimokuSettingsGroup)
delta                   = input.int(26, minval=1, title="Delta", group=ichimokuSettingsGroup)
```