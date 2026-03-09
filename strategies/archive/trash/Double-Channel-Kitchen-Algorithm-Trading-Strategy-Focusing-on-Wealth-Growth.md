> Name

Double-Channel-Kitchen-Algorithm-Trading-Strategy-Focusing-on-Wealth-Growth

> Author

ChaoZhang

> Strategy Description


## Overview 

The "Double Channel Kitchen" strategy uses Supertrend and StochRSI indicators to analyze price trends and overbought/oversold conditions in different timeframes, in order to identify potential buy and sell signals. This strategy aims to trade along the major trend direction and capture the primary price movement over the medium to long term.

## Strategy Logic

The strategy employs the Supertrend indicator in both 1-hour and 4-hour timeframes to determine the price trend direction. When the Supertrends in both timeframes point in the same direction, it signifies a relatively strong price trend.

In addition, the StochRSI indicator is used to detect overbought/oversold conditions. The StochRSI combines the strengths of both the RSI and Stochastic Oscillator indicators. When the StochRSI line crosses above the overbought threshold, it indicates a possible oversold condition in price. When the StochRSI line crosses below the oversold threshold, it flags a potential overbought condition.

Together with the dual Supertrend confirmation of the price trend, if the StochRSI also shows overbought/oversold signals, it presents a good opportunity to buy or sell. To further verify the signal, a lookback period is implemented where after the StochRSI overbought/oversold signal, the price movement in the past few bars is checked - if it confirms the StochRSI signal, then a buy or sell will be triggered.

In summary, this strategy uses the dual time frame Supertrend to determine the major trend, and StochRSI to identify local reversals, to carry out trend-following trades over the medium to long term.

## Advantages of the Strategy

- Using indicators across multiple timeframes helps to filter out false signals
- Combines the strengths of Supertrend and StochRSI for trend and overbought/oversold analysis
- Lookback verification avoids unnecessary trades 
- Medium to long term operations avoid excessive trading and slippage
- Easy to understand dual-indicator setup, with flexible parameter tuning

## Risks of the Strategy

- Choppy markets without clear mid-long term trends can generate false signals
- Excessive lookback period may cause missing good entry opportunities 
- Poor StochRSI parameter settings may lead to incorrect overbought/oversold signals
- Improper Supertrend parameters can cause wrong trend direction judgement
- Mechanical signals following overlooks major fundamental changes

Improvements:

- Optimize combinations of StochRSI and Supertrend parameters
- Adjust lookback period based on different market conditions
- Add volume indicators for signal verification
- Monitor key fundamental news events, manual intervention when necessary

## Enhancement Areas

- Add more Supertrend indicators across different timeframes for multi-stage screening 
- Replace StochRSI with other overbought/oversold indicators e.g. KD, RSI
- Incorporate trailing stop loss strategies to ride trends
- Combine key moving averages e.g. 30-period MA to determine major trends
- Develop auto parameter optimization for robustness

## Conclusion

The "Double Channel Kitchen" strategy effectively utilizes the Supertrend for major trend and StochRSI for local reversals, to implement a reliable trend following system. It focuses on medium-long term holdings to avoid excessive trading and slippage. Through parameter optimization, combining indicators, this strategy can achieve steady positive results. However investors should still watch out for major fundamental changes, instead of just mechanically following indicator signals. Overall, this strategy offers an effective technical analysis approach for active investors to generate positive returns with proper risk awareness.

|Argument|Default|Description|
|----|----|----|
|v_input_1|timestamp(01 January 2017 13:30 +0000)|(? ################# BACKTEST DATE ################ )Start_Time|
|v_input_2|timestamp(30 April 2024 19:30 +0000)|End_Time|
|v_input_3|10|(? #################  Supertrend  ################ )ATR Length|
|v_input_4|3|Factor|
|v_input_string_1|0|Short Time Period: 07 1h|02 3m|03 5m|04 15m|05 30m|06 45m|01 1m|08 2h|09 3h|10 4h|11 1D|12 1W|
|v_input_string_2|0|Long Time Period: 10 4h|02 3m|03 5m|04 15m|05 30m|06 45m|07 1h|08 2h|09 3h|01 1m|11 1D|12 1W|
|v_input_float_1|15|(? #################  Stoch RSI   ################ )Stoch Rsi Low Limit|
|v_input_floa