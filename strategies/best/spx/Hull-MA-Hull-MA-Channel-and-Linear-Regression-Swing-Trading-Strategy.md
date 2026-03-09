> Name

Hull-MA Channel and Linear Regression Swing Trading Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/20df324d5a4a600f6f2.png)
[trans]

## Overview

This is a swing trading strategy that combines Hull MA, price channel, EMA signal, and linear regression. It uses Hull MA to determine market trend direction, price channel and linear regression to identify bottom areas, EMA signal to time market entry, in order to capture medium-term trends.

## Strategy Logic

The strategy consists of the following main indicators:

1. Hull MA 
   - Typical period of Hull MA is 337, representing medium to long term trend direction  
   - When 2 times 18-period WMA is above 337-period WMA, it's a bull market, otherwise it's a bear market
2. Price Channel
   - Price channel plots EMA high and EMA low, representing support and resistance areas
3. EMA Signal
   - Typical period is 89, representing short-term trend and entry signal
4. Linear Regression
   - Fast line of 6 period for bottom and breakout
   - Slow line of 89 period for medium to long term trend  

Entry Logic: 

Long Entry: Hull MA pointing up and price above upper band, linear regression crossing up EMA signal
Short Entry: Hull MA pointing down and price below lower band, linear regression crossing down EMA signal

Exit Logic:

Long Exit: Price below lower band and crossing down linear regression 
Short Exit: Price above upper band and crossing up linear regression

## Advantage Analysis

The strategy has the following advantages:

1. Higher accuracy with multiple indicators
   - Hull MA for main trend, channel for support/resistance, EMA for entry  
2. Swing trading to capture medium-term trends 
   - Strategy mainly reversals to capture each medium-term cycle
3. Controllable risk and smaller drawdown
   - Signal only generated at high probability area, avoiding chase high kill low

## Risk Analysis

There are also some risks:  

1. Limited optimization space
   - Main parameters like EMA period is fixed, with small optimization space
2. May lose in range-bound market
   - Stop loss may be triggered in sideways range  
3. Need some technical analysis knowledge
   - Strategy logic needs price action and indicator knowledge, not suitable for everyone  

Improvements:

1. Adjust stop loss strategy, e.g. trailing stop loss
2. Optimize entry and exit logic  
3. Add other filter indicators like MACD

## Summary

The strategy combines Hull MA, price channel, EMA, and linear regression for a comprehensive medium-term swing trading strategy. Compared to single indicator strategies, it improves accuracy significantly in catching trends and reversals. But there are still risks, requiring technical analysis knowledge. Further improvements on parameters and logic can enhance stability.

||


## Overview

This is a swing trading strategy that combines Hull MA, price channel, EMA signal, and linear regression. It uses Hull MA to determine market trend direction, price channel and linear regression to identify bottom areas, EMA signal to time market entry, in order to capture medium-term trends.

## Strategy Logic

The strategy consists of the following main indicators:

1. Hull MA 
   - Typical period of Hull MA is 337, representing medium to long term trend direction  
   - When 2 times 18-period WMA is above 337-period WMA, it's a bull market, otherwise it's a bear market
2. Price Channel
   - Price channel plots EMA high and EMA low, representing support and resistance areas
3. EMA Signal
   - Typical period is 89, representing short-term trend and entry signal
4. Linear Regression
   - Fast line of 6 period for bottom and breakout
   - Slow line of 89 period for medium to long term trend  

Entry Logic: 

Long Entry: Hull MA pointing up and price above upper band, linear regression crossing up EMA signal
Short Entry: Hull MA pointing down and price below lower band, linear regression crossing down EMA signal

Exit Logic:

Long Exit: Price below lower band and crossing down linear regression 
Short Exit: Price above upper band and crossing up linear regression

## Advantage Analysis

The strategy has the following advantages:

1. Higher accuracy with multiple indicators
   - Hull MA for main trend, channel for support/resistance, EMA for entry  
