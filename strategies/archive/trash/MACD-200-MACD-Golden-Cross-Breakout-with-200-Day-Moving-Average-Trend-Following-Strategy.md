## Overview  

This strategy combines the MACD indicator to identify short-term trends and the 200-day moving average to determine long-term trends. When the MACD golden cross occurs and runs at a low level, if the price breaks through the 200-day moving average, a long position is established with a trailing stop loss. This strategy mainly utilizes the relationship between the MACD indicator's golden cross and death cross and the 200-day moving average to identify potential opportunities.

## Strategy Logic

The strategy is mainly based on the MACD indicator and 200-day moving average for judgment, the specific logic is:

1. Calculate the fast line, slow line, and MACD line of the MACD indicator. The fast line parameter is 12 days, the slow line parameter is 26 days, and the signal line parameter is 9 days.

2. Calculate the 200-day Exponential Moving Average (EMA).

3. When the MACD fast line crosses over the slow line (golden cross), the MACD line is negative (running at a low level), and the close price is above the 200-day line, go long.

4. After entering the position, set the stop loss price to 0.5% of the entry price, and the target price to 1% of the entry price.

5. If the price touches the stop loss or target price, exit the position with a stop loss or take profit.

6. Mandatory flatten before the daily close at 15:15.

7. The trading hours are set between 9:00 and 15:15 every day.

By judging the short-term trend direction and momentum with the MACD indicator and determining the long-term trend direction with the 200-day moving average, the trend following operation can be realized. The stop loss is set smaller and the target price is larger to maximize profits. The mandatory daily exit can control the overnight risk.

## Advantages of the Strategy

The strategy has the following advantages:

1. Combining multiple indicators makes signal judgement more accurate. MACD judges short-term trends and momentum, while the 200-day MA judges the main trend direction.

2. Small stop loss range can withstand certain drawdowns. The stop loss is only 0.5%, which is conducive to tracking mid-term trends.

3. Higher profit target allows more profit room. The target is 1% of the entry price, meeting the profit maximization of trend strategies.

4. Mandatory daily unwind helps avoid overnight risk of huge price swings. This controls the overall risk.

5. The strategy logic is simple and clear, easy to understand and replicate, suitable for beginners to learn.

## Risks of the Strategy

The strategy also has some risks:

1. Exhaustion risk. Prices may reverse downwards after a sharp rise, unable to stop loss in time and cause huge losses. A trailer stop loss can be used to adjust the stop loss price in real time.

2. Trend determination failure risk. MACD and moving average may give wrong signals, resulting in losses in non-trending markets. Consider combining trading volume indicators for filtering, to ensure entering only during trend acceleration stages.

3. Overnight fluctuation risks still exist despite the daily unwind mechanism. This requires traders to withstand a certain degree of risk while controlling overall position sizing.

## Optimization Directions

The strategy can also be optimized in the following aspects:

1. Combine trading volume indicators to determine real trends, avoid wrongly entering during choppy consolidations. For example, set entry rules so that volume must be 10% greater than previous period.

2. Set dynamic stop loss mechanisms. Continuously adjust stop loss price after entry based on price movement, to trail more profits.

3. Optimize MACD parameter combinations and test effectiveness across different markets. Parameters affect signal sensitivity.

4. Test other moving averages, like 100-day and 150-day lines, to see which fits better with trends.

5. Add re-entry mechanisms. Daily forced exits may miss subsequent trends, so re-entry signals can allow position holding the next day.

## Conclusion

In summary, this strategy integrates the MACD and 200-day MA for signal judgment. It enters trends conditionally when short-term indicators give sustained signals, with stop loss and take profit mechanisms. Mandatory daily unwind helps control overnight risk. The strategy logic is simple and easy to operate, suitable for beginners to learn. However, it also has certain risks of trend misjudgment and exhaustion, which require traders to have a certain level of risk tolerance. Future optimizations can include adjusting the stop loss mechanism, parameter selection, and trading volume filtering to improve profit factors.