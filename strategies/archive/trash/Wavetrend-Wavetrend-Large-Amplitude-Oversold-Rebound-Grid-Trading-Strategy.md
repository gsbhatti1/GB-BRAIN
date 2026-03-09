> Name

Wavetrend-大幅指标超跌反弹网格交易策略-Wavetrend-Large-Amplitude-Oversold-Rebound-Grid-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1138c476066faee3b5f.png)

[trans]
#### Overview
This strategy is based on the Wavetrend indicator and establishes long positions when the price reaches multiple oversold and overbought levels. It closes positions for profit when the price rebounds to the overbought level. This is a grid trading strategy designed to capture oversold rebound opportunities in the market, suitable for 15-minute cycles of cryptocurrencies such as Bitcoin and Solana.

#### Strategy Principles
1. Calculate two lines of the Wavetrend indicator, one is the original value (wt1) and the other is the smoothed value (wt2).
2. Set multiple oversold levels (oslevel1~8) and overbought levels (Oblevel1~5).
3. When both wt1 and wt2 are below a certain oversold level and wt1 is above wt2, open a long position. The lower the level, the more aggressive the position.
4. When both wt1 and wt2 are above the overbought level 1 and wt1 is below wt2, close 70% of the long position.
5. Repeat steps 3 and 4 to build a grid trading system.

#### Strategy Advantages
1. Capture oversold rebound opportunities: By setting multiple oversold levels, it opens positions after a significant price drop to profit from the rebound.
2. Batch position building to control risk: It builds positions in batches according to oversold levels, with heavier positions at lower levels, allowing better risk control.
3. Automatic profit-taking: It automatically closes most of the positions when the price rebounds to the overbought zone, locking in profits.
4. Flexible parameters: Oversold and overbought levels can be adjusted according to market characteristics and personal preferences, adapting to different trading products and cycles.

#### Strategy Risks
1. Crash risk: If the price continues to fall, triggering more and more oversold opening signals, it may lead to heavy positions being trapped.
2. Choppy market risk: If the price repeatedly fluctuates in the oversold zone, it may lead to multiple position openings without being able to take profit, thus weakening the strategy's effect.
3. Parameter risk: Different parameter settings have a significant impact on strategy performance and need to be optimized based on backtesting and experience, otherwise, they may bring losses.

#### Strategy Optimization Directions
1. Add trend filtering: Determine if the big-level trend is upward before opening a position to avoid opening positions in a downward trend.
2. Optimize position management: Adjust the opening position size according to the distance between the price and the oversold level, with larger positions for greater distances.
3. Dynamic profit-taking: Dynamically adjust the profit-taking level based on the holding profit and loss ratio, instead of closing positions at a fixed ratio.
4. Add stop-loss: Set a fixed or trailing stop-loss to control the maximum loss of a single transaction.

#### Summary
The Wavetrend Large Amplitude Oversold Rebound Grid Trading Strategy is a quantitative strategy based on oversold and overbought signals. It attempts to capture rebound opportunities after a sharp fall through batch position building and automatic profit-taking, aiming to profit from the price difference. The advantage of this strategy lies in its strong adaptability and flexible parameter adjustment. However, it also faces risks such as continued market decline and improper parameter settings. In practical applications, trend filtering, dynamic positioning, profit-taking, and stop-loss optimization methods can be considered to improve the strategy's stability and profitability. However, it still needs to be noted that this strategy is a high-risk strategy that requires strict position control and cautious use.
[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|40|channel length|
|v_input_2|60|average length|
|v_input_3|40|over bought level 1|
|v_input_4|50|over bought level 1|
|v_input_5|70|over bought level 1|
|v_input_6|80|over bought level 1|
|v_input_7|100|over bought level 2|
|v_input_8|-40|over sold level 1|
|v_input_9|-45|over sold level 1|
|v_input_10|-50|over sold level 1|
|v_input_11|-55|over sold level 1|
|v_input_12|-65|over sold level 1|
|v_input_13|-75|over sold level 1|
|v_input_14|-85|over sold level 1|
|v_input_15|-100|over sold level 2|
|v_input_16_hlc3|0|source: hlc3|high|low|open|hl2|close|hlcc4|ohlc4|

> Source (PineScript)

```pinescript
//@version=5
// © And Isaac, all rights reserved. If there is any piracy, please call the police immediately.
strategy("Wavetrend Large Amplitude Oversold Rebound Grid Trading Strategy", overlay=false, margin_long=100, margin_short=100)

channel_length = input(40, title="Channel Length")
avg_length = input(60, title="Average Length")

// Wavetrend indicator calculation
wt1 = ta.wvxl(channel_length)
wt2 = sma(wt1, avg_length)

overbought_levels = array.new_float(5, 0.0)
array.set(overbought_levels, 0, 40)
array.set(overbought_levels, 1, 50)
array.set(overbought_levels, 2, 70)
array.set(overbought_levels, 3, 80)
array.set(overbought_levels, 4, 100)

oversold_levels = array.new_float(8, 0.0)
array.set(oversold_levels, 0, -40)
array.set(oversold_levels, 1, -45)
array.set(oversold_levels, 2, -50)
array.set(oversold_levels, 3, -55)
array.set(oversold_levels, 4, -65)
array.set(oversold_levels, 5, -75)
array.set(oversold_levels, 6, -85)
array.set(oversold_levels, 7, -100)

// Long entry conditions
for i = 0 to array.size(overbought_levels) - 2
    if wt1 < overbought_levels[i] and wt1 > overbought_levels[i + 1] and wt2 > wt1
        strategy.entry("Long", strategy.long, when=bar_index == bar_index[1])

// Close partial long positions for profit-taking
if wt1 > overbought_levels[0]
    if wt1 < wt2
        strategy.close("Long", trail_percent=0.3)

```
```