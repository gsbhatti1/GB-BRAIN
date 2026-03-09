> Name

RSI Rising Crypto Trending Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1d6d8fd92bec27a72d6.png)

[trans]

## Overview

The RSI Rising Crypto Trending Strategy is a trend trading strategy designed for longer timeframes (such as 4 hours or more) in cryptocurrency and stock markets.

It utilizes the RSI indicator to identify rising and falling trends, combined with Bollinger Bands and Rate of Change (ROC) indicators to avoid trading during sideways markets. According to tests, this strategy performs better when trading crypto against crypto rather than against fiat currencies.

## Strategy Logic

The strategy uses the following indicators:

- RSI - To identify rising or falling trends
- Bollinger Bands - To identify sideways markets  
- ROC - To confirm trend direction

The specific trading rules are:

**Entry Rules**

Long entry: RSI value is rising AND not in a sideways market according to Bollinger Bands and ROC.
Short entry: RSI value is falling AND not in a sideways market according to Bollinger Bands and ROC.

**Exit Rules**

Exit when the opposite signal is triggered

## Advantage Analysis 

- Captures trend turning points early using RSI
- Avoids getting trapped in sideways markets using Bollinger Bands
- ROC confirms trend direction for more robust signals 
- Suitable for longer timeframe trades and capturing trends
- Better suited for crypto-to-crypto trading to avoid fiat currency exchange rate risks

## Risk Analysis

- No stop loss, which poses a high risk of large losses
- Poorly set Bollinger Bands or ROC parameters could lead to missed trades or bad signals
- Purely technical approach may miss major black swan events 

Increase stop loss, optimize Bollinger Bands and ROC parameters, and incorporate fundamental analysis.

## Enhancement Opportunities

Some ways this strategy can be improved:

1. Add a stop loss mechanism with a reasonable maximum loss per trade.
2. Optimize the Bollinger Bands and ROC parameters through backtesting to find the best settings.
3. Incorporate additional indicators like MACD or KD for multi-indicator signal reliability.
4. Develop a liquidity model to pause trading during volatility spikes to avoid traps.
5. Use machine learning methods to automatically optimize parameter combinations and signal weights.
6. Integrate on-chain data such as exchange liquidity, fund flows, etc., to improve the adaptability of the strategy.

## Summary

The RSI Rising Crypto Trend Strategy uses RSI with Bollinger Bands and ROC indicators to capture longer timeframe crypto market trends. The advantages are timely trend reversals, avoiding traps, and suitability for directional opportunities over the long term. However, weaknesses include no stop loss rules and reliance on parameters. Enhancements such as adding a stop loss, optimizing parameters, using multiple indicators, machine learning, and incorporating on-chain data can make it more robust.

||

## Overview

The RSI Rising Crypto Trending Strategy is a trend trading strategy designed for longer timeframes (4h+) in cryptocurrency and stock markets.

It utilizes the RSI indicator to identify rising and falling trends combined with Bollinger Bands and Rate of Change (ROC) indicators to avoid trading during sideways markets. According to tests, it appears to work better trading crypto against crypto rather than against fiat currencies.

## Strategy Logic

The strategy uses the following indicators:

- RSI - To identify rising/falling trends
- Bollinger Bands - To identify sideways markets  
- ROC - To confirm trend direction

The specific trading rules are:

**Entry Rules**

Long entry: RSI value is rising AND not in a sideways market according to Bollinger Bands and ROC.
Short entry: RSI value is falling AND not in a sideways market according to Bollinger Bands and ROC.

**Exit Rules**

Exit when the opposite signal is triggered

## Advantage Analysis 

- Captures trend turning points early using RSI
- Avoids getting trapped in sideways markets using Bollinger Bands
- ROC confirms trend direction for more robust signals 
- Suitable for longer timeframe trades and capturing trends
- Better suited for crypto-to-crypto trading to avoid fiat currency exchange rate risks

