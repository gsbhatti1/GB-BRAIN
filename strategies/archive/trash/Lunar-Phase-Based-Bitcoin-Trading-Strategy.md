> Name

Lunar-Phase-Based-Bitcoin-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1b7d266631abad693bd.png)

[trans]

## Overview

This strategy uses the lunar phase cycle as trading signals, combined with RSI, MACD, OBV and other indicators to identify trading opportunities for cryptocurrencies like Bitcoin. The key advantage of this strategy is utilizing the lunar phase, an external factor, as the trading trigger, which is different from most strategies solely relying on technical indicators, thus can avoid market manipulation to some extent.

## Strategy Logic

The core logic of this strategy is to determine long or short opportunities based on different stages of the lunar phase cycle. The lunar phase is calculated as:

Lunar phase cycle length = 29.5305882 days
Given a known full moon time, the number of days from that full moon to the current time can be calculated  
Lunar age = Days since known full moon % Lunar phase cycle length 
Lunar phase value = (1 + cos(Lunar age / Lunar phase cycle length * 2 * π)) / 2

The lunar phase value fluctuates between 0 to 1. The larger the value means closer to the full moon, while the smaller value means closer to the new moon.

The strategy judges long or short opportunities based on lunar phase thresholds. If the lunar phase value is greater than the long threshold (default 0.51), there is a chance to go long. If the lunar phase value is less than the short threshold (default 0.49), there is a chance to go short.

In addition, the strategy also combines indicators like trading volume, RSI and MACD to avoid issuing trading signals during unfavorable conditions. It only opens positions when volume surges, RSI and MACD signals align.

## Advantage Analysis

The main advantages of this strategy are:

1. Utilize unique lunar phase trading signals, which can avoid market manipulation to some extent.
2. Combine multiple indicators to determine market conditions, avoiding trading in unfavorable environments.
3. Use ATR to calculate reasonable position size, effectively controlling the maximum loss per trade.
4. Set drawdown stop loss to prevent significant losses.
5. Judge fund flow direction with OBV, avoiding trading against the trend.
6. Set trailing stop loss to lock in profits.

In summary, this strategy fully utilizes the unique advantages of lunar phases, and combines multiple technical indicators to identify high-probability trading opportunities, while leveraging risk control mechanisms to effectively manage trading risks.

## Risk Analysis

The main risks of this strategy include:

1. Lunar phase and market movements may occasionally fail to align.
2. Improper drawdown stop loss may cause the strategy to stop prematurely.
3. The probability of false signals from MACD and RSI.
4. Improper trailing stop loss may result in the strategy missing larger profits.

To control these risks, the following measures can be taken:

1. Adjust lunar phase thresholds to ensure valid lunar signals.
2. Test multiple drawdown stop loss parameters and select the optimal.
3. Fine-tune MACD and RSI parameters to efficiently generate signals.
4. Test multiple sets of trailing stop loss parameters for maximum profits.

Through parameter optimization and combined indicators, trading risks can be mitigated to a large extent.

## Optimization Directions

There is still room for further optimization of this strategy:

1. Test different lunar parameters to find the optimal thresholds.
2. Try combining more indicators for ensemble trading and improve efficiency.
3. Optimize stop loss mechanism parameters to balance risks and returns.
4. Expand to more trading assets to test generalization ability.

## Conclusion

This strategy realizes efficient Bitcoin trading through unique lunar phase trading signals, combined with mainstream technical indicators. Compared to single indicator strategies, this strategy can better hedge against market manipulation risks and has unique advantages. By leveraging stop loss to prevent risks and parameter optimization, steady and good returns can be obtained. There is still large room for improving this strategy, and it has promising application prospects.

||

## Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|v_input_1|2023|Start year|
|v_input_2|2023|End year|
|v_input_3|0.51|Long Phase Threshold|
|v_input_4|0.49|Short Phase Threshold|
|v_input_5|0.05|Risk Per Trade (as a % of Equity)|
|v_input_6|0.01|Stop Loss Percentage|
|v_input_7|21|ATR Length for Volatility|
|v_input_8|0.1|Trailing Stop Percentage|
|v_input_9|0.1|Maximum Drawdown Percentage|
|v_input_10|7|Volume MA Length|


> Source (PineScript)