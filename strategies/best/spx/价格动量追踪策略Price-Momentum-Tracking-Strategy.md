> Name

Price-Momentum-Tracking-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1646bdd6510619422d1.png)

### Overview

This strategy uses price momentum indicators to determine the trading direction. Specifically, it calculates the moving average and mean price respectively. When the price crosses above the moving average and mean price, a buy signal is generated. To filter out false signals, it requires no similar previous signals. Then it saves the signal status and generates the final opening position signal in combination with the moving average. The strategy also contains stop loss and take profit settings.

### Strategy Principle

The strategy mainly relies on price momentum indicators to judge the trend direction. First, it calculates the moving average and mean price of the price:

```pine
swmaClose = swma(close)
vwapClose = vwap(close) 
```

Where `swma` is the smoothed moving average and `vwap` is volume weighted average price. Both can reflect the average price level.

Then compare the price with the average to see if the price crosses above the moving average and mean price, to judge if it is a bullish signal:

```pine
swmaLong = close > swmaClose 
vwapLong = close > vwapClose
```

To filter out false signals, it requires no previous signals from these two indicators:

```pine  
triggerLong = vwapLong and not vwapLong[1] and not swmaLong and not swmaLong[1] 
```

Next, save the bullish signal:  

```pine
saveLong = false, saveLong := triggerLong ? true : not vwapLong ? false : saveLong[1] 
```

Finally, when the saved crossing signal and the price crosses above the moving average again, generate the opening position signal:

```pine
startLong = saveLong and swmaLong
```

This can filter out some false signals and make the signals more reliable.

The strategy also contains stop loss and take profit settings. The stop loss distance is configurable, and the take profit is set to a certain multiple of the stop loss.

### Advantage Analysis

The strategy has the following advantages:

1. Using price momentum indicators can better judge the trend direction
2. The combination of dual indicators and multi-step verification can filter false signals and make the strategy more reliable
3. The stop loss and take profit settings are reasonable to control single trade risk
4. The strategy parameters are configurable to adapt to different market environments
5. The strategy logic is simple and straightforward, easy to understand and implement

### Risk Analysis

The strategy also has some risks:

1. The moving average indicator has a lag and may miss some price fluctuations  
2. The effect relies on parameter settings, and different parameter combinations can make big differences
3. There are relatively few buy signals, with some missed trade risks
4. Multi-step verification will filter some opportunities, which may impact profit level  

Countermeasures:
1. Test different moving average parameters for parameter optimization
2. Slightly simplify the logical judgment to increase buy signals  
3. Adjust the stop loss and take profit ratio to control single loss

### Optimization Directions

The strategy can also be optimized in the following directions:

1. Test more price momentum indicators such as MACD, DMI, etc.
2. Add sell signal judgments to implement dual-direction trading
3. Incorporate trading volume indicators to avoid potential false breakouts  
4. Optimize parameter settings based on backtest results  
5. Consider automatically adjusting parameters based on market conditions
6. Add machine learning algorithms to achieve parameter self-adaptive optimization  

These optimizations can improve strategy flexibility, robustness and profitability.

### Summary

Overall, this price momentum tracking strategy is a simple, straightforward, and logical trend tracking strategy. The strategy uses price moving averages and mean prices to determine price momentum direction, and designs a multi-step verification mechanism to improve signal quality. The strategy also contains reasonable stop loss and take profit settings. In terms of code, the strategy logic is very concise, requiring only 20+ lines of Pine script to implement. In summary, this strategy is a very good learning example, beginners can use it as a very good starting point to understand quantitative trading strategies. Of course, the strategy itself also has practical trading value, through parameter optimization and function expansion, it can become a useful trading system that avoids noise and tracks trends.