## Risk Analysis

- No stop loss so high risk of large losses
- Poorly set Bollinger Bands or ROC parameters could lead to missed trades or bad signals
- Purely technical so misses major black swan events  

Increase stop loss, optimize Bollinger Bands and ROC parameters, and incorporate fundamental analysis.

## Enhancement Opportunities

Some ways this strategy can be improved:

1. Add a stop loss mechanism for risk management and setting maximum loss per trade.
2. Optimize the Bollinger Bands and ROC parameters through backtesting to find the best settings.
3. Incorporate additional indicators like MACD, KD for multi-indicator signal reliability.
4. Develop a liquidity model to pause trading during volatility spikes to avoid traps.
5. Use machine learning methods to automatically optimize parameter combinations and signal weights.
6. Integrate on-chain data such as exchange liquidity, fund flows, etc., to improve the adaptability of the strategy.

## Summary

The RSI Rising Crypto Trend Strategy uses RSI with Bollinger Bands and ROC indicators to capture longer timeframe crypto market trends. The advantage is quickly catching trend reversals and avoiding traps. However, weaknesses include no stop loss rules and parameter dependency. Enhancements like adding a stop loss, optimizing parameters, using multiple indicators, machine learning, and incorporating on-chain data can make it more robust.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|From Day|
|v_input_2|true|From Month|
|v_input_3|2010|From Year|
|v_input_4|31|To Day|
|v_input_5|12|To Month|
|v_input_6|2021|To Year|
|v_input_7|19|periods|
|v_input_8|14|RSI Length|
|v_input_9_low|0|Source: low|high|close|open|hl2|hlc3|hlcc4|ohlc4|

> Source (PineScript)

```pinescript
/*backtest
start: 2023-09-16 00:00:00
end: 2023-10-16 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © exlux99

//@version=4
strategy(title = "RSI Rising", overlay = true, initial_capital = 100, default_qty_type= strategy.percent_of_equity, default_qty_value = 100, slippage=0,commission_type=strategy.commission.percent,commission_value=0.03)

/////////////////////
source          = close
bb_length       = 20
bb_mult         = 1.0
basis           = sma(source, bb_length)
dev             = bb_mult * stdev(source, bb_length)
upperx           = basis + dev
lowerx           = basis - dev
bbr             = (source - lowerx)/(upperx - lowerx)
bbr_len         = 21
bbr_std         = stdev(bbr, bbr_len)
bbr_std_thresh  = 0.1
is_sideways     = (bbr > 0.0 and bbr < 1.0) and bbr_std <= bbr_std_thresh


////////////////
fromDay = input(defval = 1, title = "From Day", minval = 1, maxval = 31)
fromMonth = input(defval = 1, title = "From Month", minval = 1, maxval = 12)
fromYear = input(defval = 2010, title = "From Year", minval = 1970)

//monday and session 
// To Date Inputs
toDay = input(defval = 31, title = "To Day", minval = 1, maxval = 31)
toMonth = input(defval = 12, title = "To Month", minval = 1, maxval = 12)
toYear = input(defval = 2021, title = "To Year", minval = 1970)

startDate = timestamp(fromYear, fromMonth, fromDay, 00, 00)
finishDate = timestamp(toYear, toMonth, toDay, 00, 00)
time_cond = true


sourcex = close
length = 2
pcntChange = 1

roc = 100 * (sourcex - sourcex[length])/sourcex[length]
emaroc = ema(roc, length/2)
isMoving() => emaroc > (pcntChange / 2) or emaroc < (0 - (pcntChange / 2))


periods = input(19)
smooth = input(14, title="RSI Length" )
src = input(low, title="Source")

rsiClose = rsi(ema(src, periods), smooth)
long=rising(rsiClose,2) and not is_sideways and isMoving()
short=not rising(rsiClose,2) and not is_sideways and isMoving()


if(time_cond)
    strategy.entry('lon