2. Swing trading to capture medium-term trends 
   - Strategy mainly reversals to capture each medium-term cycle
3. Controllable risk and smaller drawdown
   - Signal only generated at high probability area, avoiding chase high kill low

## Risk Analysis

There are also some risks:  

1. Limited optimization space
   - Main parameters like EMA period is fixed, with small optimization space
2. May lose in range-bound market
   - Stop loss may be triggered in sideways range  
3. Need some technical analysis knowledge
   - Strategy logic needs price action and indicator knowledge, not suitable for everyone  

Improvements:

1. Adjust stop loss strategy, e.g. trailing stop loss
2. Optimize entry and exit logic  
3. Add other filter indicators like MACD

## Summary

The strategy combines Hull MA, price channel, EMA, and linear regression for a comprehensive medium-term swing trading strategy. Compared to single indicator strategies, it improves accuracy significantly in catching trends and reversals. But there are still risks, requiring technical analysis knowledge. Further improvements on parameters and logic can enhance stability.

||


> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|377|HullMA Period|
|v_input_2|89|EMA Signal|
|v_input_3|34|High Low channel Length|
|v_input_4|89|Linear Regression Length|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-11-23 00:00:00
end: 2023-11-30 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
strategy("Swing Hull/SonicR/EMA/Linear Regression Strategy", overlay=true)
// Hull MA
n = input(title="HullMA Period", defval=377)
n2ma = 2 * wma(close, round(n / 2))
nma = wma(close, n)
diff = n2ma - nma
sqn = round(sqrt(n))
// Hull MA logic
n2ma1 = 2 * wma(close[1], round(n / 2))
nma1 = wma(close[1], n)
diff1 = n2ma1 - nma1
sqn1 = round(sqrt(n))
n1 = wma(diff, sqn)
n2 = wma(diff1, sqn)
condDown = n2 >= n1
condUp = condDown != true
col = condUp ? lime : condDown ? red : yellow
plot(n1, title="Hull MA", color=col, linewidth=3)
// SonicR + Linear Regression
EMA = input(defval=89, title="EMA Signal")
HiLoLen = input(34, minval=2, title="High Low channel Length")
lr = input(89, minval=2, title="Linear Regression Length")
pacC = ema(close, HiLoLen)
pacL = ema(low, HiLoLen)
pacH = ema(high, HiLoLen)
DODGERBLUE = #1E90FFFF
// Plot the Price Action Channel (PAC) based on EMA high, low, and close
L = plot(pacL, color=DODGERBLUE, linewidth=1, title="High PAC EMA", transp=90)
H = plot(pacH, color=DODGERBLUE, linewidth=1, title="Low PAC EMA", transp=90)
C = plot(pacC, color=DODGERBLUE, linewidth=2, title="Close PAC EMA", transp=80)
// Moving Average
signalMA = ema(close, EMA)
plot(signalMA, title="EMA Signal", color=black, linewidth=3, style=line)
linereg = linreg(close, lr, 0)
lineregf = linreg(close, HiLoLen, 0)
cline = linereg > linereg[1] ? green : red
cline2 = lineregf > lineregf[1] ? green : red
plot(linereg, color=cline, title="Linear Regression Curve Slow", style=line, linewidth=1)
// plot(lineregf, color=cline2, title="Linear Regression Curve Fast", style=line, linewidth=1)
longCondition = n1 > n2
shortCondition = longCondition != true
closeLong = lineregf - pacH > (pacH - pacL) / 2
closeShort = lineregf - pacL < (pacH - pacL) / 2
plotshape(series=closeLong, title="Close Long", location=location.belowbar, color=lime, style=shape.triangleup, size=size.small)
plotshape(series=closeShort, title="Close Short", location=location.abovebar, color=red, style=shape.triangledown, size=size.small)
```

This completes the conversion of the strategy description and code into a clear, comprehensive format. If you have any further requirements or need additional modifications, feel free to ask!