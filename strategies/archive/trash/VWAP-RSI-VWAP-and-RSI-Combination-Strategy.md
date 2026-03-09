## Overview

The strategy is named "VWAP and RSI Combination Strategy." It utilizes the Value Weighted Average Price (VWAP) and Relative Strength Index (RSI) indicators to implement a combination strategy of trend following entry and overbought/oversold exit.

## Strategy Principle

The main logic of this strategy is based on the following points:

1. Use the 50-day Exponential Moving Average (EMA) crossing above the 200-day line as a signal that the market trend is up.
2. When the closing price is higher than the VWAP price of the day, and the closing price is higher than the opening price, it is considered that the market is going stronger, allowing for entry.
3. If the RSI indicator on at least one of the previous 10 K-lines is lower than 10, it is regarded as an oversold formation, a strong entry signal.
4. When the RSI indicator crosses down the overbought area of 90 again, exit the market.
5. Set a 5% stop loss to avoid excessive losses.

The above is the basic trading logic of this strategy. EMA judges the big trend, VWAP judges the daily trend, and RSI judges the overbought/oversold area, achieving an effective combination of multiple indicators. This ensures the correct direction of the main trading while increasing entry and exit signals.

## Advantage Analysis

The biggest advantage of this strategy is the combination use of indicators. The single VWAP cannot perfectly cope with all market conditions; at this time, introducing RSI can identify some short-term oversold breakout points that bring trading opportunities. Additionally, the application of EMA ensures that only long-cycle upward trends are considered for entry, avoiding being trapped by short-term reversals.

This way of using combined indicators also increases the stability of the strategy. In cases where there is one or two false breakouts in RSI, VWAP and EMA provide backup to prevent incorrect trades. Similarly, when VWAP has false breakouts, confirmation from the RSI indicator is available. Therefore, this combination usage greatly enhances the success rate of strategy implementation.

## Risk Analysis

The main risk of this strategy lies in the use of the VWAP indicator. VWAP represents the average transaction price for the day but does not guarantee that every day's price fluctuation will stay around VWAP. Therefore, VWAP breakout signals do not necessarily ensure continued breakout prices afterward. Pseudo breakouts may lead to losses.

In addition, RSI indicators are prone to divergences. When the market is in a consolidation phase, the RSI may repeatedly touch the overbought and oversold zones multiple times, resulting in frequent trading signals. Blindly following these signals can also pose certain risks.

To address this issue, we use EMA as a large cycle judgment in the strategy, only considering entry when the large cycle is upward, which can mitigate the impact of the above two issues on the strategy to some extent. Additionally, setting a stop loss ensures that single losses remain within a controlled range.

## Optimization Direction

There is still room for further optimization of this strategy, mainly in the following aspects:

1. Introduce more indicators for combination. Such as Kalman lines and Bollinger bands, to make trading signals clearer and more reliable.
2. Optimize transaction costs. The existing strategy does not consider the impact of fees and commissions; it can be combined with real trading accounts to optimize the size of open positions.
3. Adjust the stop loss model. The existing stop loss method is relatively simple and may not perfectly match market changes; testing moving stop loss or trailing stop loss methods could improve results.
4. Test the application effects on different varieties. Currently, only tested on S&P 500 and Nasdaq indices; expanding the sample range can help identify the best-suited variety for this strategy.

## Summary

This strategy integrates the advantages of EMA, VWAP, and RSI indicators to achieve an effective combination of trend tracking and overbought/oversold signals. It can find reasonable entry opportunities in both big cycle ups and short-term adjustments while maintaining strong stability. At the same time, there is considerable room for optimization through introducing more indicators, adjusting stop loss models, and testing different varieties.