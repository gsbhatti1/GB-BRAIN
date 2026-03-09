> Name

Bollinger Band Reversal Based Quantitative Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/11e3f849e2a685688b7.png)
[trans]

## Overview

This strategy is named "Bollinger Band Reversal Based Quantitative Strategy." It uses the upper and lower bands of Bollinger Bands to determine buy and sell decisions. When the stock price approaches the lower band and shows signs of a downward breakout, it suggests that the price may be reversing; thus, initiate a long position. When the price rises to the upper band, it indicates that the price may reverse downwards; therefore, go short.

## Strategy Logic

The strategy employs the RSI indicator to determine buy entries. Specifically, it checks if the closing price of the most recent bar is lower than the lowest price of the previous 6 bars, with the Bollinger Band Width (BBW) greater than a threshold, and the Bollinger Band Ratio (BBR) within a set range. If these criteria are met, it indicates that the price may be reversing; hence, initiate a long position.

The exit is straightforward. When RSI exceeds 70, indicating overheated prices, close the long position.

## Advantage Analysis

The main advantage of this strategy lies in using Bollinger Bands' upper and lower bands to determine entries. When BB reverses direction, enter or exit to capture short-term reversal opportunities. Compared to simple RSI strategies, this approach has more rigorous entry criteria, reducing the probability of incorrect trades.

Additionally, the strategy is sensitive to parameters. By adjusting BBW and BBR, it can be optimized for different products, leading to better performance.

## Risk Analysis

The main risk involves Bollinger Bands not perfectly predicting price reversals. If timing is off, it may lead to missing optimal entry points or floating losses.

Moreover, short-term fluctuations might trigger frequent entries and exits, increasing transaction costs and slippage. Insufficient reversal momentum can result in losses from forced exits.

## Optimization Directions

The strategy can be improved through the following aspects:

1. **Parameter Optimization**: Test and fine-tune BBW, BBR, and other parameters for different trading products to select optimal settings.
2. **Stop Loss Mechanisms**: Implement trailing stop loss or time-based stop loss mechanisms to control maximum losses.
3. **Combining with Other Indicators**: Integrate indicators like KDJ and MACD to make entry signals more reliable.
4. **Enhanced Exit Logic**: Simplify the current exit logic by setting appropriate trailing profit-taking levels or exiting based on volatility.

## Conclusion

This strategy utilizes Bollinger Bands' characteristics to identify potential reversal points for entries and exits. Compared to single indicators like RSI, it provides more accurate timing. Through parameter tuning and stop-loss/take-profit settings, it can be made more reliable. However, BB predictions are not perfect, so the strategy’s performance has some inherent randomness.

||

## Overview

The strategy is named "Bollinger Band Reversal Based Quantitative Strategy." It utilizes the upper and lower rails of Bollinger Bands to determine buy and sell signals. When prices are near the lower rail and show signs of a downward breakout, it suggests that a reversal may occur; thus, initiate a long position. Conversely, when prices rise to the upper rail, indicating potential price reversals, go short.

## Strategy Logic

This strategy uses the RSI indicator to determine entry points for buys. Specifically, it checks if the closing price of the most recent bar is lower than the lowest price of the previous 6 bars, with the Bollinger Band Width (BBW) greater than a threshold and the Bollinger Band Ratio (BBR) within a set range. If these conditions are met, it indicates that a potential reversal might occur; thus, initiate a long position.

The exit is simple. When RSI exceeds 70, indicating overheating in prices, close the long position.

## Advantage Analysis

The primary advantage of this strategy lies in its use of Bollinger Bands’ upper and lower rails to determine entry points. When BB reverses direction, it enters or exits positions to capture short-term reversal opportunities. Compared to simple RSI strategies, this approach offers more rigorous criteria for entries, reducing the likelihood of incorrect trades.

Additionally, the strategy is sensitive to parameters. By adjusting BBW and BBR, it can be optimized for different products, leading to better results.

