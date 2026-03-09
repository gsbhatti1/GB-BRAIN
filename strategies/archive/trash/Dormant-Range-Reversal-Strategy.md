> Name

Dormant-Range-Reversal-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/cf919468e92a0dfb16.png)

[trans]

## Overview

The dormant range reversal strategy utilizes periods of decreasing volatility as entry signals and aims to profit when volatility picks up again. It identifies situations where price is contained within a narrow dormant range and captures the upcoming price trend. This strategy works well when current volatility is low but a breakout is expected.

## Strategy Logic

The strategy first identifies a dormant range, which is when price is contained within the price range of the previous trading day. This indicates that volatility has decreased compared to a few days ago. We check if the current day high < high of n days ago (typically 4 days) and the current day low > low of n days ago to qualify as a dormant range.

Once a dormant range is identified, the strategy places two pending orders - a buy stop near the top of the range and a sell stop near the bottom of the range. It then waits for price to breakout of the range either upwards or downwards. If price breaks upwards, the buy order is triggered to go long. If price breaks downwards, the sell order is triggered to go short.

After entry, stop loss and take profit orders are placed. The stop loss controls downside risk and the take profit closes the trade for profit. The stop loss is placed at a % distance from entry price as defined in risk parameters. The take profit is placed at a distance equal to the dormant range size since we expect price to move similar to previous volatility.

Finally, a fixed fractional position sizing model manages trade size. It increases size for profits and reduces size for losses to improve risk-adjusted returns.

## Advantages

The advantages of this strategy are:

1. Captures upcoming trend by using decreased volatility as signal.
2. Dual-directional orders catch uptrend or downtrend.
3. Stop loss and take profit controls single trade risk.
4. Fixed fractional sizing improves capital efficiency.
5. Simple logic easy to implement.

## Risks

The risks to consider are:

1. Wrong breakout direction if range breakout is unclear.
2. Breakout may just be short reversal, not lasting trend.
3. Stop loss risk of being taken out by huge moves.
4. Fixed fraction sizing may amplify losses when adding to losing trades.
5. Poor performance if parameters not properly set.

## Enhancement Opportunities

Some ways to enhance the strategy are:

1. Add filters like divergence to avoid false breakouts.
2. Improve stop loss with trailing or order stop losses.
3. Add trend filter to avoid counter-trend entries.
4. Optimize fixed fraction ratios for balanced risk/reward.
5. Look at multiple timeframes to improve edge.
6. Utilize machine learning for automated parameter optimization.

## Conclusion

The dormant range reversal strategy has a clear logic and profit potential. Fine-tuning via optimizations, risk management, and signal filtering can further improve consistency. But all mean reversion strategies carry inherent risks and position sizing needs to be controlled. It suits traders familiar with reversal tactics and possessing sound risk awareness.

||


## Overview

The dormant range reversal strategy utilizes periods of decreasing volatility as entry signals and aims to profit when volatility picks up again. It identifies situations where price is contained within a narrow dormant range and captures the upcoming price trend. This strategy works well when current volatility is low but a breakout is expected.

## Strategy Logic

The strategy first identifies a dormant range, which is when price is contained within the price range of the previous trading day. This indicates that volatility has decreased compared to a few days ago. We check if the current day high < high of n days ago (typically 4 days) and the current day low > low of n days ago to qualify as a dormant range.

Once a dormant range is identified, the strategy places two pending orders - a buy stop near the top of the range and a sell stop near the bottom of the range. It then waits for price to breakout of the range either upwards or downwards. If price breaks upwards, the buy order is triggered to go long. If price breaks downwards, the sell order is triggered to go short.

After entry, stop loss and take profit orders are placed. The stop loss controls downside risk and the take profit closes the trade for profit. The stop loss is placed at a % distance from entry price as defined in risk parameters. The take profit is placed at a distance equal to the dormant range size since we expect price to move similar to previous volatility.

Finally, a fixed fractional position sizing model manages trade size. It increases size for profits and reduces size for losses to improve risk-adjusted returns.

## Advantages

The advantages of this strategy are:

1. Captures upcoming trend by using decreased volatility as signal.
2. Dual-directional orders catch uptrend or downtrend.
3. Stop loss and take profit controls single trade risk.
4. Fixed fractional sizing improves capital efficiency.
5. Simple logic easy to implement.

## Risks

The risks to consider are:

1. Wrong breakout direction if range breakout is unclear.
2. Breakout may just be short reversal, not lasting trend.
3. Stop loss risk of being taken out by huge moves.
4. Fixed fraction sizing may amplify losses when adding to losing trades.
5. Poor performance if parameters not properly set.

## Enhancement Opportunities

Some ways to enhance the strategy are:

1. Add filters like divergence to avoid false breakouts.
2. Improve stop loss with trailing or order stop losses.
3. Add trend filter to avoid counter-trend entries.
4. Optimize fixed fraction ratios for balanced risk/reward.
5. Look at multiple timeframes to improve edge.
6. Utilize machine learning for automated parameter optimization.

## Conclusion

The dormant range reversal strategy has a clear logic and profit potential. Fine-tuning via optimizations, risk management, and signal filtering can further improve consistency. But all mean reversion strategies carry inherent risks and position sizing needs to be controlled. It suits traders familiar with reversal tactics and possessing sound risk awareness.

||


## Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|4|Narrow Range Length|
|v_input_float_1|0.5|Stop Loss (in percentage of reference range)|
|v_input_int_2|400|Fixed Ratio Value ($)| 
|v_input_int_3|200|Increasing Order Amount ($)| 
|v_input_1|timestamp(1 Janv 2020 00:00:00)|Start Date|
|v_input_2|timestamp(1 July 2024 00:00:00)|End Date|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-09-29 00:00:00
end: 2023-10-29 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © gsanson66


//This code is based on the Narrow Range strategy
//Interactive Broker fees are applied on this strategy
//@version=5
strategy("NARROW RANGE BACKTESTING", shorttitle="NR BACKTESTING", overlay=true, initial_capital=1000, default_qty_type=strategy.fixed, commission_type=strategy.commission.percent, commission_value=0.18)


//--------------------------------FUNCTIONS------------------------------------//

//@function to print label
debugLabel(txt, color) =>
    label.new(bar_index, high, text = txt, color=color, style = label.style_label_lower_right, textcolor = color.black, size = size.small)

//@function which looks if the close date of the current bar falls inside the date range
inBacktest