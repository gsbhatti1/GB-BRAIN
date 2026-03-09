> Name

Correlation-Based Bullish Bearish Crypto Trading Strategy Based on Wall Street CCI Index

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/17bb1bd7ec2722307a2.png)
[trans]

## Overview

This strategy is based on the Wall Street Chasing Ring Index, comparing the bullish and bearish trends of a benchmark cryptocurrency market to achieve an automated trading strategy for bullish and bearish operations on the target cryptocurrency. The strategy can be configured with support parameters for different cryptocurrencies to track and trade multiple cryptocurrencies.

## Strategy Principles

1. Calculate the 200-period weighted moving average (WMA) of the benchmark cryptocurrency using the Wall Street Chasing Ring Index.

2. Determine the trend direction of the WMA: go long when the WMA is rising, and go short when the WMA is falling.

3. The strategy automatically opens and closes positions based on the trend direction and current position status:

    - When the WMA is rising and there is no position, the strategy uses a market order to enter a long position.
    
    - When the WMA is falling and there is no position, the strategy uses a market order to enter a short position.

    - When the long position profit is greater than or equal to the TakeProfitLong percentage, the strategy closes the long position.
    
    - When the short position profit is greater than or equal to the TakeProfitShort percentage, the strategy closes the short position.

    - When the long position loss is greater than or equal to the StopLossLong percentage, the strategy closes the long position.

    - When the short position loss is greater than or equal to the StopLossShort percentage, the strategy closes the short position.

4. The strategy updates the take profit and stop loss prices in real-time based on changes in the benchmark cryptocurrency price.

## Advantages Analysis

1. The strategy is highly adaptable, allowing different parameters to be set for various cryptocurrencies to track and trade multiple cryptocurrencies.

2. Using the Wall Street Chasing Ring Index to determine the market trend can avoid incorrect trades caused by noise. The index has a certain lag in breakouts, helping to reduce losses from false breakouts.

3. Incorporating take profit and stop loss mechanisms allows for trend following while controlling the loss per trade.

4. Fully automated trading without manual intervention allows for 24/7 operation.

## Risk Analysis

1. Risk of the target cryptocurrency price decoupling from the benchmark cryptocurrency, leading to failure of the strategy. This can be optimized by using multiple benchmark cryptos and selecting the most highly correlated one.

2. Risk of sudden volatility breaking out stop losses. This can be mitigated by adjusting the stop loss percentage or using trailing stops.

3. Risk of the take profit percentage being too small to capture sufficient trend gains. This can be addressed by incorporating trend tracking or dynamic take profit mechanisms.

4. Risk of false breakouts leading to stop loss exits. This can be mitigated by tuning the Wall Street Chasing Ring Index parameters or adding re-entry logic.

## Optimization Directions

1. Use correlation analysis across multiple benchmark cryptos and combine indicators to reduce the risk of a single benchmark crypto.

2. Add trend tracking to dynamically adjust take profit and stop loss based on volatility.

3. Add staged stops to prevent extreme moves from breaking out positions.

4. Add re-entry logic to avoid missing further trends after a stop loss exit.

5. Optimize Wall Street Chasing Ring Index parameters and settings to improve signal effectiveness.

6. Optimize parameters separately for each target cryptocurrency to improve adaptability.

7. Optimize position sizing based on account size.

## Summary

Overall, this is a typical trend-following strategy. The core idea is to determine the trend direction of a benchmark cryptocurrency using the Wall Street Chasing Ring Index and trade the target cryptocurrency accordingly. The strategy has some advantages but also risks that need to be noted. Further enhancements in tuning, trend tracking, risk control, etc., can improve stability and profitability. In summary, the strategy provides ideas and references for automated systematic cryptocurrency trading.

||

## Overview

This is an automated trading strategy that generates long/short/close signals on the target crypto currency based on the calculated trend of a benchmark crypto currency considered correlated with it, using the Wall Street Chasing Ring Index.

