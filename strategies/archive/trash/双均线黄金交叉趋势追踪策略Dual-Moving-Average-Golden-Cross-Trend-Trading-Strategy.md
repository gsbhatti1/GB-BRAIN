> Name

Dual-Moving-Average-Golden-Cross-Trend-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/e58e42b80ae4a28c2f.png)
[trans]
## Overview

The Dual-Moving-Average-Golden-Cross-Trend-Trading-Strategy uses the calculation of dual moving averages (DEMA and TEMA) to detect their crossovers forming golden cross signals to judge overall market trends and issue trading signals. This strategy combines trend indicators and breakout signals, aiming to track medium to long-term trends and capture signals at the early stages of trend development.

## Strategy Logic

The core indicators of this strategy are a 200-period DEMA and two TEMAs with periods of 9 and 50. The DEMA is used to judge overall trends, while the TEMA crossovers generate trading signals.

When the short-term 9-period TEMA crosses above the medium-term 50-period TEMA, a buy signal is generated, indicating the start of an uptrend, allowing traders to go long. When the 9-period TEMA crosses below the 50-period TEMA, a sell signal is triggered, indicating the start of a downtrend, allowing traders to go short.

To filter false breakouts, the strategy adds a DEMA filter, so that TEMA crossover signals are only valid when prices are above the DEMA. This ensures signals are captured at the start of trends.

## Advantage Analysis

This strategy combines the strengths of moving averages for trend analysis and crossovers for signal generation across short- and medium-term timeframes. It considers two types of indicators for robust signals and less noise. 

Adding the DEMA filter enhances signal reliability by avoiding unfavorable market conditions like consolidations where signals underperform. This significantly reduces losses.

## Risk Analysis

Although the stable parameter settings of this strategy allow solid historical performance, some risks may exist in specific market environments:

1. Violent price swings may cause lagging crossover signals, unable to reflect timely price movements. This can result in missed entry timing or stop loss levels.
2. The long DEMA period may fail to convert signals quickly enough when trends reverse. This can amplify losses.
3. The strategy is more suited for medium to long-term trading. Insufficient profits may occur with short-term trades.

## Optimization Directions

Further enhancements for the strategy include:

1. Optimizing DEMA and TEMA parameters for better adaptation across different products and market environments. Testing more combinations can help find the optimal settings.
2. Adding more filters with indicators like volume and volatility to reinforce signal quality.
3. Adding stop losses when prices breach the DEMA to control losses.
4. Optimizing stop loss and take profit points based on typical price swing ranges.

## Conclusion

The Dual-Moving-Average-Golden-Cross-Trend-Trading-Strategy comprehensively considers multiple timeframe trends and crossover signals. The additional filter improves signal effectiveness to track medium to long-term trends for timely opportunity captures and avoid low-efficiency trades. This stable strategy suits various market regimes and offers a robust algorithm worth long-term deployment. Future optimizations on parameters and modules can further boost its stability and profitability.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Risk Percentage (%)|
|v_input_2|30|Stop Loss (pips)|
|v_input_3|90|Take Profit (pips)|
|v_input_4|200|DEMA Length|
|v_input_5|9|TEMA 9 Length|
|v_input_6|50|TEMA 50 Length|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-02-11 00:00:00
end: 2024-02-17 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Trading Strategy", shorttitle="DEMA+TEMA", overlay=true)

// Strategy Parameters
risk_percentage = input(1, title="Risk Percentage (%)") / 100
stop_loss_pips = input(30, title="Stop Loss (pips)")
take_profit_pips = input(90, title="Take Profit (pips)")
length_DEMA = input(200, title="DEMA Length")
length_TEMA_9 = input(9, title="TEMA 9 Length")
length_TEMA_50 = input(50, title="TEMA 50 Length")

// Indicators
dema = ta.ema(close, length_DEMA)
tema_9 = ta.ema(close, length_TEMA_9)
tema_50 = ta.ema(close, length_TEMA_50)
tema_9_50_cross_up = ta.crossover(tema_9, tema_50)
tema_9_50_cross_down = ta.crossunder(tema_9, tema_50)

// Risk and Trading Management
risk_per_trade = strategy.equity * risk_percentage
stop_loss = close - stop_loss_pips * syminfo.mintick
take_profit = close + take_profit_pips * syminfo.mintick

// Trading Conditions
long_condition = close > dema and tema_9_50_cross_up
short_condition = close > dema and tema_9_50_cross_down

// Trading Strategy
if (long_condition)
    strategy.entry("Buy", strategy.long)
    strategy.exit("Sell", "Buy", stop=stop_loss, limit=take_profit)
```