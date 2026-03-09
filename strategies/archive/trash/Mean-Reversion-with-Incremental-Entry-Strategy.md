> Name

Mean-Reversion-with-Incremental-Entry-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1d4d55de4742fc476d7.png)
[trans]
## Overview

The Mean Reversion with Incremental Entry strategy is a sophisticated quantitative trading script designed by HedgerLabs, focusing on the mean reversion technique in financial markets. This strategy caters to traders who prefer a systematic approach and emphasize incremental entries based on price movements relative to a moving average.

## Strategy Logic  

At its core, this strategy relies on the Simple Moving Average (SMA). All entry and exit trades revolve around the SMA. Traders can customize the MA length to fit different trading styles and timeframes.

A unique feature of this strategy is its incremental entry mechanism. When the price deviates from the moving average by a certain percentage, it initiates the first position. Subsequently, as the price continues to deviate further from the moving average, additional positions are entered in increments defined by the trader. This approach aims to capture higher returns during increased market volatility.

The strategy also intelligently manages positions. It enters long when the price is below the moving average and short when above, adapting to changing market conditions. Exit points are set when the price touches the moving average, aiming to close positions at potential reversal points for optimal outcomes.

Enabling `calc_on_every_tick`, this strategy continuously evaluates market conditions to ensure timely responses.

## Advantage Analysis

The Mean Reversion with Incremental Entry strategy offers several advantages:

1. High systematization to reduce subjective errors
2. Incremental entry can capture higher profits during high volatility
3. Customizable parameters like MA period fit different instruments
4. Intelligent position management automatically adjusts long/short positions
5. Optimal exit points help in capturing reversals and closing positions

## Risk Analysis  

This strategy also has some risks:

1. Reliance on technical indicators, leading to false signals
2. Inability to determine market trends, making it prone to being trapped
3. Incorrect MA parameter settings may lead to frequent stop-outs
4. Larger position sizes from incremental entry increase risk

These risks can be mitigated by optimizing exits, adding trend filters, and appropriately reducing position sizing.

## Enhancement Opportunities  

The strategy can be improved in the following ways:

1. Adding trend filters to avoid unfavorable trades
2. Optimizing entry increments based on volatility  
3. Incorporating trailing stops to lock in profits
4. Experimenting with different types of moving averages
5. Using filters to reduce false signals

## Conclusion

The Mean Reversion with Incremental Entry strategy focuses on mean reversion techniques using a systematic incremental position sizing approach. With customizable settings, it is adaptable across various trading instruments. It performs well in range-bound markets and suits short-term systematic traders.

||

## Overview

The Mean Reversion with Incremental Entry strategy designed by HedgerLabs is an advanced trading script focused on the mean reversion technique in financial markets. Tailored for traders who prefer a systematic approach with emphasis on incremental entries based on price movements relative to a moving average.

## Strategy Logic  

Central to this strategy is the Simple Moving Average (SMA), around which all entry and exit trades revolve. Traders can customize the MA length to fit different trading styles and timeframes.

A unique feature of this strategy is its incremental entry mechanism. When the price deviates from the moving average by a certain percentage, it initiates the first position. Subsequently, as the price continues to deviate further from the moving average, additional positions are entered in increments defined by the trader. This approach aims to capture higher returns during increased market volatility.

The strategy also intelligently manages positions. It enters long when the price is below the moving average and short when above, adapting to changing market conditions. Exit points are set when the price touches the moving average, aiming to close positions at potential reversal points for optimal outcomes.

With `calc_on_every_tick` enabled, this strategy continuously evaluates market conditions to ensure timely responses.

## Advantage Analysis

The Mean Reversion with Incremental Entry strategy has the following key advantages:

1. Highly systematized to reduce emotional interference
2. Incremental entry captures greater profit during high volatility
3. Customizable parameters like MA period suit different instruments  
4. Intelligent position management automatically adapts long/short positions
5. Optimal exit targeting reversals to close positions

## Risk Analysis  

The risks to consider include:

1. Whipsaws from technical indicator reliance  
2. Trendlessness causing extended drawdowns
3. Poor MA settings lead to frequent stop-outs
4. Larger position size from incremental entry  

Exits can be optimized, trend filters added, and position sizing reduced to mitigate the above risks.

## Enhancement Opportunities

The strategy can be enhanced by:

1. Adding trend filters to avoid unfavorable trades
2. Optimizing entry increments with volatility  
3. Incorporating trailing stops to lock in profits
4. Experimenting with different moving averages  
5. Using filters to reduce false signals  

## Conclusion

The Mean Reversion with Incremental Entry strategy focuses on mean reversion techniques using a systemized incremental position sizing approach. With customizable settings, it is adaptable across different trading instruments. It performs well in range-bound markets and suits short-term systematic traders.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|30|MA Length|
|v_input_float_1|5|Initial Percent for First Order|
|v_input_float_2|true|Percent Step for Additional Orders|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-12-29 00:00:00
end: 2024-01-28 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Mean Reversion with Incremental Entry by HedgerLabs", overlay=true, calc_on_every_tick=true)

// Input for adjustable settings
maLength = input.int(30, title="MA Length", minval=1)
initialPercent = input.float(5, title="Initial Percent for First Order", minval=0.01, step=0.01)
percentStep = input.float(1, title="Percent Step for Additional Orders", minval=0.01, step=0.01)

// Calculating Moving Average
ma = ta.sma(close, maLength)

// Plotting the Moving Average
plot(ma, "Moving Average", color=color.blue)

var float lastBuyPrice = na
var float lastSellPrice = na

// Function to calculate absolute price percentage difference
pricePercentDiff(price1, price2) =>
    diff = math.abs(price1 - price2) / price2 * 100
    diff

// Initial Entry Condition Check Function
initialEntryCondition(price, ma, initialPercent) =>
    pricePercentDiff(price, ma) >= initialPercent

// Enhanced Entry Logic for Buy and Sell
if (low < ma)
    if (na(lastBuyPrice))
        if (initialEntryCondition(low, ma, initialPercent))
            strategy.entry("Buy", strategy.long)
            lastBuyPrice := low
    else
        if (low < lastBuyPrice and pricePercentDiff(low, lastBuyPrice) >= percentStep)
            strategy.entry("Buy", strategy.long)
            lastBuyPrice := low

if (high > ma)
    if (na(lastSellPrice))
        if (initialEntryCondition(high, ma, initialPercent))
            strategy.entry("Sell", strategy.short)
            lastSellPrice := high
    else
        if (high > lastSellPrice and pricePercentDiff(high, lastSellPrice) >= percentStep)
            strategy.entry("Sell", strategy.short)
            lastSellPrice := high

// Exit
```