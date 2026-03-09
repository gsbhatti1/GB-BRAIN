> Strategy Arguments



|Argument|Default|Description|
|---|---|---|
|stop_loss_distance|0.6|Stop loss distance multiplier for the higher price condition.|
|long_cond1_multiplier|1.8|Multiplier for the long condition when the current day's opening price is higher than the previous day's closing price.|
|long_cond2_multiplier|0.6|Multiplier for the long condition when the current day's opening price is lower than the previous day's closing price.|
|close_all_at_close|True|Whether to close all positions at the end of the day.|
|window|14|Number of days to look back for the backtest window.|
|commission|0.001|Commission rate for each trade.|
|price|Close|Price type for the strategy.|
|timeframe|1D|Timeframe for the strategy.|
|slippage|0.001|Slippage rate for the strategy.|
|backtest_start_date|2023-01-01|Start date for the backtest.|
|backtest_end_date|2023-12-31|End date for the backtest.|
|verbose|False|Whether to print detailed information during backtesting.|