``` pinescript
/* backtest
start: 2022-01-01 00:00:00
end: 2022-01-31 23:59:00
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// Strategy based on the 3 indicators:
//  - QQE MOD
//  - SSL Hybrid
//  - Waddah Attar Explosion
//
// The strategy was designed for backtesting purposes. 
// For detailed information on trade entry logic, refer to the strategy documentation.
// 
// Credits:
//  - QQE MOD: Mihkel00 (https://www.tradingview.com/u/Mihkel00/)
//  - SSL Hybrid: Mihkel00 (https://www.tradingview.com/u/Mihkel00/)
//  - Waddah Attar Explosion: shayankm (https://www.tradingview.com/u/shayankm/)

//@version=5
strategy("QQE MOD + SSL Hybrid + Waddah Attar Explosion", overlay=false, initial_capital=1000, currency=currency.NONE, max_labels_count=500, default_qty_type=strategy.cash, commission_type=strategy.commission.percent, commission_value=0.01)

// =============================================================================
// STRATEGY INPUT SETTINGS
// =============================================================================

// ---------------
// Risk Management
// ---------------
swingLength = input.int(10, "Swing High/Low Lookback Length", group='Strategy: Risk Management', tooltip='Stop Loss is calculated by the swing high or low over the previous X candles')
accountRiskPercent = input.float(2, "Account percent loss per trade", step=0.1, group='Strategy: Risk Management', tooltip='Each trade will risk X% of the account balance')

// ----------
// Date Range
// ----------
start_year = input.int(title="Start Year", defval=2022, minval=2010, maxval=3000, group='Strategy: Date Range', inline='1')
start_month = input.int(title="Start Month", defval=1, group='Strategy: Date Range', inline='1', options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
start_date = input.int(title="Start Day", defval=1, group='Strategy: Date Range', inline='1', options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28
```