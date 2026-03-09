> Name

Ehlers-MESA-Adaptive-Moving-Average-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

## Overview

This strategy is based on the Ehlers MESA Adaptive Moving Average and designed a trend trading strategy that tracks crossovers between two moving averages. It goes long when the fast line crosses above the slow line, and goes short when the fast line crosses below the slow line. This is a typical dual moving average crossover strategy.

## Strategy Logic

The core of this strategy is to compute two adaptive moving averages: the MAMA line and the FAMA line. The MAMA line is calculated as:

```pine
alpha = fl / dphase
alpha = iff(alpha < sl, sl, iff(alpha > fl, fl, alpha))  
mama = alpha*src + (1 - alpha)*nz(mama[1])
```

Where `fl` is the fast limit, `sl` is the slow limit, and `dphase` is the phase difference. `alpha` adaptively adjusts based on the phase difference to achieve adaptive smoothing.

The FAMA line is calculated as:

```pine
fama = .5*alpha*mama + (1 - .5*alpha)*nz(fama[1])
```

The FAMA line is a low pass filtered smoothing of the MAMA line.

The strategy compares the magnitude relationship between the MAMA and FAMA lines to determine if the market is currently in an uptrend or a downtrend, and generates trading signals based on this.

## Advantage Analysis

The strategy has the following advantages:

1. Uses adaptive moving averages where the parameters automatically adjust based on market changes, without needing fixed manually set parameters.
2. The low pass filter FAMA line can filter out false breakouts.
3. Using a dual moving average design can track medium to long term trends.
4. Simple and clear strategy logic that is easy to understand and modify.
5. Visual indicators that clearly show trading signals.

## Risk Analysis

The strategy also has some risks:

1. Dual line crossover strategies can generate excessive trading signals, proper drawdown and interval controls are recommended.
2. Complex MAMA and FAMA calculations, improper parameter settings may cause curve distortions.
3. Adaptive parameters may lead to overfitting, verification with other technical indicators is needed.
4. Dual line crossovers have time lags, may miss trend turning points.
5. Need to watch out for stop loss risks from false breakouts.

## Optimization Directions

The strategy can be optimized in the following areas:

1. Optimize parameter settings to find the best fast limit and slow limit combinations.
2. Add stop loss strategies to strictly control per trade stop loss.
3. Add other indicators to filter signals, such as MACD, RSI etc to avoid false breakouts.
4. Add trend judging indicators to avoid counter trend trades.
5. Optimize entry pace by adjusting crossover requirements to reduce overly frequent trading.
6. Optimize profit taking strategies according to trend strength.
7. Test parameter differences between various products to find optimal parameter combinations.

## Summary

Overall, this is a typical trend following strategy, using the Ehlers MESA adaptive moving averages to construct a visualized indicator and generate trading signals through dual line crossovers. The strategy has advantages like adaptive parameters, filtering of false breakouts and visualization, but also risks like time lags and excessive trading. Future improvements can be made through parameter optimization, stop loss strategies, signal filtering etc to make the strategy more robust.

---

> Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|v_input_1_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|0.4|Fast Limit|
|v_input_3|0.04|Slow Limit|


> Source (PineScript)

```pinescript
//@version=2
// @author ChaoZhang
//
// List of my public indicators: http://bit.ly/1LQaPK8 
// List of my app-store indicators: http://blog.tradingview.com/?p=970 
//
strategy("Ehlers MESA Adaptive Moving Average [ChaoZhang with ekoronin fix]", shorttitle="EMAMA_CZ (ekoronin fix)", overlay=false, calc_on_every_tick=true, precision=0)
src = input(close, title="Source")
fl = input(0.4, title="Fast Limit")
sl = input(0.04, title="Slow Limit")
pi = 3.1415926
sp = (4*src + 3*src[1] + 2*src[2] + src[3]) / 10.0
dt = (.0962*sp + .5769* nz(sp[2]) - .5769* nz(sp[4]) - .0962* nz(sp[6]))*(.075* nz(p[1]) + .54)
q1 = (.0962*dt + .5769* nz(dt[2]) - .5769* nz(dt[4]) - .0962* nz(dt[6]))*(.075* nz(p[1]) + .54)
i1 = nz(dt[3])
jI = (.0962*i1 + .5769* nz(i1[2]) - .5769* nz(i1[4]) - .0962* nz(i1[6]))*(.075* nz(p[1]) + .54)
jq = (.0962*jI + .5769* nz(jI[2]) - .5769* nz(jI[4]) - .0962* nz(jI[6]))*(.075* nz(p[1]) + .54)
```