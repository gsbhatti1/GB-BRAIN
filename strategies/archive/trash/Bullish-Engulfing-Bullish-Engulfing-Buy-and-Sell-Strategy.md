> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|true|(?START DATE BACKTESTING)D: |
|v_input_int_2|true|M: |
|v_input_int_3|2022|Y: |
|v_input_int_4|31|(?END DATE BACKTESTING)D: |
|v_input_int_5|12|M: |
|v_input_int_6|2023|Y: |
|v_input_float_1|true|(?TAKE PROFIT-STOP LOSS)Target profit (%): |
|v_input_float_2|true|Stop Loss (%): |
|v_input_float_3|2|(?RISK MANAGEMENT)Orders size (%): |
|v_input_string_1|0|(?BULLISH ENGULFING)Detect Trend Based On: SMA50|SMA50, SMA200|No detection|
|v_input_color_1|#2bff00|Label Color Bullish|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-12-20 00:00:00
end: 2023-12-26 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © thequantscience

// ██████╗ ██╗   ██╗██╗     ██╗     ██╗███████╗██╗  ██╗    ███████╗███╗   ██╗ ██████╗ ██╗   ██╗██╗     ███████╗██╗███╗   ██╗ ██████╗ 
// ██╔══██╗██║   ██║██║     ██║     ██║██╔════╝██║  ██║    ██╔════╝████╗  ██║██╔════╝ ██║   ██║██║     ██╔════╝██║████╗  ██║██╔════╝ 
// ██████╔╝██║   ██║██║     ██║     ██║███████╗███████║    █████╗  ██╔██╗ ██║██║  ███╗██║   ██║██║     █████╗  ██║██╔██╗ ██║██║  ███╗
// ██╔══██╗██║   ██║██║     ██║     ██║╚════██║██╔══██║    ██╔══╝  ██║╚██╗██║██║   ██║██║   ██║██║     ██╔══╝  ██║██║╚██╗██║██║   ██║
// ██████╔╝╚██████╔╝███████╗███████╗██║███████║██║  ██║    ███████╗██║ ╚████║╚██████╔╝╚██████╔╝███████╗██║     ██║██║ ╚████║╚██████╔╝
// ███████║  ╚═██╔═╝ ██╔══██║╚════██║██║██╔══██║██║  ██║    ╚════██║██║  ╚███║ ╚═══██╗ ╚███╔███╔╝██╔══██║██║     ██║██║  ╚████║ ╚═══██╗
// ██╔═══╝   ████╗ ███████║     ██║██║██║  ██║███████║    ███████║╚█████╔╝ ██████╔╝ ██╔╝╚███╔╝ ██║  ██║╚██████╗██║██║   ╚████║ ██████╔╝
// ██║       ████╗ ██╔══██║     ██║██║██║  ██║██╔══██║    ╚════██║ ╚═══██╗██╔══██╗ ██╔╝  ██╔╝  ██║  ██║ ╚═══██║██║╚██████╔╝██╔══██╗
// ████████╗╚██████╔╝██║  ██║     ██║██║╚█████╔╝██║  ██║    ███████║  █████╔╝██║  ██║██╔╝   ██║   ███████║ █████╔╝██║ ╚═╝ ██║██║  ██║
// ╚═════╝  ╚═════╝ ╚═╝  ╚═╝     ╚═╝╚═╝ ╚════╝ ╚═╝  ╚═╝    ╚══════╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝    ╚═╝   ╚══════╝ ╚═╝  ╚═╝ ╚═╝  ╚═╝╚═╝  ╚═╝
// ████████╗ ██████╗ ██╗      ██████╗ ██╗     ███████╗███████╗███████╗██╗   
// ╚══██╔══╝██╔═══██╗██║     ██╔═══██╗██║     ██╔════╝██╔════╝██╔════╝██║   
//    ██║   ██║   ██║██║     ██║   ██║██║     █████╗  ███████╗█████╗  ██║   
//    ██║   ██║   ██║██║     ██║   ██║██║     ██╔══╝  ╚════██║██╔══╝  ██║   
//    ██║   ██║   ██║███████╗╚██████╔╝███████╗███████╗███████║███████╗███████╗
//    ╚═╝   ╚═╝   ╚═╝╚══════╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝╚══════╝╚══════╝
```

This PineScript code is for a Bullish Engulfing trading strategy on the Binance Futures BTC/USDT pair. The script defines backtesting parameters, risk management settings, and detects Bullish Engulfing patterns based on specific conditions. The strategy uses stop loss and take profit levels to manage trades, and it includes various arguments to customize its behavior.