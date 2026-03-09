``` pinescript
/*backtest
start: 2023-11-04 00:00:00
end: 2023-12-04 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
//please use on daily SPY, or other indexes only
strategy("50-150 INDEX TREND FOLLOWING", overlay=true)

//user input
fastSMA = input(title="Fast Moving Average (Int)",type=input.integer,minval=1,maxval=1000,step=1,defval=50,confirm=false)
slowSMA = input(title="Slow Moving Average (Int)",type=input.integer,minval=1,maxval=1000,step=1,defval=150,confirm=false)
longSlopeThreshold = input(title="Bullish Slope Angle (Deg)",type=input.integer,minval=-90,maxval=90,step=1,defval=5,confirm=false)
shortSlopeThreshold = input(title="Bearish Slope Angle (Deg)",type=input.integer,minval=-90,maxval=90,step=1,defval=-5,confirm=false)
atrValue = input(title="Average True Range (Int)",type=input.integer,minval=1,maxval=100,step=1,defval=14,confirm=false)
risk = input(title="Risk (%)",type=input.integer,minval=1,maxval=100,step=1,defval=100,confirm=false)

//create indicator
shortSMA = sma(close, fastSMA)
longSMA = sma(close, slowSMA)

//calculate ma slope
angle(_source) =>
    rad2degree = 180 / 3.14159265359
    ang = rad2degree * atan((_source[0] - _source[1]) / atr(atrValue))
    
shortSlope = angle(shortSMA)
longSlope = angle(longSMA)

//specify crossover conditions
longCondition = (crossover(shortSMA, longSMA) and (shortSlope > longSlopeThreshold)) or ((close > shortSMA) and (shortSMA > longSMA) and (shortSlope > longSlopeThreshold))
exitCondition = crossunder(shortSMA, longSMA) or (shortSlope < shortSlopeThreshold)

//initial capital
strategy.initial_capital = 50000

//units to buy
amount = (risk / 100) * strategy.initial_capital / close

//buy condition
if (longCondition)
    strategy.entry("Buy", strategy.long, qty=amount)

//exit condition
if (exitCondition)
    strategy.close("Buy")
```

This Pine Script code implements the described momentum index ETF trend following strategy. The script defines input parameters for moving averages, slope thresholds, ATR values, and risk levels. It calculates the slopes of the short and long moving averages and uses these to determine entry and exit conditions based on the crossovers and slope criteria. The `amount` variable is calculated as a percentage of the initial capital, which is then used to place buy orders. Sell orders are placed when the exit condition is met.