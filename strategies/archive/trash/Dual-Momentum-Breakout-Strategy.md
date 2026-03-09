> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|timestamp(2021-01-02T00:00:00)|Start Date|
|v_input_2|timestamp(2021-12-31T00:00:00)|End Date|
|v_input_3|12|Length|
|v_input_4_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_5|true|Percent?|
|v_input_6|0|MOM Choice: MOM2|MOM1|
|v_input_7|{{strategy.order.alert_message}}|Buy message|
|v_input_8|{{strategy.order.alert_message}}|Sell message|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-10-16 00:00:00
end: 2023-11-15 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Dual-Momentum-Breakout-Strategy", overlay = false, precision = 2, initial_capital = 10000, default_qty_value = 10000, default_qty_type = strategy.cash, commission_type = strategy.commission.percent, commission_value = 0, calc_on_every_tick = true)

// There will be no short entries, only exits from long.
strategy.risk.allow_entry_in(strategy.direction.long)

// Calculate start/end date and time condition
startDate  = input(timestamp("2021-01-02T00:00:00"), title = "Start Date")
endDate    = input(timestamp("2021-12-31T00:00:00"), title = "End Date")
i_len      = input(12, title = "Length", minval = 1)
i_src      = input(close, title = "Source")
i_percent  = input(true, title = "Percent?")
i_mom      = input(0, title = "MOM Choice", options = ["MOM1", "MOM2"])

// Momentum code
mom0 = momentum(i_src, i_len, i_percent)
mom1 = momentum(mom0, 1, i_percent)
mom2 = momentum(i_src, 1, i_percent)

momX = mom1

if i_mom == "MOM2"
    momX := mom2

// Buy condition
if time >= startDate and time <= endDate and mom0 > 0 and momX > 0
    strategy.entry("Buy", strategy.long)

// Sell condition
if time >= startDate and time <= endDate and mom0 < 0 and momX < 0
    strategy.close("Buy")

// Buy and Sell messages
strategy.entry("Buy", strategy.long, alert_message = v_input_7)
strategy.close("Buy", alert_message = v_input_8)
```

This Pine Script defines the dual-momentum breakout strategy, ensuring that only long entries are made and shorts are used exclusively for closing positions. The strategy uses two momentum indicators with different settings and generates trading signals when both break through the zero line. The code includes the necessary Pine Script components for defining the strategy, setting up the conditions for entry and exit, and providing alerts for buy and sell actions.