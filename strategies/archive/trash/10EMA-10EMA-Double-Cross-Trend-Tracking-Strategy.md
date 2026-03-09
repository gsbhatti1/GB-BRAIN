> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|10|short ema|
|v_input_int_2|50|long ema|
|v_input_int_3|200|hourly 10 ema|
|v_input_1_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_int_4|false|Offset|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-12-22 00:00:00
end: 2023-06-01 00:00:00
symbol: BTCUSD
interval: D
*/

//@version=5
strategy("10EMA Double-Cross Trend Tracking Strategy", overlay=true)

short_ema = v_input_int_1(10)
long_ema = v_input_int_2(50)
hourly_ema = v_input_int_3(200)
source = v_input_1_close(0)
offset = v_input_int_4(false) == true ? 0 : na

// Calculate EMAs
short_emac = ta.ema(source, short_ema)
long_emac = ta.ema(source, long_ema)

// Plot EMAs on chart
plot(short_emac, color=color.blue, title="10 EMA")
plot(long_emac, color=color.red, title="50 EMA")

// Calculate hourly 10 EMA
hourly_short_emac = ta.ema(close[offset], hourly_ema)
plot(hourly_short_emac, color=color.green, title="Hourly 10 EMA")

// Buy/Sell Conditions
bullish_cross = ta.crossover(short_emac, long_emac)
bearish_cross = ta.crossunder(short_emac, long_emac)

// Filter by hourly 10 EMA trend
buy_condition = bullish_cross and hour[offset] >= 9 and hourly_short_emac > hourly_ema * 0.85
sell_condition = bearish_cross and hour[offset] <= 23 and hourly_short_emac < hourly_ema * 0.15

// Place orders
if (buy_condition)
    strategy.entry("Buy", strategy.long)
if (sell_condition)
    strategy.close("Buy")

// Trailing Stop Loss + Limit Profit Taking
trail_stop = strategy.position_avg_price * (1 - 0.02) // Adjust the stop loss percentage as needed
take_profit = strategy.position_avg_price * (1 + 0.03) // Adjust the take profit percentage as needed

if (strategy.opentrades > 0)
    strategy.exit("Sell", "Buy", limit=take_profit, stop=trail_stop)

// Display position size and P&L
pos_size = strategy.get_position_size()
pnl = strategy.close_entry_price - pos_size * source
plot(pnl, color=color.purple, title="P&L")
```