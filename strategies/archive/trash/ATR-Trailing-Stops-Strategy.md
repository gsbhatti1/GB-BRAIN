> Name

Dynamic Stop Loss Trailing Trading Strategy ATR-Trailing-Stops-Strategy

> Author

ChaoZhang

> Strategy Description


### Overview

This strategy sets dynamic stop loss lines based on the Average True Range (ATR) indicator to track stock price changes, aiming to protect stop losses while maximizing profit-taking.

### Strategy Logic

The strategy is mainly implemented through the following steps:

1. Calculate the ATR indicator; the ATR period is set by the `nATRPeriod` parameter, default to 5;
2. Calculate the stop loss line based on the ATR value; the stop loss magnitude is set by the `nATRMultip` parameter, default to 3.5 times the ATR;
3. When the price rises, if higher than the previous stop loss line, adjust the stop loss line up to the price minus the stop loss magnitude; when the price falls, if lower than the previous stop loss line, adjust the stop loss line down to the price plus the stop loss magnitude;
4. Judge if the price breaks through the stop loss line; if it breaks through, send buy or sell signals;
5. Enter long or short positions based on the stop loss line breakout signals, and close positions when the price touches the stop loss line again.

When the price rises, the stop loss line will move up continuously to lock in profits. When the price falls, the stop loss line will move down continuously to cut losses. The ATR indicator can reflect price fluctuations more accurately; dynamically adjusting the stop loss line based on ATR can avoid overly aggressive or conservative stop losses.

### Advantage Analysis

- Dynamically adjust stop loss lines for timely stops to prevent larger losses
- Smooth adjustment of the stop loss line prevents premature cutting off profits
- Use ATR to calculate a more reasonable stop loss magnitude based on recent volatility  
- Trail stop loss lines effectively lock in profits

### Risk Analysis

- Careful setting of ATR parameters is required; too short an ATR period may result in excessive stop loss line fluctuations, while too long an ATR period may fail to reflect price changes quickly
- Stop loss magnitudes need to be set according to specific stock volatility, as overly large or small values can affect strategy performance
- Trailing stops might reduce profit margins by cutting profits before a further rise in prices
- Frequent position adjustments could lead to higher trading costs

Parameters can be optimized by adjusting ATR period and stop loss magnitude to find the best balance between stopping losses and trailing. Other technical indicators can also help filter entry timing to avoid unnecessary stop losses.

### Optimization Directions

- Optimize the ATR period parameter to make the stop loss line changes more closely follow price fluctuations
- Optimize the stop loss magnitude parameter for a more reasonable stop loss
- Add other indicators to filter entry timing
- Enter long positions only when an obvious uptrend emerges  
- Consider adding a re-entry mechanism to participate in stocks with a stop loss after expecting further rises

### Summary

This strategy uses dynamic ATR trailing stop loss lines to achieve both protection and profit-taking during holding. Compared to fixed stop-loss points, it better adapts to price fluctuations, avoiding overly aggressive or conservative stop losses. The ATR indicator makes the stop loss line adjustments more targeted. However, parameter tuning and re-entry strategies need further optimization to reduce unnecessary stops and expand profit margins. Overall, this is a good dynamic trailing stop loss approach worth further research and application.

||

### Overview

This strategy sets a dynamic stop loss line based on the Average True Range (ATR) indicator to trail stock price changes in order to protect stop losses while maximizing profit-taking.

### Strategy Logic

The strategy is mainly implemented through the following steps:

1. Calculate the ATR indicator; the ATR period is set by the `nATRPeriod` parameter, default to 5;
2. Calculate the stop loss line based on the ATR value; the stop loss magnitude is set by the `nATRMultip` parameter, default to 3.5 times the ATR;
3. When the price rises, if higher than the previous stop loss line, adjust the stop loss line up to the price minus the stop loss magnitude; when the price falls, if lower than the previous stop loss line, adjust the stop loss line down to the price plus the stop loss magnitude;
4. Judge whether the price breaks through the stop loss line; if it breaks through, send buy or sell signals;
5. Enter long or short positions based on the stop loss line breakout signals and close positions when the price touches the stop loss line again.

When the price rises, the stop loss line will move up continuously to lock in profits. When the price falls, the stop loss line will move down continuously to cut losses. The ATR indicator can reflect price fluctuations more accurately; dynamically adjusting the stop loss line based on ATR can avoid overly aggressive or conservative stop losses.

### Advantage Analysis

- Dynamically adjust stop loss lines for timely stops to prevent larger losses
- Smooth adjustment of the stop loss line prevents premature cutting off profits
- Use ATR to calculate a more reasonable stop loss magnitude based on recent volatility  
- Trail stop loss lines effectively lock in profits

### Risk Analysis

- Careful setting of ATR parameters is required; too short an ATR period may result in excessive stop loss line fluctuations, while too long an ATR period may fail to reflect price changes quickly
- Stop loss magnitudes need to be set according to specific stock volatility, as overly large or small values can affect strategy performance
- Trailing stops might reduce profit margins by cutting profits before a further rise in prices
- Frequent position adjustments could lead to higher trading costs

Parameters can be optimized by adjusting ATR period and stop loss magnitude to find the best balance between stopping losses and trailing. Other technical indicators can also help filter entry timing to avoid unnecessary stop losses.

### Optimization Directions

- Optimize the ATR period parameter to make the stop loss line changes more closely follow price fluctuations
- Optimize the stop loss magnitude parameter for a more reasonable stop loss
- Add other indicators to filter entry timing
- Enter long positions only when an obvious uptrend emerges  
- Consider adding a re-entry mechanism to participate in stocks with a stop loss after expecting further rises

### Summary

This strategy uses dynamic ATR trailing stop loss lines to achieve both protection and profit-taking during holding. Compared to fixed stop-loss points, it better adapts to price fluctuations, avoiding overly aggressive or conservative stop losses. The ATR indicator makes the stop loss line adjustments more targeted. However, parameter tuning and re-entry strategies need further optimization to reduce unnecessary stops and expand profit margins. Overall, this is a good dynamic trailing stop loss approach worth further research and application.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|5|ATR Period|
|v_input_2|3.5|ATR Multiplier|
|v_input_3|false|Test with Shorts?|
|v_input_4|360|Max Days Back to Test|
|v_input_5|false|Min Days Back to Test|


> Source (PineScript)

```pinescript
//@version=3
//@okadoke
////////////////////////////////////////////////////////////
// Based on Average True Range Trailing Stops Strategy by HPotter
// Average True Range Trailing Stops Strategy, by Sylvain Vervoort 
// The related article is copyrighted material from Stocks & Commodities Jun 2009 
////////////////////////////////////////////////////////////
strategy(title="ATR Trailing Stops Strategy", shorttitle="ATRTSS", overlay=true, 
  initial_capital=100000, default_qty_type=strategy.percent_of_equity, default_qty_value=100, commission_type="percent", commission_value=0.0)
  
nATRPeriod      = input(5, "ATR Period")
nATRMultip      = input(3.5, "ATR Multiplier")
useShorts       = input(false, "Test with Shorts?")
daysBackMax     = input(defval = 360, title="Max Days Back to Test", minval=0)
daysBackMin     = input(defval = 0, title="Min Days Back to Test", minval=0)
msBackMax       =
```