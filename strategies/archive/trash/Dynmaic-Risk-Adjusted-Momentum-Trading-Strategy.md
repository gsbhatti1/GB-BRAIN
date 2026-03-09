``` pinescript
/*backtest
start: 2023-01-17 00:00:00
end: 2024-01-23 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Crunchster1

//@version=5
strategy(title="Crunchster's Normalised Trend Strategy", shorttitle="Normalised Trend Strategy", overlay=false )

// Inputs and Parameters
src = input(close, 'Source', group='Strategy Settings')
length = input.int(title="Lookback period for price normalisation filter", defval=14, minval=2, group='Strategy Settings', tooltip='This sets the lookback period for the volatility adjustment of returns, which is used to transform the price series into the "real price"')
hlength = input.int(title="Lookback period for Hull Moving Average", defval=100, minval=2, group='Strategy Settings')
offset = input.int(title="HMA Offset", defval=0, minval=0, group='Strategy Settings')
long = input(true, 'Long', inline='08', group='Strategy Settings')
short = input(true, 'Short', inline='09', group='Strategy Settings')
stop_multiple = input.float(1.3, 'Stop multiple', step=0.1, group='Risk Management Settings', tooltip='Multiplier of recent price average true range for stop loss level')
max_leverage = input.float(2, 'Max Leverage', minval=1, maxval=5, group='Risk Management Settings', tooltip='Maximum leverage allowed for this strategy')
volatility_target = input.float(10, '% Annualised Volatility Target', step=0.1, group='Risk Management Settings', tooltip='Annualised volatility target used to risk weight positions')
compound = input(false, 'Compounding', inline='26', group='Strategy Settings')
compounding_periods = input.float(50, '%', minval=0, maxval=100, group='Strategy Settings', tooltip='Percentage of compounding periods for position sizing adjustment')
backtest_start_day = input.int(1, 'From Day', inline='28', group='Backtest range')
backtest_start_mon = input.int(1, 'From Mon', inline='29', group='Backtest range')
backtest_start_yr = input.int(2018, 'From Yr', inline='30', group='Backtest range')
backtest_end_day = input.int(25, 'To Day', inline='31', group='Backtest range')
backtest_end_mon = input.int(1, 'To Mon', inline='32', group='Backtest range')
backtest_end_yr = input.int(2024, 'To Yr', inline='33', group='Backtest range')

// Functions and Variables
real_price = ta.normaliseprice(src)
hma = hma(real_price, hlength, offset)

// Strategy Logic
if (long and ta.crossover(real_price, hma))
    strategy.entry("Long", strategy.long)
else if (short and ta.crossunder(real_price, hma))
    strategy.entry("Short", strategy.short)

// Position Sizing
position_size = vol_target_to_pos_size(volatility_target, length)
strategy.exit("Stop Loss", "Long", stop=real_price - stop_multiple * ta.tr(true))
strategy.exit("Stop Loss", "Short", stop=real_price + stop_multiple * ta.tr(true))

// Helper Function to Convert Volatility Target to Position Size
vol_target_to_pos_size(volatility_target, length) =>
    vol = ta.stdev(src, length)
    exp_vol = vol * math.sqrt(252 / length)
    pos_size = volatility_target / (exp_vol * max_leverage)
    pos_size

// Compounding Logic (if enabled)
if (compound and compounding_periods > 0)
    // Implementation of compounding logic
```

This script includes the necessary parameters for defining the strategy, along with placeholders for implementing additional features like compound interest.