## Risk Analysis

The main risk involves the Bollinger Bands not perfectly predicting price reversals. If timing is off, it may result in missing optimal entry points or experiencing floating losses.

Furthermore, short-term fluctuations could trigger frequent entries and exits, increasing transaction costs and slippage. Insufficient reversal momentum might also lead to forced exits at a loss.

## Optimization Directions

The strategy can be improved through the following aspects:

1. **Parameter Optimization**: Use more sophisticated methods to test and optimize parameters like BBW and BBR for different trading products.
2. **Stop Loss Mechanisms**: Implement moving stop losses or time-based stop losses to control maximum potential losses.
3. **Combining with Other Indicators**: Incorporate other indicators such as KDJ and MACD to enhance the reliability of buy signals.
4. **Enhanced Exit Logic**: Simplify the current exit logic by setting appropriate profit-taking levels based on volatility.

## Conclusion

This strategy leverages Bollinger Bands’ characteristics to identify potential reversal points for entries and exits. Compared to single indicators like RSI, it offers more precise entry timing. Through parameter tuning and stop-loss/take-profit settings, the strategy can be made more reliable. However, BB predictions are not perfect, so there is still some randomness in performance.

[/trans]

> Strategy Arguments


| Argument | Default | Description |
|----------|---------|-------------|
| v_input_1 | 15      | bbw3        |
| v_input_2 | 0.45    | bbr3level   |
| v_input_3 | 0.4480  | bbrlower    |
| v_input_4 | 0.4560  | bbrhigher   |
| v_input_5 | 7       | sincelowestmin|
| v_input_6 | 57      | sincelowestmax|
| v_input_7 | 20      | length      |

> Source (PineScript)

```pinescript
/* backtest
start: 2022-11-15 00:00:00
end: 2023-11-21 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4

// study(title="Bolinger strategy", overlay=true)
strategy("Bolinger strategy", currency="SEK", default_qty_value=10000, default_qty_type=strategy.cash, max_bars_back=50)
len = 5
src = close
up = rma(max(change(src), 0), len)
down = rma(-min(change(src), 0), len)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

bbw3level = input(15, title="bbw3")
bbr3level = input(0.45, title="bbr3level")
bbrlower = input(0.4480, title="bbrlower")
bbrhigher = input(0.4560, title="bbrhigher")
sincelowestmin = input(7, title="sincelowestmin")
sincelowestmax = input(57, title="sincelowestmax")

length = input(20, minval=1)
mult = 20
src3 = close[3]
basis3 = sma(src3, length)
dev3 = mult * stdev(src3, length)
upper3 = basis3 + dev3
lower3 = basis3 - dev3
bbr3 = (src3 - lower3) / (upper3 - lower3)
bbw3 = (upper3 - lower3) / basis3 * 100

basis = sma(src, length)
dev = mult * stdev(src, length)
upper = basis + dev
lower = basis - dev
bbr = (src - lower) / (upper - lower)
bbw = (upper - lower) / basis * 100

criteriamet = 0
crossUnderB0 = crossunder(bbr, 0)

since_x_under = barssince(crossUnderB0)

sincelowest = barssince(close[6] > close[3] and close[5] > close[3] and close[4] > close[3] and close[2] > close[3] and close[1] > close[3] and close > close[3] and bbw3 > bbw3level and bbr3 < bbr3level) //  and bbr3 < 0 

if sincelowest > sincelowestmin and sincelowest < sincelowestmax and bbr > bbrlower and bbr < bbrhigher
    criteriamet := 1
else
    criteriamet := 0

// exit 
exitmet = 0
if rsi > 70
    exitmet := 1
``` 

This PineScript defines the strategy's logic, including its entry criteria and exit condition. The script uses Bollinger Bands and RSI to determine when to enter or exit a trade based on specific conditions. Adjustments can be made through the input parameters for better performance in different market conditions.