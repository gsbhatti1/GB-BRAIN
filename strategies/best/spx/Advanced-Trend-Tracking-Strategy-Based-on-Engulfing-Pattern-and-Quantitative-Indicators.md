> Name

Advanced-Trend-Tracking-Strategy-Based-on-Engulfing-Pattern-and-Quantitative-Indicators

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/ea00ce94ca3d127ac2.png)
[trans]

### Overview

This strategy integrates multiple quantitative techniques such as engulfing candlestick pattern recognition, oscillators, moving averages, and demand-supply zones to precisely determine and trade the trend. It extensively employs professional terminology and standard models of quantitative trading to improve decision accuracy through composite indicator judgment and effectively control risks.

### Strategy Principle  

The core logic of this strategy is based on identifying the engulfing candlestick patterns to catch turnarounds in the market. When a bullish engulfing pattern appears, close\[1\] > open\[1\] and open < close and close > open\[1\] and open\[1\] > close\[1\], a buy signal is triggered. When a bearish engulf pattern appears, close\[1\] < open\[1\] and open > close and close < open\[1\] and open\[1\] < close\[1\], a sell signal is triggered.

In addition, a 20-period demand zone and supply zone indicator is introduced. When the close breaks through the supply zone, it is determined as a bullish signal. When it breaks through the demand zone, it is determined as a bearish signal. The EMA moving average is used to determine the trend direction. Trading signals are generated only when the close breaks through the EMA. The fractal oscillator that finds pivot points assists in confirming the time of reversals.

In summary, this strategy determines potential reversals through engulfing patterns and uses filters like moving averages and supply-demand zones to confirm and trade only the highest probability points, thereby accurately tracking trends and avoiding losing all capital to whipsaws.

### Advantage Analysis

This is a highly professional and advanced trend tracking strategy with the following main advantages:

1. Multiple indicator combo improves judgment accuracy and effectively filters false signals
2. Engulfing patterns catch reversals
3. Oscillators and trends determine high probability trade points
4. Automatic pattern and indicator plotting, readable
5. Concise logic, easily extensible and optimizable

Overall, this strategy has high accuracy and good risk control. It is suitable for mid-to-long term trend tracking and can deliver steady profits.

### Risk Analysis

Despite its numerous strengths, some potential risks to note:

1. Inaccurate engulfing pattern recognition might miss actual reversals or generate false signals
2. Wrong signals probability exists in moving average systems, may buy the top and sell the bottom
3. Improper demand zone and supply zone range setting increases unnecessary trades  
4. Limited optimization space, higher avalanche risks

Countermeasures:

1. Introduce machine learning to improve reversal pattern recognition accuracy  
2. Add indicators judging violent trend to avoid unnecessary losses
3. Dynamically optimize demand and supply zone parameters   
4. Reasonably assess and control risks, adjust position sizing

### Optimization Directions  

Further optimization directions:  

1. Add AI-based pattern recognition module using machine learning for engulfing and reversals
2. Introduce more filters like BOLL and MACD for timing  
3. Add stop loss strategies like trailing stop loss and time-based stop loss
4. Dynamically optimize indicator parameters for different products and markets
5. Incorporate advanced strategies like trailing stops and martingale to manage equity curve  

The above optimizations can improve accuracy, reduce risks, and smooth equity curve.

### Summary

In summary, this is an extremely professional and efficient strategy that fully utilizes multiple quantitative indicators and models to judge market changes. It captures reversal signals through engulfing patterns and issues high probability trading signals collaborating with trend and oscillator indicators. This allows effective mid-to-long term trend tracking and steady profits. Meanwhile, certain risks need attention. Continual optimizations and strict risk management significantly lower risks, making the strategy more reliable. It has strong practicality and extensibility, suitable for traders with some quantitative basis.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|14|EMA Length|
|v_input_2|20|Demand & Supply Length|