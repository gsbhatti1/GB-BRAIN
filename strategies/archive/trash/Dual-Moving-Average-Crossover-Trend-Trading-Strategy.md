> Name

Dual-Moving-Average-Crossover-Trend-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/c111fbe211c7771088.png)

[trans]

## Overview

This strategy determines market trends by calculating the crossover situations between the 9-day moving average (MA), 20-day MA, and 200-day MA. It combines the classic idea of dual MA crossover with the addition of a long-term trend judgment through the 200-day MA. This is a relatively stable and reliable trend trading strategy.

## Strategy Logic

This strategy mainly judges price trends by calculating the relationships between the 9-day MA, 20-day MA, and 200-day MA.

Firstly, it calculates the 9-day MA and 20-day MA. If the 9-day MA crosses above the 20-day MA, it generates a buy signal; if the 9-day MA crosses below the 20-day MA, it generates a sell signal. This is the most basic judgment rule of dual MA crossover.

Secondly, it calculates the 200-day MA to serve as an indicator for judging long-term trends. If the 20-day MA crosses above the 200-day MA, it signals a long-term bullish view; if the 20-day MA crosses below the 200-day MA, it signals a long-term bearish view.

Finally, it combines the relationships between the 9-day MA, 20-day MA, and 200-day MA to determine specific entry and exit points. Only when both the 9-day MA and 20-day MA cross over together in the same direction will actual trading signals be generated.

By calculating the crossover situations between multiple MAs, this strategy fully utilizes the trend tracking capability of MAs to effectively determine short-term and long-term price movements, thereby guiding buy and sell operations.

## Advantage Analysis

1. Using dual MA crossover can effectively capture mid-short term price trends and generate profits.
2. Adding 200-day MA judgment avoids going long during long-term downtrends, reducing losses.
3. Combining multiple MA relationships makes the signals more reliable and reduces ineffective trades.
4. MA crossover signals are clear and easy to judge, suitable for manual trading practice.
5. The simple and clean code is easy to understand and implement, good for quant trading beginners.
6. Flexible to optimize, like adjusting MA periods or adding other indicators.

## Risk Analysis

1. MA strategies are sensitive to parameter tuning; different MA periods can produce very different results.
2. Dual MA crossover only judges mid-short term trends and may miss longer-term big trends.
3. Crossover signals may lag, making it difficult to completely avoid losing trades.
4. Frequent trading increases commission and slippage costs, reducing actual profit potential.
5. The overly simple code may underperform in live trading, requiring optimization.

## Optimization Directions

1. Test different MA period combinations to find the optimal parameters.
2. Add stop loss strategies to strictly control per trade loss amount.
3. Consider position sizing according to changing market conditions.
4. Optimize entry signals, such as adding Momentum confirmation.
5. Optimize exits by setting reasonable take profit levels.
6. Add more indicators to judge trends and pullback probabilities.
7. Add machine learning models to discover more complex trading logic.

## Conclusion

This strategy combines the classic ideas of dual MA crossover and long-term MA trend judgment to guide trading decisions using MA trend-following characteristics. It has simple logic and is easy to understand and implement, good for quant trading beginners. However, it is parameter sensitive and has lagging issues that require further optimization and improvement. Overall, this strategy provides a basic framework that can be extended upon to develop more powerful trading systems. Investors can choose suitable elements to add and continuously optimize the strategy based on their needs, in order to achieve long-term excess returns in quantitative trading.

[/trans]

> Source (PineScript)

```pinescript
/*backtest
start: 2023-10-29 00:00:00
end: 2023-11-05 00:00:00
period: 3m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=1
strategy("Dieyson Swingtrade EMA 20+200 and bar & line color", overlay=true)

//bar color rules
Dgbar = close>close[1] and ema(close,20)>ema(close[1],20)
Drbar = close<close[1] and ema(close,20)<ema(close[1],20)

//Barcolors
barcolor(Dgbar ? green : na)
barcolor(Drbar ? red : na)

//MM09 Colorful

MMgreen9 = ema(close,9)>ema(close[1],9) and ema(close,20)>ema(close[1],20)
MMred9 = ema(close,9)<ema(close[1],9) and ema(close,9)<ema(close[1],9)
col8 = (MMgreen9 ? color(green,0) : na)
col28 = (MMred9 ? color(red,0) : na)
col38 = (not MMgreen9 and not MMred9 ? color(black,0) : na)

//plot(ema(close,9), color=col8
```