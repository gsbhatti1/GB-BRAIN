> Strategy Arguments


|Argument|Default|Description|
|---|---|---|
|v_in|10|Initial capital investment percentage|
|v_in2|5|Second capital investment percentage (if applicable)|
|v_in3|5|Third capital investment percentage (if applicable)|
|v_in4|5|Fourth capital investment percentage (if applicable)|
|hma_length|9|Length of Hull Moving Average|
|speed_len|10|Length of speed (1st derivative) calculation|
|acceleration_len|20|Length of acceleration (2nd derivative) calculation|
|jerk_len|30|Length of jerk (3rd derivative) calculation|
|jounce_len|40|Length of jounce (4th derivative) calculation|
|trail_percent|5|Trailing stop loss percentage|
|news_filter_enabled|False|Enable news event filters|
|pause_duration|120|Duration to pause strategy after news events (in minutes)|

> Strategy Usage

This strategy can be used for both futures and spot markets. It is recommended to backtest the strategy using historical data before deploying it in live trading. The strategy should be monitored regularly to ensure optimal performance and adjust parameters as needed.

> Disclaimer

The author of this strategy does not guarantee any profit or minimize losses. Trading involves risk, please trade responsibly.

> Conclusion

This strategy utilizes multiple derivatives of the Hull Moving Average (HMA) to identify entry and exit points in the market. By combining the signs of acceleration, jerk, and jounce with a trailing stop loss mechanism, it aims to filter out false signals and optimize profits. While it offers flexibility through adjustable parameters, users should be aware of potential risks such as overfitting and impacts from significant news events.

||

## Strategy Arguments


|Argument|Default|Description|
|---|---|---|
|v_in|10|Initial capital investment percentage|
|v_in2|5|Second capital investment percentage (if applicable)|
|v_in3|5|Third capital investment percentage (if applicable)|
|v_in4|5|Fourth capital investment percentage (if applicable)|
|hma_length|9|Length of Hull Moving Average|
|speed_len|10|Length of speed (1st derivative) calculation|
|acceleration_len|20|Length of acceleration (2nd derivative) calculation|
|jerk_len|30|Length of jerk (3rd derivative) calculation|
|jounce_len|40|Length of jounce (4th derivative) calculation|
|trail_percent|5|Trailing stop loss percentage|
|news_filter_enabled|False|Enable news event filters|
|pause_duration|120|Duration to pause strategy after news events (in minutes)|

> Strategy Usage

This strategy can be used for both futures and spot markets. It is recommended to backtest the strategy using historical data before deploying it in live trading. The strategy should be monitored regularly to ensure optimal performance and adjust parameters as needed.

> Disclaimer

The author of this strategy does not guarantee any profit or minimize losses. Trading involves risk, please trade responsibly.

> Conclusion

This strategy utilizes multiple derivatives of the Hull Moving Average (HMA) to identify entry and exit points in the market. By combining the signs of acceleration, jerk, and jounce with a trailing stop loss mechanism, it aims to filter out false signals and optimize profits. While it offers flexibility through adjustable parameters, users should be aware of potential risks such as overfitting and impacts from significant news events.

[/trans]