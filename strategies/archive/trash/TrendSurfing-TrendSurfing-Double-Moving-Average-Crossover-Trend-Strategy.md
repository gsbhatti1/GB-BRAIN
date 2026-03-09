> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|9|Fast MA Length|
|v_input_2|21|Slow MA Length|
|v_input_3|14|ROC Length|
|v_input_4|14|RSI Length|
|v_input_5|2.0|ATR Multiplier for Stop Loss and Take Profit|


> Strategy Description

TrendSurfing-Double-Moving-Average-Crossover-Trend-Strategy is a trend tracking strategy primarily based on double moving average crossover signals. It also incorporates triangle visual indicators, 200-day EMA, ROC indicator, and RSI indicator to filter out noise and accurately capture trend reversals. This strategy is suitable for medium-to-long-term holding and can achieve steady growth in a bull market.

## Overview

The TrendSurfing strategy mainly relies on golden cross and death cross formed by fast moving average (FMA) and slow moving average (SMA) to generate buy and sell signals. When the FMA crosses above the SMA, a buy signal is generated; when the FMA crosses below the SMA, a sell signal is generated.

In addition, this strategy incorporates multiple auxiliary indicators to filter out false signals or determine trend quality:

1. **ROC Indicator** - To determine price trend and momentum
2. **RSI Indicator** - To detect overbought/oversold levels  
3. **200-day EMA** - To determine overall trend direction  
4. **Triangle Visual Indicators** - To mark entry points on the chart

By comprehensively judging these indicators, the TrendSurfing strategy can accurately locate trend turning points and track definite medium-to-long term trends without being misled by market noise or short-term corrections.

## Advantage Analysis

### 1. Catch Medium-to-Long Term Trends
The strategy primarily judges trend reversals based on moving average crosses (FMA crossing above SMA for buy, FMA crossing below SMA for sell), using indicators like 200-day EMA to filter out short-term noise and focus on medium-to-long term trends.

### 2. Multiple Indicators Ensure High Quality Entry
In addition to the MA crossovers themselves, the incorporation of ROC, RSI, and other indicators ensures avoidance of consolidation zones at trend reversal points, ensuring high-quality entries.

### 3. Intuitive Triangle Visual Indicators  
Green downward triangles indicate long entry opportunities, while red upward triangles indicate short entry opportunities. This makes it clear and easy to read.

### 4. Customizable Parameters for Different Needs
Users can freely adjust parameters such as MA periods, ROC length, RSI length, etc., according to their own trading style.

### 5. Stop Loss and Take Profit Control  
The strategy sets stop loss and take profit levels based on ATR multiplied by a risk percentage, enabling per-trade risk control.

## Risk Analysis

### 1. Risk of Missing Trades
Any moving average crossover-based strategy inherently has the risk of missing trades or being stopped out when MAs are oscillating.

### 2. Over-Optimization from Improper Parameter Settings  
Users should avoid chasing hypothetically ideal parameter values and test parameters based on different market conditions and products to prevent over-optimization.

### 3. Inability to Fully Filter Black Swan Events
Under extreme market conditions, strategies might still face large losses due to systemic market risks.

## Optimization Directions

### 1. Test and Optimize Parameter Values  
Periods of MAs, lengths of ROC, RSI values, etc., should undergo rigorous backtesting and optimization to fit the characteristics of different trading products.

### 2. Test and Incorporate Other Auxiliary Indicators  
Continue testing combinations of other indicators like BOLL, KDJ, etc., with moving average crosses for better performance.

### 3. Coordinate with Algorithmic Trading for Better Risk Control  
Introduce machine learning algorithms to enable more intelligent stop loss and take profit mechanisms that can adapt to dynamic market environments.

### 4. Explore Combinations with Other Strategies or Models  
Combining with fundamentals-based stock picking strategies, statistical arbitrage strategies, portfolio optimization models, etc., could further enhance risk control and return.

## Conclusion

The TrendSurfing strategy is a simple, direct trend tracking strategy with controllable risk. Trading signals are generated from moving average crosses and filtered by multiple auxiliary indicators. It is suitable for medium-to-long term holding to steadily track bull market trends. We will continue optimizing this strategy through parameter testing, indicator expansion, risk control measures, etc., to achieve more reliable performance across diverse markets.

[/trans]