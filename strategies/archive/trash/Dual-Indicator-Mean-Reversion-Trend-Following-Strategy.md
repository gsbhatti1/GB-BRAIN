> Name

Dual-Indicator-Mean-Reversion-Trend-Following-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/12285df40e668473675.png)
[trans]
### Overview

This strategy generates buy and sell signals by combining a moving average indicator and the market facilitation index. It belongs to the mean reversion trading strategy category.

### Principles  

The strategy utilizes two indicators for signal generation. The first one is the moving average indicator, specifically the combination of fast line and slow line of Stochastic Oscillator. It produces a sell signal when price closes down for two consecutive days and the fast line is above the slow line. It generates a buy signal when price closes up for two consecutive days and the fast line is below the slow line. By monitoring price reversal and the relationship between fast line and slow line, it aims to predict potential turning points of the price trend.

The second indicator is the market facilitation index. This index measures the efficiency of price movement by calculating the relationship between price range and volume. When the index rises, it indicates improving market liquidity and higher operational efficiency, signaling a trending market. Conversely, when the index declines, it shows worsening liquidity and decreasing efficiency, implying a potential sideways ranging or trend reversal market.

This strategy generates actual buy and sell orders when both indicators issue concordant trading signals simultaneously.

### Advantages  

- Improved signal accuracy by requiring confirmation from two indicators, avoiding false signals  
- Combination of mean reversion indicator and trend judging indicator helps avoid trading against major trends 
- Reduced needs for frequent parameter tuning and less manual intervention 

### Risks and Solutions  

- Difficult to capitalize on reversal opportunities if prolonged one-way uptrend or downtrend, unable to enter the market
- Can relax parameters of mean reversion indicator to increase chances of capturing buy and sell signals  
- Can also scale up position size to ride the trend and compensate profits

- Inaccurate reversal signals may invalidate the strategy 
- Can optimize parameters or add signal confirmation stages to filter out false signals  

### Enhancement Areas  

- Test more parameter combinations to find optimum settings  
- Explore more mean reversion indicators, evaluate performance of different indicators
- Introduce stop loss to constrain single trade loss 
- Incorporate machine learning models trained on big data to generate more accurate reversal signals  

### Summary   

This strategy combines a mean reversion indicator and a trend judging indicator, entering the market when a reversal signal emerges while respecting the major trend direction. Using dual indicator confirmation effectively eliminates false signals. Although risks exist during prolonged one-side trends and erroneous reversal signals. Further optimizations can be done via parameter tuning, stop loss, indicator upgrades, and machine learning models.

||

### Overview  

This strategy generates buy and sell signals by combining a moving average indicator and the market facilitation index. It belongs to the mean reversion trading strategy category.  

### Principles  

The strategy utilizes two indicators for signal generation. The first one is the moving average indicator, specifically the combination of fast line and slow line of Stochastic Oscillator. It produces a sell signal when price closes down for two consecutive days and the fast line is above the slow line. It generates a buy signal when price closes up for two consecutive days and the fast line is below the slow line. By monitoring price reversal and the relationship between fast line and slow line, it aims to predict potential turning points of the price trend.

The second indicator is the market facilitation index. This index measures the efficiency of price movement by calculating the relationship between price range and volume. When the index rises, it indicates improving market liquidity and higher operational efficiency, signaling a trending market. Conversely, when the index declines, it shows worsening liquidity and decreasing efficiency, implying a potential sideways ranging or trend reversal market.

This strategy generates actual buy and sell orders when both indicators issue concordant trading signals simultaneously.

### Advantages  

- Improved signal accuracy by requiring confirmation from two indicators, avoiding false signals  
- Combination of mean reversion indicator and trend judging indicator helps avoid trading against major trends 
- Reduced needs for frequent parameter tuning and less manual intervention 

### Risks and Solutions  

- Difficult to capitalize on reversal opportunities if prolonged one-way uptrend or downtrend, unable to enter the market
- Can relax parameters of mean reversion indicator to increase chances of capturing buy and sell signals  
- Can also scale up position size to ride the trend and compensate profits

