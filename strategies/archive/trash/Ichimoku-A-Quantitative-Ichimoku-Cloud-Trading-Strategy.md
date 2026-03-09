> Name

A-Quantitative-Ichimoku-Cloud-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1607814fab3632e6ec0.png)
[trans]

### Overview

This strategy is based on the Ichimoku Cloud, a famous trend indicator in technical analysis, to determine market trends and generate trading signals by observing the crossover relationships between the Conversion Line, Base Line, and Cloud from the Ichimoku system. It is suitable for traders who want to track intermediate-term trends in the market.

### Strategy Logic

The core components of this strategy are the three lines from the Ichimoku Cloud system: Conversion Line, Base Line, and Cloud Lines. The Conversion Line represents short-term price action, the Base Line shows intermediate-term trends, while the Cloud visualizes areas of support and resistance. The strategy identifies market trends and trading opportunities by detecting crossovers between these three elements.

Specifically, the main rules of this strategy are:

1. When the Base Line crosses above the Cloud, an upward trend is emerging in the intermediate-term, go long.
2. When the Conversion Line crosses above the Cloud, prices are starting to bounce back short-term, go long.
3. When the Base Line crosses below the Cloud, a downward trend is emerging, go short.
4. When the Conversion Line crosses below the Cloud, prices are starting to fall short-term, go short.

In addition, crossovers between price and Cloud Lines act as filters for trade signals. Only when both the Conversion/Base Line and price cross the cloud together will a valid signal be generated.

### Advantage Analysis

Compared to single indicators like moving averages, the biggest advantage of this strategy is incorporating data from multiple timeframes to detect trend changes. The Conversion Line shows short-term moves, the Base Line intermediate moves, and the Cloud reveals longer-term support/resistance levels. Their combination identifies turning points more accurately. Also, the inherent filtering mechanism of the Ichimoku reduces whipsaws from market noise, allowing us to capture the bigger trend.

### Risk Analysis

The biggest risk is that the Ichimoku system is sensitive to input parameters. Inappropriate settings may produce bad signals frequently. Additionally, during range-bound periods, the cloud tends to flatten, causing uncertain signals. Frequent order openings and stops may incur large commission fees. Moreover, intermediate-term trades come with larger loss risks per trade, requiring strict risk control.

To mitigate risks, we can tweak the parameter mix, set stop loss/take profit levels, or combine Ichimoku with other indicators.

### Enhancement Opportunities

There are several ways we can enhance this strategy:

1. Optimize parameter combinations to find the best fit for different trading instruments.
2. Add filtering conditions with other indicators to reinforce trend validation. For example, only take signals when trading volume expands.
3. Incorporate stop loss mechanisms like trailing stops or time stops to control single trade loss.
4. Combine with swing trading approaches to fine-tune entry timing within bigger trends.

### Conclusion

The Ichimoku Cloud strategy identifies intermediate-term trends using crossovers of the Conversion/Base Lines against the Cloud. Compared to single indicators, it incorporates multiple timeframes for reliable trend change detection. The inherent noise filtering also avoids whipsaws. With proper parameter tuning and risk management, this strategy can generate stable excess returns over the long run. It suits experienced trend traders with intermediate-term holding periods.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|9|Conversion Line Periods|
|v_input_2|26|Base Line Periods|
|v_input_3|52|Lagging Span 2 Periods|
|v_input_4|26|Displacement|


> Source (PineScript)

``` pinescript
//@version=3
strategy(title="Ichimoku Cloud", shorttitle="Ichimoku", overlay=true, default_qty_type=strategy.cash, default_qty_value=100000, initial_capital=100000, currency=currency.USD)


conversionPeriods = input(9, minval=1, title="Conversion Line Periods"),
basePeriods = input(26, minval=1, title="Base Line Periods")
laggingSpan2Periods = input(52, minval=1, title="Lagging Span 2 Periods"),
displacement = input(26, minval=1, title="Displacement")

donchian(len) => avg(lowest(len), highest(len))

conversionLine = donchian(conversionPeriods)
baseLine = donchian(basePeriods + displacement)
laggingSpan1 = donchian(basePeriods - laggingSpan2Periods)
laggingSpan2 = donchian(basePeriods)

plot(series=conversionLine, title="Conversion Line", color=color.blue)
plot(series=baseLine, title="Base Line", color=color.red)
plot(series=laggingSpan1, title="Lagging Span 1", color=color.orange)
plot(series=laggingSpan2, title="Lagging Span 2", color=color.green)

cloudTop = highest(conversionLine, basePeriods + displacement) - donchian(displacement)
cloudBottom = lowest(laggingSpan1, laggingSpan2Periods) + donchian(displacement)
fill(series=plot(baseLine), color=color.new(color.blue, 90), transp=50)

longCondition = crossover(conversionLine, baseLine)
shortCondition = crossunder(conversionLine, baseLine)

if (longCondition)
    strategy.entry("Long", strategy.long)

if (shortCondition)
    strategy.exit("Short", from_entry="Long", limit=cloudTop, stop=cloudBottom)
```