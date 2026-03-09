> Name

Dual-Moving-Average-Strategy-360

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1f0f44c7ab39e16b9d4.png)
[trans]
## Overview  

The Dual Moving Average Strategy 360° is a quantitative trading strategy that combines dual moving averages with trend strength determination. By calculating moving averages over different periods, it determines price trends; meanwhile, by accumulating tangent angles, it judges the strength of trends and achieves more accurate entry and exit points.

## Strategy Logic  

The core logic of the Dual Moving Average Strategy 360° is:  

1. Calculate the 1-minute and Kalman-filtered moving averages;
2. Calculate the tangent angle based on the price difference between the two moving averages; 
3. Accumulate tangent angles to determine trend strength signals;
4. Issue trading signals based on whether the accumulated tangent angles exceed preset thresholds.

Specifically, the strategy defines the raw 1-minute moving average and the Kalman-filtered moving average. The Kalman filter eliminates some noise from the moving average to make it smoother. The tangent angle between the two moving averages reflects price trend changes. For example, when the tangent angle is positive, it indicates an upward trend; conversely, a negative angle represents a downward trend.

The strategy chooses 30 minutes as the calculation period and sums all positive and negative tangent angles within that period. When the sum exceeds 360 degrees, it signals a very strong trend and issues a long signal; conversely, when the sum is below -360 degrees, it indicates a trend reversal and issues a short signal.

## Advantage Analysis  

The main advantages of the Dual Moving Average Strategy 360° are:  

1. Moving averages filter out short-term market noise for more reliable trading decisions;  
2. Tangent angles quantify trend strength, avoiding the subjectivity of judging by moving average patterns alone;
3. Summing multiple tangent angles has better noise reduction effects, resulting in more reliable trading signals;  
4. Compared to single moving average strategies, the dual moving averages combined with trend strength determinations make the strategy more comprehensive and robust.

## Risk Analysis  

The Dual Moving Average Strategy 360° also carries some risks:

1. Moving averages lag price changes and may miss short-term trend turning points;
2. Relying solely on the accumulated trend strength signal can be disrupted by market volatility;  
3. Improper parameter settings (such as calculation period lengths) may lead to missing trades or generating incorrect signals.

To mitigate the above risks, measures like shortening the moving average period, optimizing parameter combinations, adding stop-loss mechanisms can be adopted.

## Optimization Directions  

The Dual Moving Average Strategy 360° can be further optimized by:  

1. Incorporating adaptive moving averages that adjust parameters based on market volatility;  
2. Referencing multiple moving average periods to form optimized parameter combinations;  
3. Adding dynamic trend determination modules based on volatility, trading volumes, etc.;  
4. Assisting parameter tuning or trade decisions with machine learning models.

## Summary  

The Dual Moving Average Strategy 360° utilizes moving average filtering and quantitative tangent angle trend judgments to achieve a relatively robust quantitative trading strategy. Compared to single technical indicators, this strategy forms a more comprehensive consideration and has stronger practicality. But parameter tuning and risk control are still vital, and the strategy can be further optimized for even better results going forward.

[/trans]

> Source (PineScript)

```pinescript
//@version=5
//@library=math
strategy("360° Strategy (Test)", overlay=true)

// Define 1-minute moving average
ma1 = request.security(syminfo.tickerid, "1", ta.sma(close, 1)) // Using math.sma() function here

// Define Kalman filter function as per references [1] and [2]
kalman(x, g) =>
    kf = 0.0 
    dk = x - nz(kf[1], x) // Using nz() function here
    smooth = nz(kf[1], x) + dk * math.sqrt(g * 2) // Using math.sqrt() function here
    velo = 0.0 
    velo := nz(velo[1], 0) + g * dk // Using nz() function again
    kf := smooth + velo
    kf

// Define Kalman-filtered moving average
ma2 = kalman(ma1, 0.01)
plot(ma2, color=color.blue, title="Filtered Moving Average")

// Define tangent angle
angle = math.todegrees(math.atan(ma2 - ma2[1])) // Using math.degrees() and math.atan() functions here

// Define cumulative tangent angle
cum_angle = 0.0
cum_angle := nz(cum_angle[1], 0) + angle // Using nz() function again

// Define 30-minute period
period = 30 // You can adjust this parameter as needed

// Define period
```