> Name

The-Dual-RSI-Mean-Reversion-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1c7f9b7ce76020d8ea6.png)
[trans]
## Overview

The Dual RSI Mean Reversion Strategy is a trend following strategy that identifies overbought and oversold conditions using two RSI indicators on different timeframes. It aims to capitalize on mean reversion by going long after oversold conditions and going short after overbought conditions. The strategy uses Heikin-Ashi candles, RSI indicators and an open color filter to identify trading opportunities.

## Strategy Logic

The strategy uses two RSI indicators with different periods - one on the 5 minute chart and one on the 1 hour chart. For the RSI indicators, oversold levels are identified below 30 and overbought levels above 70.

It tracks RSI values and looks for situations where the RSI has been below 30 or above 70 for a defined number of bars, indicating extended oversold or overbought conditions.

In addition, it uses Heikin-Ashi candles and checks for a defined number of green or red candles to confirm the trend direction before entering trades. An open color filter helps avoid false signals.

When both RSI and Heikin-Ashi conditions align, the strategy will go long after oversold conditions or go short after overbought conditions, betting on a reversion to the mean.

Positions are closed out at the end of each day to avoid holding trades overnight.

## Advantages

- Uses a multi-timeframe approach to identify overbought/oversold conditions
- Heikin-Ashi candles filter out noise and identify trend direction
- Open color filter avoids false signals
- Clear entry/exit rules based on two indicators aligning
- Risk management by closing positions before end of each day

## Risks

- Whipsaws possible if strong trend persists after RSI overbought/oversold signal
- Market gaps can trigger stops
- Heikin-Ashi lag can delay trade entries and cause missed moves
- Closing positions at day end gives up potential gains of overnight holds

## Enhancements

- Add additional filters like volume or volatility to confirm signals
- Optimize RSI periods and overbought/oversold levels for instrument
- Consider dynamic position sizing based on volatility 
- Experiment with profit targets or trailing stops instead of end-of-day exits
- Test effectiveness on different instruments and adjust parameters

## Conclusion

The Dual RSI Mean Reversion strategy takes a rules-based approach to trading momentum. By combining two timeframes, overbought/oversold indicators, candlestick analysis and an entry filter, it aims to identify high probability mean reversion setups. Strict risk management and prudent position sizing help balance profits with managing drawdowns. Further optimization and robustness testing would help deploy it successfully across various markets.

|||

## Summary

The Dual RSI Mean Reversion strategy is a trend-following approach that uses two RSI indicators on different timeframes to identify overbought and oversold conditions. By aligning the RSI and Heikin-Ashi conditions, the strategy goes long after oversold conditions and short after overbought conditions, betting on a reversion to the mean. Positions are closed at the end of each trading day.

## Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Long|
|v_input_2|true|Short|
|v_input_3|100|Lot, %|
|v_input_4|14|RSI period|
|v_input_5|30|RSI limit|
|v_input_6|3|RSI signals|
|v_input_7|true|Use Open Color Filter|
|v_input_8|2|Open Color, Bars|
|v_input_9|true|Show indicator RSI|
|v_input_10|2018|From Year|
|v_input_11|2100|To Year|
|v_input_12|true|From Month|
|v_input_13|12|To Month|
|v_input_14|true|From Day|
|v_input_15|31|To Day|

## Source (PineScript)

```pinescript
/*backtest
start: 2023-09-01 00:00:00
end: 2023-09-30 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//Gidra
//2018

//@version=2
strategy(title = "Gidra's Vchain Strategy v0.1", shorttitle = "Gidra's Vchain Strategy v0.1", overlay = false, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, pyramiding = 100)

//Settings
needlong = input(true, defval = true, title = "Long")
needshort = input(true, defval = true, title = "Short")
capital = input(100, defval = 100, minval = 1, maxval = 10000, title = "Lot, %")
rsiperiod = input(14, defval = 14, minval = 2, maxval = 100, title = "RSI period")
rsilimit = input(30, defval = 30, minval = 1, maxval = 50, title = "RSI limit")
rsibars = input(3, defval = 3, minval = 1, maxval = 20, title = "RSI signals")
useocf = input(true, defval = true, title = "Use Open Color Filter")
openbars = input(2, defval = 2, minval = 1, maxval = 20, title = "Open Color, Bars")
showrsi = input(true, defval = true, title = "Show indicator RSI")
fromyear = input(2018, defval = 2018, minval = 1900, maxval = 2100, title = "From Year")
toyear = input(2100, defval = 2100, minval = 1900, maxval = 2100, title = "To Year")
frommonth = input(01, defval = 01, minval = 01, maxval = 12, title = "From Month")
tomonth = input(12, defval = 12, minval = 01, maxval = 12, title = "To Month")
fromday = input(01, defval = 01, minval = 01, maxval = 31, title = "From Day")
today = input(31, defval = 31, minval = 01, maxval = 31, title = "To Day")


//Heikin Ashi Open/Close Price
o=open
c=close
h=high
l=low
haclose = (o+h+l+c)/4
haopen = na(haopen[1]) ? (o +