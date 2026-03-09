> Name

Ichimoku-Early-Cloud-Trend-Following-Strategy-一云双提前知机会均线趋势跟踪策略

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/13e48f7c4135f2fe6ce.png)
[trans]

## Overview

The Ichimoku Early Cloud Trend Following Strategy is a trend-following strategy based on the popular Ichimoku Cloud indicator. It utilizes the crossover lines of the Ichimoku Cloud to generate early entry signals and capture trends ahead of time. The strategy also incorporates moving averages for trend validation to avoid false breakouts.

## Strategy Logic

The strategy is mainly based on the following elements:

1. Construct the Ichimoku Cloud using the Conversion Line and Base Line, and plot the cloud with a 26-period displacement.
2. Trigger a long signal when close breaks above the top of the cloud; trigger a short signal when close breaks below the bottom of the cloud.
3. Require close to also break the max/min of the Conversion and Base Lines to filter out false breakouts.
4. Optionally set a 5% stop loss based on entry price.

With such multilayer filtering, it can effectively identify trend reversal points and capture emerging trading opportunities in a timely manner. The strict breakout criteria also help reduce false signals.

## Advantages

The strategy has the following advantages:

1. Ichimoku Cloud crossover lines have clear early indication before trend reversal.
2. Incorporating moving averages avoids false breakout due to overnight gaps.
3. Multiple filter conditions reduce false signals and improve signal quality.
4. Long holding periods result in smaller drawdowns and easier profit taking.
5. Applicable to different products, especially trending instruments.

## Risks

There are also some risks to consider:

1. Works better for trending markets; may generate more false signals during range-bound periods.
2. Ichimoku parameters need to be optimized for different products.
3. Stop loss placement requires caution to avoid premature exit.
4. Relatively low signal frequency, tends to miss short-term opportunities.

Risks can be reduced by:

1. Select strongly trending products, avoid ranging products.
2. Optimize Ichimoku parameters for different timeframes to find best combinations.
3. Employ trailing stop loss to control loss on single trades.
4. Add other indicators to increase signal frequency.

## Enhancements

The strategy can be further improved on the following aspects:

1. Add position sizing to control amount traded programmatically via `strategy.position_size`.
2. Add security universe filtering to auto detect trend strength via `security()`.
3. Incorporate stop loss/profit taking techniques for risk management.
4. Build multi-indicator system combining indicators like Bollinger Bands and RSI to improve signal quality.
5. Apply machine learning to judge signal reliability and dynamically adjust order quantities.

## Conclusion

The Ichimoku Early Cloud Trend Following Strategy utilizes Ichimoku Cloud for early trend identification, reinforced by moving average filters, to reliably detect high-quality trading opportunities. The strategy is stable with much room for enhancements and can be widely adopted for live trading.

||

## Overview

The Ichimoku Early Cloud Trend Following Strategy is a trend-following strategy based on the popular Ichimoku Cloud indicator. It utilizes the crossover lines of the Ichimoku Cloud to generate early entry signals and capture trends ahead of time. The strategy also incorporates moving averages for trend validation to avoid false breakouts.

## Strategy Logic

The strategy is mainly based on the following elements:

1. Construct the Ichimoku Cloud using the Conversion Line and Base Line, and plot the cloud with a 26-period displacement.
2. Trigger a long signal when close breaks above the top of the cloud; trigger a short signal when close breaks below the bottom of the cloud.
3. Require close to also break the max/min of the Conversion and Base Lines to filter out false breakouts.
4. Optionally set a 5% stop loss based on entry price.

With such multilayer filtering, it can effectively identify trend reversal points and capture emerging trading opportunities in a timely manner. The strict breakout criteria also help reduce false signals.

## Advantages

The strategy has the following advantages:

1. Ichimoku Cloud crossover lines have clear early indication before trend reversal.
2. Incorporating moving averages avoids false breakout due to overnight gaps.
3. Multiple filter conditions reduce false signals and improve signal quality.
4. Long holding periods result in smaller drawdowns and easier profit taking.
5. Applicable to different products, especially trending instruments.

