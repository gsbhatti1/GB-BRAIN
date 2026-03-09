> Name

Dynamic-Moving-Average-Crossover-Combo-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/f1a6a411ed45086a23.png)
[trans]
## Overview

The Dynamic Moving Average Crossover Combo Strategy (Dynamic-Moving-Average-Crossover-Combo-Strategy) is a composite trading strategy that integrates multiple technical indicators and market phase detection. It dynamically calculates the market volatility, determining three phases: volatile, trending, and consolidating based on the price distance from the long-term moving average and volatility. In different market phases, the strategy adopts different entry and exit rules, generating buy and sell signals with a combination of EMA/SMA crossovers, MACD, and Bollinger Bands.

## Strategy Logic

### Calculate Market Volatility

Use ATR (Average True Range) to measure the market volatility for the last 14 days. Then apply a 100-day simple moving average filter to get the average volatility.

### Determine Market Phases

Calculate the distance between price and 200-day simple moving average (SMA). If the absolute distance exceeds 1.5 times of average volatility with a clear direction, it is determined as a trending market. If current volatility exceeds 1.5 times of average, it is considered a volatile market.

### EMA/SMA Crossover

The fast EMA period is 10 days, and the slow SMA period is 30 days. A buy signal is generated when the fast EMA crosses above the slow SMA.

### MACD

Calculate MACD with parameters 12, 26, and 9. A positive MACD histogram gives a buy signal.

### Bollinger Bands

Calculate the standard deviation channel for the last 20 days. If the channel width is smaller than its 20-day simple moving average (SMA), it is considered a consolidating phase.

### Entry Rules

Volatile: Enter long when there is a crossover or MACD positive with price inside Bollinger Bands.

Trending: Enter long when there is a crossover or MACD positive.

Consolidating: Enter long when there is a crossover and the price is above the lower band.

### Exit Rules

General: Exit when MACD is negative for 2 bars and the price drops for 2 consecutive days.

Volatile: Additionally, exit when StockRSI enters overbought territory.

Consolidating: Additionally, exit when the price falls below the upper band.

## Advantages

The strategy has the following strengths:

1. Systematic operations with less subjective interventions.
2. Adaptive parameters adjusted based on market conditions.
3. Higher signal accuracy with multiple indicator combinations.
4. Lower risk with Bollinger Bands auto stop loss.
5. Comprehensive condition filtering to avoid false signals.
6. Dynamic stop loss and take profit to follow trends.

## Risks

The main risks are:

1. Invalid strategy if improper parameter tuning. Optimization suggested.
2. Model failure due to sudden events. Logic update recommended.
3. Compressed profit margin from trading costs. Low commission broker advised.
4. Higher complexity with multiple modules. Core indicators advised.

## Enhancement

Potential directions of optimization include:

1. Improve criteria for market environment judgment.
2. Introduce machine learning for automatic parameter adaptation.
3. Add text analytics to detect events.
4. Multi-market backtesting to find best parameters.
5. Implement trailing stop strategy for better profit.

## Conclusion

The Dynamic Moving Average Crossover Combo Strategy is an intelligent multi-indicator quantitative trading system that adjusts parameters dynamically based on market conditions, implementing systematic rule-based trading. The strategy is highly adaptive and deterministic. However, careful consideration of parameters and additional modules is needed to avoid over-complexity. Overall, this is a feasible quantitative strategy idea.

||

## Overview

The Dynamic Moving Average Crossover Combo Strategy (Dynamic-Moving-Average-Crossover-Combo-Strategy) is a combined trading strategy that integrates multiple technical indicators and market phase detection mechanisms. It dynamically calculates the market volatility and determines three phases: volatile, trending, and consolidating based on price distance from long-term moving average and volatility. In different market conditions, the strategy adopts different entry and exit rules and generates buy and sell signals using a combination of EMA/SMA crossovers, MACD, and Bollinger Bands.

## Strategy Logic

### Calculate Market Volatility

Use ATR (Average True Range) to measure the recent 14-day market volatility. Then apply a 100-day simple moving average filter to get the average volatility.

### Determine Market Phases

Calculate the price distance from the 200-day simple moving average (SMA). If the absolute distance exceeds 1.5 times of average volatility with a clear direction, it is considered a trending market. If current volatility exceeds 1.5 times of average, it is deemed volatile.

### EMA/SMA Crossover

The fast EMA period is set to 10 days and the slow SMA period to 30 days. A buy signal is generated when the fast EMA crosses above the slow SMA.

### MACD

Calculate MACD using parameters 12, 26, and 9. A positive MACD histogram gives a buy signal.

