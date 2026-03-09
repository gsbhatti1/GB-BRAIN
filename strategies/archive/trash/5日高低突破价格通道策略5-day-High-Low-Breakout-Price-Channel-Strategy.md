> Name

5-day High-Low Breakout Price Channel Strategy

> Author

ChaoZhang

> Strategy Description



``` pinescript
/*backtest
start: 2023-08-13 00:00:00
end: 2023-09-12 00:00:00
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// @version=4
// Based on Sort pseudo-array v2 by apozdnyakov https://www.tradingview.com/script/IUlIoSnA-Sort-pseudo-array-v2/

strategy(title="5 Day high/low breakout strategy", shorttitle="5 days range breakout", overlay=true)
entry_factor = input(title="Entry - % point above high/low", type=input.float, defval=0.3, minval=0, maxval=5)
profit_target = input(title="Profit Target %", type=input.float, defval=0.5, minval=0, maxval=5)
trade_type   = input(defval = "BOTH", title = "Trade Type: LONG, SHORT, BOTH ( case sensitive )", type = input.string)
width = input(defval = 2, title = "High/Low line width (Enter 0 to hide )", type = input.integer, minval=0, maxval=5)
debug = input(defval= "NO", title = "Display sorted low/high: YES, NO ( case sensitive )", type = input.string)

high_day1 = security(syminfo.tickerid, "D", high[1], lookahead = barmerge.lookahead_on)
high_day2 = security(syminfo.tickerid, "D", high[2], lookahead = barmerge.lookahead_on)
high_day3 = security(syminfo.tickerid, "D", high[3], lookahead = barmerge.lookahead_on)
high_day4 = security(syminfo.tickerid, "D", high[4], lookahead = barmerge.lookahead_on)
high_day5 = security(syminfo.tickerid, "D", high[5], lookahead = barmerge.lookahead_on)

low_day1 = security(syminfo.tickerid, "D", low[1], lookahead = barmerge.lookahead_on)
low_day2 = security(syminfo.tickerid, "D", low[2], lookahead = barmerge.lookahead_on)
low_day3 = security(syminfo.tickerid, "D", low[3], lookahead = barmerge.lookahead_on)
low_day4 = security(syminfo.tickerid, "D", low[4], lookahead = barmerge.lookahead_on)
low_day5 = security(syminfo.tickerid, "D", low[5], lookahead = barmerge.lookahead_on)

// sorts a list of up to the fixed length
sort_all(type) =>
	float s0 = na
	float s1 = na
	float s2 = na
	float s3 = na
	float s4 = na

    h_val = security(syminfo.tickerid, "D", high, false)
	
	float min = na
	float last = na

	for i = 0 to 4
		float min_local = na
		float last_local = na
		float val = na
		
		for l = 0 to 4
    		if type == "high"
    		    val := l == 0 ? high_day1 : val
                val := l == 1 ? high_day2 : val
		        val := l == 2 ? high_day3 : val
    		    val := l == 3 ? high_day4 : val
	    	    val := l == 4 ? high_day5 : val
            else
    		    val := l == 0 ? low_day1 : val
	    	    val := l == 1 ? low_day2 : val
		        val := l == 2 ? low_day3 : val
    		    val := l == 3 ? low_day4 : val
	    	    val := l == 4 ? low_day5 : val

			if(na(min) or val > min or (val == min and l > last))
				new_min_local = na(min_local) ? val : min(min_local, na(min) ? val : max(min, val))
				if(na(min_local) or new_min_local != min_local)
					last_local := l
					min_local := new_min_local
		
		min := min_local
		last := last_local
		
		s0 := i == 0 ? min : s0
		s1 := i == 1 ? min : s1
		s2 := i == 2 ? min : s2
		s3 := i == 3 ? min : s3
		s4 := i == 4 ? min : s4

	[s0, s1, s2, s3, s4]


[high5, high4, high3, high2, high1] = sort_all("high")
[low1, low2, low3, low4, low5] = sort_all("low")

plot(high1, color = color.blue, style=plot.style_circles, linewidth=width)
plot(high2, color = color.red, style=plot.style_circles, linewidth=width)
plot(low1, color = color.blue, style=plot.style_circles, linewidth=width)
plot(low2, color = color.red, style=plot.style_circles, linewidth=width)


if close >= (high1 * (1 + entry_factor/100)) and strategy.position_size == 0 and hour <= 12
    strategy.entry(id = "long_entry", long = true, qty = 1, stop = high2)

strategy.close(id = "long_entry", when = strategy.position_size != 0 and (close < high2  or close > high1 * (1 + (entry_factor + profit_target)/100)))


if close <= (low1 * (1 - entry_factor/100)) and strategy.position_size == 0
    strategy.entry(id="short_entry", long=false, qty=1, stop = low2)

strategy.close(id="short_entry", when=strategy.position_size != 0 and (close > low2 or close < low1 * (1 - (entry_factor + profit_target)/100)))
```

This script defines the "5-day High-Low Breakout Price Channel Strategy" where the strategy calculates the highest highs and lowest lows over the past five trading days to construct a price channel. It then triggers trades based on when prices break above or below these levels.

The steps are:

1. Calculate the highest high and lowest low prices over the past 5 trading days.
2. Use the top 2 highest high prices to build the upper rail, and the bottom 2 lowest low prices for the lower rail.
3. Generate a buy signal when price rises above the upper rail by a certain percentage (e.g., 0.3%).
4. Generate a sell signal when price falls below the lower rail by a certain percentage.
5. After entering a trade, use the second highest/lowest price as the stop loss level or track profit at a certain percentage before exiting.

The advantages of this strategy include using key high/low breakouts to identify trend reversal points. Breaking the channel indicates concentrated price-volume movement. However, it should be used with caution in ranging markets to avoid generating too many false signals.

Overall, watching key price area breakouts is a classic approach for trend following. However, traders still need to confirm this strategy using other indicators and optimize parameters to maximize its utility.
```