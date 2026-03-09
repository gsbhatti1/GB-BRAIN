#### Overview
The Multi-Indicator Volatility Breakout Trading System Based on Volume-Price Relationship is a comprehensive quantitative trading strategy that combines volume spike detection, ATR volatility channels, and RSI momentum filtering. The core concept of this strategy is to capture instances of sudden volume surges in the market, viewing them as potential trading opportunities, while incorporating price dynamics and technical indicators for multi-level filtering to enhance the precision of trading decisions. The strategy utilizes ATR volatility channels as references for stop-loss and take-profit levels, and leverages the RSI indicator to avoid excessive buying or selling, creating a complete trading system framework.

#### Strategy Principles
The operation of this strategy is based on the following key modules:

1. **Volume Spike Detection**: The strategy first defines the "VolSpike" concept by comparing the current volume with the total volume of the previous N candles. When the current candle's volume exceeds the sum of the previous N candles, it is identified as a volume spike signal. This abnormal trading volume typically indicates a potential directional change in the market.

2. **ATR Volatility Channels**: The strategy calculates the Average True Range (ATR) and creates upper and lower bands as reference ranges for price volatility. These channels not only serve to visualize market volatility but are also directly used to set stop-loss positions. The ATR channel calculation employs user-adjustable periods and multipliers, allowing the strategy to adapt to different market environments.

3. **RSI Momentum Filtering**: Trading signals are filtered through the Relative Strength Index (RSI) to avoid trading during extreme overbought or oversold conditions. Users can set upper and lower threshold values for RSI, and the strategy will only consider opening positions when the RSI value is between these thresholds.

4. **Candlestick Pattern Analysis**: The strategy also incorporates candlestick pattern analysis by measuring the ratio of the candlestick body to its upper and lower shadows, filtering out signals from candles with excessively long shadows, which helps avoid entering markets that might quickly reverse.

5. **Trade Execution Logic**:
   - When a volume spike is detected and the RSI filtering conditions and candlestick pattern requirements are met, the strategy will determine the entry direction based on the position of the closing price relative to the opening price.
   - Long condition: Closing price greater than opening price (bullish candle) and the upper shadow does not exceed the maximum set ratio.
   - Short condition: Closing price less than opening price (bearish candle) and the lower shadow does not exceed the maximum set ratio.
   - Stop-loss positions are set at the boundaries of the ATR channel, while take-profit positions are based on the distance between the entry price and the ATR channel, multiplied by a user-defined multiplier.

#### Strategy Advantages
1. **Multi-dimensional Signal Confirmation**: By combining volume, price patterns, and technical indicators through multiple c