> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_float_1|0.01|Max Position Size (%)|
|v_input_float_2|2|Risk Factor|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-06 00:00:00
end: 2024-02-05 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Momentum Trend Optimization Combination Strategy", overlay=true)

// Input arguments
max_position_size = input.float(0.01, title="Max Position Size (%)")
risk_factor = input.float(2, title="Risk Factor")

// Moving averages and volume
sma6 = ta.sma(close, 6)
sma35 = ta.sma(close, 35)
ema2 = ta.ema(close, 2)
vol_20ema = ta.sma(volume, 20)

// Slope calculation for signals
slope8 = (close[7] - close[0]) / 8

// Buy and sell conditions
buy_condition = ta.crossover(ema2, sma35) and close > sma35 and volume > vol_20ema and slope8 > 0 and ta.sma(close, 14).val[-7] < ta.sma(close, 14).val[-1]
sell_condition = ta.crossunder(ema2, sma35)

// Position sizing
position_size = max_position_size * strategy.equity / risk_factor

// Risk management
if (buy_condition)
    strategy.entry("Buy", strategy.long, size=position_size)
if (sell_condition)
    strategy.exit("Sell", "Buy")

plot(sma6, color=color.blue, title="SMA 6")
plot(sma35, color=color.red, title="SMA 35")
plot(ema2, color=color.green, title="EMA 2")
plot(vol_20ema, color=color.orange, title="Vol 20EMA")
```