With default parameters and ETH/USDT as the base symbol, the strategy shows good backtest results on symbols like DENT/USDT, BTT/USDT, FTT/USDT, DOT/USDT, etc. This makes sense as ETH is quite influential in crypto markets so many cryptos tend to follow ETH's major movements.

Note: The strategy with default parameters is intended for a 4-hour timeframe. On other timeframes, try different support length.

## How The Strategy Works

1. A 200-period WMA is calculated on the base symbol.

2. When the WMA is rising, go long. When falling, go short.

3. TakeProfit for Long/Short and StopLoss for Long/Short are calculated as percentages, so 0.05 = 5%, etc. Also, TakeProfit and StopLoss are calculated based on the base symbol, not the chart's symbol.

4. The strategy uses market orders for entry and exit based on the following logic:

    - When the WMA is rising and there is no position, enter a long position.
    
    - When the WMA is falling and there is no position, enter a short position.

    - When the long position profit is greater than or equal to the TakeProfitLong percentage, close the long position.
    
    - When the short position profit is greater than or equal to the TakeProfitShort percentage, close the short position.

    - When the long position loss is greater than or equal to the StopLossLong percentage, close the long position.

    - When the short position loss is greater than or equal to the StopLossShort percentage, close the short position.

5. TakeProfit and StopLoss prices are updated in real-time based on changes in the base symbol's price.

## Advantage Analysis

1. The strategy is highly adaptable for use on multiple crypto currencies by tuning parameters.

2. Using the Wall Street CCI to determine the trend avoids noise-led wrong trades. The CCI has a certain lag in breakouts, helping to avoid false breakout losses.

3. Incorporating take profit and stop loss mechanisms allows for trend following while controlling the loss per trade.

4. Fully automated trading without manual intervention allows for 24/7 operation.

## Risk Analysis

1. Risk of the target crypto price decoupling from the base crypto, leading to failure of the strategy. This can be optimized by using multiple base cryptos and selecting the most highly correlated one.

2. Risk of sudden volatility breaking out stop losses. This can be mitigated by adjusting the stop loss percentage or using trailing stops.

3. Risk of the take profit percentage being too small to capture sufficient trend gains. This can be addressed by incorporating trend tracking or dynamic take profit mechanisms.

4. Risk of false breakouts leading to stop loss exits. This can be mitigated by tuning the Wall Street CCI parameters or adding re-entry logic.

## Optimization Directions

1. Use correlation analysis across multiple base cryptos and combine indicators to reduce the risk of a single base crypto.

2. Add trend tracking to dynamically adjust take profit and stop loss based on volatility.

3. Add staged stops to prevent extreme moves from breaking out positions.

4. Add re-entry logic to avoid missing further trends after a stop loss exit.

5. Optimize CCI parameters and settings to improve signal effectiveness.

6. Optimize parameters separately for each target crypto to improve adaptability.

7. Optimize position sizing based on account size.

## Summary

Overall, this is a typical trend-following strategy. The core idea is to determine the trend direction of a benchmark cryptocurrency using the Wall Street CCI and trade the target cryptocurrency accordingly. The strategy has some advantages but also risks to note. Further enhancements in tuning, trend tracking, risk control, etc., can improve stability and profitability. In summary, the strategy provides ideas and references for automated systematic cryptocurrency trading.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_int_1|200|Support Length|
|v_input_1|BTC_USDT:swap|Correlated Symbol|
|v_input_2_hlc3|0|Price Source: hlc3|high|low|open|hl2|close|hlcc4|ohlc4|
|v_input_float_1|0.2|Take Profit Long|
|v_input_float_2|0.15|Take Profit Short|
|v_input_float_3|0.1|Stop Loss Long|
|v_input_float_4|0.04|Stop Loss Short|
|v_input_3|timestamp(01 Jan 2016 00:00 +0000)|Start Time|
|v_input_4|timestamp(31 Dec 2050 23:59 +0000)|End Time|


> Source (PineScript)

```pinescript
/*backtest
start: 2022-10-25 00:00:00
end: 2023-10-31 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at