> Name

DEMA Quick Double Exponential Moving Average Strategy DEMA-Double-Exponential-Moving-Average-Strategy

> Author

ChaoZhang

> Strategy Description


## Overview

The DEMA quick double exponential moving average strategy is a short-term trading strategy based on the DEMA (Double Exponential Moving Average). It combines the smoothing of moving averages with the fast response advantage of EMAs, aiming to capture short-term price trends by utilizing crossovers between DEMA lines for profitable trades.

## Strategy Logic

The strategy mainly relies on golden crosses and death crosses between the DEMA fast line and DEMA slow line to determine buy and sell signals. 

Specifically, the fast line is calculated as:

`demaFast = 2 * ema(close, fastPeriod) - ema(ema(close, fastPeriod), fastPeriod)`

And the slow line is:

`demaSlow = 2 * ema(close, slowPeriod) - ema(ema(close, slowPeriod), slowPeriod)`

Where `fastPeriod` and `slowPeriod` represent the periods of the fast and slow lines respectively.

When the fast line crosses above the slow line, a buy signal is generated. When the fast line crosses below the slow line, a sell signal is generated.

```python
buy = crossover(demaSlow, demaFast)
sell = crossunder(demaSlow, demaFast)
```

The strategy determines the trading direction based on DEMA line crossovers.

## Advantage Analysis

Compared to traditional moving averages, DEMA lines are more sensitive and can react to price changes faster. This allows the strategy to capture more short-term trading opportunities.

Also, DEMA lines incorporate the smoothing characteristics of moving averages, which helps filter out some market noise and avoid false signals.

In addition, using a combination of fast and slow lines can help avoid fake crossovers. With different parameter settings, crossover signals become more reliable.

Overall, the DEMA quick double exponential moving average strategy has the advantages of fast response, noise filtering, and stable reliable signals.

## Risk Analysis

Although more stable than EMAs, DEMA lines can still suffer from false crossovers, generating incorrect signals. This can be addressed by fine-tuning the period parameters of the fast and slow line to ensure enough sensitivity and stability.

Also, as a short-term strategy, it is sensitive to trading costs. High trading frequency or small trade sizing may erode profits. Reasonable trade parameters should be set to control costs.

Lastly, no technical indicator strategy can completely avoid stop loss. Proper risk management should be implemented to limit downside.

## Optimization Directions

There are still areas for optimization:

1. Test different period combinations to find the optimal parameters.
2. Incorporate other indicators like RSI to confirm signals and avoid false signals.
3. Optimize stop loss mechanisms, such as trailing stop loss to lock in profits.
4. Optimize capital management strategies, such as position sizing based on account size or volatility adjusted sizing.

## Conclusion

The DEMA quick double exponential moving average strategy is overall a stable short-term trading strategy. It has fast response and smoothing capabilities. Compared to SMAs, it can capture more short-term opportunities. With parameter tuning and proper mechanisms, the strategy's profitability and stability can be further improved. It suits investors who desire high-frequency short-term trading.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|32|DEMA FAST Period|
|v_input_2|2|DEMA SLOW Period|
|v_input_3|120|Resolution - not lower than chart|


> Source (PineScript)

```pinescript
/*backtest
start: 2022-09-19 00:00:00
end: 2023-09-25 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

strategy(title = "DEMA Strategy", shorttitle = "DEMA Strategy",initial_capital=1000, commission_value=0.2, commission_type = strategy.commission.percent, default_qty_value=100 , overlay = false, pyramiding=10, default_qty_type=strategy.percent_of_equity)
//@Moneros 2017
//Based on The DEMA is a fast-acting moving average that is more responsive to market changes than a traditional moving average
// !!!! IN ORDER TO AVOID REPAITING ISSUES !!!!
// !!!! DO NOT VIEW IN LOWER RESOLUTIONS THAN res/2 PARAMETER  !!!!
// for example res = 120 view >= 60m  res = 60 view >= 30m
// the length of the DEMA sampling shouldn't be longer than a candle 

// Best profits tested on BTCUSD
//res = 105 slowPeriod = 2 fastPeriod = 32
//res = 125 slowPeriod = 3 fastPeriod = 21
//res = 120 slowPeriod = 2 fastPeriod = 32 
//res = 130 slowPeriod = 1 fastPeriod = 24 
//res = 40 slowPeriod = 4 fastPeriod = 93 
//res = 60 view >= 30m
```