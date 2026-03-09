> Name

Trading Strategy Based on Hull Moving Average and Candlestick

> Author

ChaoZhang

> Strategy Description

## Overview

The core idea of this strategy is to compare the Hull Moving Average (HMA) with the candlestick values to generate buy and sell signals. It will buy when HMA is above the candlestick and sell when HMA is below the candlestick.

## Principles

Firstly, the strategy calculates the HMA of a certain period using the `hma()` function. Then, it gets the open price of the previous candlestick as a benchmark. If HMA is higher than the previous candle's open price, a buy signal is generated. If HMA is lower than the previous candle's open price, a sell signal is generated.

The entry conditions are that the price needs to break HMA in the reverse direction before entering the market. That means it will buy only when the price breaks above HMA from below. It will sell only when the price breaks below HMA from above. This avoids being whipsawed by oscillating markets.

The exit conditions are to stop loss when the price falls back to the other side of HMA. For example, if the price drops below HMA after buying, it will stop loss sell.

In summary, this strategy identifies the major trend direction using the smoothness of HMA to generate signals. Meanwhile, it requires price breakout to filter false signals and avoid being whipsawed by market noise.

## Advantage Analysis

1. Using HMA instead of SMA can better identify trends and filter noise.
2. The breakout mechanism can reduce the probability of being trapped and opening repetitive positions.
3. Adopting the previous candle price rather than the current price avoids curve fitting.
4. The rules are simple and clear, suitable for parameter optimization and robot trading.
5. Can be flexibly applied to any instrument and timeframe, with universality.

## Risks and Improvements

1. Improper HMA parameter setting may miss trends or be too sensitive. Can test different periods to find optimal values.
2. Relying on a single indicator is prone to be stopped out by breakout retries, consider combining other indicators to filter signals.
3. The stop loss is too close to HMA, may be trapped again by subsequent breakout. Can appropriately widen the stop to support/resistance.
4. Unable to determine trend direction and strength. Consider adding trend classification indicators.
5. Fixed stop loss causes large fluctuations in risk/reward. Can try adaptive stops or money management.

## Conclusion

This strategy is relatively simple and practical overall with a clear core idea. It identifies the major trend with HMA and filters false signals with breakout. It avoids being whipsawed by choppy markets. Proper parameter optimization can achieve decent results. However, reliability and win rate are still limited as a single indicator strategy. It's recommended to combine with other technical indicators or money management methods to significantly improve robustness. In conclusion, this strategy provides a simple and effective approach for quantitative trading, which is worth in-depth research and application.

||

## Overview

The core idea of this strategy is to compare the Hull Moving Average (HMA) with candlestick values to generate buy and sell signals. It will buy when HMA is above the candlestick and sell when HMA is below the candlestick.

## Principles

Firstly, the strategy calculates the HMA of a certain period using the `hma()` function. Then, it gets the open price of the previous candlestick as a benchmark. If HMA is higher than the previous candle's open price, a buy signal is generated. If HMA is lower than the previous candle's open price, a sell signal is generated.

The entry conditions are that the price needs to break HMA in the reverse direction before entering the market. That means it will buy only when the price breaks above HMA from below. It will sell only when the price breaks below HMA from above. This avoids being whipsawed by oscillating markets.

The exit conditions are to stop loss when the price falls back to the other side of HMA. For example, if the price drops below HMA after buying, it will stop loss sell.

In summary, this strategy identifies the major trend direction using the smoothness of HMA to generate signals. Meanwhile, it requires price breakout to filter false signals and avoid being whipsawed by market noise.

## Advantage Analysis

1. Using HMA instead of SMA can better identify trends and filter noise.
2. The breakout mechanism can reduce the probability of being trapped and opening repetitive positions.
3. Adopting the previous candle price rather than the current price avoids curve fitting.
4. The rules are simple and clear, suitable for parameter optimization and robot trading.
5. Can be flexibly applied to any instrument and timeframe, with universality.

## Risks and Improvements

1. Improper HMA parameter setting may miss trends or be too sensitive. Can test different periods to find optimal values.
2. Relying on a single indicator is prone to be stopped out by breakout retries, consider combining other indicators to filter signals.
3. The stop loss is too close to HMA, may be trapped again by subsequent breakout. Can appropriately widen the stop to support/resistance.
4. Unable to determine trend direction and strength. Consider adding trend classification indicators.
5. Fixed stop loss causes large fluctuations in risk/reward. Can try adaptive stops or money management.

## Conclusion

This strategy is relatively simple and practical overall with a clear core idea. It identifies the major trend with HMA and filters false signals with breakout. It avoids being whipsawed by choppy markets. Proper parameter optimization can achieve decent results. However, reliability and win rate are still limited as a single indicator strategy. It's recommended to combine with other technical indicators or money management methods to significantly improve robustness. In conclusion, this strategy provides a simple and effective approach for quantitative trading, which is worth in-depth research and application.

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|50|Hull MA Period|
|v_input_2|D|Candle Resolution|
|v_input_3_open|0|Source of Price: open|high|low|close|hl2|hlc3|hlcc4|ohlc4|


> Source (PineScript)

```pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © SeaSide420. Any timeFrame/pair , Hull Moving Average vs Candle
//@version=4
strategy("Hull Moving Average vs Candle", shorttitle="HMA-vs-Candle", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=100, commission_type=strategy.commission.cash_per_order, commission_value=1.00, slippage=1)
Period = input(title="Hull MA Period", type=input.integer, defval=50, minval=1)
Resolution = input(title="Candle Resolution", type=input.resolution, defval="D")
Price = input(title="Source of Price", type=input.source, defval=open)
HMA = hma(Price, Period)
Candle = security(syminfo.tickerid, Resolution, Price, barmerge.gaps_off, barmerge.lookahead_off)
change_color = HMA > Candle ? color.green : color.red
plot1 = plot(Candle, color=change_color, title="Candle Line", linewidth=2, transp=50)
plot2 = plot(HMA[1], color=change_color, title="Hull MA Line", linewidth=2, transp=50)
fill(plot1, plot2, color=change_color, transp=50)
strategy.close("BUY", when=Price < HMA and HMA < Candle, comment="close buy entry")
strategy.close("SELL", when=Price > HMA and HMA > Candle, comment="close sell entry")
if (Price > HMA and HMA > Candle and Price > Price[1])
    strategy.entry("BUY", strategy.long)
if (Price < HMA and HMA < Candle and Price < Price[1])
    strategy.entry("SELL", strategy.short)
```