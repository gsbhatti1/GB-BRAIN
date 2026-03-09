> Name

Trading-Strategy-Based-on-Hull-Moving-Average-and-WT-Cross

> Author

ChaoZhang

> Strategy Description

## Overview

This strategy primarily integrates Hull Moving Average and WT crossover signals to leverage the strengths of each indicator for more accurate trend judgment and entry timing.

## Strategy Logic

The strategy consists of the Hull Moving Average and WT crossover signals.

The Hull Moving Average part calculates short-term and long-term Hull MAs and fills color to determine the trend direction. The formulas are:

Short Hull MA = WMA(2*WMA(n/2) - WMA(n), sqrt(n))

Long Hull MA = WMA(WMA(n/3)*3 - WMA(n/2), n/2)

Where WMA is the Weighted Moving Average. When the short MA crosses over the long MA, it is a bullish signal, otherwise a bearish signal.

The WT part calculates the WT lines and observes their crossings to determine entries. The formulas are:

TCI = (Close - EMA(Close,n1)) / (k * STD(Close - EMA(Close,n1),n1))

WT1 = EMA(TCI,n2)

WT2 = SMA(WT1,m)

Where TCI is the Trend Composite Index, reflecting the deviation of price from the EMA; WT1 is the EMA of TCI, WT2 is the SMA of WT1, m is usually 4. The crossing of WT1 over WT2 indicates a bullish signal, while the crossing of WT1 under WT2 indicates a bearish signal.

By combining the Hull MA trend judgment and the WT crossing signals, we can enter the market in the right direction.

## Advantage Analysis

The advantages of this strategy are:

1. Hull MA captures price changes faster by modifying the calculation, and filters out market noise effectively for reliable trend judgment.

2. WT uses the price fluctuation within the channel to capture turning points quickly and generate relatively accurate trading signals.

3. The combination considers both trend and crossing for better risk control when trend aligns.

4. The Hull MA and WT parameters are customizable for adjustment and optimization based on symbol characteristics and trading preferences.

5. Hull MA and WT signals can be used alone or together for both trend following and crossing validation.

6. Stop loss and take profit can be set to effectively control single trade risks.

## Risk Analysis

The main risks of this strategy are:

1. Both Hull MA and WT smooth out prices to some extent, which may cause lagging entry signals.

2. WT may generate false bullish/bearish divergence signals without a clear trend.

3. Inappropriate parameter settings may impact trading performance and require ongoing optimization.

4. Stop loss may be triggered frequently during trend consolidations, causing some loss.

The risks can be addressed and optimized as follows:

1. Adjust Hull MA and WT parameters to find the optimal balance. Other indicators may also be tested with Hull MA.

2. Add trend validation mechanisms to avoid false WT signals without a confirmed trend.

3. Optimize parameters through backtesting and demo trading, and set reasonable stop loss ranges.

4. Reduce position sizes or stop trading when trend is unclear.

## Optimization Directions

The strategy can be further optimized from the following aspects:

1. Test different moving averages combined with WT, to find better balance, e.g. KAMA, TEMA etc.

2. Add other indicators such as oscillators, Bollinger Bands to improve decision accuracy.

3. Optimize parameters through backtesting and demo trading. Build parameter optimization programs for fast tuning.

4. Optimize stop loss strategies e.g. trailing stop, volatility-based stop, moving from near to far etc., to reduce unwanted triggering.

5. Optimize position sizing strategies, reduce sizes and frequencies in unclear trends to lower risks.

6. Introduce machine learning and other advanced techniques for smarter trading decisions and adaptive parameters.

## Summary

This strategy combines the Hull MA smoothing and WT crossing strengths for both trend judgment and validation. Trading with confirmed direction helps control risks. Further improvements can be made on parameter optimization, stop loss strategies, position sizing etc. Integrating other indicators and intelligent techniques are also future optimization directions. Overall, this strategy is simple, reliable, and easy to optimize, making it a practical trend-following strategy.