> Name

Momentum-Oscillation-Crossing-Bollinger-Bands-with-Moving-Average-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/13f8bcd85b80b7f898c.png)
[trans]

## Overview

This is a quantitative trading strategy based on Bollinger Bands and MACD indicators. It combines two mainstream technical indicators to identify trading opportunities, aiming to achieve a higher win rate in trending markets.  

The strategy will establish a long position when price breaks through the lower band of Bollinger Bands for trend following, and close the position when price breaks through the upper band. MACD indicator is used to filter false breakouts by judging momentum direction. RSI indicator can be configured to assist in identifying overbought and oversold levels to further avoid losses.

## Strategy Logic

The strategy consists mainly of Bollinger Bands and MACD indicators.  

Bollinger Bands calculate upper and lower bands based on the standard deviation of prices. An upward breakout of the upper band signals an overbought condition, while a downward breakout of the lower band signals an oversold condition. This strategy goes long when price breaks down the lower band, and closes the position when it breaks up the upper band.

MACD indicator judges momentum and direction of prices. A crossover of the short term moving average above the long term moving average is a buy signal, while a crossover below is a sell signal. MACD helps filter false breakouts of Bollinger Bands in this strategy.

Additionally, RSI indicator can assist in identifying overbought/oversold levels. A low RSI represents oversold and enhances the buy signal, while a high RSI represents overbought and enhances the sell signal.

## Advantages of the Strategy   

The strategy combines Bollinger Bands, MACD and RSI indicators, which can effectively determine price trend and volatility. Its advantages include:

1. Bollinger Bands capture trend following when price breaks out of bands  
2. MACD filters false signals from Bollinger Bands by judging momentum
3. RSI avoids buying at peak by identifying overbought/oversold levels
4. Higher win rate can be achieved through parameter optimization

## Risks of the Strategy

There are also some risks to be aware of:   

1. High risk of stop loss when prices fluctuate violently
2. Profitability decreases with improper parameter settings
3. MACD may misjudge when trend reverses  

Countermeasures:  

1. Stop loss percentage can be loosened appropriately 
2. Extensive backtesting required to find optimum parameters
3. More indicators can be used to predict trend reversal  

## Directions for Optimization

Major directions to optimize the strategy include:

1. Optimize parameters of Bollinger Bands for more market regimes 
2. Increase indicators to improve robustness
3. Utilize machine learning to auto optimize parameters  
4. Test strategy performance on high frequency data
5. Add risk management module to limit per trade loss

## Conclusion   

Overall this is a typical trend following strategy. By combining multiple technical indicators, it improves robustness and can achieve decent win rate when signals are accurate. However risks need to be monitored. Further improvements can be made through continuous optimization and tuning.  

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|0|Simple bot: simple|composite|
|v_input_2||3Commas Bot ID|
|v_input_3||Bot Email Token|
|v_input_4|10|Base order size|
|v_input_5|400|Safety order size|
|v_input_6|1.83|Safety Order Vol Scale (%)|
|v_input_7|1.55|Safety Order Step Scale (%)|
|v_input_8|2|Max Number of Safety Orders|
|v_input_9|1.54|Initial SO Deviation (%)|
|v_input_10|15|Long Stop Loss (%)|
|v_input_11|1.4|Long Take Profit (%)|
|v_input_12|21|Short MA Window|
|v_input_13|100|Long MA Window|
|v_input_14|2.2|Upper Band Offset|
|v_input_15|2.4|Lower Band Offset|
|v_input_16|0|Entry at Cross Over/Under Lower: under|over|
|v_input_17|true|Start Date|
|v_input_18|true|Start Month|
|v_input_19|2016|Start Year|
|v_input_20|31|End Date|
|v_input_21|12|End Month|
|v_input_22|2022|End Year|
|v_input_47|true|Use long?|
|v_input_48|true|Use short?|
|v_input_23|23|(?MACD)Fast Length|
|v_input_24|16|Slow Length|
|v_input_25_open|0|Source: open|high|low|close|hl2|hlc3|hlcc4|ohlc4|
|v_input_26|9|Signal Smoothing|
|v_input_27|0|Simple MA FAST (Oscillator): EMA|DHMA|THMA|FHMA|WMA|DWMA|TWMA|FWMA|SMA|DSMA|TSMA|FSMA|HMA|DEMA|TEMA|FEMA|RMA|DRMA|TRMA|FRMA|
|v_input_28|0|Simple MA SLOW (Oscillator): EMA|DHMA|THMA|FHMA|WMA|DWMA|TWMA|FWMA|SMA|DSMA|TSMA|FSMA|HMA|DEMA|TEMA|FEMA|RMA|DRMA|TRMA|FRMA|
|v_input_29|0|Simple MA(Signal Line): EMA|DHMA|THMA|FHMA|WMA|DWMA|TWMA|FWMA|SMA|DSMA|TSMA|FSMA|HMA|DEMA|TEMA|FEMA|RMA|DRMA|TRMA|FRMA|
|v_input_30|true|(?Stress)Use stress on recent bars|
|v_input_31|0.41|Stress on recent bars|
|v_input_32|6|Level of stress|
|v_input_33|true|