## Risks

There are also some risks to consider:

1. Works better for trending markets; may generate more false signals during range-bound periods.
2. Ichimoku parameters need to be optimized for different products.
3. Stop loss placement requires caution to avoid premature exit.
4. Relatively low signal frequency, tends to miss short-term opportunities.

Risks can be reduced by:

1. Select strongly trending products, avoid ranging products.
2. Optimize Ichimoku parameters for different timeframes to find best combinations.
3. Employ trailing stop loss to control loss on single trades.
4. Add other indicators to increase signal frequency.

## Enhancements

The strategy can be further improved on the following aspects:

1. Add position sizing to control amount traded programmatically via `strategy.position_size`.
2. Add security universe filtering to auto detect trend strength via `security()`.
3. Incorporate stop loss/profit taking techniques for risk management.
4. Build multi-indicator system combining indicators like Bollinger Bands and RSI to improve signal quality.
5. Apply machine learning to judge signal reliability and dynamically adjust order quantities.

## Conclusion

The Ichimoku Early Cloud Trend Following Strategy utilizes Ichimoku Cloud for early trend identification, reinforced by moving average filters, to reliably detect high-quality trading opportunities. The strategy is stable with much room for enhancements and can be widely adopted for live trading.

||

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|9|Conversion Line Period|
|v_input_2|26|Base Line Period|
|v_input_3|52|Lagging Span 2 Period|
|v_input_4|26|Displacement|
|v_input_5|false|Long Only|
|v_input_6|5|Stop-loss (%)|
|v_input_7|false|Use Stop-Loss|


> Source (PineScript)

```pinescript
/*backtest
start: 2022-12-05 00:00:00
end: 2023-12-11 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © QuantCT

//@version=4
strategy("Ichimoku Cloud Strategy Idea",
         shorttitle="Ichimoku", 
         overlay=true,
         pyramiding=0,     
         default_qty_type=strategy.percent_of_equity, 
         default_qty_value=99, 
         initial_capital=1000,           
         commission_type=strategy.commission.percent, 
         commission_value=0.1)

// ____ Inputs

conversion_period = input(9, minval=1, title="Conversion Line Period")
base_period = input(26, minval=1, title="Base Line Period")
lagging_span2_period = input(52, minval=1, title="Lagging Span 2 Period")
displacement = input(26, minval=1, title="Displacement")
long_only = input(title="Long Only", defval=false)
slp = input(title="Stop-loss (%)", minval=1.0, maxval=25.0, defval=5.0)
use_sl = input(title="Use Stop-Loss", defval=false)

// ____ Logic

donchian(len) => avg(lowest(len), highest(len))

conversion_line = donchian(conversion_period)
base_line = donchian(base_period)
lead_line1 = avg(conversion_line, base_line)
lead_line2 = donchian(lagging_span2_period + displacement)

// Cloud boundaries
cloud_top = max(conversion_line, base_line) + lead_line2
cloud_bottom = min(conversion_line, base_line) - lead_line2

// Entry and Exit conditions
long_condition = close > cloud_top and close > highest(conversion_line, base_line)
short_condition = close < cloud_bottom and close < lowest(conversion_line, base_line)

if (long_only == false)
    if long_condition
        strategy.entry("Long", strategy.long)
    if short_condition
        strategy.close("Long")
else 
    if long_condition
        strategy.entry("Long", strategy.long)
    
stop_loss_level = na
if use_sl and not isnan(slp)
    stop_loss_level := slp / 100 * strategy.opentrades.price_avg

strategy.exit("Exit Long", "Long", stop=stop_loss_level)

// ____ Plotting
plot(conversion_line, color=color.blue)
plot(base_line, color=color.orange)
plot(lead_line1, color=color.red)
plot(lead_line2, color=color.green)
fill(area(conversion_line, base_line), color=color.gray)
```