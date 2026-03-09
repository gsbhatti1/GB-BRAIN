> Name

Dual-Indicators-Combo-Crazy-Intraday-Scalping-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/11fba740b932e76ed3d.png)

## Overview

This strategy combines the buy and sell signals from LuxAlgo's TMO and AMA indicators to catch the beginning of a trend during range-bound consolidation. It goes long or short when the conditions of TMO signal, AMA extremities, and increasing candle body size are met. The stop loss is set at the latest swing high/low based on recent bars.

## Strategy Logic

The TMO indicator reflects price momentum. It belongs to the oscillator indicator type and can generate trading signals when divergence occurs. The AMA indicator is a smoothed moving average. It shows a range of price fluctuations, indicating overbought/oversold conditions when price approaches the upper/lower band.

The main logic behind this strategy is: TMO can detect trend divergence to generate trading signals. AMA can identify price reversal zones. Together with the confirmation from increasing candle body size, they can improve the accuracy of capturing trend start. So the strategy will go long/short when:

1. TMO gives buy signal, i.e. bullish divergence AND AMA shows its max extremity
2. TMO gives sell signal, i.e. bearish divergence AND AMA shows its min extremity
3. Also requires the most recent 3 candle's body to expand in size

This solves the false signal problem of single indicators. The stop loss based on recent bars' highest high/lowest low can control risk effectively.

## Advantages

The advantages of this strategy include:

1. Indicator combo improves signal accuracy. TMO and AMA validate each other to reduce false signals and improve accuracy.
2. Multiple conditions capture trend start. The combo of TMO signal, AMA extremities, and increasing candle size allows the strategy to effectively identify trend initiation, which scalping strategies pursue.
3. Candle-based stop loss manages risk. By using recent bars' highest/lowest price as stop loss, it controls the risk of each trade while avoiding the lagging risk from indicator recalculation.
4. Concise and effective logic. With just two indicators, the strategy has implemented a complete scalping system with clear and simple logic. The backtest results also look profitable.

## Risks

The main risks of the strategy:

1. Frequent in-out trades risk. As a scalping strategy targeting short holding period, high trading cost can affect its profitability.
2. Aggressive stop loss risk. By using the recent extreme prices for stop loss, it may be vulnerable to market noise and increase the chance of stop loss trigger.
3. Difficult parameter optimization risk. The strategy involves multiple parameters. Finding the optimal parameter combination can be challenging.

## Optimization

The strategy can be further optimized in the following areas:

1. Add more filter indicators like volume to remove false signals and further improve signal quality.
2. Test modifications on stop loss rules to make it less aggressive, e.g., add confirmation bars before triggering stop loss.
3. Conduct parameter optimization to find the best parameter combination for the indicators, which may help filter out more noise and increase win rate. Mainly optimize TMO Length, AMA Length and Multiplier.
4. Backtest and trade it live across different products and timeframes to find out the best fitting market condition for this strategy logic.

## Conclusion

This strategy combines the trading signals from TMO and AMA to scalp in range-bound markets by capturing early trend moves. It has the advantages of high signal accuracy, early trend capture, and effective risk control. Further optimizations on parameters and strategy rules can make it a highly practical intraday scalping strategy.

||

## Overview

This strategy combines the buy and sell signals from LuxAlgo's TMO and AMA indicators to catch the beginning of a trend during range-bound consolidation. It goes long or short when the conditions of TMO signal, AMA extremities, and increasing candle body size are met. The stop loss is set at the latest swing high/low based on recent bars.

## Strategy Logic

The TMO indicator reflects price momentum. It belongs to the oscillator indicator type and can generate trading signals when divergence occurs. The AMA indicator is a smoothed moving average. It shows a range of price fluctuations, indicating overbought/oversold conditions when price approaches the upper/lower band.

The main logic behind this strategy is: TMO can detect trend divergence to generate trading signals. AMA can identify price reversal zones. Together with the confirmation from increasing candle body size, they can improve the accuracy of capturing trend start. So the strategy will go long/short when:

1. TMO gives buy signal, i.e., bullish divergence AND AMA shows its max extremity
2. TMO gives sell signal, i.e., bearish divergence AND AMA shows its min extremity
3. Also requires the most recent 3 candle's body to expand in size

This solves the false signal problem of single indicators. The stop loss based on recent bars' highest high/lowest low can control risk effectively.

## Advantages

The advantages of this strategy include:

1. Indicator combo improves signal accuracy. TMO and AMA validate each other to reduce false signals and improve accuracy.
2. Multiple conditions capture trend start. The combo of TMO signal, AMA extremities, and increasing candle size allows the strategy to effectively identify trend initiation, which scalping strategies pursue.
3. Candle-based stop loss manages risk. By using recent bars' highest/lowest price as stop loss, it controls the risk of each trade while avoiding the lagging risk from indicator recalculation.
4. Concise and effective logic. With just two indicators, the strategy has implemented a complete scalping system with clear and simple logic. The backtest results also look profitable.

## Risks

The main risks of the strategy:

1. Frequent in-out trades risk. As a scalping strategy targeting short holding period, high trading cost can affect its profitability.
2. Aggressive stop loss risk. By using the recent extreme prices for stop loss, it may be vulnerable to market noise and increase the chance of stop loss trigger.
3. Difficult parameter optimization risk. The strategy involves multiple parameters. Finding the optimal parameter combination can be challenging.

## Optimization

The strategy can be further optimized in the following areas:

1. Add more filter indicators like volume to remove false signals and further improve signal quality.
2. Test modifications on stop loss rules to make it less aggressive, e.g., add confirmation bars before triggering stop loss.
3. Conduct parameter optimization to find the best parameter combination for the indicators, which may help filter out more noise and increase win rate. Mainly optimize TMO Length, AMA Length and Multiplier.
4. Backtest and trade it live across different products and timeframes to find out the best fitting market condition for this strategy logic.

## Conclusion

This strategy combines the trading signals from TMO and AMA to scalp in range-bound markets by capturing early trend moves. It has the advantages of high signal accuracy, early trend capture, and effective risk control. Further optimizations on parameters and strategy rules can make it a highly practical intraday scalping strategy.

| Argument | Default | Description |
| ---- | ---- | ---- |
| v_input_float_1 | 2 | Factor |
| v_input_1 | true | As Smoothed Candles |
| v_input_2 | true | Show Alternating Extremities |
| v_input_int_1 | 7 | (TMO Settings) TMO Length |
| v_input_source_1_close | 0 | TMO Source: close/high/low/open/hl2/hlc3/hlcc4/ohlc4 |
| v_input_source_2_close | 0 | (AMA Settings) AMA Source: close/high/low/open/hl2/hlc3/hlcc4/ohlc4 |
| v_input_int_2 | 50 | AMA Length |
| v_input_float_2 | true | (AMA Kernel Parameters) Lag |
| v_input_float_3 | 0.5 | Overshoot |
| v_input_int_3 | 10 | (Stop Loss Settings) SL Period |

## Source (PineScript)

```pinescript
/*backtest
start: 2023-11-23 00:00:00
end: 2023-11-30 00:00:00
```