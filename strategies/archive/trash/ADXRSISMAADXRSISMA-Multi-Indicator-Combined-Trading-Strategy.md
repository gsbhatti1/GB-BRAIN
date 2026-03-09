> Name

ADXRSISMA multi-indicator combination trading strategy ADXRSISMA-Multi-Indicator-Combined-Trading-Strategy

> Author

ChaoZhang

> Strategy Description


[trans]

## Strategy Principle

This strategy uses a combination of technical indicators to identify trend directions and overbought and oversold areas to generate trading signals.

Key indicators include:

1. Average Directional Index (ADX): Determine the strength of the trend
2. Relative Strength Index (RSI): Determine overbought and oversold conditions
3. Simple Moving Average (SMA): Determine short-term trends
4. Extremely fast SAR indicator: Identify long-term and short-term trends
5. Channel breakout: Enter on trend breakout

Specific transaction logic:

1. ADX confirms the presence and strength of a trend
2. SAR confirms the consistent direction of both long-term and short-term trends
3. RSI identifies overbought and oversold levels
4. Enter when the price breaks through the SMA moving average
5. Enter when the price breaks through the channel

Multiple indicators verify each other to improve the accuracy of judgment, and different strategies are combined to form a systematic trading system.

## Strategic Advantages

- Multiple indicator combinations enhance signal quality
- Different strategy combinations for systematic entry
- ADX identifies trends, RSI determines overbought and oversold conditions
- SAR captures trends, SMA and channel breakouts for entry

## Strategy Risk

- Multiple parameter settings require repeated testing and optimization
- Combined conditions occur less frequently
- Difficult to handle conflicting signals from indicators

## Summary

This strategy fully utilizes the advantages of various indicators to build a robust trading system. However, parameter settings need to be optimized to ensure reasonable transaction frequency. Overall, it combines strong trend identification with efficient entry.

||


## Strategy Logic

This strategy integrates various technical indicators to identify trend direction and overbought/oversold levels for trade signals.

The main indicators used are:

1. Average Directional Index (ADX): Determine trend strength
2. Relative Strength Index (RSI): Identify overbought/oversold conditions
3. Simple Moving Average (SMA): Determine short-term trends
4. SuperTrend: Identify long/short term trends
5. Channel Breakout: Enter on trend breakout

The trading logic is:

1. ADX confirms the presence and strength of a trend
2. SuperTrend confirms alignment of long/short term trends
3. RSI identifies overbought/oversold levels
4. Enter on SMA crossover
5. Enter on channel breakout

The multi-indicator combination improves signal accuracy, combining different strategies into a systematic approach.

## Advantages

- Multiple indicators enhance signal quality
- Strategies combine for systematic entry
- ADX identifies trends, RSI determines overbought/oversold conditions
- SuperTrend captures trends, SMA and channel breakouts for entry

## Risks

- Multi-parameter tuning requires optimization
- Combination conditions occur less frequently
- Conflicting indicator signals difficult to resolve

## Summary

This strategy fully utilizes the strengths of various indicators to build a robust system. However, parameter optimization is key for ideal trade frequency. Overall, it combines strong trend identification with efficient entries.

[/trans]

> Strategy Arguments


| Argument | Default | Description |
| ---- | ---- | ---- |
| v_input_1 | 7 | ADX Smoothing |
| v_input_2 | 7 | DI Length |
| v_input_3 | 70 | OB |
| v_input_4 | 30 | OS |
| v_input_int_1 | 5 | Length |


> Source (PineScript)

```pinescript
/*backtest
start: 2023-09-12 00:00:00
end: 2023-09-13 00:00:00
Period: 45m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Combined Strategy", overlay=true, default_qty_value=100, initial_capital=1000, margin_long=0.1)

adxlen = input(7, title="ADX Smoothing")
dilen = input(7, title="DI Length")
dirmov(len) =>
    up = ta.change(high)
    down = -ta.change(low)
    plusDM = na(up) ? na : (up > down and up > 0 ? up : 0)
    minusDM = na(down) ? na : (down > up and down > 0 ? down : 0)
    truerange = ta.rma(ta.tr, len)
    plus = fixnan(100 * ta.rma(plusDM, len) / truerange)
    minus = fixnan(100 * ta.rma(minusDM, len) / truerange)
    [plus, minus]

adx(dilen, adxlen) =>
    [plus, minus] = dirmov(dilen)
    sum = plus + minus
    adx = 100 * ta.rma(math.abs(plus - minus) / (sum == 0 ? 1 : sum), adxlen)
    sig = adx(dilen, adxlen)

// The same on Pine Script™
pine_supertrend(factor, atrPeriod) =>
    src=hl2
    atr = ta.atr(atrPeriod)
    upperBand = src + factor * atr
    lowerBand = src - factor * atr
    prevLowerBand = nz(lowerBand[1])
    prevUpperBand = nz(upperBand[1])

    lowerBand := lowerBand > prevLowerBand or close[1] < prevLowerBand ? lowerBand : prevLowerBand
    upperBand := upperBand < prevUpperBand or close[1] > prevUpperBand ? upperBand : prevUpperBand
    int direction = na
    float superTrend = na
    prevSuperTrend = superTrend[1]
    if na(atr[1]) and ta.rsi(close, 21) < 66 and ta.rsi(close,3) > 80 and ta.rsi(close, 28) > 49 and sig > 20
        direction := 1
    else if prevSuperTrend == prevUpperBand
        direction := close > upperBand ? -1 : 1
    else
        direction := close < lowerBand ? 1 : -1
    superTrend := direction == -1 ? lowerBand : upperBand
    [superTrend, direction]

[pineSupertrend, pineDirection] = pine_supertrend(3, 10)
upTrend = pineDirection < 0
downTrend = pineDirection > 0

// Define the 20-period SMA
sma20 = ta.sma(close, 20)

a = ta.rsi(close,14)
OB = input(70)
OS = input(30)
os = a > OB
ob = a < OS

if upTrend and close > pineSupertrend and close > sma20 and os
    strategy.entry("Buy", strategy.long)

if ta.crossunder(close, sma20) or ob
    strategy.close_all()

// define when to breakout of channel
```