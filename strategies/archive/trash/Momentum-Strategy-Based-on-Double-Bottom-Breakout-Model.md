## Overview

This strategy is based on the double bottom model using technical indicators. It looks for breakthrough signals when the market is in an oversold state and a double bottom pattern is formed near the bottom area. The strategy combines multiple indicators to judge the overbought and oversold state of the market and generates buy signals when a double bottom forms. This strategy is mainly suitable for medium- and short-term trading.

## Strategy Principle

This strategy mainly judges whether prices are forming a double bottom around key support levels and whether the market is in an oversold state. Specifically, the strategy uses the following indicators for judgment:

1. RSI Indicator: When the RSI indicator shows the market is oversold, it is considered a buy signal.

2. RVI Indicator: When the RVI indicator shows the market is oversold, it is considered a buy signal.

3. MFI Indicator: When the MFI indicator shows the market is oversold, it is considered a buy signal.

4. SAR Indicator: When prices break above the SAR indicator, it is considered a buy signal.

5. SMA500 Indicator: When prices break above the SMA500 indicator, it is considered a buy signal.

This strategy takes into account the judgments of the multiple indicators above and generates buy signals when a double bottom pattern forms around key support levels.

## Advantages of the Strategy

This strategy has the following advantages:

1. Combining multiple indicators to judge market status makes signals more reliable.

2. Generating buy signals when double bottoms form has a relatively high probability of profit.

3. Using indicator combinations to judge oversold and overbought states avoids missing buy opportunities.

4. Integrating the double bottom breakout model with indicator strategies combines the advantages of trend following and mean reversion trading.

5. The strategy has large parameter optimization space, and parameters can be adjusted for different markets.

## Risks of the Strategy

The strategy also has the following risks:

1. The risk of false signals from indicators, resulting in losses from buying. This can be reduced through parameter optimization.

2. The risk that double bottoms fail to break through. Stop-losses can be set to reduce per trade loss.

3. The difficulty of high-dimensional parameter optimization is large and requires massive historical data support. Stepwise algorithms can be adopted for gradual optimization.

4. Reliance on historical data for testing results, actual performance will differ. Validation is needed across different markets.

## Optimization Directions

The main optimization directions for this strategy include:

1. Optimizing the weights of buy indicators to determine the optimal weight combination.
2. Optimizing indicator parameters to determine the best parameter combination.
3. Adding stop-loss strategies to reduce per trade loss.
4. Increasing position management modules for more stable profits.
5. Incorporating machine learning algorithms to build adaptive parameter optimization mechanisms.

## Conclusion

This strategy integrates the double bottom breakout model and oversold indicator judgments, generating buy signals when double bottoms form around key support levels. It has large optimization space to adjust weights, parameters, stop-losses, positions, etc., for more stable and reliable strategies. It has high practical value.

---

### Strategy Arguments

| Argument | Default  | Description                                                                                                                                                                                                                           |
|----------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| v_input_string_1 | "0"      | Trade in: Uptrend and down trend | Only on Up Trends                                                  |
| v_input_float_1 | 3.7      | Expected profit %                                                                                                                                                                                                                   |
| v_input_int_1 | 10       | (?Time Period Values)From Month                                                                                                                                          |
| v_input_int_2 | true     | From Day                                                                                                                                                                |
| v_input_int_3 | 2021     | From Year                                                                                                                                                            |
| v_input_int_4 | true     | Thru Month                                                                                                                                                            |
| v_input_int_5 | true     | Thru Day                                                                                                                                                            |
| v_input_int_6 | 2112     | Thru Year                                                                                                                                                            |
| v_input_float_2 | 0.0002   | (?SAR Values)SAR value 1                                                                                                                                                       |
| v_input_float_3 | 0.0004   | SAR value 2                                                                                                                                                                 |
| v_input_float_4 | 0.1      | SAR value 3                                                                                                                                                                 |
| v_input_1_close | 0        | SAR Source - close: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
| v_input_2_open | 0        | SAR Source - open: open|high|low|close|hl2|hlc3|hlcc4|ohlc4|
| v_input_3 | false    | Show SAR                                                                                                                                                                    |
| v_input_int_7 | 16       | (?Super Trend)Supertrend - Trend                                                                                                                                        |
| v_input_int_8 | 7        | Supertrend - Direction                                                                                                                                                    |
| v_input_int_9 | true     | Supertrend - SMA                                                                                                                                                           |
| v_input_4 | false    | Show Super Trend                                                                                                                                                        |
| v_input_5_high | 0        | (?SMA500)SMA500 - Source: high|close|low|open|hl2|hlc3|hlcc4|ohlc4|
| v_input_int_10 | 143      | SMA500 - Look back period                                                                                                                                                |
| v_input_6 | false    | Show SMA500                                                                                                                                                                |
| v_input_int_11 | 10       | (?RSI Indicator - 10)Length                                                                                                                                                  |
| v_input_7_ohlc4 | 0        | Source: ohlc4|high|low|open|hl2|hlc3|hlcc4|close|
| v_input_int_12 | 50       | (?RSI Indicator - 50)Length                                                                                                                                                |
| v_input_8_high | 0        | Source: high|close|low|open|hl2|hlc3|hlcc4|ohlc4|