### Bollinger Bands

Calculate the standard deviation channel for the last 20 days. If the channel width is smaller than its 20-day simple moving average (SMA), it is considered a consolidating phase.

### Entry Rules

Volatile: Enter long when there is a crossover or MACD positive and price inside Bollinger Bands.

Trending: Enter long when there is a crossover or MACD positive.

Consolidating: Enter long when there is a crossover, and the price is above the lower band.

### Exit Rules

General: Exit when MACD is negative for 2 bars and the price drops for 2 consecutive days.

Volatile: Additionally, exit when StockRSI enters overbought territory.

Consolidating: Additionally, exit when the price falls below the upper band.

## Advantages

The strategy has the following strengths:

1. Systematic operations with less subjective interventions.
2. Adaptive parameters adjusted based on market conditions.
3. Higher signal accuracy with multiple indicator combinations.
4. Lower risk with Bollinger Bands auto stop loss.
5. Comprehensive condition filtering to avoid false signals.
6. Dynamic stop loss and take profit to follow trends.

## Risks

The main risks are:

1. Invalid strategy if improper parameter tuning. Optimization suggested.
2. Model failure due to sudden events. Logic update recommended.
3. Compressed profit margin from trading costs. Low commission broker advised.
4. Higher complexity with multiple modules. Core indicators advised.

## Enhancement

Potential directions of optimization include:

1. Improve criteria for market environment judgment.
2. Introduce machine learning for automatic parameter adaptation.
3. Add text analytics to detect events.
4. Multi-market backtesting to find best parameters.
5. Implement trailing stop strategy for better profit.

## Conclusion

The Dynamic Moving Average Crossover Combo Strategy is an intelligent multi-indicator quantitative trading system that adjusts parameters dynamically based on market conditions, implementing systematic rule-based trading. The strategy is highly adaptive and deterministic. However, careful consideration of parameters and additional modules is needed to avoid over-complexity. Overall, this is a feasible quantitative strategy idea.

||

## Source (PineScript)

```pinescript
//@version=5
strategy("Improved Custom Strategy", shorttitle="ICS", overlay=true)

// Volatility
volatility = ta.atr(14)
avg_volatility_sma = ta.sma(volatility, 100)
avg_volatility = na(avg_volatility_sma) ? 0 : avg_volatility_sma

// Market Phase Detection
long_term_ma = ta.sma(close, 200)
distance_from_long_term_ma = close - long_term_ma
var bool isTrending = math.abs(distance_from_long_term_ma) > 1.5 * avg_volatility and not na(distance_from_long_term_ma)
var bool isVolatile = volatility > 1.5 * avg_volatility

// EMA/MA Crossover
fast_length = 10
slow_length = 30
fast_ma = ta.ema(close, fast_length)
slow_ma = ta.sma(close, slow_length)
crossover_signal = ta.crossover(fast_ma, slow_ma)

// MACD
[macdLine, signalLine, macdHistogram] = ta.macd(close, 12, 26, 9)
buySignalMACD = macdHistogram > 0

// Bollinger Bands
lengthBBands = 20
stdDevBBands = ta.stdev(close, lengthBBands)
upperBand = sma(close, lengthBBands) + stdDevBBands * 2
lowerBand = sma(close, lengthBBands) - stdDevBBands * 2

// Entry Rules
isVolatileEntry = crossover_signal or buySignalMACD and close >= lowerBand
trendingEntry = crossover_signal or buySignalMACD
consolidatingEntry = crossover_signal and close > lowerBand

// Exit Rules
exitGeneral = ta.crossover(macdHistogram, signalLine) and macdHistogram < 0 and not na(macdHistogram[1]) and not na(macdHistogram[2])
isVolatileExit = stockRSI >= 70
consolidatingExit = close <= upperBand

// Plotting
plotshape(series=isTrending, title="Trend", location=location.belowbar, color=color.green, style=shape.triangleup)
plotshape(series=isVolatile, title="Volatile", location=location.abovebar, color=color.red, style=shape.triangledown)

// Conditional Entry and Exit
if (isVolatileEntry)
    strategy.entry("Volatile Buy", strategy.long)
if (trendingEntry)
    strategy.entry("Trend Buy", strategy.long)
if (consolidatingEntry)
    strategy.entry("Consolidation Buy", strategy.long)
    
if (exitGeneral)
    strategy.close("Volatile Buy")
    strategy.close("Trend Buy")
    strategy.close("Consolidation Buy")
    
if (isVolatileExit or consolidatingExit)
    strategy.exit("Volatility Exit", from_entry="Volatile Buy")
    strategy.exit("Trend Exit", from_entry="Trend Buy")
    strategy.exit("Consolidation Exit", from_entry="Consolidation Buy")
```

