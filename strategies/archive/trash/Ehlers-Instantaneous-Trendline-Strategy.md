> Name

Ehlers Instantaneous Trendline Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/752e6967715196d91f.png)

[trans]

### Overview

The Ehlers Instantaneous Trendline strategy is proposed by John Ehlers in his book "Cybernetic Analysis for Stocks and Futures." It utilizes technical indicators to identify real-time trends of stocks or futures and open positions when trends reverse.

### Strategy Logic

The core of this strategy is calculating the Instantaneous Trendline (IT). The formula for IT is:

```
it := (a-((a*a)/4.0))*src+0.5*a*a*src[1]-(a-0.75*a*a)*src[2]+2*(1-a )*it[1]-(1-a )*(1-a )*it[2]
```

where `src` is the price, and `a` is a smoothing factor with a default value of 0.07. This formula is a second-order filter that can smooth the price and generate trends.

Another key indicator is the lag line, calculated by:

```  
lag = 2.0 * it - nz(it[2])
```

The lag line lags IT line by one bar. When the price crosses above the lag line, it signals an upside breakout, go long; when the price crosses below the lag line, it signals a downside breakout, go short.

In addition, the strategy sets stop loss orders to control risks.

### Advantage Analysis

This strategy has the following advantages:

1. The IT line effectively filters noise and improves signal quality.
2. The 2nd order filter provides more tuning flexibility and robustness.
3. The lag line avoids unnecessary whipsaws within trends.
4. Incorporated stop losses control risks at predefined levels.
5. Clean code structure, easy to understand and modify.

### Risk Analysis

There are also some risks associated with this strategy:

1. Improper parameter tuning of IT/lag line may generate false signals.
2. Bad stop loss configuration could result in premature stop out or oversized loss.
3. High trading frequency leads to accumulated commission fees.
4. Long holding times increase loss magnification risk.

These risks can be alleviated by:

1. Applying machine learning for parameter optimization.
2. Setting adaptive stop loss levels.
3. Reducing position sizes to lower trade frequencies.
4. Incorporating holding period stop losses.

### Optimization Directions

This strategy can be further optimized in the following aspects:

1. Test impacts of different filter parameters to find optimum values.
2. Try combining other indicators to filter signals and improve quality.
3. Improve entry logic to size up during trend acceleration stages.
4. Set up adaptive stop loss based on market volatility.
5. Conduct time series analysis on trading sessions and frequencies.

### Conclusion

Overall, the Ehlers Instantaneous Trendline strategy utilizes technical indicators to identify real-time trends in stocks or futures and open positions when trends reverse. It has the advantages of effective noise filtering, high parameter tuneability, clear signal generation logic, and incorporated risk control. With further optimization on parameter selection, signal filtering, position sizing, and stop loss tuning, this strategy can achieve even better performance. The clear code structure also makes it easy to understand and modify. In summary, this is an efficient trend following system worth testing and improving.

[/trans]

> Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|v_input_1_hl2|0|Source: hl2|high|low|open|close|hlc3|hlcc4|ohlc4|
|v_input_2|0.07|Alpha|
|v_input_3|false|Fill Trend Region|
|v_input_4|0.35|rngFrac|
|v_input_5|0.015|revPct|
|v_input_6|0|Stop type: stop-order|market-order|None|
|v_input_7|0.5|Spread|
|v_input_8|false|Custom Backtesting Dates|
|v_input_9|2018|Backtest Start Year|
|v_input_10|9|Backtest Start Month|
|v_input_11|true|Backtest Start Day|
|v_input_12|false|Backtest Start Hour|
|v_input_13|2018|Backtest Stop Year|
|v_input_14|12|Backtest Stop Month|
|v_input_15|14|Backtest Stop Day|
|v_input_16|14|Backtest Stop Hour|

> Source (PineScript)

```pinescript
//@version=3
strategy("Ehlers Instantaneous Trendline Strategy", shorttitle = "Ehlers Instantaneous Trendline Strategy", overlay = true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100.0, pyramiding = 1, backtest_fill_limits_assumption = 1)
src = input(hl2, title="Source")
a = input(0.07, title="Alpha", step=0.01) 
fr = input(false, title="Fill Trend Region")
it = na
if (na(it[2]) or na(it[1]))
    it := (src + 2 * src[1] + src[2]) / 4.0
else
    it := (a-((a*a)/4.0))*src+0.5*a*a*src[1]-(a-0.75*a*a)*src[2]+2*(1-a )*it[1]-(1-a )*(1-a )*it[2]
lag = 2.0 * it - nz(it[2])
rngFrac = input(0.35)
revPct = input(0.015)
stopType = input(title="Stop type", defval = "stop-order", options = ["stop-order", "market-order",