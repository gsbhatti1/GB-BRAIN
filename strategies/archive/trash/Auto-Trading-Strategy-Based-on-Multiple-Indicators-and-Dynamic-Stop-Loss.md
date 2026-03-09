> Name

Auto-Trading-Strategy-Based-on-Multiple-Indicators-and-Dynamic-Stop-Loss

> Author

ChaoZhang

> Strategy Description

## Overview

This strategy combines the use of fast, medium, and slow Moving Average (EMA) lines along with MACD to generate comprehensive trading signals. It employs a dynamic stop-loss mechanism based on ATR to control risk levels. The strategy is suitable for medium-term automated trading.

## Strategy Logic

The strategy primarily uses EMA, MACD, and ATR indicators. EMA fast, medium, and slow lines form the trend judgment system. MACD helps generate trading signals while ATR sets dynamic stop-loss lines. Specifically, the trend direction is determined by the combination of EMA line positions. The entry for long positions occurs when the fast line crosses above the medium line, and exit happens when it crosses below. For short positions, entry comes when the fast line crosses below the medium line, with exit at the opposite condition. Stop-loss lines adjust dynamically based on ATR to manage risk according to market volatility.

## Advantage Analysis

- Combining multiple indicators makes trading signals accurate and reliable.
- The fast, medium, and slow EMA system provides clear trend judgment.
- MACD assists in entry to avoid false breakouts.
- Dynamic stop-loss better manages risk.
- The mechanical nature of the strategy suits automated trading well.

## Risks and Improvements

- Complex parameter settings require extensive optimization.
- Complex logic involving multiple indicators makes manual trading difficult.
- Should add additional filters like volume to avoid being trapped in positions.
- Can consider optimizing into a machine learning-based trading strategy for automated parameter tuning.

## Summary

The strategy integrates the advantages of multiple indicators, providing both accurate trend identification and effective risk management. Further enhancements through parameter optimization and adding additional filters can improve its robustness. Overall, it is a typical and reliable strategy suitable for medium-term automated trading with significant practical value.

||

## Overview

This strategy combines multiple indicators like fast, medium, slow MA lines and MACD to generate comprehensive trading signals, and uses dynamic stop loss based on ATR to control risk level. It is suitable for medium-term automated trading.

## Strategy Logic

The strategy mainly utilizes EMA, MACD, and ATR indicators. EMA fast, medium, and slow lines form the trend judgment system. MACD generates trading signals. ATR sets stop-loss lines dynamically. Specifically, the trend direction is determined by the combination of the EMA lines. The entry for long positions occurs when the fast line crosses above the medium line, and exit happens when it crosses below. For short positions, entry comes when the fast line crosses below the medium line, with exit at the opposite condition. Stop-loss lines adjust dynamically based on ATR to manage risk according to market volatility.

## Advantage Analysis

- Combining multiple indicators makes trading signals accurate and reliable.
- The fast, medium, and slow EMA system provides clear trend judgment.
- MACD assists in entry to avoid false breakouts.
- Dynamic stop-loss better manages risk.
- The mechanical nature of the strategy suits automated trading well.

## Risks and Improvements

- Complex parameter settings require extensive optimization.
- Complex logic involving multiple indicators makes manual trading difficult.
- Should add additional filters like volume to avoid being trapped in positions.
- Can consider optimizing into a machine learning-based trading strategy for automated parameter tuning.

## Summary

The strategy integrates the advantages of multiple indicators, providing both accurate trend identification and effective risk management. Further enhancements through parameter optimization and adding additional filters can improve its robustness. Overall, it is a typical and reliable strategy suitable for medium-term automated trading with significant practical value.

---

> Strategy Arguments