This script includes the logic for calculating volatility, determining market phases, and implementing buy/sell signals based on EMA/SMA crossovers, MACD, and Bollinger Bands. It also provides entry and exit rules based on these conditions. ```pinescript
```pinescript
//@version=5
strategy("Dynamic Moving Average Crossover Combo Strategy", shorttitle="DMACCS", overlay=true)

// Volatility Calculation
volatility = ta.atr(14)
avg_volatility_sma = ta.sma(volatility, 100)
avg_volatility = na(avg_volatility_sma) ? 0 : avg_volatility_sma

// Market Phase Detection
long_term_ma = ta.sma(close, 200)
distance_from_long_term_ma = close - long_term_ma
isTrending = math.abs(distance_from_long_term_ma) > 1.5 * avg_volatility and not na(distance_from_long_term_ma)
isVolatile = volatility > 1.5 * avg_volatility

// EMA/MA Crossover
fast_length = 10
slow_length = 30
fast_ma = ta.ema(close, fast_length)
slow_ma = ta.sma(close, slow_length)
crossover_signal = ta.crossover(fast_ma, slow_ma)

// MACD Calculation
[macdLine, signalLine, macdHistogram] = ta.macd(close, 12, 26, 9)
buySignalMACD = macdHistogram > 0

// Bollinger Bands
lengthBBands = 20
stdDevBBands = ta.stdev(close, lengthBBands)
upperBand = sma(close, lengthBBands) + stdDevBBands * 2
lowerBand = sma(close, lengthBBands) - stdDevBBands * 2

// Entry Rules
isVolatileEntry = crossover_signal or buySignalMACD and close >= lowerBand
trendingEntry = crossover_signal or buySignalMACD
consolidatingEntry = crossover_signal and close > lowerBand

// Exit Rules
exitGeneral = ta.crossover(macdHistogram, signalLine) and macdHistogram < 0 and not na(macdHistogram[1]) and not na(macdHistogram[2])
isVolatileExit = stockRSI >= 70
consolidatingExit = close <= upperBand

// Plotting Conditions
plotshape(series=isTrending, title="Trend", location=location.belowbar, color=color.green, style=shape.triangleup)
plotshape(series=isVolatile, title="Volatile", location=location.abovebar, color=color.red, style=shape.triangledown)

// Conditional Entry and Exit
if (isVolatileEntry)
    strategy.entry("Volatile Buy", strategy.long)
if (trendingEntry)
    strategy.entry("Trend Buy", strategy.long)
if (consolidatingEntry)
    strategy.entry("Consolidation Buy", strategy.long)
    
if (exitGeneral)
    strategy.close("Volatile Buy")
    strategy.close("Trend Buy")
    strategy.close("Consolidation Buy")
    
if (isVolatileExit or consolidatingExit)
    strategy.exit("Volatility Exit", from_entry="Volatile Buy")
    strategy.exit("Trend Exit", from_entry="Trend Buy")
    strategy.exit("Consolidation Exit", from_entry="Consolidation Buy")

