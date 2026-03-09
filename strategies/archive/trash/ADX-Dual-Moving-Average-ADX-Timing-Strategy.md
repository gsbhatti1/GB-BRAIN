> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|Length ADX|
|v_input_2|14|Length ADXR|
|v_input_float_1|13|Signal1|
|v_input_float_2|45|Signal2|
|v_input_int_1|14|(?●═════ 2/20 EMA ═════●)Length|
|v_input_bool_1|false|(?●═════ MISC ═════●)Trade reverse|
|v_input_int_2|true|(?●═════ Time Start ═════●)From Day|
|v_input_int_3|true|From Month|
|v_input_int_4|2005|From Year|


> Source (PineScript)

``` pinescript
//@version=5
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 04/04/2022
// This is combo strategies for get a cumulative signal. 
//
// First strategy
// This indicator plots 2/20 exponential moving average. For the Mov 
// Avg X

```

## Overview

The Dual Moving Average ADX Timing strategy identifies trends by combining 2/20 moving averages and the ADXR indicator to generate trading signals at the beginning of trends. It first uses the 2/20 exponential moving averages to determine the price trend direction, then further confirms the trend signal in combination with the ADXR indicator, thus producing more reliable trading signals.

## Strategy Logic

The core logic of the Dual Moving Average ADX Timing strategy is based on the following main components:

1. **2/20 Exponential Moving Average (EMA)**
   - Uses 2 EMAs with different parameters of 2 and 20 days.
   - A upward cross of price over 2-day EMA is considered a bullish signal.
   - A downward cross of price below 20-day EMA is considered a bearish signal.

2. **ADXR Indicator**
   - ADXR is a variant of the ADX indicator.
   - It calculates a simple moving average of ADX to smooth out fluctuations.
   - ADXR below a threshold implies weaker trend.
   - ADXR above a threshold implies stronger trend.

3. **Trading Signals**
   - A bullish signal is generated when 2-day EMA Golden Cross AND ADXR is higher than threshold.
   - A bearish signal is generated when 20-day EMA Dead Cross AND ADXR is lower than threshold.
   - Combining with ADXR filters out some false breaks and enhances real trend signals.

The main innovation of this strategy is using ADXR indicator to identify trends in the initial stage, and combining it with traditional moving average signals to improve quality and stability.

## Advantages

The main advantages of the Dual Moving Average ADX Timing strategy are:

1. Combining dual MAs and ADXR, signals are more accurate and reliable with false signals filtered out.
2. Identifying early trend by using ADXR to detect initial stage of trends.
3. Flexible ADXR parameter tuning to adapt to changing market conditions.
4. Simple and clear logic, easy to understand, convenient to adjust parameters.
5. Applicable in various market environments with decent historical performance.

## Risks

There are also several main risks for this strategy:

1. Improper ADXR parameter setting may lead to missing trades.
   - Expand ADXR parameter range or adjust by products.

2. More false signals may occur in special market conditions.
   - Consider combining with other indicators for further signal filtering.

3. Fixed EMA parameters fail to adapt to market changes.
   - Test optimization version with adaptive EMA parameters.

4. Unable to identify trading ranges, may generate excessive insignificant trades.
   - Add extra logic or indicators to detect ranging markets.

## Enhancement Directions

The strategy can be further optimized and enhanced from the following aspects:

1. EMA parameter optimization for automatic adaptation to market conditions.
2. Expand ADXR parameter range for capturing more effective trading signals.
3. Add extra trend judgment indicators for combinational signals to improve quality.
4. Add stop loss strategies and take profit standards to control per trade risks.
5. Optimize money management for dynamic position sizing based on account status.

## Conclusion

The Dual Moving Average ADX Timing strategy innovatively combines traditional dual moving averages and the ADXR indicator to improve signal quality and enhance stability. It can effectively identify the initial stage of trends with decent historical performance. The strategy has ample room for optimization to make it robust and profitable across more complex markets.
```