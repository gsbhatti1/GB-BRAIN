> Name

Dual-Take-Profit-Moving-Average-Crossover-Quantitative-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/153eb96d33fdfcbaf40.png)
[trans]

### Overview

This strategy uses simple moving average crossover and dual take profit techniques to control risk and increase profitability. It is suitable for medium-term trading and capturing opportunities during trend changes.

### Strategy Logic

The strategy is based on EMA and WMA crossover to determine market trends. It goes long when EMA crosses above WMA, and goes short when EMA crosses below WMA.

Upon entry, two take profit levels are set. The first take profit is fixed at entry price + 20 pips, and the second take profit is fixed at entry price + 40 pips. Meanwhile, a stop loss is placed at entry price - 20 pips.

When price hits the first take profit, it will close out half of the position. The remaining position will keep running towards the second take profit or until stopped out.

There are three possible outcomes for each trade:

1. Price hits stop loss, takes 2% loss directly.

2. Price hits first take profit first, closes half position locking 1% profit, then keeps running until stopped out, ending with break even.

3. After hitting first take profit, price keeps running and hits second take profit, ending with 1% + 2% = 3% total profit.

### Advantage Analysis

The biggest advantage of this dual take profit strategy is that it controls risk and avoids huge single loss. Stop loss caps maximum loss within 2% when market moves against. The two take profits allow bigger gain when trend goes as expected.

Compared to single take profit/stop loss, this strategy has three outcomes - loss, win or break even, reducing the probability of stop loss. Even if stopped out, max loss is limited to 2%. Compared to traditional strategies, the dual take profit mechanism significantly reduces DD and improves win rate.

Another advantage is its simplicity. EMA and WMA are well-known indicators that are easy to understand. The take profit/stop loss logic is straightforward to monitor. These make the strategy easy to be adopted by beginners.

### Risk Analysis

Despite the advantages, there are also risks to be aware of for this strategy.

Firstly, as moving average indicators, EMA and WMA have relatively weak capabilities in identifying ranging market. Too many false signals may occur when trend is unclear, leading to over-trading.

Secondly, the fixed take profit/stop loss levels may not adapt to market volatility. They could be penetrated easily during high volatility, rendering them ineffective.

Lastly, the strategy cannot respond to unexpected events, with risk of being trapped. Major news events can create huge price gaps that directly breach the profit/loss levels, causing huge losses.

### Optimization Directions

There are several aspects to further optimize the strategy:

1. Improve entry signals. Test better moving average or trend indicators than EMA and WMA to generate higher quality signals.

2. Dynamically adjust take profit/stop loss. Use methods like ATR, trailing stop loss etc to make profit/loss levels adapt to markets.

3. Add filters. Require volume or secondary indicator confirmation before crossover to avoid traps. Also consider whether to trade around major events.

4. Optimize position sizing. Fine tune position size according to capital management rules.

### Conclusion

In summary, this is a simple and practical trend following strategy. It utilizes EMA and WMA crossover for entries, and dual take profit to control risks. Compared to traditional strategies, it has higher win rate and lower risk. Of course, limitations of the indicators and profit/loss settings should be watched out for. Further optimizations can make the strategy more robust.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Buy|
|v_input_2|true|Sell|
|v_input_3|2019|Start year|
|v_input_4|true|Start month|
|v_input_5|true|Start day|
|v_input_6|false|Start hour |
|v_input_7|false|Start minute|
|v_input_8|false|set end time?|
|v_input_9|2019|end year|
|v_input_10|12|end month|
|v_input_11|31|end day|
|v_input_12|23|end hour|
|v_input_13|59|end minute|
|v_input_14|10|EMA period|
|v_input_15|20|WMA period|
|v_input_16|20|a|
|v_input_17|40|b|
|v_input_18|10|Risk per trade%|


> Source (PineScript)

```pinescript
//@version=4
strategy("FS ATR & PS (MA)", overlay=true)

// Strategy
Buy  = input(true)
Sell = input(true)
```