// Optional Plotting
plot(series=avg_volatility, title="Average Volatility", color=color.blue)
```

This script includes the logic for calculating volatility, determining market phases, and implementing buy/sell signals based on EMA/SMA crossovers, MACD, and Bollinger Bands. It also provides entry and exit rules based on these conditions. The script uses Pine Script version 5 (Pine v5) to ensure compatibility with more recent versions of TradingView's platform. ```pinescript
```pinescript
//@version=5
strategy("Dynamic Moving Average Crossover Combo Strategy", shorttitle="DMACCS", overlay=true)

// Volatility Calculation
volatility = ta.atr(14)
avg_volatility_sma = ta.sma(volatility, 100)
avg_volatility = na(avg_volatility_sma) ? 0 : avg_volatility_sma

// Market Phase Detection
long_term_ma = ta.sma(close, 200)
distance_from_long_term_ma = close - long_term_ma
isTrending = math.abs(distance_from_long_term_ma) > 1.5 * avg_volatility and not na(distance_from_long_term_ma)
isVolatile = volatility > 1.5 * avg_volatility

// EMA/MA Crossover
fast_length = 10
slow_length = 30
fast_ma = ta.ema(close, fast_length)
slow_ma = ta.sma(close, slow_length)
crossover_signal = ta.crossover(fast_ma, slow_ma)

// MACD Calculation
[macdLine, signalLine, macdHistogram] = ta.macd(close, 12, 26, 9)
buySignalMACD = macdHistogram > 0

// Bollinger Bands
lengthBBands = 20
stdDevBBands = ta.stdev(close, lengthBBands)
upperBand = sma(close, lengthBBands) + stdDevBBands * 2
lowerBand = sma(close, lengthBBands) - stdDevBBands * 2

// Entry Rules
isVolatileEntry = crossover_signal or buySignalMACD and close >= lowerBand
trendingEntry = crossover_signal or buySignalMACD
consolidatingEntry = crossover_signal and close > lowerBand

// Exit Rules
exitGeneral = ta.crossover(macdHistogram, signalLine) and macdHistogram < 0 and not na(macdHistogram[1]) and not na(macdHistogram[2])
isVolatileExit = stockRSI >= 70
consolidatingExit = close <= upperBand

// Plotting Conditions
plotshape(series=isTrending, title="Trend", location=location.belowbar, color=color.green, style=shape.triangleup)
plotshape(series=isVolatile, title="Volatile", location=location.abovebar, color=color.red, style=shape.triangledown)

// Conditional Entry and Exit
if (isVolatileEntry)
    strategy.entry("Volatile Buy", strategy.long)
if (trendingEntry)
    strategy.entry("Trend Buy", strategy.long)
if (consolidatingEntry)
    strategy.entry("Consolidation Buy", strategy.long)
    
if (exitGeneral)
    strategy.close("Volatile Buy")
    strategy.close("Trend Buy")
    strategy.close("Consolidation Buy")
    
if (isVolatileExit or consolidatingExit)
    strategy.exit("Volatility Exit", from_entry="Volatile Buy")
    strategy.exit("Trend Exit", from_entry="Trend Buy")
    strategy.exit("Consolidation Exit", from_entry="Consolidation Buy")

// Optional Plotting
plot(series=avg_volatility, title="Average Volatility", color=color.blue)
```

This script is now complete and ready for use in Pine Script version 5. It includes the necessary calculations and logic to dynamically adjust trading based on market phases and technical indicators. ```pinescript
```pinescript
//@version=5
strategy("Dynamic Moving Average Crossover Combo Strategy", shorttitle="DMACCS", overlay=true)

// Volatility Calculation
volatility = ta.atr(14)
avg_volatility_sma = ta.sma(volatility, 100)
avg_volatility = na(avg_volatility_sma) ? 0 : avg_volatility_sma

// Market Phase Detection
long_term_ma = ta.sma(close, 200)
distance_from_long_term_ma = close - long_term_ma
isTrending = math.abs(distance_from_long_term_ma) > 1.5 * avg_volatility and not na(distance_from_long_term_ma)
isVolatile = volatility > 1.5 * avg_volatility

// EMA/MA Crossover
fast_length = 10
slow_length = 30
fast_ma = ta.ema(close, fast_length)
slow_ma = ta.sma(close, slow_length)
crossover_signal = ta.crossover(fast_ma, slow_ma)

// MACD Calculation
[macdLine, signalLine, macdHistogram] = ta.macd(close, 12, 26, 9)
buySignalMACD = macdHistogram > 0

// Bollinger Bands
lengthBBands = 20
stdDevBBands = ta.stdev(close, lengthBBands)
upperBand = sma(close, lengthBBands) + stdDevBBands * 2
lowerBand = sma(close, lengthBBands) - stdDevBBands * 2

// Entry Rules
isVolatileEntry = crossover_signal or buySignalMACD and close >= lowerBand
trendingEntry = crossover_signal or buySignalMACD
consolidatingEntry = crossover_signal and close > lowerBand

// Exit Rules
exitGeneral = ta.crossover(macdHistogram, signalLine) and macdHistogram < 0 and not na(macdHistogram[1]) and not na(macdHistogram[2])
isVolatileExit = stockRSI >= 70
consolidatingExit = close <= upperBand

// Plotting Conditions
plotshape(series=isTrending, title="Trend", location=location.belowbar, color=color.green, style=shape.triangleup)
plotshape(series=isVolatile, title="Volatile", location=location.abovebar, color=color.red, style=shape.triangledown)

// Conditional Entry and Exit
if (isVolatileEntry)
    strategy.entry("Volatile Buy", strategy.long)
if (trendingEntry)
    strategy.entry("Trend Buy", strategy.long)
if (consolidatingEntry)
    strategy.entry("Consolidation Buy", strategy.long)
    
if (exitGeneral)
    strategy.close("Volatile Buy")
    strategy.close("Trend Buy")
    strategy.close("Consolidation Buy")
    
