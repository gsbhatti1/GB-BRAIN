```markdown
# Overview

The Dual Exponential Moving Average Trend Oscillator Strategy is a dynamic trend-following approach based on the Normalized DEMA Oscillator and Standard Deviation bands. It adapts in real-time to market volatility with the goal of improving entry accuracy and optimizing risk management. The core mechanism involves normalizing DEMA values on a 0-100 scale for intuitive identification of trend strength, combined with a two-bar confirmation filter and ATR-multiple trailing stops to enhance reliability and profitability. This is a comprehensive quantitative trading system suitable for various market conditions, particularly for traders seeking consistent performance in trending markets.

#### Strategy Principles

The Dual Exponential Moving Average Trend Oscillator Strategy's core logic is built on multiple layers of technical indicators:

1. **Dual Exponential Moving Average (DEMA) calculation**: Implemented through the F_DEMA function with the formula 2 * E1 - E2, where E1 is the EMA of price and E2 is the EMA of E1. This calculation method reduces lag, making the indicator more responsive to price movements.

2. **Normalization process**: The strategy uses BASE (SMA of DEMA) and SD (standard deviation of DEMA multiplied by 2) to create upper and lower bands (upperSD and lowerSD). Subsequently, DEMA values are normalized to a 0-100 range using the formula NormBase = 100 * (DEMA - lowerSD)/(upperSD - lowerSD).

3. **Entry conditions**:
   - **Long entry**: When NormBase > 55 and the candle low is above the upper SD band, with the previous candle forming a bullish pattern
   - **Short entry**: When NormBase < 45 and the candle high is below the lower SD band, with the previous candle forming a bearish pattern

4. **Risk management**: The strategy employs a triple exit mechanism - fixed stop-loss at the SD band, dynamic take-profit set at a risk-reward ratio of 1.5, and an ATR-based trailing stop (default at 2x ATR).

5. **Trade direction control**: The lastDirection variable ensures no consecutive entries in the same direction, improving capital efficiency.

The code implements parameter adjustability, allowing traders to optimize based on different market conditions and individual risk preferences.

#### Strategy Advantages

Through in-depth code analysis, the Dual Exponential Moving Average Trend Oscillator Strategy demonstrates multiple advantages:

1. **Reduced signal lag**: DEMA itself has lower lag than traditional EMA and SMA, responding faster to price movements. With normalization processing, trend identification becomes more timely and accurate.
2. **Intelligent filtering mechanism**: Requiring two consecutive bullish or bearish candles for confirmation significantly reduces market noise and the possibility of false signals.
3. **Adaptive volatility bands**: The standard deviation dynamically adjusts band width, enabling the strategy to automatically adapt to different market volatility conditions in low-volatility periods by contracting and expanding in high-volatility periods.
4. **Multi-layer risk management**: Combining fixed stop-loss, risk-reward ratio take-profit, and ATR-based trailing stops provides a three-pronged protection mechanism that both secures capital safety and maximizes profits during strong trends.
5. **Visual intuitiveness**: The strategy displays upper and lower SD bands and entry signal arrows on the chart, making it easier for traders to understand market conditions and strategy logic.
6. **Parameter flexibility**: All core parameters can be adjusted, including DEMA period, base length, entry threshold, and risk management settings, allowing the strategy to adapt to different trading instruments and timeframes.

7. **Code structure clarity**: The implementation is concise and clear, making it easy to understand and optimize further, reducing technical barriers for implementation.
```

Please note that the code blocks and formatting remain unchanged from your original text.