- Inaccurate reversal signals may invalidate the strategy 
- Can optimize parameters or add signal confirmation stages to filter out false signals  

### Enhancement Areas  

- Test more parameter combinations to find optimum settings  
- Explore more mean reversion indicators, evaluate performance of different indicators
- Introduce stop loss to constrain single trade loss 
- Incorporate machine learning models trained on big data to generate more accurate reversal signals  

### Summary   

This strategy combines a mean reversion indicator and a trend judging indicator, entering the market when a reversal signal emerges while respecting the major trend direction. Using dual indicator confirmation effectively eliminates false signals. Although risks exist during prolonged one-side trends and erroneous reversal signals. Further optimizations can be done via parameter tuning, stop loss, indicator upgrades, and machine learning models.

||

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|---- 123 Reversal ----|
|v_input_2|14|Length|
|v_input_3|true|KSmoothing|
|v_input_4|3|DLength|
|v_input_5|50|Level|
|v_input_6|true|---- MFI ----|
|v_input_7|6.2|SellZone|
|v_input_8|true|BuyZone|
|v_input_9|false|Trade reverse|


> Source (PineScript)

``` pinescript
//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 02/02/2021
// This is combo strategies for get a cumulative signal. 
//
// First strategy
// This System was created from the Book "How I Tripled My Money In The 
// Futures Market" by Ulf Jensen, Page 183. This is reverse type of strategies.
// The strategy buys at market, if close price is higher than the previous close 
// during 2 days and the meaning of 9-days Stochastic Slow Oscillator is lower than 50. 
// The strategy sells at market, if close price is lower than the previous close price 
// during 2 days and the meaning of 9-days Stochastic Fast Oscillator is higher than 50.
//
// Second strategy
// The Market Facilitation Index is an indicator that relates price range to 
// volume and measures the efficency of price movement. Use the indicator to 
// determine if the market is trending. If the Market Facilitation Index increased, 
// then the market is facilitating trade and is more efficient, implying that the 
// market is trending. If the Market Facilitation Index decreased, then the market 
// is becoming less efficient, which may indicate a trading range is developing that 
// may be a trend reversal.
//
// WARNING:
// - For purpose educate only
// - This script to change bars colors.
//////////////////////////////////////////
```

``` pinescript
//@version=4
strategy("Dual-Indicator-Mean-Reversion-Trend-Following-Strategy", overlay=true)

v_input_1 = input(true, title="---- 123 Reversal ----")
v_input_2 = input(14, title="Length")
v_input_3 = input(true, title="KSmoothing")
v_input_4 = input(3, title="DLength")
v_input_5 = input(50, title="Level")
v_input_6 = input(true, title="---- MFI ----")
v_input_7 = input(6.2, title="SellZone")
v_input_8 = input(true, title="BuyZone")
v_input_9 = input(false, title="Trade reverse")

// First strategy
stoch_slow = stochastic(close, high, low, v_input_2)
k_line = sma(stoch_slow, 3)
d_line = sma(k_line, 3)

long_condition = close > close[1] and close > close[2] and d_line < v_input_5
short_condition = close < close[1] and close < close[2] and k_line > v_input_5

if (long_condition)
    strategy.entry("Long", strategy.long)

if (short_condition)
    strategy.exit("Short", "Long")

// Second strategy
mfi = marketfacilitationindex(close, v_input_2, v_input_3, v_input_4)
buy_zone = v_input_7
sell_zone = v_input_8

if (mfi > buy_zone and v_input_6)
    strategy.entry("Buy", strategy.long)

if (mfi < sell_zone and v_input_6)
    strategy.close("Buy")

plotshape(series=strategy.opentrades>0, location=location.belowbar, color=color.green, style=shape.labelup, text="Long Entry")
plotshape(series=strategy.closedtrades>0, location=location.abovebar, color=color.red, style=shape.labeldown, text="Short Exit")
```