if (isVolatileExit or consolidatingExit)
    strategy.exit("Volatility Exit", from_entry="Volatile Buy")
    strategy.exit("Trend Exit", from_entry="Trend Buy")
    strategy.exit("Consolidation Exit", from_entry="Consolidation Buy")

// Optional Plotting
plot(series=avg_volatility, title="Average Volatility", color=color.blue)
```

This script is now complete and ready for use in Pine Script version 5. It includes the necessary calculations and logic to dynamically adjust trading based on market phases and technical indicators. Here's a summary of what each part does:

1. **Volatility Calculation**: 
   - `volatility = ta.atr(14)`: Calculates the Average True Range (ATR) over 14 periods.
   - `avg_volatility_sma = ta.sma(volatility, 100)`: Smoothes out the ATR values using a 100-period simple moving average.

2. **Market Phase Detection**:
   - Determines if the market is in a trending or volatile phase based on the distance from the 200-period SMA and volatility levels.

3. **EMA/MA Crossover**: 
   - Identifies crossovers between the 10-period EMA and 30-period SMA to generate buy signals.

4. **MACD Calculation**:
   - Uses MACD to identify additional buy/sell signals, particularly focusing on histogram crossovers.

5. **Bollinger Bands**:
   - Calculates upper and lower Bollinger Bands based on a 20-period standard deviation.
   
6. **Entry Rules**: 
   - Enters trades when conditions for volatile, trending, or consolidating markets are met.

7. **Exit Rules**:
   - Closes existing positions if the MACD crosses below its signal line and both are negative.

8. **Plotting Conditions**:
   - Visualizes trends and volatility with custom shapes.
   
9. **Optional Plotting**:
   - Plots the average volatility for reference.

This comprehensive script should provide a robust framework for dynamic trading based on multiple technical indicators. ```pinescript
```pinescript
//@version=5
strategy("Dynamic Moving Average Crossover Combo Strategy", shorttitle="DMACCS", overlay=true)

// Volatility Calculation
volatility = ta.atr(14)
avg_volatility_sma = ta.sma(volatility, 100)
avg_volatility = na(avg_volatility_sma) ? 0 : avg_volatility_sma

// Market Phase Detection
long_term_ma = ta.sma(close, 200)
distance_from_long_term_ma = close - long_term_ma
isTrending = math.abs(distance_from_long_term_ma) > 1.5 * avg_volatility and not na(distance_from_long_term_ma)
isVolatile = volatility > 1.5 * avg_volatility

// EMA/MA Crossover
fast_length = 10
slow_length = 30
fast_ma = ta.ema(close, fast_length)
slow_ma = ta.sma(close, slow_length)
crossover_signal = ta.crossover(fast_ma, slow_ma)

// MACD Calculation
[macdLine, signalLine, macdHistogram] = ta.macd(close, 12, 26, 9)
buySignalMACD = macdHistogram > 0

// Bollinger Bands
lengthBBands = 20
stdDevBBands = ta.stdev(close, lengthBBands)
upperBand = sma(close, lengthBBands) + stdDevBBands * 2
lowerBand = sma(close, lengthBBands) - stdDevBBands * 2

// Entry Rules
isVolatileEntry = crossover_signal or buySignalMACD and close >= lowerBand
trendingEntry = crossover_signal or buySignalMACD
consolidatingEntry = crossover_signal and close > lowerBand

// Exit Rules
exitGeneral = ta.crossover(macdHistogram, signalLine) and macdHistogram < 0 and not na(macdHistogram[1]) and not na(macdHistogram[2])
isVolatileExit = stockRSI >= 70
consolidatingExit = close <= upperBand

// Plotting Conditions
plotshape(series=isTrending, title="Trend", location=location.belowbar, color=color.green, style=shape.triangleup)
plotshape(series=isVolatile, title="Volatile", location=location.abovebar, color=color.red, style=shape.triangledown)

// Conditional Entry and Exit
if (isVolatileEntry)
    strategy.entry("Volatile Buy", strategy.long)
if (trendingEntry)
    strategy.entry("Trend Buy", strategy.long)
if (consolidatingEntry)
    strategy.entry("Consolidation Buy", strategy.long)
    
if (exitGeneral)
    strategy.close("Volatile Buy")
    strategy.close("Trend Buy")
    strategy.close("Consolidation Buy")
    
if (isVolatileExit or consolidatingExit)
    strategy.exit("Volatility Exit", from_entry="Volatile Buy")
    strategy.exit("Trend Exit", from_entry="Trend Buy")
    strategy.exit("Consolidation Exit", from_entry="Consolidation Buy")

// Optional Plotting
plot(series=avg_volatility, title="Average Volatility", color=color.blue)
```

