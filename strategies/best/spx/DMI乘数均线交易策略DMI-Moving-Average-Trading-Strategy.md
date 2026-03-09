> Name

DMI Multiplier Moving Average Trading Strategy DMI-Moving-Average-Trading-Strategy

> Author

ChaoZhang

> Strategy Description


[trans]

A new quantitative trading strategy that primarily relies on the DMI (Average Directional Movement Index) indicator to identify market bottoms and tops. This article will provide a detailed explanation of the rationale, advantages, and potential risks associated with this trading strategy.

## Strategy Logic

The DMI indicator, also known as Average Directional Movement Index, was introduced by Welles Wilder in the 1970s to assess market trends and their strength. The DMI consists of three lines:

- +DI: Represents the strength of an uptrend
- -DI: Represents the strength of a downtrend  
- ADX: Represents the overall trend strength

When +DI crosses above -DI, it indicates a strengthening uptrend and suggests entering a long position; when -DI crosses above +DI, it signals a strengthening downtrend and suggests entering a short position.

The core logic of this strategy is:

1. Enter a long position when +DI drops below 10 and -DI rises above 40.
2. Enter a short position when -DI drops below 10 and +DI rises above 40.

In other words, when the reverse DI diverges significantly from the forward DI, it can be determined that the current trend is likely to reverse, allowing for appropriate counter-trend trading positions.

To filter out noise, this strategy uses moving averages of DIs with parameters set as follows:

- The periods for +DI and -DI are both 11.
- The smoothing period for ADX is 11.

By adjusting the moving average parameters, the frequency of trading signals can be controlled.

This strategy primarily applies to NIFTY50 index options trading but can also be used on other products. Specifically in trading:

- Choose at-the-money options.
- Set a stop loss at 20%.
- Add positions if losses exceed 10%, but exit the trade if losses expand beyond 20% of initial capital.

## Advantages

Compared to simple DI crossover strategies, this strategy uses moving averages of DIs to effectively reduce whipsaws and decrease trade frequency, thus lowering transaction costs and slippage.

Compared to pure trend-following strategies, this strategy is more precise in identifying trend reversal points, enabling timely capture of opportunities around turning points.

The strategy optimization process is straightforward, making it easy to fine-tune for better performance.

## Risk Warnings

This strategy provides only directional signals. Specific stop loss and take profit requirements should be set according to individual risk preferences.

DMI may generate many false signals during range-bound periods; therefore, avoid using this strategy in non-trending markets.

DI crossovers cannot fully predict trend reversals and may have some timing errors. Other indicators should be used to validate trading signals.

## Conclusion

By filtering with DIs' moving averages, this strategy can effectively identify trend reversal opportunities. Compared to other trend-following strategies, it has the advantage of stronger reversal recognition capabilities. Overall, this strategy allows for flexible parameter tuning and is suitable as a module in a quantitative trading system. When using it, be cautious of false signals and properly assess market conditions.

||

Recently, I have developed a new quantitative trading strategy mainly based on the DMI indicator to identify bottoms and tops in the market. This article will explain in detail the rationale, advantages, and potential risks associated with this trading strategy.

## Strategy Logic

The DMI (Average Directional Movement Index) was created by Welles Wilder in the 1970s to gauge the trend and strength of the market. The DMI consists of three lines:

- +DI: Represents the strength of an uptrend
- -DI: Represents the strength of a downtrend  
- ADX: Represents the overall trend strength

When +DI crosses above -DI, it indicates a strengthening uptrend and suggests entering a long position; when -DI crosses above +DI, it signals a strengthening downtrend and suggests entering a short position.

The core logic of this strategy is:

1. Enter a long position when +DI drops below 10 and -DI rises above 40.
2. Enter a short position when -DI drops below 10 and +DI rises above 40.

In other words, when the reverse DI diverges significantly from the forward DI, it can be determined that the current trend is likely to reverse, allowing for appropriate counter-trend trading positions.

To filter out noise, this strategy uses moving averages of DIs with parameters set as follows:

- The periods for +DI and -DI are both 11.
- The smoothing period for ADX is 11.

By tuning the moving average parameters, the frequency of trading signals can be adjusted.

This strategy primarily applies to NIFTY50 index options trading. It can also be used on other products. Specifically for trading:

- Choose at-the-money options.
- Set a stop loss at 20%.
- Add positions if losses exceed 10%, but exit the trade if losses expand beyond 20% of initial capital.

## Advantages

Compared to simple DI cross strategies, this strategy uses moving averages of DIs to effectively reduce whipsaws and decrease trade frequency, thus lowering transaction costs and slippage. 

Compared to pure trend following strategies, this strategy is more precise at catching trend reversal points, enabling timely entries around turns.

The strategy optimization process is straightforward with flexible parameters for performance tuning.

## Risk Warnings

This strategy only provides directional signals. Specific requirements on stop loss and take profit should be set according to personal risk preference.

DMI may produce many false signals during range-bound periods. Avoid using this strategy in non-trending markets.

DI crossovers cannot fully predict trend reversals. There could be some timing errors. Other indicators should be used to validate the trading signals.

## Conclusion

By screening with DI moving averages, this strategy can effectively identify trend reversal opportunities. Compared to other trend following strategies, it has the advantage of stronger reversal recognition abilities. Overall, this strategy allows for flexible parameter tuning and is suitable as a module in quantitative trading systems. When using it, pay attention to false signals and properly assess market conditions.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_int_1|11|ADX Smoothing|
|v_input_int_2|11|DI Length|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-09-05 00:00:00
end: 2023-09-12 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © email_analysts
// This code gives indication on the chart to go long based on DMI and exit based on RSI. 
//Default value has been taken as 14 for DMI+ and 6 for RSI.
//@version=5
strategy(title="DMI Strategy", overlay=false)
lensig = input.int(11, title="ADX Smoothing", minval=1, maxval=50)
len = input.int(11, minval=1, title="DI Length")
up = ta.change(high)
down = -ta.change(low)
plusDM = na(up) ? na : (up > down and up > 0 ? up : 0)
minusDM = na(down) ? na : (down > up and down > 0 ? down : 0)
trur = ta.rma(ta.tr, len)
plus = fixnan(100 * ta.rma(plusDM, len) / trur)
minus = fixnan(100 * ta.rma(minusDM, len) / trur)
sum = plus + minus
adx = 100 * ta.rma(math.abs(plus - minus) / (sum == 0 ? 1 : sum), lensig)
//plot(adx, color=#F50057, title="ADX")
plot(plus, color=color.green, title="+DI")
plot(minus, color=color.red, title="-DI")
hlineup = hline(40, color=#787B86)
hlinelow = hline(10, color=#787B86)

buy = plus < 10 and minus > 40
if buy
    strategy.entry('long', strategy.long)

sell = plus > 40 and minus < 10
if sell
    strategy.entry('short', strategy.short)
```

> Detail

https://www.fmz.com/strategy/426579

> Last Modified

2023-09-13 14:42:19