||

## Overview

This strategy aims to utilize Bitmex's trailing stop function to dynamically adjust the stop loss price for more accurate and flexible stops. The strategy is not used for entries or exits, but rather gives reasonable stop loss ranges under different market conditions. It is suggested to backtest with different values. The strategy can also be integrated into existing strategies that give entries/exits to act as a stop loss.

## Strategy Logic  

The strategy mainly uses 3 indicators: highest price, lowest price and close price. The strategy first defines the stop loss ranges for long and short positions, namely the `longoffset` for long trailing stop distance and `shortoffset` for short trailing stop distance. The default long distance is 228.5 points and the short distance is 243.5 points.  

Then the strategy uses the following logic to adjust the trailing stop price `trailstop`:  

- If the lowest price of the latest candle is lower than the trailing stop price of the previous candle, and the lowest price of the candle before that is higher than the trailing stop price of the previous 2 candles, then the current candle's trailing stop price = close price + short trailing stop distance

- If the highest price of the latest candle is higher than the trailing stop price of the previous candle, and the highest price of the candle before that is lower than the trailing stop price of the previous 2 candles, then the current candle's trailing stop price = close price - long trailing stop distance  

- If the highest price of the latest candle is higher than the trailing stop price of the previous candle, then the current candle's trailing stop price = max(previous candle's trailing stop price, latest candle's highest price - long trailing stop distance)

- If the lowest price of the latest candle is lower than the trailing stop price of the previous candle, then the current candle's trailing stop price = min(previous candle's trailing stop price, latest candle's lowest price + short trailing stop distance)  

- Otherwise the current candle's trailing stop price = close price

This dynamically adjusts the trailing stop price based on changes in the highest and lowest market prices to achieve dynamic stops.  

## Advantage Analysis

The biggest advantage of this strategy is the implementation of truly dynamic and flexible trailing stops. Compared to fixed stop loss prices, dynamic trailing can adjust the stop loss range based on market fluctuations, avoiding unnecessary losses due to too large stop distances, while also avoiding being stopped out by normal price fluctuations when the distance is too small. This reduces unnecessary losses while also reducing the probability of premature stops.  

Another advantage is that the stop loss distance is customizable and optimizable. Users can choose stop loss ranges suitable for themselves according to the characteristics of different products and trading styles. This allows the strategy to be applied to a wider range of scenarios.   

Finally, the stop loss logic of this strategy is simple and clear, easy to understand, and easy to further develop and integrate into other strategies. This is also one of its advantages.

## Risk Analysis

The main risks of this strategy are:  

1. Dynamic stops can only reduce losses under normal market conditions, but cannot withstand major events or extreme market conditions. This is an inherent limitation.   

2. If the trailing stop distance is set too large, it may lead to greater losses. If set too small, it may stop out prematurely. The setting needs careful testing and optimization based on product characteristics.

3. In the first few candles after opening a position, due to the mechanism of trailing stops, the stop distance may be too large, posing some additional risk during this period.

## Optimization Directions

This strategy can be optimized in the following aspects:  

1. Parameter optimization for different products: Choose reasonable long and short trailing stop distances based on volatility, intraday range and other metrics for different products. This is the most critical direction.  

2. Reduce extra risk in early candles after opening positions: Limit the adjustment of trailing stop distance in the first few candles after opening a position to avoid excessively large stop distances.

3. Combine with trading volume indicators: For example, reduce the stop loss distance during periods of increased trading volume to prevent getting stuck at losses due to arbitrage opportunities.

4. Integrate with other entry and exit strategies: This strategy primarily serves as a trailing stop mechanism and can be integrated into existing strategies that provide entries and exits for use in conjunction with their rules.

## Summary

This strategy implements dynamic tracking stops based on changes in the highest and lowest market prices, effectively reducing unnecessary losses under normal market conditions. It also addresses the issue of fixed stop loss distances being either too large or too small. The key optimization direction is to test suitable parameters for different products and manage risk during the first few candles after opening positions. The strategy's stop loss logic is simple and clear, easy to understand and further develop, making it versatile enough to be integrated into other strategies or used as a standalone stop loss tool.