> Name

Three-Bar and Four-Bar Breakout Reversion Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/b14fb69f28005f643a.png)
 [trans]

### Overview

The Three-Bar and Four-Bar Breakout Reversion strategy identifies K-lines with strong momentum, either three or four consecutive bars. After several smaller-range K-lines form support or resistance levels, a reversal K-line is identified to initiate a counter-trend trade, which falls under mean-reversion trading.

### Strategy Logic

The core identification logic of this strategy includes:

1. **Identifying Large-Magnitude Bars (Gap Bars):** Bars that break through 1.5 times the Average True Range (ATR), with a body percentage above 65%. These bars are considered to have strong upward or downward momentum.

2. **Identifying Low-Range Bars (Collecting Bars):** One or two subsequent K-lines following Gap Bars, with high/low levels close to those of the Gap Bar. These bars represent slowing momentum and consolidation, forming support or resistance levels.

3. **Identifying Reversal Signal Bars:** After a period of consolidation, if a bar breaks through the high or low of previous bars, it can be considered a reversal signal. Positions are taken based on the direction of the signal bar.

4. **Stop Loss and Take Profit:** Set stop loss below or above the Gap Bar's low/high point; take profit is determined by multiplying the risk-reward ratio with the stop loss distance.

### Advantage Analysis

The main advantages of this strategy include:

1. Using K-line features to identify trends and reversals without relying on any indicators, achieving "indicator-free" trading.
2. Strict rules for Gap Bars and Collecting Bars ensure accurate identification of true trends and consolidations.
3. Judging reversal bars by the body reduces the probability of false signals.
4. Each trade only requires 3-4 K-lines; this results in short holding periods and high frequency.
5. Clear stop loss and take profit rules make risk management easier.

### Risk Analysis

The main risks associated with this strategy include:

1. Dependency on parameter settings, which can increase the likelihood of false signals and losing trades if set too loosely.
2. Vulnerability to frequent false breakouts that cannot be fully filtered out.
3. Risk of being trapped in consolidations after failed breakout attempts, making it difficult to cut losses.
4. Wide stop loss range leading to potential large losses on occasion.

To mitigate these risks:

1. Optimize parameters for Gap Bars and Collecting Bars identification.
2. Add filters such as confirmation bars before entering positions.
3. Optimize stop loss algorithms to make them more adaptive.

### Optimization Directions

Main optimization directions include:

1. Adding composite filters to avoid false breakouts, e.g., requiring an increase in volume.
2. Combining with moving averages and only taking signals when key MA levels are broken.
3. Requiring agreement across multiple timeframes before entering trades.
4. Dynamically adjusting profit targets based on market volatility and risk preference.
5. Integrating a market regime identification system to enable the strategy only in trending environments.

These optimizations can further improve stability and profitability.

### Conclusion

The Three-Bar and Four-Bar Breakout Reversion strategy aims to capture high-quality trending moves and reversal trades through identifying strong momentum bars, followed by consolidation bars forming support or resistance levels. It has the advantage of short holding periods and high frequency, though there are inherent risks that need to be reduced through continued optimization. By effectively identifying self-contained trend and reversal signals from raw price action, this strategy warrants further research and application.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|From Month|
|v_input_2|true|From day|
|v_input_3|2021|From Year|
|v_input_4|12|To Month|
|v_input_5|31|To day|
|v_input_6|2100|To Year|
|v_input_7|1.5|Gap Bar Size|
|v_input_8|0.65|Gap Bar Body Size|
|v_input_9|0.1|Bull Top Bar Size|
|v_input_10|2|Profit Multiplier|
|v_input_11|true|Show Buy/Sell Labels?|

> Source (PineScript)

```pinescript
//@version=4
strategy(title="Three (3)-Bar and Four (4)-Bar Plays Strategy", shorttitle="Three (3)-Bar and Four (4)-Bar Plays Strategy", overlay=true, calc_on_every_tick=true, currency=currency.USD, default_qty_value=1.0, initial_capital=30000.00, default_qty_type=strategy.percent_of_equity)

frommonth = input(defval = 1, minval = 01, maxval = 12, title = "From Month")
fromday = input(defval = 1, minval = 01, maxval = 31, title = "From day")
fromyear = input(defval = 2021, minval = 1900, maxval = 2100, title = "From Year")

tomonth = input(defval = 12, minval = 01, maxval = 12, title = "To Month")
today = ...