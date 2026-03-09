<!-- AUTO-TRANSLATE FAILED: the JSON object must be str, bytes or bytearray, not NoneType -->

## Overview

This strategy uses Double Exponential Moving Average (DEMA) to calculate price volatility and further smooths the volatility to detect trends in price fluctuations, going long when volatility rises and short when volatility falls.

## Strategy Logic

1. Calculate Double Exponential Moving Average (DEMA) of price using the formula: DEMA = 2*EMA(price, N) - EMA(EMA(price, N), N)

2. Calculate price volatility relative to DEMA: Volatility = (price - DEMA) / price * 100%

3. Apply DEMA smoothing on volatility again to get a trend signal

4. When the smoothed volatility crosses above a certain level, go long. When it crosses below that level, go short.

5. Can set to trade only during specific time periods.

## Advantages

1. DEMA catches trend changes faster than simple moving averages.

2. Volatility reflects market sentiment; an increase in volatility indicates dominance of bulls, while a decrease shows bears.

3. Smoothing volatility filters out short-term noise and captures major trends.

4. Trading within specific time periods avoids unnecessary slippage costs.

5. Stop loss and exit strategies control risk.

## Risks

1. DEMA may lag during strong trends, potentially missing the best entry points.

2. Volatility indicators might give false signals; they should be combined with other indicators for verification.

3. Should set a stop loss to prevent losses from escalating.

4. Missing trading opportunities outside of defined trading periods.

5. The selected trading period needs to be tested on historical data; an inappropriate time frame may reduce profits.

### Risk Management

1. Optimize DEMA parameters, using smaller N values.

2. Combine other indicators like RSI and MACD for confirmation.

3. Set a stop loss based on historical data and maximum tolerable loss.

4. Optimize the selection of trading periods.

5. Test optimal trading times separately for different products.

## Enhancement Opportunities

1. Test different DEMA parameter combinations to find the best smoothing effect.

2. Try other types of moving averages like EMA and SMA.

3. Smooth volatility with multiple parameters to find the best setting.

4. Add additional indicators for multi-factor verification.

5. Use machine learning methods to automatically optimize entry and exit parameters.

6. Test optimal parameter combinations separately for different products.

7. Implement stop loss and exit strategies to strictly control risk.

## Summary

This strategy captures trend changes in market sentiment by calculating smoothed DEMA volatility, going long when volatility rises and short when it falls. However, there are risks such as DEMA lag and false signals. Parameters should be optimized, strict stop losses implemented, and other indicators combined for confirmation. If used appropriately, this strategy can catch trend reversals and provide good investment returns.

---

## Strategy Arguments

| Argument      | Default Value | Description                                      |
| ------------- | ------------- | ------------------------------------------------- |
| v_input_1     | -2            | buyper                                            |
| v_input_2     | 2             | sellper                                           |
| v_input_3     | 50            | DEMA Length                                       |
| v_input_4     | true          | Band for OverBought                               |
| v_input_5     | -1            | Band for OverSold                                 |
| v_input_6     | 21            | DEMA to Calculate dema of DPD                     |
| v_input_7     | 2018          | yearfrom                                          |
| v_input_8     | 2019          | yearuntil                                         |
| v_input_9     | 6             | monthfrom                                         |
| v_input_10    | 12            | monthuntil                                        |
| v_input_11    | true          | dayfrom                                           |
| v_input_12    | 31            | dayuntil                                          |

## Source (PineScript)

```pinescript
// backtest
// start: 2022-10-17 00:00:00
// end: 2023-10-23 00:00:00
// period: 1d
// basePeriod: 1h
// exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]

//@version=2
strategy("DEMA of DPD Strategy", shorttitle="DPD% DEMA", overlay=false)

buyper = input(-2)
sellper = input(2)

demalen = input(50, title="DEMA Length")

e1 = ema(close, demalen)
e2 = ema(e1, demalen)
demaprice = 2 * e1 - e2

price = close
demadifper = ((price - demaprice) / price) * 100

OverDemaPer = input(1, title="Band for OverBought")
UnderDemaPer = input(-1, title="Band for OverSold")

band1 = hline(OverDemaPer)
band0 = hline(UnderDemaPer)
zeroline = 0
fill(band1, band0, color=green, transp=90)

demalen2 = input(21, title="DEMA to Calculate dema of DPD")
demaofdpd = ema(demadifper, demalen2)
demaofdpd2 = ema(demaofdpd, demalen2)
resultstrategy = 2 * demaofdpd - demaofdpd2

plot(resultstrategy, color=blue)

yearfrom = input(2018)
yearuntil = input(2019)
monthfrom = input(6)
monthuntil = input(12)
dayfrom = input(1)
dayuntil = input(31)

if (crossover(resultstrategy, buyper))
    strategy.entry("BUY", strategy.long, stop=close, oca_name="TREND", comment="BUY")
else
    strategy.cancel(id="BUY")

if (crossunder(resultstrategy, sellper)) 
    strategy.entry("SELL", strategy.short, stop=close, oca_name="TREND", comment="SELL")
else
    strategy.cancel(id="SELL")
```

## Detail

https://www.fmz.com/strategy/430050

## Last Modified

2023-10-24 16:04:37