> Name

Dual-DI-Crossover-Daily-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/13cc2e99e18f12c6352.png)
[trans]


## Overview

This strategy is based on the crossover of the positive directional indicator (DI+) and negative directional indicator (DI-) derived from the Average True Range (ATR) indicator. It identifies buy and sell opportunities by detecting these crossovers, making it a trend-following strategy that uses DI+ and DI- crossovers to determine trend reversals. ATR is employed to set stop loss and take profit levels.

## Strategy Logic

1. Calculate ATR(14): Compute the average true range over the past 14 days using high, low, and close prices.

2. Compute DI+ and DI-:

    - DI+ = 100 * RMA(MAX(UP, 0), N) / ATNR  

    - DI- = 100 * RMA(MAX(DOWN, 0), N) / ATNR

    Where UP is the difference between today's high and yesterday's close, DOWN is the difference between today's low and yesterday's close, N is the parameter length (default to 14), and ATNR is the ATR calculated from step 1.

3. Determine entry and exit:

    - When DI+ crosses over DI-, a buy signal is generated.

    - When DI+ crosses below DI-, a sell signal is generated.

4. Set stop loss and take profit:

    - Long stop loss is set at the entry price minus ATR multiplied by the stop loss multiplier.

    - Long take profit is set at the entry price plus ATR multiplied by the take profit multiplier.

    - Short stop loss is set at the entry price plus ATR multiplied by the stop loss multiplier.

    - Short take profit is set at the entry price minus ATR multiplied by the take profit multiplier.

## Advantage Analysis

1. Using DI+ and DI- crossovers to determine trend reversals provides timely signals for new trend directions.

2. ATR as a dynamic stop loss/take profit indicator can set reasonable levels based on market volatility.

3. The strategy has few parameters, making it easy to understand and implement.

4. Backtest results show that this strategy has a positive profit factor and outperforms buy-and-hold strategies.

## Risks and Solutions

1. False signal risk from DI crossovers

    - Filter signals with moving averages or other indicators to avoid false breakouts, by adjusting the DI period parameters.

2. Stop loss/take profit levels too close

    - Adjust ATR multipliers to better accommodate market volatility.

3. Ineffective in range-bound markets

    - Combine with other indicators to filter out unnecessary signals during consolidation periods.

4. Drawdown risk

    - While acceptable, systematic strategies cannot completely avoid drawdowns; adjust position sizing to control them.

## Optimization Suggestions

1. Add filters like moving averages or other technical indicators to reduce false signals in range-bound markets.

2. Implement position sizing mechanisms such as fixed fractional or Martingale to better manage risk and enhance profitability.

3. Optimize ATR parameters to better match the volatility of different trading instruments.

4. Conduct parameter optimization on DI periods, ATR periods, and ATR multipliers to find the best combination.

5. Add overnight and early session logic to run the strategy continuously 24/7.

## Conclusion

This is a simple and practical day trading strategy that generates signals from DI crossovers and sets stop loss/take profit levels dynamically using ATR. With few parameters, it's easy to test and optimize. However, DI crossover may not perform well in range-bound markets. Future improvements could focus on adding additional filters. Overall, this strategy demonstrates stable performance suitable for short-term day trading.

|||

## Overview

This strategy generates trading signals based on the crossover of the positive directional indicator (DI+) and negative directional indicator (DI-) calculated from the Average True Range (ATR). It belongs to the trend-following category that identifies trend reversals through DI+ and DI- crossovers. ATR is used to set stop loss and take profit levels.

## Strategy Logic

1. Calculate ATR(14): Compute the average true range over the past 14 days using high, low, and close prices.

2. Compute DI+ and DI-:

    - DI+ = 100 * RMA(MAX(UP, 0), N) / ATNR  

    - DI- = 100 * RMA(MAX(DOWN, 0), N) / ATNR

    Where UP is the difference between today's high and yesterday's close, DOWN is the difference between today's low and yesterday's close, N is the parameter length (default to 14), and ATNR is the ATR calculated from step 1.

3. Determine entry and exit:

    - When DI+ crosses over DI-, a buy signal is generated.

    - When DI+ crosses below DI-, a sell signal is generated.

4. Set stop loss and take profit:

    - Long stop loss is set at the entry price minus ATR multiplied by the stop loss multiplier.

    - Long take profit is set at the entry price plus ATR multiplied by the take profit multiplier.

    - Short stop loss is set at the entry price plus ATR multiplied by the stop loss multiplier.

    - Short take profit is set at the entry price minus ATR multiplied by the take profit multiplier.

## Advantage Analysis

1. Using DI+ and DI- crossovers to determine trend reversals provides timely signals for new trend directions.

2. ATR as a dynamic stop loss/take profit indicator can set reasonable levels based on market volatility.

3. The strategy has few parameters, making it easy to understand and implement.

4. Backtest results show this strategy has a positive profit factor and outperforms buy-and-hold strategies.

## Risks and Solutions

1. False signal risk from DI crossovers

    - Filter signals with moving averages or other indicators to avoid false breakouts by adjusting the DI period parameters.

2. Stop loss/take profit levels too close

    - Adjust ATR multipliers to better accommodate market volatility.

3. Ineffective in range-bound markets

    - Combine with other indicators to filter out unnecessary signals during consolidation periods.

4. Drawdown risk

    - While acceptable, systematic strategies cannot completely avoid drawdowns; adjust position sizing to control them.

## Optimization Suggestions

1. Add filters like moving averages or other technical indicators to reduce false signals in range-bound markets.

2. Implement position sizing mechanisms such as fixed fractional or Martingale to better manage risk and enhance profitability.

3. Optimize ATR parameters to better match the volatility of different trading instruments.

4. Conduct parameter optimization on DI periods, ATR periods, and ATR multipliers to find the best combination.

5. Add overnight and early session logic to run the strategy continuously 24/7.

## Conclusion

This is a simple and practical day trading strategy that generates signals from DI crossovers and sets stop loss/take profit levels dynamically using ATR. With few parameters, it's easy to test and optimize. However, DI crossover may not perform well in range-bound markets. Future improvements could focus on adding additional filters. Overall, this strategy demonstrates stable performance suitable for short-term day trading.

|||

```pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © TheHulkTrading
//@version=4
strategy("DI Crossing Daily Straregy HulkTrading", overlay=true)
// ATR Multiplier. Recommended values between 1..4
atr_multiplier = input(1, minval=1, title="ATR Multiplier") 
//Length of DI. Recommended default value = 14
length = input(14, minval=1, title="Length di")
up = change(high)
down = -change(low)
range = rma(tr, 14)

//DI+ and DI- Calculations
di_plus = fixnan(100 * rma(up > down and up > 0 ? up : 0, length) / range)
di_minus = fixnan(100 * rma(down > up and down > 0 ? down : 0, length) / range)

//Long and short conditions
longCond = crossover(di_plus,di_minus)
shortCond = crossunder(di_plus,di_minus) 


//Stop levels and take profits
stop_level_long = strategy.position_avg_price - atr_multiplier*atr(14)
take_level_long = strategy.position_avg_price + 2*atr_multiplier*atr(14)
stop_level_short = strate