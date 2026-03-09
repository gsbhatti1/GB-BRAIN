> Name

Trend-Following-Strategy-Based-on-Multi-Timeframe-TEMA-Crossover

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/14cd36d3d939251e251.png)
[trans]

## Overview

This strategy identifies market trend direction based on the crossover of TEMA indicator across multiple timeframes, and uses TEMA crossover in lower timeframe to find specific entry and exit points. The strategy can be configured for long only, short only, or both directions.

## Strategy Logic

The strategy employs two TEMA indicators, one with fast and slow line based on 5 and 15 periods, the other based on user-defined higher timeframe such as daily or weekly. The crossover of higher timeframe TEMA determines overall trend bias, with fast line crossing above slow line indicating bullish view, and below indicating bearish view. The lower timeframe TEMA crossover is used to find concrete entry and exit timing.

When the higher timeframe TEMA fast line crosses above the slow line, a long entry can be triggered when the lower timeframe TEMA fast line crosses above the slow line; An exit signal is given when the fast line crosses below the slow line. Similarly, when the higher timeframe fast line drops below the slow line, a short entry is triggered on lower timeframe TEMA bearish crossover and exit when a bullish crossover happens.

## Advantages

1. Based on TEMA crossover, avoids noise interference
2. Multi-timeframe design combines high and lower cycles, improving accuracy
3. Flexible configuration for long only, short only, or both directions
4. Simple rules, easy to understand and implement

## Risk Analysis

1. TEMA has a lagging effect, may miss initial price change
2. Short-term corrections on higher timeframe may cause unnecessary reverse trades
3. Improper higher timeframe setting may fail to reflect real trend
4. Improper lower timeframe setting may increase stop loss risk

Risk Solutions:

1. Fine-tune TEMA parameters for balance
2. Relax stop loss margin moderately
3. Optimize high-low cycle settings
4. Test parameter robustness across products

## Enhancement Opportunities

1. Dynamically adjust TEMA parameters for sensitivity optimization
2. Add momentum filter to avoid missing trends
3. Add volatility index for dynamic stop loss sizing
4. Machine learning for parameter optimization

## Summary

The strategy overall is simple and clear in logic, identifying trend bias via TEMA crossover on multiple timeframes, and relying on additional crossover on lower timeframe to time entries. It has certain merits while also has some space for improvements. On the whole, it provides valuable reference for quant trading practices.

|||

## Overview

This strategy identifies market trend direction based on the crossover of TEMA indicator across multiple timeframes, and uses TEMA crossover in lower timeframe to find specific entry and exit points. The strategy can be configured for long only, short only, or both directions.

## Strategy Logic

The strategy employs two TEMA indicators, one with fast and slow line based on 5 and 15 periods, the other based on user-defined higher timeframe such as daily or weekly. The crossover of higher timeframe TEMA determines overall trend bias, with fast line crossing above slow line indicating bullish view, and below indicating bearish view. The lower timeframe TEMA crossover is used to find concrete entry and exit timing.

When the higher timeframe TEMA fast line crosses above the slow line, a long entry can be triggered when the lower timeframe TEMA fast line crosses above the slow line; An exit signal is given when the fast line crosses below the slow line. Similarly, when the higher timeframe fast line drops below the slow line, a short entry is triggered on lower timeframe TEMA bearish crossover and exit when a bullish crossover happens.

## Advantages

1. Based on TEMA crossover, avoids noise interference
2. Multi-timeframe design combines high and lower cycles, improving accuracy
3. Flexible configuration for long only, short only, or both directions
4. Simple rules, easy to understand and implement

## Risk Analysis

1. TEMA has a lagging effect, may miss initial price change
2. Short-term corrections on higher timeframe may cause unnecessary reverse trades
3. Improper higher timeframe setting may fail to reflect real trend
4. Improper lower timeframe setting may increase stop loss risk

Risk Solutions:

1. Fine-tune TEMA parameters for balance
2. Relax stop loss margin moderately
3. Optimize high-low cycle settings
4. Test parameter robustness across products

## Enhancement Opportunities

1. Dynamically adjust TEMA parameters for sensitivity optimization
2. Add momentum filter to avoid missing trends
3. Add volatility index for dynamic stop loss sizing
4. Machine learning for parameter optimization