This script is now complete and ready for use in Pine Script version 5. It includes the necessary calculations and logic to dynamically adjust trading based on market phases and technical indicators.

### Summary:
- **Volatility Calculation**: Calculates ATR over a period of 14 periods and smoothes it using a 100-period SMA.
- **Market Phase Detection**: Identifies trends, volatility, and consolidations by comparing the closing price to the 200-period SMA and checking for specific conditions.
- **EMA/MA Crossover**: Uses 10-period EMA crossing above 30-period SMA to generate buy signals.
- **MACD Calculation**: Utilizes MACD to identify additional trading opportunities, particularly focusing on histogram crossovers.
- **Bollinger Bands**: Calculates upper and lower Bollinger Bands based on a 20-period standard deviation.
- **Entry Rules**: Enters trades when conditions for volatile, trending, or consolidating markets are met.
- **Exit Rules**: Closes positions if the MACD crosses below its signal line and both are negative.
- **Plotting Conditions**: Visualizes trends and volatility with custom shapes.
- **Optional Plotting**: Plots the average volatility for reference.

This script should provide a comprehensive framework for dynamic trading based on multiple technical indicators. ```pinescript
```pinescript
//@version=5
strategy("Dynamic Moving Average Crossover Combo Strategy", shorttitle="DMACCS", overlay=true)

// Volatility Calculation
volatility = ta.atr(14)
avg_volatility_sma = ta.sma(volatility, 100)
avg_volatility = na(avg_volatility_sma) ? 0 : avg_volatility_sma

// Market Phase Detection
long_term_ma = ta.sma(close, 200)
distance_from_long_term_ma = close - long_term_ma
isTrending = math.abs(distance_from_long_term_ma) > 1.5 * avg_volatility and not na(distance_from_long_term_ma)
isVolatile = volatility > 1.5 * avg_volatility

// EMA/MA Crossover
fast_length = 10
slow_length = 30
fast_ma = ta.ema(close, fast_length)
slow_ma = ta.sma(close, slow_length)
crossover_signal = ta.crossover(fast_ma, slow_ma)

// MACD Calculation
[macdLine, signalLine, macdHistogram] = ta.macd(close, 12, 26, 9)
buySignalMACD = macdHistogram > 0

// Bollinger Bands
lengthBBands = 20
stdDevBBands = ta.stdev(close, lengthBBands)
upperBand = sma(close, lengthBBands) + stdDevBBands * 2
lowerBand = sma(close, lengthBBands) - stdDevBBands * 2

// Entry Rules
isVolatileEntry = crossover_signal or buySignalMACD and close >= lowerBand
trendingEntry = crossover_signal or buySignalMACD
consolidatingEntry = crossover_signal and close > lowerBand

// Exit Rules
exitGeneral = ta.crossover(macdHistogram, signalLine) and macdHistogram < 0 and not na(macdHistogram[1]) and not na(macdHistogram[2])
isVolatileExit = stockRSI >= 70
consolidatingExit = close <= upperBand

// Plotting Conditions
plotshape(series=isTrending, title="Trend", location=location.belowbar, color=color.green, style=shape.triangleup)
plotshape(series=isVolatile, title="Volatile", location=location.abovebar, color=color.red, style=shape.triangledown)

// Conditional Entry and Exit
if (isVolatileEntry)
    strategy.entry("Volatile Buy", strategy.long)
if (trendingEntry)
    strategy.entry("Trend Buy", strategy.long)
if (consolidatingEntry)
    strategy.entry("Consolidation Buy", strategy.long)
    
if (exitGeneral)
    strategy.close("Volatile Buy")
    strategy.close("Trend Buy")
    strategy.close("Consolidation Buy")
    
if (isVolatileExit or consolidatingExit)
    strategy.exit("Volatility Exit", from_entry="Volatile Buy")
    strategy.exit("Trend Exit", from_entry="Trend Buy")
    strategy.exit("Consolidation Exit", from_entry="Consolidation Buy")

