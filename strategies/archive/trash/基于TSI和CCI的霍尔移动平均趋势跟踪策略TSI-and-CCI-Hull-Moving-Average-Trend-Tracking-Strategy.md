> Name

TSI-and-CCI-Hull-Moving-Average-Trend-Tracking-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1674aec3ecb384ea6f5.png)

[trans]

## Overview

This strategy integrates the Relative Strength Index (TSI), Commodity Channel Index (CCI), and Hull Moving Average (Hull MA) indicators to form a trend tracking trading strategy. It can perform long-term tracking trades on any trading variety in hourly or higher time frames.

## Strategy Principle

The strategy mainly uses the TSI and CCI indicators to judge the trend direction and overbought/oversold conditions of the market, as well as the Hull MA to determine the intermediate trend of prices, and the three are combined as the basic conditions for opening positions.

Specifically, when the fast line of TSI crosses above the slow line, and CCI indicator crosses above +20 && n1 rises, go long; when the fast line of TSI crosses below the slow line, and CCI indicator crosses below -20 && n1 falls, go short. Hull MA is used to filter the intermediate trend, only going long when the price is below Hull MA, and going short when the price is above Hull MA.

By confirming with indicators across different cycles, false breakouts can be effectively filtered to track medium- and long-term trends.

## Advantage Analysis

This is a relatively stable and efficient trend tracking strategy, with the following main advantages:

1. Using TSI to judge long-term trend directions is more reliable, avoiding interference from short-term market noise;
2. The addition of the CCI indicator can confirm overbought/oversold phenomena and filter out some false signals;
3. Hull MA’s judgment makes entry points more precise, greatly improving the probability of profit;
4. The integration of indicators with different parameters can improve the reliability of signals and reduce interference probability.
5. Flexible parameter settings of the strategy can be optimized for different market cycles.

## Risk Analysis

Although the strategy is relatively stable, there are still some risks to note:

1. The market may experience violent reversals that cannot be quickly stopped for loss, causing relatively large losses;
2. TSI Diff and CCI indicators may both have false signals and lags, missing some entry points;
3. Improper parameter settings can also lead to excessively high trading frequency or decline in signal quality.

Countermeasures:

1. Adjust stop loss appropriately to control single loss;
2. Confirm with other indicators as appropriate to improve signal accuracy;
3. Adjust parameters according to market to ensure strategy stability.

## Optimization Directions

The strategy can also be optimized in the following aspects:

1. Try different combinations of parameter indicators to find the best match;
2. Introduce machine learning algorithms to achieve adaptive optimization of parameters;
3. Increase capital management module for more stable profits;
4. Incorporate more filters to increase strategy win rate.

These will be the focuses for future optimizations.

## Summary

This strategy comprehensively utilizes the TSI, CCI, and Hull MA indicators to form a relatively stable and efficient trend tracking strategy. It successfully leverages the advantages of multi-cycle indicators to improve signal quality. The next step will be to further enhance the stability and profitability of the strategy through parameter optimization, filter enhancement, and other means.

[/trans]

> Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|v_input_1|50|Long Length|
|v_input_2|50|Short Length|
|v_input_3|25|Signal Length|
|v_input_4_open|0|Source: open|high|low|close|hl2|hlc3|hlcc4|ohlc4|
|v_input_5|25|Period|
|v_input_6|100|Upper Line|
|v_input_7|-100|Lower Line|

> Source (PineScript)

```pinescript
//@version=4
strategy(title="TSI CCI Hull", shorttitle="TSICCIHULL", default_qty_type=strategy.percent_of_equity, default_qty_value=100, calc_on_order_fills=false, calc_on_every_tick=true, pyramiding=0)
long = input(title="Long Length", type=input.integer, defval=50)
short = input(title="Short Length", type=input.integer, defval=50)
signal = input(title="Signal Length", type=input.integer, defval=25)
price=input(title="Source",type=input.source,defval=open)
Period=input(25, minval=1)
lineupper = input(title="Upper Line", type=input.integer, defval=100)
linelower = input(title="Lower Line", type=input.integer, defval=-100)
p=price
length= Period
double_smooth(src, long, short) =>
    fist_smooth = ema(src, long)
    ema(fist_smooth, short)
pc = change(price)
double_smoothed_pc = double_smooth(pc, long, short)
double_smoothed_abs_pc = double_smooth(abs(pc),
```