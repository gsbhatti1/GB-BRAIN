> Name

Kifier Hidden MFI-STOCH Divergence Trend Breaker Trading Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/13274bb987ce0284996.png)
 [trans]

### Overview

This is a universal trading strategy designed for the crypto market, aiming to find good entry opportunities when being bullish on cryptos for mid-to-long term holding. It combines various technical indicators like MFI, STOCH, VWMA to identify potential trend reversals based on hidden divergence.

### Trading Logic

The strategy has two entry logics:

1. MFI Hidden Divergence + STOCH Filter: When there's a hidden divergence between price and MFI, i.e., price reaches new high but MFI does not, it indicates a potential trend reversal. To avoid false signals, we add STOCH>50% as a further filter.

2. STOCH/MFI Trend System: When STOCH > 50% and MFI crosses above 50, it signals an uptrend in action. We can ride the trend for better risk-adjusted returns.

To ensure the accuracy of trend detection, a trend system comprised of VWMA and SMA is constructed. Entries are only allowed when VWMA crosses over SMA, confirming an upward trend. Besides, OBV is used to check if the overall market is active or ranging. This further filters out some false signals.

ATR is used to determine if the market is ranging. We prefer to take entries on hidden divergence during range-bound markets. The stop loss is set based on recent support levels. Take profit exits when a certain percentage of profits is reached based on entry price.

### Advantage Analysis

The strategy combines various indicators to filter out market noise and avoid false signals. The hidden divergence system provides high-probability entries with controlled risk during ranging and corrective markets. The STOCH/MFI trend system generates additional profits when a clear trend establishes. Reasonable TP and SL settings prevent chasing momentum and stop hunts. The strategy suits the highly volatile crypto market very well for solid risk-adjusted returns.

### Risk Analysis

The major risk is that hidden divergence does not always lead to an immediate reversal as it merely suggests shifting market sentiment. Noisy STOCH and other signals may result from bad parameter tuning. Overly tight TP/SL levels can also lead to excessive exits and re-entries, dragging down net profits.

We tackle these issues via additional trend and market condition filters, more tolerant TP/SL levels, etc. Still significant losses may occur in case of major black swan events or a failure to cut loss in time.

### Optimization Directions

There remains room for improving this strategy:

1. Optimize MFI/STOCH parameters for better hidden divergence accuracy
2. Add ML models to determine market conditions and fine-tune parameters
3. Test dynamic TP/SL to balance profitability and risk control
4. Check cross-asset differences and set personalized parameters
5. Add stock selection filters for better quality picks

These efforts can potentially enhance the stability and profitability further.

### Conclusion

This is a very practical crypto trading strategy. It judiciously applies various technical indicators to determine market conditions and delivers solid risk-adjusted profits. The main caveat is hidden divergence does not always precisely predict immediate reversals. We handle this issue via a sequence of filters. There remains room for boosting stability and returns. It offers fruitful ideas for quants to harvest consistent gains in the crypto space.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|false|Enable Date Range?|
|v_input_2|true|Today as End Date|
|v_input_3|timestamp(01 Jan 2021 00:00 +0300)|Start Date|
|v_input_4|timestamp(16 July 2021 00:00 +0300)|End Date|
|v_input_5|50|(?Indicator Settings)VWMA Length|
|v_input_6|50|SMA Length|
|v_input_7|28|Stoch Length|
|v_input_8|7|MFI Length|
|v_input_9|100|OBV Length|
|v_input_10|100|ATR Ranging-trend len|
|v_input_11|5|(?Divergance Settings)Price Divergant Pivots|
|v_input_12|0.05|Price Inaccuracy|
|v_input_13|3|Divergance Valid Period|
|v_input_14|5|MFI Left/Right Pivots|
|v_input_15|2|i_mfi_right|
|v_input_16|10|(?Exit Settings)TP Percentage|
|v_input_17|0.03|Support Inaccuracy|
|v_input_18|true|(?Individual Entries)Use Stoch/MFI Trend|
|v_input_19|true|Use Stoch/MFI Divergance |
|v_input_20|yellow|(?Indicator Colours)MFI/STOCH Colour     |
|v_input_21|silver|c_stoch|
|v_input_22|green|Buy/Sell Colour      |
|v_input_23|red|c_sell|
|v_input_24|blue|Flat/Trending