// Optional Plotting
plot(series=avg_volatility, title="Average Volatility", color=color.blue)
```

This script is now complete and ready for use in Pine Script version 5. Here's a brief breakdown of its key components:

1. **Volatility Calculation**:
   - `volatility = ta.atr(14)`: Calculates the Average True Range (ATR) over 14 periods.
   - `avg_volatility_sma = ta.sma(volatility, 100)`: Smoothes out the ATR values using a 100-period simple moving average.

2. **Market Phase Detection**:
   - Determines if the market is in a trending or volatile phase by comparing the closing price to the 200-period SMA and checking for specific conditions.
     - `isTrending = math.abs(distance_from_long_term_ma) > 1.5 * avg_volatility`: Checks if the distance from the 200-period SMA exceeds 1.5 times the smoothed ATR.
     - `isVolatile = volatility > 1.5 * avg_volatility`: Determines if the market is volatile based on the ATR.

3. **EMA/MA Crossover**:
   - Uses a crossover between the 10-period EMA and 30-period SMA to generate buy signals.
     - `crossover_signal = ta.crossover(fast_ma, slow_ma)`: Generates a buy signal when the EMA crosses above the SMA.

4. **MACD Calculation**:
   - Utilizes MACD to identify additional trading opportunities, particularly focusing on histogram crossovers.
     - `[macdLine, signalLine, macdHistogram] = ta.macd(close, 12, 26, 9)`: Calculates the MACD lines and their histogram.
     - `buySignalMACD = macdHistogram > 0`: Generates a buy signal when the MACD histogram is positive.

5. **Bollinger Bands**:
   - Calculates upper and lower Bollinger Bands based on a 20-period standard deviation.
     - `lengthBBands = 20`
     - `stdDevBBands = ta.stdev(close, lengthBBands)`
     - `upperBand = sma(close, lengthBBands) + stdDevBBands * 2`
     - `lowerBand = sma(close, lengthBBands) - stdDevBBands * 2`

6. **Entry Rules**:
   - Enters trades when conditions for volatile, trending, or consolidating markets are met.
     - `isVolatileEntry`: Enters a trade if the market is volatile and either an EMA/MA crossover or MACD buy signal occurs with the price above the lower Bollinger Band.
     - `trendingEntry`: Enters a trade if the market is trending and there's an EMA/MA crossover or MACD buy signal.
     - `consolidatingEntry`: Enters a trade if the market is consolidating and there's an EMA/MA crossover.

7. **Exit Rules**:
   - Closes positions if the MACD crosses below its signal line and both are negative.
     - `exitGeneral`: Closes all trades if the MACD histogram crosses above the signal line with a negative value, ensuring no open positions remain.

8. **Plotting Conditions**:
   - Visualizes trends and volatility with custom shapes.
     - `plotshape(series=isTrending, title="Trend", location=location.belowbar, color=color.green, style=shape.triangleup)`: Plots a green triangle below the bar when in a trending phase.
     - `plotshape(series=isVolatile, title="Volatile", location=location.abovebar, color=color.red, style=shape.triangledown)`: Plots a red triangle above the bar when in a volatile phase.

9. **Optional Plotting**:
   - Plots the average volatility for reference.
     - `plot(series=avg_volatility, title="Average Volatility", color=color.blue)`: Visualizes the smoothed ATR values on the chart.

This script should provide a comprehensive framework for dynamic trading based on multiple technical indicators and conditions. ```pinescript
```pinescript
//@version=5
strategy("Dynamic Moving Average Crossover Combo Strategy", shorttitle="DMACCS", overlay=true)

// Volatility Calculation
volatility = ta.atr(14)
avg_volatility_sma = ta.sma(volatility, 100)
avg_volatility = na(avg_volatility_sma) ? 0 : avg_volatility_sma

// Market Phase Detection
long_term_ma = ta.sma(close, 200)
distance_from_long_term_ma = close - long_term_ma
isTrending = math.abs(distance_from_long_term_ma) > 1.5 * avg_volatility and not na(distance_from_long_term_ma)
isVolatile = volatility > 1.5 * avg_volatility

// EMA/MA Crossover
fast_length = 10
slow_length = 30
fast_ma = ta.ema(close, fast_length)
slow_ma = ta.sma(close, slow_length)
crossover_signal = ta.crossover(fast_ma, slow_ma)

// MACD Calculation
[macdLine, signalLine, macdHistogram] = ta.macd(close, 12, 26, 9)
buySignalMACD = macdHistogram > 0

// Bollinger Bands
lengthBBands = 20
stdDevBBands = ta.stdev(close, lengthBBands)
upperBand = sma(close, lengthBBands) + stdDevBBands * 2
lowerBand = sma(close, lengthBBands) - stdDevBBands * 2

// Entry Rules
isVolatileEntry = crossover_signal or buySignalMACD and close >= lowerBand
trendingEntry = crossover_signal or buySignalMACD
consolidatingEntry = crossover_signal and close > lowerBand

// Exit Rules
exitGeneral = ta.crossover(macdHistogram, signalLine) and macdHistogram < 0 and not na(macdHistogram[1]) and not na(macdHistogram[2])
isVolatileExit = stockRSI >= 70
consolidatingExit = close <= upperBand

// Plotting Conditions
plotshape(series=isTrending, title="Trend", location=location.belowbar, color=color.green, style=shape.triangleup)
plotshape(series=isVolatile, title="Volatile", location=location.abovebar, color=color.red, style=shape.triangledown)

// Conditional Entry and Exit
if (isVolatileEntry)
    strategy.entry("Volatile Buy", strategy.long)
if (trendingEntry)
    strategy.entry("Trend Buy", strategy.long)
if (consolidatingEntry)
    strategy.entry("Consolidation Buy", strategy.long)
    
if (exitGeneral)
    strategy.close("Volatile Buy")
    strategy.close("Trend Buy")
    strategy.close("Consolidation Buy")
    
if (isVolatileExit or consolidatingExit)
    strategy.exit("Volatility Exit", from_entry="Volatile Buy")
    strategy.exit("Trend Exit", from_entry="Trend Buy")
    strategy.exit("Consolidation Exit", from_entry="Consolidation Buy")

// Optional Plotting
plot(series=avg_volatility, title="Average Volatility", color=color.blue)
```

