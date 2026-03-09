``` pinescript
/*backtest
start: 2022-05-12 00:00:00
end: 2022-05-18 23:59:00
period: 3m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
//

study(title="Scalping PullBack Tool R1.1 by JustUncleL", shorttitle="SCALPTOOL R1.1", overlay=true)

//
// Revision:        1.1
// Original Author: JustUncleL
//
// Description:
//    This study project is a Scalping Pullback trading Tool that incorporates the majority of the indicators
//    needed to analyse and scalp Trends for Pull Backs and reversals intended for lower time frame
//    charts upto 15min, but it should work just as well on higher time frame charts for
//    longer term trades.
//
//    This Tool can be used with Heikin Ashi (HA) candle charts or normal candle charts, HA candles
//    will show a cleaner/smoother looking candle trend  but not show true prices.
//
//    Incorporated within this tool are the following indicators:
//    1. Trader selectable important EMAs in an EMA style Ribbon: 
//       - Green = fast EMA (default=89)
//       - Blue  = medium EMA (default=200) 
//       - Black = slow EMA (default=600)
//    2. The PAC EMA (default=34) High/Low+Close creates the Price Action Channel (PAC).
//    3. Fractals
//    4. HH, LH, LL, HL finder may help with drawing Trend lines and mini Trend Lines.
//    5. Coloured coded Bar high lighting based on the PAC: 
//       - blue = bar closed  above PAC
//       - red  = bar closed below PAC
//       - gray = bar closed inside PAC
//       - red line = PAC EMA (34) of bar close
//    6. Coloured chart Background to indicate Trend direction 
//       (NOTE: slow EMA(600) is not used in this Algo):
//       - green  = Trend direction is up when PAC and fast EMA(89) are above medium EMA(200).
//       - red    = Trend direction is down when PAC and fast EMA(89) are below medium EMA(200).
//       - yellow = Trend direction is in transition.
//    7. Pullback is defined as Price starts outside the PAC and then pulls back into the PAC
//       closing the opposite side of the PAC centre line, then a recovery arrow can occur.
//    8. Coloured Alert Arrows:
//       - maroon down arrow  = Pullback recovery Sell alert
//       - green up arrow     = Pullback recovery Buy alert
//    9. Option to force Heikin Ashi candles in Algo calculations.
//
// Setup and hints:
//
//  - I also add "Sweetspot Gold10" indicator to the chart as well to help with support and resistance 
//    finding and shows where the important "00" and "0" lines are.
//  - When price is above the PAC (blue bars) we are only looking to buy as price comes back to the PAC
//    When price is below the PAC (red bars), we are only looking to sell when price comes back to the PAC
//  - What we’re looking for when price comes back into the PAC we draw mini Trendlines (TL) utilising 
//    the Fractals and HH/LL points to guide your TL drawing.
//  - Now look for the trend to pull back and break the drawn mini TL. That's where we can place the scalp
//    trade.
//  - So we are looking for continuation signals in terms of a strong, momentum driven pullbacks 
//    of the PAC EMA(36).
//  - The other EMAs are there to check for other Pullbacks when PAC EMA (36) is broken.
//  - Other than the "Sweetspot Gold10" indicator, you should not need any other indicator to scalp 
//    for pullbacks.

```