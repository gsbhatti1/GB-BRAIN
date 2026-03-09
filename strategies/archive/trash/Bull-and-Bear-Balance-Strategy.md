> Name

Bull and Bear Balance Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/c391ba63e21887730a.png)
[trans]


## Overview

The Bull and Bear Balance Strategy is an enhanced trend-following strategy. It analyzes the balance between bullish and bearish forces by examining the relationship between the current K-line and the previous K-line. This helps determine the current trend direction. When the balance between bullish and bearish forces is broken, the strategy generates trading signals. This strategy is inspired by the traditional Elder Ray indicator but has been improved to more accurately identify trends.

## Strategy Logic

The core indicator of this strategy is `nBBB`, which reflects the balance between bullish and bearish forces of the current K-line versus the previous K-line. The `nBBB` is calculated as follows:

```
nBBB = value2 - value
```

Where `value` and `value2` calculate the bullish and bearish forces of the current and previous K-lines, respectively. The calculation is complex and involves judgments on the relationship between the close, open, high, and low prices. In general, `value` measures the bullish/bearish force of the current K-line, while `value2` measures that of the previous K-line. Their difference reflects the change in bullish/bearish balance.

When `nBBB` falls below the threshold `SellLevel`, a short signal is generated. When `nBBB` rises above the threshold `BuyLevel`, a long signal is generated. The thresholds can be adjusted through parameters.

## Advantages

The main advantages of this strategy are:

1. Based on reversal signals from candlesticks, it can identify strong trend turning points.
2. By measuring the balance between bullish and bearish forces, the signals are more accurate and reliable.
3. By comparing the current K-line with the previous K-line, it filters out some noise for clearer signals.
4. It is applicable to different timeframes with good flexibility.
5. The `nBBB` indicator is intuitive, and the signals are simple and clear.

## Risks

Some risks to note:

1. The bullish/bearish balance indicator `nBBB` may generate false signals, requiring price confirmation.
2. Relying solely on `nBBB` has blind spots, better to incorporate other indicators.
3. The `SellLevel` and `BuyLevel` parameters directly impact performance and need careful optimization.
4. Signals may lag during extreme volatility, requiring risk assessment.
5. More suitable for mid/long-term, short-term may get whipsawed.

## Enhancements

Some ways to enhance the strategy:

1. Optimize `SellLevel` and `BuyLevel` based on historical backtests for the best fit.
2. Incorporate stop-loss mechanisms like trailing stop loss to control risks.
3. Add other indicators like volume, stochastic, etc. to improve decision accuracy.
4. Introduce machine learning to auto-optimize parameters and generate better signals.
5. Separate parameter optimization for different products and timeframes.

## Conclusion

The Bull and Bear Balance Strategy judges trend reversals by measuring changes in bullish/bearish balance, making it a relatively simple and practical trend-following strategy. It has certain advantages but also risks. With parameter optimization, stop losses, additional indicators, etc., it can be improved further. Overall, it presents an interesting quantitative approach worth deeper research and application.

|||

## Source (PineScript)

```pinescript
//@version=2
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 03/02/2017
//    This new indicator analyzes the balance between bullish and
//    bearish sentiment.
//    One can say that it is an improved analogue of Elder Ray indicator.
//    For more information, please see "Bull And Bear Balance Indicator" 
//    by Vadim Gimelfarb.
////////////////////////////////////////////////////////////
strategy(title = "Bull And Bear Balance Strategy")
SellLevel = input(-15, step=0.01)
BuyLevel = input(15, step=0.01)
reverse = input(false, title="Trade reverse")
hline(SellLevel, color=red, linestyle=line)
hline(BuyLevel, color=green, linestyle=line)
value =  iff (close < open , 
          iff (close[1] > open ,  max(close - open, high - low), high - low), 
           iff (close > open, 
             iff(close[1] > open, max(close[1] - low, high - close), max(open - low, high - close)), 
              iff(high - close > close - low, 
               iff (close[1] > open, max(close[1] - open, high - low), high - low), 
                 iff (high - close < close - low, 
                  iff(close > open, max(close - low, high - close),open - low), 
                   iff (close