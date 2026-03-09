> Name

BEST-Supertrend-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/112d5650fcb1ecdeb15.png) 
The Supertrend Strategy is a simple and effective trading strategy that can be used to profit from both the uptrend and downtrend markets. The strategy is based on the Supertrend indicator, which is a trend-following indicator that helps to identify the current trend and potential reversal points.

The BEST Supertrend Strategy is a modification of the standard Supertrend strategy that uses a higher factor and period. This makes the indicator more sensitive to changes in the trend, and can help to identify more profitable trading opportunities.

The strategy works by entering long trades when the price breaks above the Supertrend line and exiting long trades when the price breaks below the Supertrend line. Short trades are entered when the price breaks below the Supertrend line and exited when the price breaks above the Supertrend line.

The BEST Supertrend Strategy is a simple and effective strategy that can be used by traders of all experience levels. The strategy is also relatively low-risk, as it uses stop losses to limit losses.

Here are some of the benefits of using the BEST Supertrend Strategy:

- Simple and easy to understand
- Effective in both uptrend and downtrend markets
- Low-risk
- Profitable

If you are looking for a simple and effective trading strategy, the BEST Supertrend Strategy is a great option. The strategy is easy to learn and use, and it has the potential to generate profits in both uptrend and downtrend markets.

Here are some tips for using the BEST Supertrend Strategy:

- Use a high factor and period to make the indicator more sensitive to changes in the trend.
- Use stop losses to limit losses.
- Trade with a small size to manage risk.
- Backtest the strategy on historical data to see how it performs.

The BEST Supertrend Strategy is a great way to get started with trading. It is a simple and effective strategy that can be used by traders of all experience levels. If you are looking for a way to profit from the markets, the BEST Supertrend Strategy is a great option.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|0|What type of Orders: Longs+Shorts|LongsOnly|ShortsOnly|
|v_input_2|7|Fast Length SMA|
|v_input_3|20|Slow Length SMA|
|v_input_4|3|[ST] Factor|
|v_input_5|3|[ST] PD|
|v_input_6|0|Supertrend timeframe: daily|weekly|monthly|quartly|yearly|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-08-09 00:00:00
end: 2023-09-08 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
args: [["v_input_4",2]]
*/

//@version=4
//@author=Daveatt

// strategy(title="BEST Supertrend Strategy", shorttitle="Supertrend Strategy", overlay=true, 
//  pyramiding=0, default_qty_value=100, precision=7, currency=currency.USD,
//  commission_value=0.2,commission_type=strategy.commission.percent, initial_capital=1000000)


///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
/////////////////////////// Strategy Component /////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

orderType = input("Longs+Shorts",title="What type of Orders", options=["Longs+Shorts","LongsOnly","ShortsOnly"])
isLong   = (orderType != "ShortsOnly")
isShort  = (orderType != "LongsOnly")

// SMA
fastLength = input(7, title="Fast Length SMA")
slowLength = input(20, title="Slow Length SMA")

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
///////////////////////////// SUPERTREND /////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

Factor=input(3,title="[ST] Factor", minval=1,maxval = 100, type=input.float)
Pd=input(3, title="[ST] PD", minval=1,maxval = 100)
TF=input("daily", title="Supertrend timeframe", options=["daily","weekly","monthly","quartly","yearly"])

//////////////////////////
//* COLOR CONSTANTS *//
//////////////////////////

AQUA = #00FFFFFF
BLUE = #0000FFFF
RED  = #FF0000FF
LIME = #00FF00FF
GRAY = #808080FF
DARKRED   = #8B0000FF
DARKGREEN = #006400FF
GOLD = #FFD700
WHITE = color.white

// Plots
GREEN_LIGHT     = color.new(color.green, 40)
RED_LIGHT       = color.new(color.red, 40) 
BLUE_LIGHT      = color.new(color.aqua, 40)
PURPLE_LIGHT    = color.new(color.purple, 40) 


///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
/////////////////////// SUPERTREND DETECTION //////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

f_supertrend(Factor, Pd) =>

    Up=hl2-(Factor*atr(Pd))
    Dn=hl2+(Factor*atr(Pd))
    
    TrendUp = 0.0
    TrendUp := close[1]>TrendUp[1] ? max(Up,TrendUp[1]) : Up
    TrendDown = 0.0
    TrendDown := close[1]<TrendDown[1]? min(Dn,TrendDown[1]) : Dn
    Trend = 0.0
    Trend := close > TrendDown[1] ? 1: close< TrendUp[1]? -1: nz(Trend[1],1)
    Tsl = Trend==1? TrendUp: TrendDown

    Tsl

st_tsl = f_supertrend(Factor, Pd)

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
////////////////////////// MULTI TIMEFRAMES CALCS /////////////////////////////
///////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////