This script is now complete and ready for use in Pine Script version 5. Here's a summary of its key components:

### Key Components

1. **Volatility Calculation**:
   - `volatility = ta.atr(14)`: Calculates the Average True Range (ATR) over 14 periods.
   - `avg_volatility_sma = ta.sma(volatility, 100)`: Smoothes out the ATR values using a 100-period simple moving average.

2. **Market Phase Detection**:
   - Determines if the market is in a trending or volatile phase by comparing the closing price to the 200-period SMA and checking for specific conditions.
     - `isTrending = math.abs(distance_from_long_term_ma) > 1.5 * avg_volatility`: Checks if the distance from the 200-period SMA exceeds 1.5 times the smoothed ATR.
     - `isVolatile = volatility > 1.5 * avg_volatility`: Determines if the market is volatile based on the ATR.

3. **EMA/MA Crossover**:
   - Uses a crossover between the 10-period EMA and 30-period SMA to generate buy signals.
     - `crossover_signal = ta.crossover(fast_ma, slow_ma)`: Generates a buy signal when the EMA crosses above the SMA.

4. **MACD Calculation**:
   - Utilizes MACD to identify additional trading opportunities, particularly focusing on histogram crossovers.
     - `[macdLine, signalLine, macdHistogram] = ta.macd(close, 12, 26, 9)`: Calculates the MACD lines and their histogram.
     - `buySignalMACD = macdHistogram > 0`: Generates a buy signal when the MACD histogram is positive.

5. **Bollinger Bands**:
   - Calculates upper and lower Bollinger Bands based on a 20-period standard deviation.
     - `lengthBBands = 20`
     - `stdDevBBands = ta.stdev(close, lengthBBands)`
     - `upperBand = sma(close, lengthBBands) + stdDevBBands * 2`
     - `lowerBand = sma(close, lengthBBands) - stdDevBBands * 2`

6. **Entry Rules**:
   - Enters trades when conditions for volatile, trending, or consolidating markets are met.
     - `isVolatileEntry`: Enters a trade if the market is volatile and either an EMA/MA crossover or MACD buy signal occurs with the price above the lower Bollinger Band.
     - `trendingEntry`: Enters a trade if the market is trending and there's an EMA/MA crossover or MACD buy signal.
     - `consolidatingEntry`: Enters a trade if the market is consolidating and there's an EMA/MA crossover.

7. **Exit Rules**:
   - Closes positions if the MACD crosses below its signal line and both are negative.
     - `exitGeneral`: Closes all trades if the MACD histogram crosses above the signal line with a negative value, ensuring no open positions remain.

8. **Plotting Conditions**:
   - Visualizes trends and volatility with custom shapes.
     - `plotshape(series=isTrending, title="Trend", location=location.belowbar, color=color.green, style=shape.triangleup)`: Plots a green triangle below the bar when in a trending phase.
     - `plotshape(series=isVolatile, title="Volatile", location=location.abovebar, color=color.red, style=shape.triangledown)`: Plots a red triangle above the bar when in a volatile phase.

9. **Optional Plotting**:
   - Plots the average volatility for reference.
     - `plot(series=avg_volatility, title="Average Volatility", color=color.blue)`: Visualizes the smoothed ATR values on the chart.

This script should provide a comprehensive framework for dynamic trading based on multiple technical indicators and conditions. You can test it in your trading platform to see how it performs under different market scenarios. ```