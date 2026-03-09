> Name

Pivot-Reversal-Strategy-with-Pivot-Exit-基于枢轴点反转和退出的交易策略

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/175c47473db833c3289.png)

#### Overview
This strategy uses Pivot Points to identify market reversal points and make trading decisions based on them. When a Pivot High is formed within the last 4 candles on the left, the strategy enters a long position; when a Pivot Low is formed within the last 4 candles on the left, the strategy enters a short position. The stop loss is set at one tick size (syminfo.mintick) above or below the entry price. There are two exit conditions: 1) exit when the next opposite pivot point appears; 2) exit when the floating loss reaches 30%.

#### Strategy Principles
1. Use `ta.pivothigh()` and `ta.pivotlow()` functions to calculate the Pivot High (swh) and Pivot Low (swl) within the range of 4 candles on the left and 2 candles on the right.
2. When a Pivot High exists (swh_cond), update the highest price (hprice), and when the current high is higher than the previous high, enable the long entry condition (le).
3. When the long entry condition (le) is met, enter a long position at one tick size (syminfo.mintick) above the Pivot High.
4. Similarly, when a Pivot Low exists (swl_cond), update the lowest price (lprice), and when the current low is lower than the previous low, enable the short entry condition (se).
5. When the short entry condition (se) is met, enter a short position at one tick size (syminfo.mintick) below the Pivot Low.
6. In the `exitAtNextPivot()` function, if holding a long position, set the stop loss at one tick size below the next Pivot Low; if holding a short position, set the stop loss at one tick size above the next Pivot High.
7. In the `exitIfProfitLessThanThirtyPercent()` function, calculate the profit and loss percentage for long and short positions, and close the position if the loss exceeds 30%.

#### Strategy Advantages
1. Pivot Points can well reflect the support and resistance levels in the market, and are a commonly used technical analysis indicator with certain market recognition.
2. Entering at the breakout of Pivot Points can capture market reversal opportunities.
3. Two exit conditions are set, one based on the next opposite pivot point for technical exit, and the other based on loss percentage for risk control exit, which can control the strategy drawdown to a certain extent.

#### Strategy Risks
1. The Pivot Point indicator itself has certain lag and frequent signal issues, and may not perform well in a fluctuating market.
2. The fixed calculation parameters of 4 candles and 2 candles may not be applicable to all market conditions, lacking certain adaptability and flexibility.
3. The stop loss is set close to the entry price (one tick size), which may be thrown away during violent market fluctuations.
4. The 30% loss stop setting may be too loose, with a large drawdown amplitude.

#### Strategy Optimization Directions
1. Try using other types of Pivot Point indicators, such as Factor Pivot Points, Weighted Pivot Points, etc., to improve the sensitivity and timeliness of the indicators.
2. The number of left and right candles can be used as input parameters, and the optimal values can be found through parameter optimization.
3. The stop loss position can be optimized to ATR or percentage stop loss. The former can adaptively adjust with changes in market volatility, while the latter can limit risks within a controllable range.
4. The 30% loss stop condition can be tightened to reduce strategy drawdown. In addition, a profit percentage stop condition can be added to manage both floating profits and losses.
5. Other filtering conditions, such as trend filtering and volatility filtering, can be superimposed on the basis of Pivot Point breakout to improve signal quality.

#### Summary
This strategy builds a bi-directional trading system based on the Pivot Point indicator, capturing market reversal opportunities by going long at Pivot Highs and short at Pivot Lows. The strategy has certain theoretical basis and practical value, but due to the limitations of the Pivot Point indicator itself, the strategy may face some risks and challenges in actual operation. By optimizing the Pivot Point indicator type, parameters, filtering conditions, stop loss and profit taking, etc., it is expected to further improve the robustness and profitability of the strategy.