| Argument | Default | Description |
| --- | --- | --- |
| v_input_1 | 7 | EMA_Smooth_Period |
| v_input_2 | 7 | ST_VWAP_Period |
| v_input_3 | false | VWAP_TUNING_MULT |
| v_input_4 | 13 | ATR Period |
| v_input_5 | 2 | ATR Multiplier |
| v_input_6 | true | Show Buy/Sell Labels ? |
| v_input_7 | true | Highlight State ? |
| v_input_8 | 22 | StopLoss_Long_Adjust |
| v_input_9 | 16 | StopLoss_Short_Adjust |
| v_input_10 | true | fastLength |
| v_input_11 | 4 | medLength |
| v_input_12 | 24 | slowLength |
| v_input_13 | 8 | signalLength |
| v_input_14 | 2 | ATR_Signal_Period |
| v_input_15 | 0.986 | ATR_SIGNAL_FINE_TUNE |
| v_input_16 | true | StopLoss_Initial_Short |
| v_input_17 | 5 | StopLoss_Initial_Long |
| v_input_18 | 42 | VOLUME_CHECK_SHORT |
| v_input_19 | 16 | VOLUME_CHECK_LONG |
| v_input_20 | false | MAX_LOSS |
| v_input_21 | false | From Minute |
| v_input_22 | false | From Hour |
| v_input_23 | true | From Day |
| v_input_24 | true | From Month |
| v_input_25 | 2019 | From Year |
| v_input_26 | false | Till Minute |
| v_input_27 | false | Till Hour |
| v_input_28 | true | Till Day |
| v_input_29 | true | Till Month |
| v_input_30 | 2021 | Till Year |

---

> Source (PineScript)

```pinescript
//@version=4
strategy("STRAT_STEMWAP", overlay=true, pyramiding = 0, default_qty_value = 10, slippage = 3)

EMA_Smooth_Period = input(7, minval=1)
ST_EMA = ema(close, EMA_Smooth_Period)

ST_VWAP_Period = input(7, minval=1)
VWAP_TUNING_MULT = input(type=input.float, defval=0.000)
ST_VWAP = ema(vwap, ST_VWAP_Period)


ST_VWAP_TUNING = VWAP_TUNING_MULT * (ST_EMA - ST_VWAP)

length = input(title="ATR Period", type=input.integer, defval=13)
mult = input(title="ATR Multiplier", type=input.float, step=0.1, defval=2.0)
showLabels = input(title="Show Buy/Sell Labels ?", type=input.bool, defval=true)
highlightState = input(title="Highlight State ?", type=input.bool, defval=true)

atr = mult * atr(length)

StopLoss_Long_Adjust = input(22.00, type=input.float)
StopLoss_Short_Adjust = input(16.00, type=input.float)

longStop = (ST_EMA) - atr - (ST_VWAP_TUNING) - StopLoss_Long_Adjust
longStopPrev = nz(longStop[1], longStop)
longStop := (close[1]) > longStopPrev ? max(longStop, longStopPrev) : longStop

shortStop = (ST_EMA) + atr - (ST_VWAP_TUNING) + StopLoss_Short_Adjust
shortStopPrev = nz(shortStop[1], shortStop)
shortStop := (close[1]) < shortStopPrev ? min(shortStop, shortStopPrev) : shortStop

dir = 1
dir := nz(dir[1], dir)
dir := dir == -1 and (close) > shortStopPrev ? 1 : dir == 1 and (close) < longStopPrev ? -1 : dir

fastLength = input(1, minval=1), medLength=input(4, minval=1), slowLength=input(24, minval=1), signalLength=input(8,minval=1)
fastMA = ema(close, fastLength)
medMA = ema(close, medLength)
slowMA = ema(close, slowLength)
signal = crossover(fastMA, medMA) ? 1 : 0
entryLong = signal and close > longStop
exitShort = crossunder(medMA, fastMA) or (close < shortStop)
entryShort = crossunder(fastMA, medMA) ? 1 : 0
exitLong = crossover(medMA, fastMA) or (close > longStop)

if (entryLong)
    strategy.entry("Long", strategy.long)
    if (highlightState)
        label.new(x=bar_index, y=open, text="B", color=color.green, style=label.style_label_down, size=size.tiny)

if (exitShort)
    strategy.close("Long")
    if (highlightState)
        label.new(x=bar_index, y=open, text="S", color=color.red, style=label.style_label_up, size=size.tiny)
```

Please note that the PineScript code has been modified to include proper logic for entering and exiting positions based on the defined signals.