```markdown
> Name

Dynamic Average Cost Dollar Cost Averaging Compound Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/198c51b795f2997eeab.png)
[trans]

#### Overview

The dynamic average cost DCA compound strategy dynamically adjusts the quantity of each opening position. At the beginning of the trend, it first opens small positions to build a position. As the depth of consolidation increases, it gradually increases the position size. The strategy uses exponential functions to calculate stop loss price levels, and re-opens new batches when triggered, which can cause the cost of holding positions to continue to decline exponentially. As the depth increases, the cost of the positions can be gradually reduced. When the price reverses, the batch profit taking allows for greater returns.

#### Strategy Logic

This strategy uses a simple combination of RSI oversold signals and moving averages timing to determine entry opportunities. A first entry order is submitted when RSI drops below oversold level and close price below moving average. After the first entry, the exponential function calculates price drop percentage for next levels. Each time it triggers a DCA order, position sizing is recalculated to keep equal amount per entry. As position size and cost change dynamically, it creates a leverage effect.

As DCA count increases, average holding cost continues to decline. Just a small rebound is enough for take profit of each position. After continuous entries submitted, a stop loss line is plotted above average holding price. Once the price breaks out above average price and stop loss line, all positions are closed.

The biggest advantage is that as the holding cost continues to decline, even during consolidation, cost can still be reduced cumulatively step by step. When trend reverses, due to much lower holding cost than market price, much bigger profit can be realized.

#### Risks and Defects

The biggest risk is the limited position size initially. During continuous decline, there can be stop loss risk. So the stop loss percentage needs to be set reasonably based on personal risk appetite.

In addition, setting stop loss level has two extremes. If too loose, not enough retracement can be captured. But if too tight, probability of getting stopped out during mid-term corrections increases. So choosing proper stop loss levels according to different market conditions and risk preference is crucial.

If there are too many DCA levels, when price rises substantially, extremely high holding cost may prevent effective stop loss. So maximum layers of DCA need to be set reasonably based on total capital allocation and highest cost one can endure.

#### Optimization Suggestions

1. Optimize entry timing signals, by testing parameters and other indicators combinations for higher win rate signals.
2. Optimize stop loss mechanisms, by testing Λ trailing stop loss or curve fitted trailing stop loss to get better results. Also the levels can be adjusted dynamically based on position allocation percentage.
3. Optimize take profit ways. Different types of trailing take profits can be examined for better exit opportunities and higher total return.
4. Add anti-whipsaw mechanism. Sometimes DCA signal can be triggered again soon after stop loss. A whipsaw range can be added to avoid aggressive re-entries right after stops.

#### Conclusion

This strategy utilizes RSI to determine entries, exponential dynamic stop loss DCA mechanism to adjust position sizing and average costs dynamically, in order to gain price advantage during consolidations. The main optimization areas are focused on entry/exit signals, stop loss and take profit. The core concept of exponential DCA is implemented to shift holding cost lower continually, thus providing more room during consolidations, and achieving multiplied returns when trend emerges. But parameters still need be set carefully based on capital allocation plans to control overall position risks.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|timestamp(01 April 2021 20:00)|(?Backtest Window)Start Time|
|v_input_2|timestamp(01 Aug 2030 20:00)|End Time|
|v_input_float_1|3|(?Risk)Take Profit %|
|v_input_float_2|6|Close All %|
|v_input_int_1|8|(?DCA Settings)Max Amount of Entries|
|v_input_float_3|2|Price Drop % to open First DCA Order|
|v_input_float_4|1.4|Exponential Scale DCA levels|
|v_input_int_2|4999|Lines Bar Lookback|
|v_input_bool_1|false|(?Moving Average)Plot Moving Average|
|v_input_int_3|100|MA Length|
|v_input_int_4|14|(?RSI Settings)RSI Length|
|v_input_source_1_close|0|Source
```