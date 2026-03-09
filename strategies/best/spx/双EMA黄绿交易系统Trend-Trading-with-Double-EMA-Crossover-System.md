> Name

Double EMA Yellow-Green Trading System

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/12313093dbe5b78c0e8.png)

[trans]


## Overview

The Double EMA Yellow-Green Trading System is a trend-following trading system based on the comparison of two Exponential Moving Averages (EMAs). This system uses two EMAs with different periods to determine the current trend direction and generate trading signals accordingly. With its simple logic and easy implementation, this system can effectively capture market trends and is suitable for medium to long-term investors.

## Strategy Principles

The strategy primarily relies on two EMAs: a faster EMA and a slower EMA. When the fast EMA is above the slow EMA, it is considered bullish. Conversely, when the fast EMA is below the slow EMA, it is considered bearish.

Based on the relationship between the price and the two EMAs, the bars can be categorized into different trading zones:

- When the fast EMA is above the slow EMA, and the price is above the fast EMA (G1), it is a strong buy zone. A long position can be taken here.
- When the fast EMA is below the slow EMA, and the price is below the fast EMA (R1), it is a strong sell zone. A short position can be taken here.
- When the two EMAs cross, the warning (yellow) and watch (orange) zones are determined based on the price's relationship with the two EMAs. These zones indicate potential trend reversals and trades should be taken with caution using additional indicators.

Trading signals are generated when the price moves across different zones. In the strong zones G1 and R1, signals can be directly taken. In the warning and watch zones, additional indicator confirmation is required.

StochRSI is also implemented to assist in identifying potential entry and exit points. Oversold and overbought readings from StochRSI can provide additional buy and sell signals.

## Advantages

- Simple and clear logic, easy to understand and implement.
- Effectively captures medium to long-term trends.
- Distinguishes strong zones from warning/watch zones, producing reliable trade signals.
- StochRSI inclusion further improves entry and exit timing.

## Risks

- As a pure trend-following system, performance may suffer in non-trending markets.
- Incorrect EMA period settings may cause false signals.
- Warning and watch zones carry higher trading risks and should be treated with caution.
- Lack of stop loss may lead to increased losses.

Risks can be reduced by:

1. Selecting strongly trending instruments and pausing trading when trends are weak.
2. Optimizing EMA periods to minimize false signals.
3. Introducing additional indicators for confirmation in warning/watch zones.
4. Implementing stop loss to control loss per trade.

## Enhancement Opportunities

The system can be further improved in the following areas:

1. Incorporate more indicators like MACD, KDJ for signal confirmation.
2. Add filters such as volume expansion in trading zones to improve trade success rate.
3. Dynamically adjust EMA periods based on market conditions for optimized parameters.
4. Implement stop loss strategies to exit trades at certain loss percentages.
5. Optimize position sizing and money management.
6. Test and fine-tune parameters across different instruments to find best configurations.

By introducing more signal confirmation, dynamic parameter optimization, stop loss, and proper money management, the system's robustness can be improved and risks reduced for better results.

## Conclusion

The Double EMA Yellow-Green Trading System is a trend-following system based on the comparison of two EMAs. It identifies different trading zones based on the price's relationship with the EMAs to determine trend direction and generate trading signals. As a system with clear logic and easy implementation, it can effectively capture trends. While risks exist, they can be reduced through auxiliary indicators, dynamic optimization, stop loss, and money management. Overall, the Double EMA Yellow-Green Trading System is a solid trend-following system suitable for medium to long-term investors.

||

## Overview

The Double EMA Crossover system is a trend following trading system based on two Exponential Moving Averages (EMAs). It uses two EMAs with different periods to determine the current trend direction and generate trading signals accordingly. With its simple logic and easy implementation, this system can effectively capture market trends and is suitable for medium to long-term traders.

## How It Works

The core of this system relies on two EMAs, one faster EMA and one slower EMA. When the fast EMA is above the slow EMA, it is considered bullish. When the fast EMA is below the slow EMA, it is considered bearish.

Based on the price's relationship with the two EMAs, the bars can be categorized into different trading zones:

- When the fast EMA is above the slow EMA and the price is above the fast EMA (G1), it is a strong buy zone, a long position can be taken here.
- When the fast EMA is below the slow EMA and the price is below the fast EMA (R1), it is a strong sell zone, a short position can be taken here.
- When the two EMAs cross, the warning (yellow) and transition (orange) zones are determined based on the price's relationship with the two EMAs. These zones indicate potential trend shifts and trades should be taken with caution using additional indicators.

Trading signals are generated when the price moves across different zones. In the strong zones G1 and R1, signals can be directly taken. In the warning and transition zones, additional indicator confirmation is required.

StochRSI is also implemented to assist with identifying potential entry and exit points. Oversold and overbought readings from StochRSI can provide additional buy and sell signals.

## Advantages

- Simple and clean logic that is easy to understand and implement.
- Effectively catches medium to long term trends.
- Distinguishes strong zones from warning/transition zones, producing reliable trade signals.
- StochRSI inclusion further improves entry and exit timing.

## Risks

- As a pure trend following system, performance may suffer in non-trending markets.
- Inappropriate EMA period settings may cause false signals.
- Warning and transition zones carry higher trading risks and should be treated with caution.
- Lack of stop loss may lead to accentuated losses.

The risks can be reduced by:

1. Selecting strongly trending instruments and pausing trading when trends are weak.
2. Optimizing EMA periods to minimize false signals.
3. Introducing additional indicators for confirmation in warning/transition zones.
4. Implementing stop loss to control loss per trade.

## Enhancement Opportunities

The system can be further improved in the following areas:

1. Incorporate more indicators like MACD, KDJ for signal confirmation.
2. Add filters such as volume expansion in trading zones to improve trade success rate.
3. Dynamically adjust EMA periods based on market conditions for optimized parameters.
4. Implement stop loss strategies to exit trades at certain loss percentages.
5. Optimize position sizing and money management.
6. Test and fine-tune parameters across different instruments to find best configurations.

By introducing more signal confirmation, dynamic parameter optimization, stop loss, and proper money management, the system's robustness can be improved and risks reduced for better results.

## Conclusion

The Double EMA Crossover system is a trend following system based on comparing two EMAs. It identifies different trading zones based on the price's relationship with the EMAs to determine trend direction and generate trading signals. As a system with clear logic and easy implementation, it can effectively capture trends. While risks exist, they can be reduced through auxiliary indicators, dynamic optimization, stop loss, and money management. Overall, the Double EMA Crossover system is a solid trend following system suitable for medium to long-term traders.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|true|Fixed Timeframe|
|v_input_3|D|Timeframe in|
|v_input_4|12|Fast EMA|
|v_input_5|26|Slow EMA|
|v_input_6|true|EMA 100|
|v_input_7|2|Smoothing period (1 = no smoothing)|
|v_input_8|true|Fill Bar Color|
|v_input_9|true|Show EMA|
|v_input_10|true|Show Buy-Sell signal|