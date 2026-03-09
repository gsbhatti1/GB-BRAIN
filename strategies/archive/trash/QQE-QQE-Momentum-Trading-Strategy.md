> Name

QQE-Momentum-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/ec0249404e7f6a45c2.png)
 [trans]

## Overview

This strategy is a momentum trading strategy based on the QQE (Qualitative Quantitative Estimation) indicator. It uses the QQE indicator to identify opportunities in stock prices and moving averages to filter out false signals.

## Strategy Logic

The strategy uses 3 types of QQE indicator crosses to identify buy/sell opportunities:

1. QQE curve crossing 0 axis (XZ): Early signal of price reversal when overbought/oversold.
2. QQE curve crossing fast QQE line (XQ): Opportunity for short-term price adjustment.
3. QQE curve exiting RSI channel (XC): Opportunity for mid-term price adjustment.

When a buy/sell signal is identified, the strategy also checks the moving average indicator as an additional filter to avoid wrong trades in non-trending situations:

1. Fast MA above medium MA, and medium MA above slow MA.
2. Medium MA direction upward (for long signals) or downward (for short signals).

## Advantages

The strategy combines QQE for opportunity identification and moving averages for signal quality improvement, with the following main advantages:

1. QQE crosses capture opportunities at different price reversal levels.
2. Moving averages effectively filter out false breaks.
3. Flexible parameters suit different products and timeframes.
4. QQE crosses can be used alone or combined with other filters.

## Risks

The main risks of the strategy include:

1. More false signals may occur in ranging markets.
2. Moving averages as lagging indicators may filter some valid signals.
3. Improper parameter tuning leads to extended drawdown or missed opportunities.
4. Appropriate stop loss/profit taking mechanism required to limit per trade losses.

## Enhancements

The strategy can be enhanced from the following aspects:

1. Tune QQE parameters to suit securities of different volatility levels.
2. Optimize moving average parameters for better filtering performance.
3. Add other filters, such as volume filter.
4. Introduce stop loss and take profit mechanisms to control trade risk.
5. Evaluate actual trading results and fine-tune key parameters.

## Summary

The strategy integrates QQE signal identification with moving average directional filtering into a quality momentum trading system. It is adaptable through configurable parameters for differentiated needs. With proper stop loss/profit taking, steady returns can be expected.

||

## Overview

This strategy is a momentum trading strategy based on the QQE (Qualitative Quantitative Estimation) indicator. It uses the QQE indicator to identify opportunities in stock prices and moving averages to filter out false signals.

## Strategy Logic  

The strategy uses 3 types of QQE indicator crosses to identify buy/sell opportunities:  

1. QQE curve crossing 0 axis (XZ): Early signal of price reversal when overbought/oversold.

2. QQE curve crossing fast QQE line (XQ): Opportunity for short-term price adjustment.

3. QQE curve exiting RSI channel (XC): Opportunity for mid-term price adjustment.

When a buy/sell signal is identified, the strategy also checks the moving average indicator as an additional filter to avoid wrong trades in non-trending situations:

1. Fast MA above medium MA, and medium MA above slow MA.

2. Medium MA direction upward (for long signals) or downward (for short signals).

## Advantages

The strategy combines QQE for opportunity identification and moving averages for signal quality improvement, with the following main advantages:

1. QQE crosses capture opportunities at different price reversal levels.
2. Moving averages effectively filter out false breaks.
3. Flexible parameters suit different products and timeframes.
4. QQE crosses can be used alone or combined with other filters.

## Risks

The main risks of the strategy include:

1. More false signals may occur in ranging markets.
2. Moving averages as lagging indicators may filter some valid signals.
3. Improper parameter tuning leads to extended drawdown or missed opportunities.
4. Appropriate stop loss/profit taking mechanism required to limit per trade losses.

## Enhancements

The strategy can be enhanced from the following aspects:

1. Tune QQE parameters to suit securities of different volatility levels.
2. Optimize moving average parameters for better filtering performance.
3. Add other filters e.g. volume filter.
4. Introduce stop loss and take profit mechanisms to control trade risk.
5. Evaluate actual trading results and fine tune key parameters.

## Summary

The strategy integrates QQE signal identification with moving average directional filtering into a quality momentum trading system. It is adaptable through configurable parameters for differentiated needs. With proper stop loss/profit taking, steady returns can be expected.

||

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|4|Relative TimeFrame Multiplier for Second MA Ribbon (0=none, max=100)|
|v_input_2|true|Show Moving Average Lines|
|v_input_3|0|Fast MA Type: EMA|SMA|WMA|VWMA|SMMA|DEMA|TEMA|HullMA|ZEMA|TMA|SSMA|
|v_input_4|16|Fast - Length|
|v_input_5|0|Medium MA Type: EMA|SMA|WMA|VWMA|SMMA|DEMA|TEMA|HullMA|ZEMA|TMA|SSMA|
|v_input_6|21|Medium - Length|
|v_input_7|0|Slow MA Type: EMA|SMA|WMA|VWMA|SMMA|DEMA|TEMA|HullMA|ZEMA|TMA|SSMA|
|v_input_8|26|Slow Length|
|v_input_9|14|RSI Length|
|v_input_10|8|RSI Smoothing Factor|
|v_input_11|5|Fast QQE Factor|
|v_input_12|10|RSI Threshhold|
|v_input_13|true|Show QQE Signal crosses|
|v_input_14|false|Show QQE Zero crosses|
|v_input_15|true|Show QQE Thresh Hold Channel Exits|
|v_input_16|0|Select which QQE signal to Buy/Sell: XC|XQ|XZ|
|v_input_17|0|Select which QQE signal to Close Order: XQ|XC|XZ|
|v_input_18|true|Filter XQ Buy/Sell Orders by Threshold|
|v_input_19|false|Use Moving Average Filter|
|v_input_20|true|Use Trend Directional Filter|
|v_input_21|false|Only Alert First Buy/Sell in a new Trend|
|v_input_22_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_23|2018|Backtest Start Year|
|v_input_24|6|Backtest Start Month|
|v_input_25|12|Backtest Start Day|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-01-15 00:00:00
end: 2024-01-21 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
//

//*** START of COMMENT OUT [Alerts]
strategy(title="Momentum Trading By Mahfuz Azim", shorttitle="Momentum Trading v1.6 By Mahfuz Azim", overlay=true)
//*** END of COMMENT OUT [Alerts]
//<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<//

//>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>//
//*** START of COMMENT OUT [BackTest]
//study(title="[Alerts]QQE Cross v6.0 by Mahfuz Azim", shorttitle="[AL]QQEX v6.0", overlay=true,max_bars_back=2000)
//*** END of COMMENT OUT [BackTest]

//
// Author:  ChaoZhang
// Date:    15-January-2023
// Version: v 1.6, Major Release January-2023
//
// Description:
// A momentum trading strategy based on QQE (Qualitative Quantitative Estimation) indicator that uses fast QQE crosses with Moving Averages for trend direction filtering. QQE is based on the relative strength index (RSI), but uses a smoothing technique as an additional transform.
```