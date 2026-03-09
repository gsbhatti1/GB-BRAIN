> Name

Dual-Reversal-Momentum-Index-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1ccebae9bb0794ccbb9.png)
[trans]

## Overview
This strategy is based on the Dual Reversal Momentum Index indicator for trading. It calculates a reversal momentum index over a certain time period using highest price, lowest price, and closing price, and generates trading signals when the index reverses down from the overbought zone or reverses up from the oversold zone. It also sets a breakout stop loss mechanism.

## Strategy Logic
The core indicator of this strategy is the Stochastic Momentum Index (SMI). The calculation formula of SMI is:

$$SMI = \frac{Close-(HH+LL)/2}{AVGDIFF/2} \times 100$$

Where HH is the highest price over the past N days, LL is the lowest price over the past N days, N is determined by parameter a; AVGDIFF is the M-day moving average of HH-LL, M is determined by parameter b.

SMI shows the reversal characteristic of prices. When the stock price approaches the highest point over the past N days, SMI is close to 100, indicating overbought of the stock; when it approaches the lowest point over the past N days, SMI is close to -100, indicating oversold. Buy/sell signals are generated when SMI reverses down from the 100 level or reverses up from the -100 level.

The strategy uses the M-day moving average SMA of SMI as the trading signal line. When SMI reverses down from the overbought zone and breaks below SMA, a buy signal is generated. When SMI reverses up from the oversold zone and breaks above SMA, a sell signal is generated.

Also, the strategy judges the candlestick body breakout for stop loss.

## Advantage Analysis
The advantages of this strategy are:

1. Utilizing the price reversal principle, it can generate trading signals at reversal points and capture reversal opportunities.
2. SMI combines highest price, lowest price, and closing price for judging overbought and oversold conditions, making more reliable signals.
3. With candlestick body breakout stop loss, it can exit positions in time and effectively control risks.
4. The strategy has few parameters and is easy to implement and optimize.

## Risk Analysis
There are also some risks for this strategy:

1. Reversal trading finds it hard to determine the exact timing of successful reversals, and may incur multiple losses before capturing trend reversal.
2. Wrong judgment of reversal points may lead to amplified losses.
3. The body breakout stop loss may be too sensitive with a high probability of being trapped.

The solutions are:
1. Optimize SMI parameters to adjust reversal trading frequency.
2. Combine other indicators to determine reversal timing.
3. Adjust body size for stop loss to prevent being too sensitive.

## Optimization
The strategy can be optimized in the following aspects:

1. Optimize parameters a and b of SMI to adjust the sensitivity of capturing reversals.
2. Add other indicators for judgment to avoid missing major trend directions, e.g., moving averages, volatility indicators, etc.
3. Add more stop loss methods to prevent being too sensitive or insensitive, such as trailing stop loss, curve stop loss, etc.
4. Incorporate machine learning models to judge the probability of reversal success, avoiding failed reversal trades.

## Conclusion
In conclusion, this is a dual-direction trading strategy based on the reversal momentum index SMI. The advantage lies in capturing more short-term trading opportunities by utilizing price reversal and generating signals at reversal points. But there are also typical risks of reversal trading. Parameter tuning and stop loss optimization are needed to prevent amplified losses. Overall speaking, this strategy suits investors interested in reversal trading, but must incorporate other indicators and strict stop loss to control risks.

||

## Source (PineScript)

```pinescript
/*backtest
start: 2023-11-01 00:00:00
end: 2023-11-30 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// Noro
// 2018

//@version=2
strategy(title = "Noro's Stochastic Strategy v1.0", shorttitle = "Stochastic str 1.0", overlay = false, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, pyrami
```