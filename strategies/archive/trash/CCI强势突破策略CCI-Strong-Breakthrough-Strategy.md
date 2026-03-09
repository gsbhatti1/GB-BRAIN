> Name

CCI Strong Breakthrough Strategy CCI-Strong-Breakthrough-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/12e7d96673ef9d4c089.png)
[trans]

## Overview

This strategy is based on the classic Commodity Channel Index (CCI) and only goes long. It enters the market when the CCI indicator is at an extremely low level (CCI <-150 or user-defined threshold) and regains strength (i.e., CCI > CCI of previous candle), with a filter on the "strength" of the prices themselves (i.e., the closing price of the signal bar must be higher than the opening by a certain percentage - fixed at 0.25%). When either a stop loss is triggered or prices rise above the CCI upper band, it exits the market.

The strategy aims to achieve high-profit trades with an over 50% win rate rather than capturing the full length of a trend. It is therefore suitable for traders who "can't stand potential losses."

## Strategy Logic

1. Construct the CCI indicator and its bands using `ta.sma()` and `ta.dev()` functions.

2. Use input to select start date for backtesting.

3. Entry signal: CCI crosses below the lower band and starts increasing, with an additional filter that requires the closing price > opening by 0.25%.

4. Exit condition 1: CCI rises above the upper band, take profit.

5. Exit condition 2: Price drops below the stop loss level, cut losses.

6. The strategy only goes long based on CCI strength, with stops to control risk.

## Advantage Analysis

The strategy has the following advantages:

1. Identify overbought/oversold situations using CCI to capitalize on reversals.
2. Only long direction avoids excessive risk from bad trades.
3. Price strength filter ensures support is formed before entry.
4. Stop loss mechanism limits per trade loss and manages capital.
5. Flexible backtest parameters to adjust entry filters.
6. High win rate suits investors focused on risk management.
7. Clear logic and simple implementation.

## Risk Analysis

This strategy also has some risks:

1. Going only long may miss short-term downtrends.
2. Poor CCI parameter tuning leads to failure.
3. Stop loss too loose fails to limit losses.
4. Strong uptrend blows through stops causing large losses.
5. High trade frequency increases transaction costs.

Possible solutions:

1. Optimize CCI parameters to find best values.
2. Adjust stop loss to balance risk and slippage.
3. Manage entry frequency considering costs.
4. Combine with trend and range filters.

## Enhancement Opportunities

Some ways to improve the strategy:

1. Implement dynamic stops based on market volatility.
2. Add filters like MACD to avoid stops being too wide.
3. Incorporate short side when CCI overheats.
4. Consider costs, set minimum profit target.
5. Optimize parameters for time frame.
6. Machine learning for automated parameter tuning.
7. Add position sizing for dynamic allocation.

## Conclusion

In summary, this long-only strategy capitalizes on CCI overbought/oversold levels with a price strength filter and stop losses. It offers easy implementation, good risk control, and high win percentage. The limitations of being long-only and fixed stops can be addressed through parameter optimization, short entries, dynamic stops, etc. The strategy suits investors seeking high win rates and proper risk management.

||

## Overview

This strategy is based on the classic Commodity Channel Index (CCI) and only goes long. It enters the market when the CCI indicator is at an extremely low level (CCI <-150 or user-defined threshold) and regains strength (i.e., CCI > CCI of previous candle), with a filter on the "strength" of the prices themselves (i.e., the closing price of the signal bar must be higher than the opening by a certain percentage - fixed at 0.25%). The strategy exits when either the stop loss is triggered or prices rise above the CCI upper band.

The goal is to achieve high-profit trades with an over 50% win rate rather than capturing the full duration of a trend. It is therefore suitable for those who "hate to see potential losses."

## Strategy Logic

1. Construct CCI indicator and bands using `ta.sma()` and `ta.dev()` functions.

2. Use input to select start date for backtest.

3. Entry signal: CCI crosses below lower band and starts increasing, with an additional filter that requires the closing price > opening by 0.25%.

4. Exit condition 1: CCI rises above upper band, take profit.

5. Exit condition 2: Price drops below stop loss level, cut losses.

6. The strategy only goes long based on CCI strength, with stops to control risk.

## Advantage Analysis

The strategy has the following advantages:

1. Identify overbought/oversold situations using CCI to capitalize on reversals.
2. Only long direction avoids excessive risk from bad trades.
3. Price strength filter ensures support is formed before entry.
4. Stop loss mechanism limits per trade loss and manages capital.
5. Flexible backtest parameters to adjust entry filters.
6. High win rate suits investors focused on risk management.
7. Clear logic and simple implementation.

## Risk Analysis

This strategy also has some risks:

1. Going only long may miss short-term downtrends.
2. Poor CCI parameter tuning leads to failure.
3. Stop loss too loose fails to limit losses.
4. Strong uptrend blows through stops causing large losses.
5. High trade frequency increases transaction costs.

Possible solutions:

1. Optimize CCI parameters to find best values.
2. Adjust stop loss to balance risk and slippage.
3. Manage entry frequency considering costs.
4. Combine with trend and range filters.

## Enhancement Opportunities

Some ways to improve the strategy:

1. Implement dynamic stops based on market volatility.
2. Add filters like MACD to avoid stops being too wide.
3. Incorporate short side when CCI overheats.
4. Consider costs, set minimum profit target.
5. Optimize parameters for time frame.
6. Machine learning for automated parameter tuning.
7. Add position sizing for dynamic allocation.

## Conclusion

In summary, this long-only strategy capitalizes on CCI overbought/oversold levels with a price strength filter and stop losses. It offers easy implementation, good risk control, and high win percentage. The limitations of being long-only and fixed stops can be addressed through parameter optimization, short entries, dynamic stops, etc. The strategy suits investors seeking high win rates and proper risk management.

||

## Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1_close|0|src: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_int_1|20|Period|
|v_input_float_1|8|Stop Loss percentage|
|v_input_float_2|0.25|Close of the signal bar higher than Open %|
|v_input_int_2|150|Upper Band|
|v_input_int_3|-150|Lower Band|
|v_input_int_4|true|From Month|
|v_input_int_5|true|From Day|
|v_input_int_6|2016|From Year|
|v_input_int_7|true|Thru Month|
|v_input_int_8|true|Thru Day|
|v_input_int_9|2112|Thru Year|


> Source (PineScript)

```pinescript
//@version=5
strategy(title='CCI High Performance long only', overlay=false)
src = input(close)
length = input.int(20, title='Period', minval=1)
lossp = input.float(8, title='Stop Loss percentage', minval=0.5, step=0.5)
scart = input.float(0.25, title='Close of the signal bar higher than Open %', minval=0)
upperline = input.int(150, title='Upper Band', minval=0, step=10)
lowline = input.int(-150, title='Lower Band', maxval=0, step=10)

// construction of CCI (not on close but in totalprice) and of bands
ma = ta.sma(src, length)
cci = (src - ma) / (0.015 * ta.dev(src, length))
plot(cci, 'CCI', color=color.new(#996A15, 0))
band1 = hline(upperline, 'Upper Band', color=#C0C0C0, linestyle=hline.style_dashed)
band0 = hline(lowline, 'Lower Band', color=#C0C0C0, linestyle=hline.style_dashed)

```