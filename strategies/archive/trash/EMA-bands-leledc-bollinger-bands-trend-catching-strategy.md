```
Name

EMA-bands-leledc-bollinger-bands-trend-catching-strategy

Author

ChaoZhang

Strategy Description

The basics:
In its simplest form, this strategy is a positional trend following strategy which enters long when price breaks out above "middle" EMA bands and closes or flips short when price breaks down below "middle" EMA bands. The top and bottom of the middle EMA bands are calculated from the EMA of candle highs and lows, respectively.

The idea is that entering trades on breakouts of the high EMAs and low EMAs rather than the typical EMA based on candle closes gives a bit more confirmation of trend strength and minimizes getting chopped up. To further reduce getting chopped up, the strategy defaults to close on crossing the opposite EMA band (i.e., long on break above high EMA middle band and close below low EMA middle band).

This strategy works on all markets on all timeframes, but as a trend following strategy it works best on markets prone to trending such as crypto and tech stocks. On lower timeframes, longer EMAs tend to work best (I've found good results with EMA lengths even up to 1000), while 4H charts and above tend to work better with EMA lengths 21 and below.

As an added filter to confirm the trend, a second EMA can be used. Inputting a slower EMA filter can ensure trades are entered in accordance with longer term trends, inputting a faster EMA filter can act as confirmation of breakout strength.

Bar coloring can be enabled to quickly visually identify a trend's direction for confluence with other indicators or strategies.


The goods:
Waiting for the trend to flip before closing a trade (especially when a longer base EMA is used) often leaves money on the table. This script combines a number of ways to identify when a trend is exhausted for backtesting the best early exits.

"Delayed bars inside middle bands" - When a number of candles in a row open and close between the middle EMA bands, it could be a sign the trend is weak, or that the breakout was not the start of a new trend. Selecting this will close out positions after a number of bars has passed.

"Leledc bars" - Originally introduced by glaz, this is a price action indicator that highlights a candle after a number of bars in a row close the same direction and result in the greatest high/low over a period. It often triggers when a strong trend has paused before further continuation or marks the end of a trend. To mitigate closing on false Leledc signals, this strategy has two options: 1. Introducing requirement for increased volume on the Leledc bars can help filter out Leledc signals that happen mid-trend. 2. Closing after a number of Leledc bars appear after position opens. These two options work great in isolation but don't perform well together in my testing.

"Bollinger Bands exhaustion bars" - These bars are highlighted when price closes back inside the Bollinger Bands and RSI is within specified overbought/sold zones. The idea is that a trend is overextended when price trades beyond the Bollinger Bands. When price closes back inside the bands it's likely due for mean reversion back to the base EMA in which this strategy will ideally re-enter a position. Since the added RSI requirements often make this indicator too strict to trigger a large enough sample size to backtest, I've found it best to use "non-standard" settings for both the bands and the RSI as seen in the default settings.

"Buy/Sell zones" - Similar to the idea behind using Bollinger Bands exhaustion bars as a closing signal. Instead of calculating off of standard deviations, the Buy/Sell zones are calculated off multiples of the middle EMA bands. When trading beyond these zones and subsequently failing back inside, price may be due for mean reversion back to the base EMA. No RSI filter is used for Buy/Sell zones.

If any early close conditions are selected, it's often worth enabling trade re-entry on "middle EMA band bounce". Instead of waiting for a candle to close back inside the middle EMA bands, this feature will re-enter position on only a wick back into the middle bands as will sometimes happen when the trend is strong.

Any and all of the early close conditions can be combined. Experimenting with these, I've found can result in less net profit but higher win-rates and Sharpe ratios as less time is spent in trades.


The deadly:
The trend is your friend. But wouldn't it be nice to catch the trends early? In ranging markets (or when using slower base EMAs in this strategy), waiting for confirmation of a breakout of the EMA bands at best will cause you to miss half the move, at worst will result in getting consistently chopped up. Enabling "counter-trend" trades on this strategy will allow the strategy to enter positions on the opposite side of the EMA bands on either a Leledc bar or Bollinger Bands exhaustion bar. There is a filter requiring either a high/low (for Leledc) or open (for BB bars) outside the selected inner or outer Buy/Sell zone. There are also a number of different close conditions for the counter-trend trades to experiment with and backtest.

There are two ways I've found best to use counter-trend trades:
1. Mean reverting scalp trades when a trend is clearly overextended. Selecting from the first 5 counter-trend closing conditions on the dropdown list will usually close the trades out quickly, with less profit but less risk.
2. Trying to catch trends early. Selecting any of the close conditions below the first 5 can cause the strategy to behave as if it's entering into a new trend (from the wrong side).

This feature can be deadly effective in profiting from every move price makes, or deadly to the strategy's PnL if not set correctly. Since counter-trend trades open opposite the middle bands, a stop-loss is recommended to reduce risk. If stop-losses for counter-trend trades are disabled, the strategy will hold a position open often until liquidation in a trending market if the trade is offsides.
```