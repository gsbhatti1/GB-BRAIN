``` pinescript
/*backtest
start: 2022-05-10 00:00:00
end: 2022-05-16 23:59:00
period: 3m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © RedKTrader

//@version=5
indicator('[dev]RedK Momentum Bars', shorttitle='RedK MoBars v3.0', explicit_plot_zorder = true, timeframe='', timeframe_gaps=false)

// A trading system composed of 2 short Lazy Lines (preferably one open and one close - 2-3 bars apart) and a WMA long filter 
// loosely inspired by Edler Impulse System
// v2.0 cleaned up code and added MA options to be able to mix and match, and experiment with various setups 
// default values (my personal preference) remain the same as in v1.0 
// for example, some traders will consider "bear territory" only below SMA50, others will use EMA30 .. and so on.
// ---------------------------------------------------------------------------------------------------------------
// MoBars v3.0: 
// updated defaults to match the most common 3x MA cross-over set-up of SMA (10, 20, 50)
// updated visuals to push the 0 line to the background of the plot (using the explicit_plot_zorder param)
// and added a
```