``` pinescript
/*backtest
start: 2021-05-17 00:00:00
end: 2022-05-16 23:59:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5

// Revision:        3
// Author:          @millerrh
// Strategy:  
//      Entry: Buy when Donchian Channel breaks out
//      Exit: Trail a stop with the lower Donchian Channel band. 
// Conditions/Variables:
//    1. Can add a filter to only take setups that are above a user-defined moving average on current timeframe and/or longer timeframe (helps avoid trading counter trend) 
//    2. Manually configure which dates to back test
//    3. User-Configurable DC Channel length, with independent settings for top and bottom (Similar to Jessee Livermore Trading System where he used 150/50)
//    4. ADR (average of 21 days) added to a table as well as the percentage between the two bands.  Ability to filter out trades with stops wider than a % of the ADR for better Risk/Reward setups.
//    5. Optionally use a tighter lower DC Channel for your initial stop.  Once in profit, trail with wider DC channel to give more breathing room.

strategy('Rev Donchian Breakout', overlay=true, initial_capital=100000, currency='USD', default_qty_type=strategy.percent_of_equity, calc_on_every_tick = true,
  default_qty_value=100, commission_type=strategy.commission.percent, commission_value=0.1)

// === BACKTEST RANGE ===

// == INPUTS ==
// Donchian Channel Inputs
dcPeriodHigh = input.int(title="Upper Band: Period", defval=15, group = "donchian inputs", inline = "upper",
  tooltip = "Lookback period and color for the high price boundary.")
upperColor = input(color.new(color.blue, 10), title = "Color", group = "donchian inputs", inline = "upper")
dcPeriodLow = input.int(title="Lower Band: Period", defval=15, group = "donchian inputs", inline = "lower",
  tooltip = "Lookback period and color for the low price boundary.")
lowerColor = input(color.new(color.blue, 10), title = "Color", group = "donchian inputs", inline = "lower")
fillColor = input(color.new(color.gray, 90), title = "Fill Color", group = "donchian inputs",
  tooltip = "Adjust the color of the fill between the two main Donchian Channels.")
useTightStop = input.bool(title='Use a Tighter Channel for Initial Stop?', defval=false, group = "donchian inputs",
  tooltip = "'Keep your losers small and let winners run' is the saying.  This will allow you to use a tight initial stop 
  and then let it run once in profit with the looser stop of the wider main channel.")
dcPeriod2Low = input.int(title="Initial Stop: Period", defval=8, group = "donchian inputs", inline = "tight",
  tooltip = "Lookback period and color for the initial stop level when using a tighter initial stop.")
tightColor = input(color.new(color.orange, 10), title = "Color", group = "donchian inputs", inline = "tight")
trigInput = input.string(title='Execute Trades On...', defval='Close', options=['Wick', 'Close'], group = "donchian inputs",
  tooltip = "Useful for comparing standing stop orders at the Donchian channel boundary (executing on the wick) vs. waiting for candle closes prior to taking action")

// Moving Average Filtering Inputs
useMaFilterSlope = input.bool(title='Use Rising/Falling Moving Average as Filter?', defval=true, group = "moving average filtering")
tfSetSlope = input.timeframe(defval="D", title="Timeframe of Moving Average", group = "moving average filtering",
  tooltip = "Allows you to set a different time frame for a moving average filter.  Trades will be ignored when this moving average is declining.
  The idea is to keep your eye on the larger moves in the market and stay on the right side of the longer term trends and help you be pickier about 
  the stocks you trade.")
maSlopeType = input.string(defval='SMA', options=['EMA', 'SMA'], title='MA Type For Filtering', group = "moving average filtering")
maSlopeLength = input.int(defval=5, title="Moving Average: Length", minval=1, group = "moving average filtering", inline = "slope")
maSlopeColorR = input(color.new(color.green, 50), title = "Rising", group = "moving average filtering", inline = "slope")
maSlopeColorF = input(color.new(color.red, 50), title = "Falling", group = "moving average filtering", inline = "slope")
useMaFilterCurrent = input.bool(title='Use Moving Average for Filtering (Current Timeframe)?', defval=false, group = "moving average filtering",
  tooltip = "Use the current timeframe's moving average to filter trades.")
maSlopeColorRCur = input(color.new(color.green, 50), title = "Rising", group = "moving average filtering")
maSlopeColorFCur = input(color.new(color.red, 50), title = "Falling", group = "moving average filtering")
useMaFilterHigh = input.bool(title='Use Moving Average for Filtering (High Timeframe)?', defval=false, group = "moving average filtering",
  tooltip = "Use the high timeframe's moving average to filter trades.")
tfSetSlopeHigh = input.timeframe(defval="D", title="Timeframe of Moving Average", group = "moving average filtering")
maSlopeTypeHigh = input.string(defval='SMA', options=['EMA', 'SMA'], title='MA Type For Filtering', group = "moving average filtering")
maSlopeLengthHigh = input.int(defval=50, title="Moving Average: Length", minval=1, group = "moving average filtering", inline = "slope")
maSlopeColorRH = input(color.new(color.green, 50), title = "Rising", group = "moving average filtering")
maSlopeColorFH = input(color.new(color.red, 50), title = "Falling", group = "moving average filtering")

// ADR Filtering Inputs
useAdrFilter = input.bool(title='Use ADR for Filtering?', defval=false, group = "adr filtering")
adrLength = input.int(defval=120, title="% of ADR Value", minval=1, group = "adr filtering",
  tooltip = "Use the average range divided by a user-defined percentage to filter trades.")
adrTableVisibility = input.string(defval='Bottom', options=['Bottom', 'Top'], title="ADR Table Visibility", group = "adr filtering")

```