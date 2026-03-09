``` pinescript
/*backtest
start: 2022-05-02 00:00:00
end: 2022-05-08 23:59:00
period: 15m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © cmlaydinn

//@version=5
indicator(shorttitle='Angle-Attack-Follow-Line-Indicator', title='Angle Attack Follow Line Indicator ', overlay=false, max_bars_back=1000)

//INPUTS ————————————————————————————————————————————————————————————
FL = input(title='FOLLOW LINE CURRENT CHART RESOLUTION', defval=true)
BBperiod = input.int(defval=21, title='Period', minval=1)
BBdeviations = input.float(defval=1.00, title='Deviations', minval=0.1, step=0.05)
UseATRfilter = input(title='ATR Filter', defval=true)
ATRperiod = input.int(defval=5, title='ATR Period', minval=1)

FLH = input(title='FOLLOW LINE HIGHER TIME FRAME', defval=true)

AIB = input(title='Activate Indicator Background', defval=true)
TYPE = input.string(title='Type Of MA', defval='SMA', options=['SMA', 'EMA', 'WMA', 'VWMA', 'SMMA', 'KMA', 'TMA', 'HullMA', 'DEMA', 'TEMA', 'CTI'])
RES = input.timeframe('240', title='Resolution')
LEN = input(21, title='Period')
BBdeviations_ = input.float(defval=1.00, title='Deviations', minval=0.1, step=0.05)
ATRperiod_ = input.int(defval=5, title='ATR Period', minval=1)
SOUR = input(title='Source', defval='close')

MD = input(title='MODE', defval=true)

MODE = input.string(title='Type Of Mode', defval='FILTER HIGHER TIME FRAME', options=['NO FILTER HIGHER TIME FRAME', 'FILTER HIGHER TIME FRAME'])

AC = input(title='ANGLE CONFIGURATION', defval=true)

i_lookback = input.int(8, 'Angle Period', minval=1)
i_atrPeriod = input.int(10, 'ATR Period', minval=1)

BSA = input(title='BUY/SELL', defval=true)

Buy_0 = input(defval=true, title='Buy Change Follow Line')
Sell_0 = input(defval=true, title='Sell Change Follow Line')

OTA = input(title='OPTIONS TO ADD', defval=true)

Add_Buy_0 = input(defval=false, title='Option 1 to Add Buy')
Add_Sell_0 = input(defval=false, title='Option 1 to Add Sell')
Add_Buy_1 = input(defval=false, title='Option 2 to Add Buy')
Add_Sell_1 = input(defval=false, title='Option 2 to Add Sell')
Add_Buy_2 = input(defval=false, title='Option 3 to Add Buy')
Add_Sell_2 = input(defval=false, title='Option 3 to Add Sell')

OTR = input(title='OPTIONS TO REDUCE', defval=true)

Max_level_1 = input.int(defval=40, title='Max Angle Level 1', minval=1)
Max_level_2 = input.int(defval=65, title='Max Angle Level 2', minval=1)
Min_level_1 = input.int(defval=-40, title='Min Angle Level 1', minval=-100)
Min_level_2 = input.int(defval=-65, title='Min Angle Level 2', minval=-100)
Red_Buy_0 = input(defval=false, title='Option 1 to Reduce Buy Max Angle Level 1')
Red_Buy_1 = input(defval=true, title='Option 2 to Reduce Buy Max Angle Level 2')
Red_Buy_2 = input(defval=false, title='Option 3 to Reduce Buy 2 Bars Above Max Angle Level 2')
Red_Buy_3 = input(defval=true, title='Option 4 to Reduce Buy 3 Bars Above Max Angle Level 2')
Red_Buy_4 = input(defval=false, title='Option 5 to Reduce Buy 4 Bars Above Max Angle Level 2')
Red_Sell_0 = input(defval=true, title='Option 1 to Reduce Sell Min Angle Level 1')
Red_Sell_1 = input(defval=true, title='Option 2 to Reduce Sell Min Angle Level 1')
Red_Sell_2 = input(defval=false, title='Option 3 to Reduce Sell 2 Bars Below Min Angle Level 2')
Red_Sell_3 = input(defval=true, title='Option 4 to Reduce Sell 3 Bars Below Min Angle Level 2')
Red_Sell_4 = input(defval=false, title='Option 5 to Reduce Sell 4 Bars Below Min Angle Level 2')

OTH = input(title='OTHERS', defval=true)
```