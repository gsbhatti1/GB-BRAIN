## Overview

The core idea of this strategy is to identify market trend directions by combining Hull moving average and average true range (ATR), and enter positions after the trend direction is confirmed. Specifically, it calculates the difference between the Hull moving averages of a certain period and the previous period. When the difference rises, it indicates a bullish trend; when the difference declines, it indicates a bearish trend. At the same time, the ATR index is used to determine the amplitude. It enters positions when the trend direction is confirmed and the amplitude keeps expanding.

## Strategy Logic

This strategy mainly relies on two types of indicators: Hull moving average and ATR.

The Hull moving average is a trend-following indicator developed by American futures trader Alan Hull. Similar to moving averages, the Hull moving average has higher sensitivity and can capture price changes and trends faster. The strategy sets an adjustable parameter `hullLength` to control the period of the Hull moving average. By calculating the difference between the current period's Hull MA and previous period's, it determines the current price trend direction.

ATR stands for Average True Range. It reflects the amplitude of daily price fluctuations. When volatility increases, ATR rises; when volatility declines, ATR falls. The strategy sets parameters like `atrLength` and `atrSmoothing` to control the ATR calculation. And ATR is plotted on the chart as one reference for entries.

Specifically, the strategy logic is:

1. Calculate current period Hull MA (`hullLength`) and previous period Hull MA.
2. Calculate the difference: `hullDiff = currentHullMA - previousHullMA`
3. When `hullDiff > 0`, it indicates a bullish trend. When `hullDiff < 0`, it indicates a bearish trend.
4. Calculate ATR (`atrLength`) of a period as an amplitude benchmark.
5. When the bullish trend is identified and ATR > price > price of `atrLength` periods ago, go long. When the bearish trend is identified and ATR < price < price of `atrLength` periods ago, go short.
6. Use the positive/negative of `hullDiff` to determine close signals.

## Advantage Analysis

The advantages of this strategy:

1. Combining trend judgment and volatility index, it can enter positions when the price trend is clear and volatility rises to avoid being trapped in range-bound markets.
2. Hull MA responds faster to price changes and can quickly identify new trend directions.
3. ATR reflects market volatility and heat, providing guidance for entry timings.
4. Multiple adjustable parameters can be optimized for best parameter combinations.

## Risk Analysis

Some risks of this strategy:

1. Both Hull MA and ATR cannot completely avoid false breakouts and thus hold the risk of being trapped.
2. Improper parameter settings may lead to over-trading or insufficient sensitivity, undermining strategy efficacy.
3. It cannot handle violent price actions like sharp spikes or crashes effectively.

Solutions:

1. Set proper stop loss to avoid being trapped by false breakouts.
2. Test and optimize parameters to fit different market environments.
3. Suspend the strategy when facing violent volatility.

## Optimization Directions

There is still large room for optimization:

1. Test different `hullLength` parameters to find the optimal settings for current markets.
2. Test ATR period combinations to grasp market heat the best.
3. Try different ATR smoothing methods (RMA, SMA, EMA) to see which performs the best.
4. Optimize entry conditions with other volatility indicators like Reaction combined with ATR.
5. Optimize stop loss to avoid being trapped.

## Conclusion

This strategy integrates the trend-following capacity of Hull MA and the heat judgment ability of ATR. It enters positions when a trend is confirmed and volatility rises, filtering out some invalid signals. Further enhancement can be achieved by parameter optimization and better risk management. In summary, this strategy combines multiple factors of trend tracking and heat judgment. When parameters are adjusted and optimized appropriately, it can achieve good results.

||

## Overview

The core idea of this strategy is to identify market trend directions by combining Hull moving average and average true range (ATR), and enter positions after the trend direction is confirmed. Specifically, it calculates the difference between the Hull moving averages of a certain period and the previous period. When the difference rises, it indicates a bullish trend; when the difference declines, it indicates a bearish trend. At the same time, the ATR index is used to determine the amplitude. It enters positions when the trend direction is confirmed and the amplitude keeps expanding.

## Strategy Logic

This strategy mainly relies on two types of indicators: Hull moving average and ATR.

The Hull moving average is a trend-following indicator developed by American futures trader Alan Hull. Similar to moving averages, the Hull moving average has higher sensitivity and can capture price changes and trends faster. The strategy sets an adjustable parameter `hullLength` to control the period of the Hull moving average. By calculating the difference between the current period's Hull MA and previous period's, it determines the current price trend direction.

ATR stands for Average True Range. It reflects the amplitude of daily price fluctuations. When volatility increases, ATR rises; when volatility declines, ATR falls. The strategy sets parameters like `atrLength` and `atrSmoothing` to control the ATR calculation. And ATR is plotted on the chart as one reference for entries.

Specifically, the strategy logic is:

1. Calculate current period Hull MA (`hullLength`) and previous period Hull MA.
2. Calculate the difference: `hullDiff = currentHullMA - previousHullMA`
3. When `hullDiff > 0`, it indicates a bullish trend. When `hullDiff < 0`, it indicates a bearish trend.
4. Calculate ATR (`atrLength`) of a period as an amplitude benchmark.
5. When the bullish trend is identified and ATR > price > price of `atrLength` periods ago, go long. When the bearish trend is identified and ATR < price < price of `atrLength` periods ago, go short.
6. Use the positive/negative of `hullDiff` to determine close signals.

## Advantage Analysis

The advantages of this strategy:

1. Combining trend judgment and volatility index, it can enter positions when the price trend is clear and volatility rises to avoid being trapped in range-bound markets.
2. Hull MA responds faster to price changes and can quickly identify new trend directions.
3. ATR reflects market volatility and heat, providing guidance for entry timings.
4. Multiple adjustable parameters can be optimized for best parameter combinations.

## Risk Analysis

Some risks of this strategy:

1. Both Hull MA and ATR cannot completely avoid false breakouts and thus hold the risk of being trapped.
2. Improper parameter settings may lead to over-trading or insufficient sensitivity, undermining strategy efficacy.
3. It cannot handle violent price actions like sharp spikes or crashes effectively.

Solutions:

1. Set proper stop loss to avoid being trapped by false breakouts.
2. Test and optimize parameters to fit different market environments.
3. Suspend the strategy when facing violent volatility.

## Optimization Directions

There is still large room for optimization:

1. Test different `hullLength` parameters to find the optimal settings for current markets.
2. Test ATR period combinations to grasp market heat the best.
3. Try different ATR smoothing methods (RMA, SMA, EMA) to see which performs the best.
4. Optimize entry conditions with other volatility indicators like Reaction combined with ATR.
5. Optimize stop loss to avoid being trapped.

## Conclusion

This strategy integrates the trend-following capacity of Hull MA and the heat judgment ability of ATR. It enters positions when a trend is confirmed and volatility rises, filtering out some invalid signals. Further enhancement can be achieved by parameter optimization and better risk management. In summary, this strategy combines multiple factors of trend tracking and heat judgment. When parameters are adjusted and optimized appropriately, it can achieve good results.