---
> Name

DEMA with TEMA Cross Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/c956109721342d9a4b.png)
[trans]

### I. Strategy Overview

This strategy is named the "Dual and Triple Exponential Moving Average Crossover Strategy." It combines the crossover signals of Dual Exponential Moving Average (DEMA) and Triple Exponential Moving Average (TEMA) to determine entry and exit points.

### II. Strategy Logic

This strategy primarily generates trading signals based on the crossover of Dual Exponential Moving Average (DEMA) and Triple Exponential Moving Average (TEMA).

The formula for DEMA is:

```pinescript
DEMA = 2*EMA1 - EMA2
```

Where EMA1 and EMA2 are Exponential Moving Averages with a period of N. DEMA combines the smoothing of EMA with its responsiveness.

The formula for TEMA is:

```pinescript
TEMA = 3*(EMA1 - EMA2) + EMA3
```

Where EMA1, EMA2, and EMA3 are Exponential Moving Averages with a period of N. TEMA filters out false breakouts by applying triple smoothing.

When DEMA crosses above TEMA, a buy signal is generated. When DEMA crosses below TEMA, a sell signal is generated. According to the crossover principle, it can capture cycle conversion and enter and exit the market timely.

### III. Strategy Advantages

1. Both DEMA and TEMA are optimized versions of EMA, enhancing trading accuracy.
2. DEMA smooths price changes, while TEMA filters out false breakouts, forming a synergy to improve the win rate.
3. Combining fast DEMA and slow TEMA, crossover signals are more reliable.
4. Timely capture of cycle conversion based on the crossover principle.

### IV. Strategy Risks and Solutions

1. Frequent crossover under market volatility may generate false signals. Parameter tuning is needed.
2. Inappropriate parameter setting can affect signal quality. Parameter optimization is required.
3. The strategy relies solely on technical indicators, lacking fundamental validation. Other indicators or models can be used to assist.

### V. Strategy Optimization

1. Test and optimize parameters for DEMA and TEMA to find the best combination.
2. Add other technical indicators for filtering, such as KDJ to determine long/short positions.
3. Incorporate machine learning predictions to validate signals and reduce false signals.
4. Evaluate trading volume or market sentiment to distinguish true from false crossovers.

### VI. Summary

This strategy generates trading signals from the crossover of DEMA and TEMA, combining DEMA's responsiveness and TEMA's filtering capability to improve accuracy. However, a single indicator combination is prone to illusions and requires multiple verification tools to form a systematic trading system for long-term stable profits.

||

### I. Strategy Overview

This strategy is named "Dual and Triple Exponential Moving Average Crossover Strategy." It combines the crossover signals of Dual Exponential Moving Average (DEMA) and Triple Exponential Moving Average (TEMA) to determine entries and exits.

### II. Strategy Logic

This strategy mainly uses the crossover of Dual Exponential Moving Average (DEMA) and Triple Exponential Moving Average (TEMA) to generate trading signals.

The formula for DEMA is:

```pinescript
DEMA = 2*EMA1 - EMA2
```

Where EMA1 and EMA2 are Exponential Moving Averages with period N. DEMA combines the smoothness of EMA and responsiveness.

The formula for TEMA is:

```pinescript
TEMA = 3*(EMA1 - EMA2) + EMA3
```

Where EMA1, EMA2, and EMA3 are Exponential Moving Averages with period N. TEMA filters out fake breakouts by triple smoothing.

When DEMA crosses above TEMA, a buy signal is generated. When DEMA crosses below TEMA, a sell signal is generated. According to the crossover principle, it can capture cycle conversion timely.

### III. Advantages

1. Both DEMA and TEMA optimize EMA, improving trading accuracy.
2. DEMA smooths price change, TEMA filters out fakeouts, forming synergy and improving win rate.
3. Combining fast DEMA and slow TEMA, crossover signals are more reliable.
4. Capturing cycle conversion timely based on the crossover principle.

### IV. Risks and Solutions

1. Frequent crossover under volatility causes false signals. Parameter tuning needed.
2. Inappropriate parameter setting affects signal quality. Parameter optimization required.
3. Lack of fundamental validation. Other indicators or models can assist.

### V. Optimization

1. Test and optimize parameters of DEMA and TEMA to find the best combination.
2. Add other technical indicators for filtering, e.g., KDJ for trend.
3. Add machine learning prediction to validate signals and reduce false signals.
4. Check trading volume or sentiment to judge true or fake crossover.

### VI. Summary

This strategy generates trading signals from the DEMA and TEMA crossover, combining DEMA's responsiveness and TEMA's filtering capability to improve accuracy. However, a single indicator combination is prone to illusions. Multi-verification tools are still needed to form a systematic trading system for long-term stable profits.

---

> Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|v_input_int_1|10|DEMA Length|
|v_input_1_close|0|DEMA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_int_2|8|TEMA Length|
|v_input_2_close|0|TEMA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|

> Source (PineScript)

```pinescript
//@version=5
strategy("DEMA-TEMA Cross Strategy", shorttitle="DEMA-TEMA Cross", overlay=true)

// Input options for Double EMA (DEMA)
dema_length = input.int(10, title="DEMA Length", minval=1)
dema_src = input(close, title="DEMA Source")

// Calculate Double EMA (DEMA)
dema_e1 = ta.ema(dema_src, dema_length)
dema_e2 = ta.ema(dema_e1, dema_length)
dema = 2 * dema_e1 - dema_e2

// Input options for Triple EMA (TEMA)
tema_length = input.int(8, title="TEMA Length", minval=1)
tema_src = input(close, title="TEMA Source")

// Calculate Triple EMA (TEMA)
tema_ema1 = ta.ema(tema_src, tema_length)
tema_ema2 = ta.ema(tema_ema1, tema_length)
tema_ema3 = ta.ema(tema_ema2, tema_length)
tema = 3 * (tema_ema1 - tema_ema2) + tema_ema3

// Crossover signals for long (small green arrow below candle)
crossover_long = ta.crossover(dema, tema)

// Crossunder signals for short (small red arrow above candle)
crossunder_short = ta.crossunder(dema, tema)

plotshape(crossunder_short ? 1 : na, title="Short Entry", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)
plotshape(crossover_long ? -1 : na, title="Long Entry", location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)

plot(dema, "DEMA", color=color.green)
plot(tema, "TEMA", color=color.blue)

if (crossover_long)
    strategy.entry("Long", strategy.long)

if (crossunder_short)
    strategy.entry("Short", strategy.short)
```

> Detail

https://www.fmz.com/strategy/437552

> Last Modified

2024-01-03 16:47:08
---