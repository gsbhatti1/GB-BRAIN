> Name

SMA-Based-Intelligent-Trailing-Stop-Strategy-with-Intraday-Pattern-Recognition

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/6701dfa5622f7c083e.png)

#### Overview
This is a strategy based on the 18-day Simple Moving Average (SMA18), combining intraday pattern recognition and intelligent trailing stop mechanisms. The strategy primarily observes the price relationship with SMA18, along with intraday high and low positions, to execute long entries at optimal times. It employs a flexible stop-loss approach, offering both fixed stop-loss points and a two-day low trailing stop option.

#### Strategy Principles
The core logic includes several key elements:
1. Entry conditions based on price position relative to the 18-day moving average, with options for breakout or above-line entries
2. Analysis of intraday candlestick patterns, particularly focusing on Inside Bar patterns, to improve entry accuracy
3. Selective trading based on day-of-week characteristics
4. Entry price setting using limit orders with small upward offset from lows to improve fill probability
5. Dual stop-loss mechanisms: fixed stops based on entry price or trailing stops based on two-day lows

#### Strategy Advantages
1. Combines technical indicators and price patterns for more reliable entry signals
2. Flexible trading time selection mechanism for market-specific optimization
3. Intelligent stop-loss system that both protects profits and allows adequate price movement
4. Highly adjustable parameters for different market environments
5. Effective false signal reduction through Inside Bar pattern filtering

#### Strategy Risks
1. Fixed stops may trigger early exits in volatile markets
2. Trailing stops might lock in minimal profits during quick reversals
3. Frequent Inside Bars during consolidation may lead to overtrading
Mitigation measures:
- Dynamic stop-loss adjustment based on market volatility
- Addition of trend confirmation indicators
- Implementation of minimum profit targets to filter low-quality trades

#### Optimization Directions
1. Incorporate volatility indicators (like ATR) for dynamic stop-loss adjustment
2. Add volume analysis dimension to improve signal reliability
3. Develop smarter date selection algorithms based on historical performance
4. Implement trend strength filters to avoid trading in weak trends
5. Enhance Inside Bar recognition algorithms for improved pattern identification

#### Summary
This strategy constructs a comprehensive trading system by combining multiple analytical dimensions. Its core strengths lie in flexible parameter settings and intelligent stop-loss mechanisms, enabling adaptation to various market environments. Through continuous optimization and improvement, the strategy shows promise for maintaining stable performance across different market conditions.

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2025-01-16 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT","balance":49999}]
*/

//@version=5
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © zweiprozent

strategy('Buy Low over 18 SMA Strategy', overlay=true, default_qty_value=1)
xing = input(false, title='crossing 18 sma?')
sib = input(false, title='trade inside Bars?')
shortinside = input(false, title='trade inside range bars?')
offset = input(title='offset', defval=0.001)
belowlow = input(title='stop below low minus', defval=0.001)
alsobelow = input(false, title='Trade only above 18 sma?')
tradeabove = input(false, title='Trade with stop above order?')
trailingtwo = input(false, title='exit with two days low trailing?')

insideBar() =>  //and high <= high[1] and low >= low[1] ? 1 : 0
    open <= close[1] and close >= open[1] and close <= close[1] or open >= close[1] and open <= open[1] and close <= open[1] and close >= close[1] ? 1 : 0

inside() =>
    high <= high[1] and low >= low[1] ? 1 : 0
enterIndex = 0.0
enterIndex := enterIndex[1]

inPosition = not na(strategy.position_size) and strategy.position_size > 0
if inPosition and na(enterIndex)
    enterIndex := bar_index
    enterIndex

T_Low = request.security(syminfo.tickerid, 'D', low[0])
D_High = request.security(syminfo.tickerid, 'D', high[1])
D_Low = request.security(syminfo.tickerid, 'D', low[1])
D_Close = request.security(syminfo.tickerid, 'D', close[1])
D_Open = request.security(syminfo.tickerid, 'D', open[1])

W_High2 = request.security(syminfo.tickerid, 'W', high[1])
W_High = request.security(syminfo.tickerid, 'W', high[0])
W_Low = request.security(syminfo.tickerid, 'W', low[0])