> Name

Three-Bar and Four-Bar Breakout Reversion Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/b14fb69f28005f643a.png)
 [trans]

### Overview

The Three-Bar and Four-Bar Breakout Reversion strategy identifies K-line bars with strong momentum, typically three or four consecutive large-range K-bars. After several smaller-range K-bars form support or resistance levels, a reversal occurs when an opposing K-bar is detected. This strategy falls under the category of mean-reversion strategies.

### Strategy Logic

The core identification logic for this strategy includes:

1. **Identify Large-Range Bars (Gap Bars):** These are bars that break through 1.5 times the Average True Range (ATR) and have a body percentage above 65%. They are considered to have strong momentum.

2. **Identify Small-Ranged Bars (Collecting Bars):** One or two subsequent smaller-range K-bars following Gap Bars, with their highs or lows close to those of the Gap Bar. These bars represent slowing momentum and consolidation, forming support or resistance levels.

3. **Identify Reversal Signal Bars:** If a bar breaks through the high or low of previous bars after consolidation, it can be considered a reversal signal. We take positions based on the direction of the reversal signal bar.

4. **Stop Loss and Take Profit:** Set stop loss below/above the Gap Bar's low/high points. Take profit is determined by multiplying risk-reward ratio with stop loss distance.

### Advantage Analysis

The main advantages of this strategy are:

1. Identifying trends and reversals using K-line patterns, no need for additional indicators.
2. Strict rules on Gap Bars and Collecting Bars ensure accurate identification of true trends and consolidations.
3. Judging reversal bars by their bodies reduces false signals.
4. Each trade only requires 3-4 K-bars, with short holding periods and high frequency.
5. Clear stop loss and take profit rules simplify risk management.

### Risk Analysis

The main risks associated with this strategy include:

1. Relying heavily on parameter settings; loose parameters can increase the likelihood of false signals and losing trades.
2. Vulnerable to frequent false breakouts, which cannot be filtered out entirely.
3. Risk of being trapped in consolidations following failed breakout attempts.
4. Wide stop loss range could lead to significant losses if positions are taken.

To mitigate these risks:

1. Optimize parameters for Gap Bars and Collecting Bars identification.
2. Add filters such as confirmation bars before entering positions.
3. Optimize stop loss algorithms to make them more adaptive.

### Optimization Directions

Main optimization directions include:

1. Adding composite filters to avoid false breakouts, such as requiring an increase in volume.
2. Combining with moving averages (e.g., only taking signals when key MA levels are broken).
3. Requiring agreement across multiple timeframes before entering trades.
4. Dynamically adjusting profit targets based on market volatility and risk preference.
5. Integrating a market regime identification system, enabling the strategy only in trending environments.

These optimizations can further improve stability and profitability.

### Conclusion

The Three-Bar and Four-Bar Breakout Reversion strategy aims to capture high-quality trending moves and reversal trades by identifying K-line patterns with strong momentum. It has the advantage of short holding periods and high frequency but also comes with inherent risks that need to be reduced through continued optimization. By effectively identifying self-contained trend and reversal signals from raw price action, this strategy warrants further research and application.

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
strategy(title="Three-Bar and Four-Bar Breakout Reversion Strategy", shorttitle="3-4 Bar Play Strategy", overlay=true, calc_on_every_tick=true, currency=currency.USD, default_qty_value=1.0, initial_capital=30000.00, default_qty_type=strategy.percent_of_equity)

frommonth = input(defval=1, minval=1, maxval=12, title="From Month")
fromday = input(defval=1, minval=1, maxval=31, title="From day")
fromyear = input(defval=2021, minval=1900, maxval=2100, title="From Year")

tomonth = input(defval=12, minval=1, maxval=12, title="To Month")
today 