> Name

Percentage-Volume-Oscillator-Strategy

> Author

ChaoZhang

> Strategy Description


![IMG](https://www.fmz.com/upload/asset/127576aa2b2f95ff6a8.png)
[trans]

Overview:

The Percentage Volume Oscillator (PVO) is a momentum oscillator for volume. PVO measures the difference between two volume-based moving averages as a percentage of the larger moving average to gauge shifts in volume trends. This strategy uses PVO to identify volume trends to confirm or refute price action. Typically, a breakout or support break is validated when PVO is rising or positive.

Strategy Logic:

1. Calculate short period volume EMA (default 12 days)
2. Calculate long period volume EMA (default 26 days)
3. Calculate PVO as the percentage difference between short and long EMA
4. Calculate signal line EMA on PVO (default 9 days)
5. Calculate histogram as difference between PVO and signal line
6. Go short when signal line crosses above PVO, go long when crosses below
7. Option to reverse trade direction
8. Color bars based on signal

The strategy forms PVO indicator through double EMA composition and uses signal line to identify volume trend changes to anticipate potential price direction. Unlike regular double EMA, PVO focuses more on volume percentage difference for clearer judgement of volume increase/decrease.

Advantages:

1. Utilize volume changes to determine future price trends as early warning
2. Simple and practical double EMA structure with flexible parameter tuning
3. Visualized color bars for intuitive trend judgement and easy operation
4. Signal line reduces false signals and improves stability
5. Optional reverse trading enriches strategy usage
6. Applicable for mid-to-long term trends and short term trading

The strategy fully utilizes the indicative effect of volume changes on price action. Compared to single indicator, the PVO structure is more stable with customizable parameters to judge volume trend changes and detect potential price direction in advance. The intuitive color differentiation strengthens trend decision and reverse trading option makes it a versatile volume based strategy.

Risks:

1. Volume indicator lags price signal and may diverge
2. Improper EMA parameter setting may misjudge market state
3. Reverse trading needs caution, can increase loss
4. Volume change alone cannot determine specific entry point
5. Volume does not fully predict price, needs combining with other indicators

Volume change often lags price action and PVO may give wrong signal when price approaches trend end. Wrong parameter settings can also affect judgement accuracy. Caution is needed when reverse trading, as trend may extend. Volume alone cannot determine precise entry point and needs aid of other indicators for timing. Volume does not fully predict price and needs prudent following.

Optimization:

1. Optimize EMA periods for different products and timeframes
2. Add filter conditions to avoid invalid signals
3. Combine other indicators to confirm entry timing  
4. Add stop loss

Testing and optimizing EMA combinations to find best periods for trend detection. Adding volume fluctuation threshold to filter ineffective signals. Incorporating MACD, KD for further entry confirmation. Setting stop loss to control single trade loss. These will greatly improve strategy applicability.

Conclusion:

The Percentage Volume Oscillator strategy judges volume trend changes by calculating the percentage difference between volume EMAs to anticipate potential price direction. It adopts simple and effective double EMA structure to measure volume fluctuations and uses intuitive color coding to enhance visual effect. The flexible reverse trading option and parameter settings make it suitable for both mid-to-long term and short term trading. But as volume indicator lags price signal and cannot determine precise entry timing, parameters and incorporation of other indicators need optimization to improve strategy performance.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|12|LengthShortEMA|
|v_input_2|26|LengthLongEMA|
|v_input_3|9|LengthSignalEMA|
|v_input_4|false|Trade reverse|


> Source (PineScript)

```pinescript
//@version=2
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 27/09/2017
// The Percentage Volume Oscillator (PVO) is a momentum oscillator for volume.
// PVO measures the difference between two volume-based moving averages as a percentage of the larger moving average to gauge shifts in volume trends.

study("Percentage-Volume-Oscillator-Strategy", shorttitle="PVO", precision=0)

short_ema_length = input(v_input_1, title="LengthShortEMA")
long_ema_length = input(v_input_2, title="LengthLongEMA")
signal_ema_length = input(v_input_3, title="LengthSignalEMA")

pvo = (volume[0] - volume[-short_ema_length]) / volume[-short_ema_length] * 100
pvo_short_ema = ema(pvo, short_ema_length)
pvo_long_ema = ema(pvo, long_ema_length)

pvo_signal_ema = ema(pvo_short_ema, signal_ema_length)

plot(pvo_short_ema, "PVO", color=green, linewidth=2)
plot(pvo_long_ema, "Signal Line", color=red, linewidth=1.5)
histogram(pvo_signal_ema - pvo_short_ema, "Histogram")

buy_condition = crossover(pvo_long_ema, pvo_signal_ema)
sell_condition = crossunder(pvo_long_ema, pvo_signal_ema)

plotshape(series=buy_condition, title="Buy Signal", location=location.belowbar, color=lime, style=shape.labelup, text="BUY")
plotshape(series=sell_condition, title="Sell Signal", location=location.abovebar, color=red, style=shape.labeldown, text="SELL")

strategy("PVO Strategy", overlay=true)
if (buy_condition)
    strategy.entry("Long Position", strategy.long)
if (sell_condition)
    strategy.close("Long Position")

reverse_trade = v_input_4
if (reverse_trade)
    if (not buy_condition and not sell_condition)
        strategy.entry("Short Position", strategy.short)
    if buy_condition or sell_condition
        strategy.close("Short Position")
```