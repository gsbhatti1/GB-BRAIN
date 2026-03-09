``` pinescript
/*backtest
start: 2024-01-10 00:00:00
end: 2024-01-17 00:00:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy(title="A-Strict-Trend-Following-Strategy-Based-on-Ichimoku", shorttitle="A-Strict-Trend-Following", overlay=true)

atr_period = input(title="ATR Period",  defval=20)
conversion_period = input(title="Conversion Line Period", defval=9, minval=1)
base_period = input(title="Base Line Period", defval=26, minval=1)
span_b_period = input(title="Span B Period", defval=52, minval=1)
displacement = input(title="Displacement", defval=26, minval=1)
min_current_cloud_atr = input(title="Min Current Cloud ATR", type=float, defval=1.0)
min_future_cloud_atr = input(title="Min Future Cloud ATR", type=float, defval=0)
check_base_line_above_cloud = input(title="Check Base Line above Cloud?", type=bool, defval=true)
check_conversion_line_above_base_line = input(title="Check Conversion Line above Base Line?", type=bool, defval=true)
check_price_above_conversion_line = input(title="Check Price above Conversion Line?", type=bool, defval=true)
check_span_a_point_up = input(title="Check Current Span A is pointing Up?", type=bool, defval=false)
check_span_b_point_up = input(title="Check Current Span B is pointing Up?", type=bool, defval=false)
check_future_span_a_point_up = input(title="Check Future Span A is pointing Up?", type=bool, defval=true)
check_future_span_b_point_up = input(title="Check Future Span B is pointing Up?", type=bool, defval=true)
check_base_line_point_up = input(title="Check Base Line is Pointing Up?", type=bool, defval=true)
check_conversion_line_point_up = input(title="Check Conversion Line is Pointing Up?", type=bool, defval=true)
```