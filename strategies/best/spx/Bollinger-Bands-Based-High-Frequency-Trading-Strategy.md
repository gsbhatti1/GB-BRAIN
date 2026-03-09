> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|20|Length of Bollinger Bands period|
|v_input_2|2|Multiplicator for standard deviation|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-12-14 00:00:00
end: 2023-12-20 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Bollinger Bands-Based High-Frequency Trading Strategy", shorttitle="BB Strategy", overlay=true)

// Bollinger Bands parameters
length = input(20, title="Length")
mult = input(2.0, title="Multiplicator")

// Calculate the Bollinger Bands
basis = ta.sma(close, length)
upper_band = basis + mult * ta.stdev(close, length)
lower_band = basis - mult * ta.stdev(close, length)

// Conditions to trigger trades
price_touches_basis_up = ta.crossover(close, basis)
price_touches_basis_down = ta.crossunder(close, basis)

// Initial investment amount
initial_investment = 10

// Strategy logic
if (price_touches_basis_up)
    qty = strategy.equity + strategy.netprofit // Invest the total capital plus floating profit in each trade
    direction = close > basis ? strategy.long : strategy.short
    strategy.entry("Trade", direction, qty=1)

// Stop profit range
stop_profit_range = 0.5 / 100

if (price_touches_basis_down)
    if (close > basis + stop_profit_range * initial_investment)
        strategy.close("Trade")
```

Note: The `stop_profit_range` is calculated as a percentage of the initial investment and is applied when the price crosses below the middle band.