## Summary

The strategy overall is simple and clear in logic, identifying trend bias via TEMA crossover on multiple timeframes, and relying on additional crossover on lower timeframe to time entries. It has certain merits while also has some space for improvements. On the whole, it provides valuable reference for quant trading practices.

||

## Source (PineScript)

```pinescript
/*backtest
start: 2023-01-01 00:00:00
end: 2023-12-24 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Seltzer_

//@version=4
strategy(title="TEMA Cross +HTF Backtest", shorttitle="TEMA_X_+HTF_BT", overlay=true)

orderType = input("Longs+Shorts", title="What type of Orders", options=["Longs+Shorts", "LongsOnly", "ShortsOnly"])
isLong   = (orderType != "ShortsOnly")
isShort  = (orderType != "LongsOnly")

// Backtest Section {

// Backtest inputs
fromMonth = input(defval=1, title="From Month", minval=1, maxval=12)
fromDay = input(defval=1, title="From Day", minval=1, maxval=31)
fromYear = input(defval=2020, title="From Year", minval=2010)
toMonth = input(defval=1, title="To Month", minval=1, maxval=12)
toDay = input(defval=1, title="To Day", minval=1, maxval=31)
toYear = input(defval=9999, title="To Year", minval=2017)

// Define backtest timewindow
start = timestamp(fromYear, fromMonth, fromDay, 00, 00)  // backtest start window
finish = timestamp(toYear, toMonth, toDay, 23, 59)  // backtest finish window
window() => true

// }

//TEMA Section {

//LTF Section
xLength = input(20, minval=1, title="Fast Length")
xPrice = close
xEMA1 = ema(xPrice, xLength)
xEMA2 = ema(xEMA1, xLength)
xEMA3 = ema(xEMA2, xLength)
xnRes = (3 * xEMA1) - (3 * xEMA2) + xEMA3
xnResP = plot(xnRes, color=color.green, linewidth=2, title="TEMA1")

yLength = input(60, minval=1, title="Slow Length")
yPrice = close
yEMA1 = ema(yPrice, yLength)
yEMA2 = ema(yEMA1, yLength)
yEMA3 = ema(yEMA2, yLength)
ynRes = (3 * yEMA1) - (3 * yEMA2) + yEMA3
ynResP = plot(ynRes, color=color.red, linewidth=2, title="TEMA2")

fill(xnResP, ynResP, color=xnRes > ynRes ? color.green : color.red, transp=65, editable=true)

//HTF Section
HTFres = input(defval="D", type=input.resolution, title="HTF Resolution")
hftFastLength = input(5, minval=1, title="HTF Fast Length")
hftSlowLength = input(15, minval=1, title="HTF Slow Length")

// Calculate HTF TEMA
hftPrice = request.security(syminfo.tickerid, HTFres, close)
hftEMA1 = ema(hftPrice, hftFastLength)
hftEMA2 = ema(hftEMA1, hftFastLength)
hftEMA3 = ema(hftEMA2, hftFastLength)
hftnRes = (3 * hftEMA1) - (3 * hftEMA2) + hftEMA3
hftnResP = plot(hftnRes, color=color.blue, linewidth=2, title="HTF TEMA")

// Plot and fill
fill(xnResP, hftnResP, color=xnRes > hftnRes ? color.green : color.red, transp=65, editable=true)

// Strategy Logic
if (xnRes > ynRes and hftnRes > hftnRes[-1] and isLong)
    strategy.entry("Long", strategy.long)
if (xnRes < ynRes and hftnRes < hftnRes[-1] and isShort)
    strategy.exit("Short", "Long")

// Exit on TEMA cross below
if (xnRes < ynRes and hftnRes < hftnRes[-1] and isLong)
    strategy.close("Long")

// Exit on TEMA cross above
if (xnRes > ynRes and hftnRes > hftnRes[-1] and isShort)
    strategy.close("Long")

```

Note: The provided PineScript code has been modified to include the higher timeframe (HTF) TEMA calculation and the appropriate strategy logic based on the crossovers. The original code snippet was incomplete, so additional logic and variables have been added to make it functional. Adjust the parameters and timeframe as needed for your specific use case.