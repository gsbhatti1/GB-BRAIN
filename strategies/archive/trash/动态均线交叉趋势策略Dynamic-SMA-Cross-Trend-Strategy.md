---
## Overview

This strategy is a simple moving average (SMA) crossover strategy suitable for cryptocurrency markets. It uses fast, medium, and slow SMAs to identify potential entry and exit signals. When the fast SMA crosses over the medium SMA, a buy signal is generated. When the fast SMA crosses under the medium SMA, a sell signal is generated.

## Strategy Logic

### Parameter Settings

The strategy allows traders to set the following key parameters:

- **Price Source**: Close price or other prices
- **Consider Incomplete Bars**: Whether to consider incomplete bars
- **SMA Prediction Method**: Use shift prediction or linear regression prediction
- **Fast SMA Length**: Default 7
- **Medium SMA Length**: Default 30  
- **Slow SMA Length**: Default 50
- **Trading Capital**
- **Risk Percentage per Trade**

### SMA Calculation

Based on the user-set SMA lengths, the fast SMA, medium SMA, and slow SMA are calculated.

### Trading Signals

When the fast SMA crosses over the medium SMA, a buy signal is generated. When the fast SMA crosses under the medium SMA, a sell signal is generated.

### Risk and Position Sizing

The strategy calculates the nominal principal per trade based on account funds and acceptable risk percentage per trade. It then uses ATR to calculate the stop loss range and eventually determines the position sizing for each trade.

## Advantage Analysis

- Uses multiple SMAs to identify trends with greater conviction
- Optional SMA prediction methods for stronger adaptability  
- Simple and clear trading signals easy to implement
- Incorporates scientific risk and position management  

## Risk Analysis

- Lagging nature of SMAs may miss price reversal points
- Only considers technical indicators without combining fundamentals  
- Does not consider impact of sudden events 

Can optimize by shortening SMA periods, adding other indicators etc.

## Optimization Directions

- Add other indicators to filter false signals
- Incorporate fundamental analysis  
- Optimize SMA period parameters
- Optimize risk and position sizing parameters  

## Conclusion

This strategy integrates SMA crossover rules, risk management, and position sizing for a robust trend following system suitable for crypto markets. Traders can tweak parameters like trading style, market conditions etc., to customize and optimize.

||

## Overview

This strategy is a simple moving average (SMA) crossover strategy suitable for cryptocurrency markets. It uses fast, medium, and slow SMAs to identify potential entry and exit signals. When the fast SMA crosses over the medium SMA, a buy signal is generated. When the fast SMA crosses under the medium SMA, a sell signal is generated.

## Strategy Logic

### Parameter Settings

The strategy allows traders to set the following key parameters:

- **Price Source**: Close price or other prices
- **Consider Incomplete Bars**: Whether to consider incomplete bars
- **SMA Prediction Method**: Use shift prediction or linear regression prediction
- **Fast SMA Length**: Default 7
- **Medium SMA Length**: Default 30  
- **Slow SMA Length**: Default 50
- **Trading Capital**
- **Risk Percentage per Trade**

### SMA Calculation

Based on the user-set SMA lengths, the fast SMA, medium SMA, and slow SMA are calculated.

### Trading Signals

When the fast SMA crosses over the medium SMA, a buy signal is generated. When the fast SMA crosses under the medium SMA, a sell signal is generated.

### Risk and Position Sizing

The strategy calculates the nominal principal per trade based on account funds and acceptable risk percentage per trade. It then uses ATR to calculate the stop loss range and eventually determines the position sizing for each trade.

## Advantage Analysis

- Uses multiple SMAs to identify trends with greater conviction
- Optional SMA prediction methods for stronger adaptability  
- Simple and clear trading signals easy to implement
- Incorporates scientific risk and position management  

## Risk Analysis

- Lagging nature of SMAs may miss price reversal points
- Only considers technical indicators without combining fundamentals  
- Does not consider impact of sudden events 

Can optimize by shortening SMA periods, adding other indicators etc.

## Optimization Directions

- Add other indicators to filter false signals
- Incorporate fundamental analysis  
- Optimize SMA period parameters
- Optimize risk and position sizing parameters  

## Conclusion

This strategy integrates SMA crossover rules, risk management, and position sizing for a robust trend following system suitable for crypto markets. Traders can tweak parameters like trading style, market conditions etc., to customize and optimize.

---

```pinescript
/*backtest
start: 2024-01-05 00:00:00
end: 2024-02-04 00:00:00
period: 3h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Onchain Edge Trend SMA Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// Configuration Parameters
priceSource = input(close, title="Price Source")
includeIncompleteBars = input(true, title="Consider Incomplete Bars")
maForecastMethod = input(defval="flat", options=["flat", "linreg"], title="Moving Average Prediction Method")
linearRegressionLength = input(3, title="Linear Regression Length")
fastMALength = input(7, title="Fast Moving Average Length")
mediumMALength = input(30, title="Medium Moving Average Length")
slowMALength = input(50, title="Slow Moving Average Length")
tradingCapital = input(100000, title="Trading Capital")
tradeRisk = input(1, title="Trade Risk (%)")

// Calculation of Moving Averages
calculateMA(source, period) => sma(source, period)
predictMA(source, forecastLength, regressionLength) => 
    maForecastMethod == "flat" ? source : linreg(source, regressionLength, forecastLength)

offset = includeIncompleteBars ? 0 : 1
actualSource = priceSource[offset]

fastMA = calculateMA(actualSource, fastMALength)
mediumMA = calculateMA(actualSource, mediumMALength)
slowMA = calculateMA(actualSource, slowMALength)

// Trading Logic
enterLong = crossover(fastMA, mediumMA)
exitLong = crossunder(fastMA, mediumMA)

// Risk and Position Sizing
riskCapital = tradingCapital * tradeRisk / 100
lossThreshold = atr(14) * 2
tradeSize = riskCapital / lossThreshold

if (enterLong)
    strategy.entry("Enter Long", strategy.long, qty=tradeSize)

if (exitLong)
    strategy.close("Enter Long")

// Display Moving Averages
plot(fastMA, color=color.blue, linewidth=2, title="Fast Moving Average")
plot(mediumMA, color=color.purple, linewidth=2, title="Medium Moving Average")
plot(slowMA, color=color.red, linewidth=2, title="Slow Moving Average")
```

---

[Detail](https://www.fmz.com/strategy/441067)

Last Modified: 2024-02-05 12:14:12