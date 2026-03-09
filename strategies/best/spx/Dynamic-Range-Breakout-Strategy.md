> Name

Dynamic-Range-Breakout-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/fa9946100827307239.png)
[trans]

## Overview
This strategy is designed based on the Bollinger Bands indicator to create a dynamic breakout trading strategy. It combines K-line body filtering and color filtering conditions to identify entry opportunities near the Bollinger lower band. Exits are based on body filtering. The strategy automatically manages position size and risk.

## Strategy Logic  
### Indicator Calculation
First, calculate the base line and lower band of Bollinger Bands using low price:

```
src = low 
basis = sma(src, length)
dev = mult * stdev(src, length) 
lower = basis - dev
```

Where `src` is the low price, `length` is the calculation period, `basis` is the moving average, `dev` is the standard deviation, and `lower` is the lower band.  

`mult` is usually set to 2, meaning the lower band is one standard deviation away.

### Filter Conditions
The strategy incorporates two filter conditions:

**K-line Body Filter** 
Use the body size `nbody` and its mean `abody` to determine, only generate trading signal when `nbody` is greater than half of `abody`.

**Color Filter**  
Do not go long when candle closes positive (close > open). This avoids false breakouts at the head of hbox.

### Trading Signals  
Generate buy signals when the following conditions are met:

```
low < lower  // price breaks below lower band
close < open or usecol == false // color filter
nbody > abody / 2 or usebod == false // body filter  
```

Close position when `nbody` exceeds half of the mean again:

```
close > open and nbody > abody / 2  
```

### Position Sizing  
The strategy calculates trade size automatically for exponential growth in position size:

```
lot = strategy.position_size == 0 ? strategy.equity / close * capital / 100 : lot[1] 
```

### Risk Control
Add constraints on year, month, and date to limit trading only within specific dates:

```
when=(time > timestamp(fromyear, frommonth, fromday, 00, 00) and time < timestamp(toyear, tomonth, today, 23, 59))
```

## Advantages
### Dynamic Trading Range
The Bollinger lower band provides a dynamic support area to capture retracements after trends.

### Dual Filter  
Combining K-line body and color filters avoids false breakouts effectively.  

### Automatic Position Sizing
Positions size up exponentially to 100%, managing risk automatically.

### Date Range  
Setting a date range lowers the risk associated with market volatility in specific periods.

## Risks
### Prolonged Drawdown  
When experiencing a strong uptrend, the Bollinger middle and upper bands may shift up quickly, causing prolonged drawdown.

#### Solutions
Combine with trend indicators, stop strategy when judged as bull market to avoid prolonged drawdown.  

### Failed Breakout
Breakouts may fail with pullbacks and retrial of the lower band. 

#### Solutions 
Add a stop loss below support level. Or add logic to detect failed retests for quick stop loss.

## Enhancements 
### Add Stop Loss  
Optimize stop loss levels based on backtest results.

### Optimize Parameters 
Fine-tune body filter `abody` period, COLOR filter settings etc to find the optimum parameters.

### Add Trend Filter
Stop strategy when judged as bull market. Reduce drawdown time.

## Conclusion
This strategy combines Bollinger support with K-line body and color filters for breakout entry to capture high probability retracements. In practice, parameters can be optimized based on backtest results, with stop loss and trend filter additions to control risks and improve performance.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|100|Capital, %|
|v_input_2|25|BB Period|
|v_input_3|false|Use Body-Filter|
|v_input_4|false|Use Color-Filter|
|v_input_5|false|Show Arrows|
|v_input_6|1900|From Year|
|v_input_7|2100|To Year|
|v_input_8|true|From Month|
|v_input_9|12|To Month|
|v_input_10|true|From Day|
|v_input_11|31|To Day|


> Source (PineScript)

```pinescript
//@version=2
strategy(title = "Noro's Wizard Strategy v1.0", shorttitle = "Wizard str 1.0", overlay = true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, pyramiding = 10)

//Settings
c