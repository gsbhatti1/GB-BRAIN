> Name

Dual-Moving-Average-Convergence-Trend-Tracking-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1452c3fcf0735c860f1.png)
[trans]

### Overview  

The Dual-Moving-Average-Convergence-Trend-Tracking-Strategy (Dual Moving Average Convergence Trend Tracking Strategy) calculates fast, slow, and superslow moving average lines in combination with the MACD indicator to determine price trend direction and implement trend tracking transactions. It goes long when the fast and slow moving averages have a golden cross, and goes short when a dead cross happens. Use the long-term moving average to filter false breaks.

### Principle  

The strategy first calculates the 12-day fast moving average, 26-day slow moving average, and 200-day superslow moving average. When the fast moving average crosses above the slow one, a golden cross occurs, indicating the start of a bull market. When the fast moving average crosses below the slow one, a dead cross happens, indicating the start of a bear market. The strategy goes long on golden crosses and goes short on dead crosses.

The strategy also uses the MACD indicator to determine trend direction. MACD consists of a fast line, a slow line, and MACD bars. When the fast line crosses above the slow line, it's a bullish signal; when crossing below it's a bearish signal. Combined with the long-term moving average to filter false signals, only when the fast line breaks up through the slow one, the MACD bar turns from negative to positive, and the price stands above the 200-day moving average, a long signal triggers. Only when the fast line breaks down through the slow one, the MACD bar turns from positive to negative, and the price drops below the 200-day moving average, a short signal triggers.

With dual confirmation from moving averages system and MACD indicator, false breaks can be avoided, ensuring entering at trend start.

### Advantages

1. Dual confirmation avoids false breaks, ensuring entry only at trend start.
  
2. The 200-day moving average filters erroneous trades during market fluctuations.

3. A stop loss is set to limit maximum loss.

4. Customizable parameters like moving average lengths and stop-loss levels can be adjusted for different products.

5. Simple and clear logic, easy to understand and optimize.

### Risks 

1. Long-term trend tracking unable to capture short-term opportunities.

2. Tracking effect depends on parameter settings; wrong parameters may fail to capture trends properly.

3. Improper stop loss setting may be too loose or too tight, enlarging losses or stopping out prematurely.

4. Long holding periods lead to certain capital pressure.

### Optimization

1. Optimize moving average lengths parameter for the best parameter combination.

2. Add other indicators as auxiliary judgment signals, such as KDJ.

3. Optimize stop loss strategies like tighter stops and trailing stops.

4. Adjust moving average parameters based on product and timeframe.

5. Add volume filter to avoid false signals.

### Conclusion

The Dual Moving Average Convergence Trend Tracking Strategy judges trend direction by calculating multiple moving average systems and uses the MACD indicator for signal filtering. Its advantages are simple and clear logic, controllable risks, suitable for trend tracking. It can be improved through parameter optimization, stop loss optimization, and adding auxiliary indicators. This is a recommendable trend tracking strategy.

||

### Strategy Arguments

| Argument | Default | Description |
| --- | --- | --- |
| v_input_1_close | 0 | source: close | high | low | open | hl2 | hlc3 | hlcc4 | ohlc4 |
| v_input_2 | 12 | MACD fast moving average |
| v_input_3 | 26 | MACD slow moving average |
| v_input_4 | 9 | MACD signal line moving average |
| v_input_5 | 200 | Very slow moving average |
| v_input_6 | true | Enable Bar Color? |
| v_input_7 | true | Enable Moving Averages? |
| v_input_8 | true | Enable Background Color? |

> Source (PineScript)

```pinescript
//@version=2
strategy("Trend Strategy", shorttitle="TSTrend Strategy", overlay=true)

// Trend Strategy
// If the inverse logic is true, the strategy
// goes short. For the worst case there is a
// max intraday equity loss of 50% filter.

// Input
source = input(close)
fastLength = input(12, minval=1, title="MACD fast moving average")
slowLength=input(26,minval=1, title="MACD slow moving average")
signalLength=input(9,minval=1, title="MACD signal line moving average")
veryslowLength=input(200,minval=1, title="Very slow moving average")
switch1=input(true, title="Enable Bar Color?")
switch2=input(true, title="Enable Moving Averages?")
switch3=input(true, title="Enable Background Color?")

// Calculation
fastMA = sma(source, fastLength)
slowMA = sma(source, slowLength)
veryslowMA = sma(source, veryslowLength)
macd = fastMA - slowMA
signal = sma(macd, signalLength)
hist = macd - signal

// Colors
MAtrendcolor = change(veryslowMA) > 0 ? green : red
trendcolor = fastMA > slowMA and change(veryslowMA) > 0 and close > slowMA ? green : 
```