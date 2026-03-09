```pinescript
/*backtest
start: 2023-11-15 00:00:00
end: 2023-11-22 08:00:00
period: 3m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// LOVE JOY PEACE PATIENCE KINDNESS GOODNESS FAITHFULNESS GENTLENESS SELF-CONTROL 
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © JoshuaMcGowan
// I needed to test/verify the functionality for canceling an open limit order in a strategy and also work thru the pieces needed to set the position sizing so each loss is a set amount. 
// This is not meant to be dropped into a chart but rather gives the code/logic in order to use in your own script w/alerts or strategy. Hope it helps. 
 
//@version=4
strategy("Momentum-Breakout-Strategy-Based-on-Internal-Amplitude-Stop-Loss", 
         shorttitle="Momentum Breakout Strategy", 
         overlay=false, 
         default_qty_type=strategy.percent_of_equity, 
         default_qty_value=25, 
         initial_capital=10000, 
         currency="USD", 
         default_price_type=strategy.close)

// Parameters
year_start = input(2020, title="Backtest Start Year")
month_start = input(2, title="Backtest Start Month")
day_start = input(true, title="Backtest Start Day")
year_end = input(2020, title="Backtest Stop Year")
month_end = input(12, title="Backtest Stop Month")
day_end = input(31, title="Backtest Stop Day")
leverage = input(1, title="Leverage Amount Desired: 10, 2, 3, 5, 1, 25, 50, 100")
risk_per_trade = input(true, title="Risk Total Per Trade in USD")

// Function to check if the K-line is an abnormal surge
is_abnormal_surge(kline) =>
    close > open and high < high[1] and low > low[1]

// Entry and Stop Loss
if is_abnormal_surge(close)
    strategy.entry("Long", strategy.long, comment="Entry on Abnormal Surge")
    strategy.exit("Stop Loss", "Long", stop=low[1], comment="Stop Loss at Previous Low")
```

This Pine Script implements the described strategy, with the entry and stop loss logic based on the conditions specified. The `is_abnormal_surge` function checks for the conditions that define an abnormal surge, and if such a condition is met, the script places a long trade entry and a stop loss order.