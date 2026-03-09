> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_timeframe_1||(?EMA Settings)Timeframe|
|v_input_int_1|200|Length|
|v_input_string_1|0|Type: EMA|SMA|RMA|WMA|
|v_input_source_1_close|0|Source: close|


## Overview

The EMA mean reversion trading strategy opens and closes positions based on the degree to which price diverges from the EMA. It uses the percentage difference between price and EMA as the entry signal and trailing stop loss to manage positions.

## Strategy Logic

The strategy uses EMA as the benchmark and calculates the percentage difference between current price and EMA. It goes long when the price is far enough from the EMA (default 9%), and closes position when price gets close enough to the EMA (default 1%). After opening positions, it uses trailing stop loss to lock in profit as it increases.

Specifically, the strategy includes the following components:

1. Calculate EMA. The period (default 200), source (close price) and method (EMA, SMA, RMA, WMA) are configurable.
2. Calculate the percentage difference between current price and EMA. Pay attention to the positive/negative sign.
3. Open positions based on difference threshold. Default long entry is 9% and short entry is 9%.
4. Support ladder entry. The number of rungs and percentage step per rung can be configured.
5. Use trailing stop loss after entry. The threshold to start trailing (default 1% profit) and trailing percentage (default 1%) are configurable.
6. Close positions based on difference threshold. Default exit is 1% for both long and short.
7. Cancel unfilled orders when price reverts to EMA.
8. Configurable stop loss percentage.
9. Support backtesting and live trading.

## Advantage Analysis

The advantages of this strategy:

1. Utilize mean reversion concept to trade trend based on EMA deviation. Aligns with trend trading theory.
2. Entry, stop loss, exit parameters are configurable to adapt to different market conditions.
3. Ladder entry allows gradual position build up and reduces cost.
4. Trailing stop locks in profit and manages risk.
5. Highly optimizable by adjusting EMA parameters or entry/exit thresholds.
6. Pine Script allows straightforward use in TradingView.
7. Intuitive charting for observation and analysis.

## Risk Analysis

The risks of this strategy:

1. Backtest overfitting risk. Parameter optimization may overfit backtest data and underperform in live trading.
2. EMA failure risk. Price may deviate from EMA for extended periods.
3. Stop loss getting run over risk. Stop loss may get penetrated by volatile moves.
4. High trading frequency leads to higher commission costs.
5. Require longer lookback period. More susceptible to sudden events.

Risk management:

1. Robust parameter selection through optimization and multi-market verification.
2. Reasonable EMA period, not too short or too long.
3. Wider stop loss buffer to prevent getting stopped out prematurely.
4. Less aggressive entry rules to reduce trade frequency.
5. Incorporate additional indicators like volume, Bollinger Bands, RSI to adapt to events.

## Optimization Directions

The strategy can be improved in the following aspects:

1. Add filters like volume, Bollinger Bands, RSI to reduce false signals.
2. Add dual EMA for higher probability trend trading.
3. Enhance stop loss with adaptive stops, Chandelier Exits to further limit risk.
4. Add auto parameter optimization to find better parameter sets.
5. Incorporate machine learning for chance of EMA deviation.
6. Consider intraday or overnight position to take advantage of gaps.
7. Integrate stock universe selection for larger capacity.

## Conclusion

The EMA mean reversion strategy trades based on the mean reverting behavior of prices around a moving average. It utilizes the statistical properties of EMA rationally to identify trend changes and uses stop loss to control risk. Compared to traditional moving average strategies, it focuses more on dynamic trailing stops than rigid entry and exit rules. The strategy can complement trend following strategies, but requires caution on curve fitting and controlling trade frequency. Further improvements on stop loss and entry quality may lead to better live performance.

[/trans]