``` pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Custom Strategy with Stop Loss and EMA", overlay=true)

src = input(close, title='Source')
h = input(10, title='Lookback Window', tooltip='The number of bars used for the estimation.')
r = input(10, title='Relative Weighting', tooltip='Relative weighting of time frames.')
x_0 = input(50, title='Start Regression at Bar',  tooltip='Bar index on which to start regression.')
lag = input(2, title='Lag', tooltip='Lag for crossover detection.')
stopLossBars = input(3, title='Stop Loss Bars', tooltip='Number of bars to check for stop loss condition.')
emaPeriod = input(46, title='EMA Period',  tooltip='Period for Exponential Moving Averages.')

lenjeje = input(32, title='ATR Period', tooltip='Period to calculate upper and lower band')
coef = input(2.7, title='Multiplier', tooltip='Multiplier to calculate upper and lower band')

// Function for Nadaraya-Watson Kernel Regression
kernel_regression1(_src
```