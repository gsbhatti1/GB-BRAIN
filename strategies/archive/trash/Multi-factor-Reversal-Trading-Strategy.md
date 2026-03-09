``` pinescript
/*backtest
start: 2023-09-11 00:00:00
end: 2023-09-13 08:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 16/04/2021
// This is combo strategies for get a cumulative signal. 
//
// First strategy
// This System was created from the Book "How I Tripled My Money In The 
// Futures Market" by Ulf Jensen, Page 183. This is reverse type of strategies.
// The strategy buys at market, if close price is higher than the previous close 
// during 2 days and the meaning of 9-days Stochastic Slow Oscillator is lower than 50. 
// The strategy sells at market, if close price is lower than the previous close price 
// during 2 days and the meaning of 9-days Stochastic Fast Oscillator is higher than 50.
//
// Second strategy
// The Polarized Fractal Efficiency (PFE) indicator measures the efficiency 
// of price movements by drawing on concepts from fractal geometry and chaos 
// theory. The more linear and efficient the price movement, the shorter the 
// distance the prices must travel between two points and thus the more efficient 
// the price movement.
//
// WARNING:
// - For purpose educate only
// - This script to change bars colors.
////////////////////////////////////////////////////////////
Reversal123(Length, KSmoothing, DLength, Level) =>
    vFast = sma(stoch(close, high, low, Length), KSmoothing) 
    vSlow = sma(vFast, DLength)
    pos = 0.0
    pos := iff(close[2] < close[1] and close > close[1] and vFast < vSlow and vFast > Level, 1,
	         iff(close[2] > close[1] and close < close[1] and vFast > vSlow and vFast < Level, -1, nz(pos[1], 0))) 
    pos


PFE(Length, LengthEMA, BuyBand, SellBand) =>
    pos = 0.0
    PFE = sqrt(pow(close - close[Length], 2) + 100)
    C2C = sum(sqrt(pow((close - close[1]), 2) + 1), Length)
    xFracEff = iff(close - close[Length] > 0,  round((PFE / C2C) * 100) , round(-(PFE / C2C) * 100))
    xEMA = ema(xFracEff, LengthEMA)
    pos := iff(xEMA < SellBand, -1,
    	      iff(xEMA > BuyBand, 1, nz(pos[1], 0))) 
    pos

strategy(title="Multi-factor Reversal Trading Strategy", 
         shorttitle="MFR", 
         overlay=false, 
         default_qty_type=strategy.percent_of_equity, 
         default_qty_value=5, 
         initial_capital=100000, 
         currency="USD") 

    // 123 Reversal
    is123Reversal = input(title="123 Reversal", type=bool, defval=true)
    length123 = input(14, title="Length")
    kSmoothing123 = input(title="KSmoothing", type=bool, defval=true)
    dLength123 = input(3, title="DLength")
    level123 = input(50, title="Level")
    
    // PFE
    isPFE = input(title="PFE", type=bool, defval=true)
    lengthPFE = input(9, title="LengthPFE")
    lengthEMA = input(5, title="LengthEMA")
    buyBand = input(50, title="BuyBand")
    sellBand = input(-50, title="SellBand")
    tradeReverse = input(false, title="Trade reverse")

    // 123 Reversal Signal
    reversal123 = Reversal123(length123, kSmoothing123, dLength123, level123)
    
    // PFE Signal
    pfe = PFE(lengthPFE, lengthEMA, buyBand, sellBand)
    
    // Combined Signal
    combinedSignal = is123Reversal and isPFE ? (reversal123 == pfe) : (reversal123 != 0)
    
    // Trade Logic
    if (combinedSignal)
        strategy.entry("Buy", strategy.long)
        strategy.close("Buy", when=combinedSignal != true)
    else
        strategy.entry("Sell", strategy.short)
        strategy.close("Sell", when=combinedSignal != true)
    
    // Plotting
    hline(0, "Zero Line")
    plot(reversal123, color=color.blue, title="123 Reversal Signal")
    plot(pfe, color=color.red, title="PFE Signal")
    plot(combinedSignal, color=color.green, title="Combined Signal")
```

This Pine Script code defines a multi-factor reversal trading strategy as described. The script includes the 123 reversal and PFE signals and combines them to generate trade entries. The strategy parameters are set to match the provided inputs.