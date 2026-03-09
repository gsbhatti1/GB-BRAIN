> Name

Trade03-Double moving average volatility difference filtering

> Author

TradeMan

> Strategy Description

To give back to the FMZ platform and community, share strategies & codes & ideas & templates.

Introduction:
Volume price factor combination

✱Contact information (welcome to communicate and discuss, learn and progress together)
WECHAT: haiyanyydss
TEL: https://t.me/JadeRabbitcm
✱Fully automatic CTA & HFT trading system @2018 - 2023

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|S1|100|S1|
|percent|10|Percent|


> Source (MyLanguage)

``` pascal
(*backtest
start: 2018-01-01 00:00:00
end: 2021-06-30 23:59:00
Period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_OKCoin","currency":"BTC_USD","stocks":10}]
args: [["percent",5],["ContractType","quarter",126961]]
*)

S2:=10*S1;

ST:=1;

//LOTS:=MAX(1,INTPART(percent/100*MONEYTOT/(C*MARGIN*UNIT)));//Golden book
LOTS:= MAX(1,INTPART(percent/100*MONEYTOT*C/(MARGIN*UNIT)));//Coin book

MA1^^EMA(REF(C,1),S2); //Moving average 1
MA2^^EMA(MA1,S1); //Moving average 2

DBF:=IF((HIGH+LOW)<=(REF(HIGH,1)+REF(LOW,1)),0,MAX(ABS(HIGH-REF(HIGH,1)),ABS(LOW-REF(LOW,1)))); //If the sum of the high and low of the current bar is smaller than that of the previous bar, take 0. If it is larger, take the maximum value between HIGH-HIGH[1] and LOW-LOW[1];
KBF:=IF((HIGH+LOW)>=(REF(HIGH,1)+REF(LOW,1)),0,MAX(ABS(HIGH-REF(HIGH,1)),ABS(LOW-REF(LOW,1)))); //If the sum of the high and low of the current bar is greater than that of the previous bar, take 0. If it is smaller, take the maximum value between HIGH-HIGH[1] and LOW-LOW[1];
DBL:=(DBF+S1)/((DBF+S1)+(KBF+S1)); //Calculate the ratio difference calculated by DBF with respect to the sum of DBF+KBF;
KBL:=(KBF+S1)/((KBF+S1)+(DBF+S1)); //Calculate the ratio difference calculated by KBF with respect to the sum of KBF+DBF;
CHANGE:=DBL-KBL; //Difference between long and short change rates to get the volatility difference;
MACHANGE:=MA(CHANGE,S1); //Calculate the moving average of the volatility difference over S1 periods;
MACHANGE2:=EMA(MACHANGE,S1); //Smooth the moving average twice to obtain the final moving average;

BUYK:=BARPOS>S2 AND REF(C,1)>MA1 AND MA1>MA2 AND CHANGE>0 AND MACHANGE>MACHANGE2; //Conditions for opening a long position
SELLK:=BARPOS>S2 AND REF(C,1)<MA1 AND MA1<MA2 AND CHANGE<0 AND MACHANGE<MACHANGE2; //Conditions for opening a short position

SELLY:=REF(C,1)<MA1 AND REF(C,1)>BKPRICE*(1+0.01*ST); //Long take profit
BUYY:=REF(C,1)>MA1 AND REF(C,1)<SKPRICE*(1-0.01*ST); //Short take profit


BKVOL<=0 AND REF(BUYK,1),BPK(LOTS);

SKVOL<=0 AND REF(SELLK,1),SPK(LOTS);

BKVOL>0 AND REF(SELLY,1),SP(BKVOL);

SKVOL>0 AND REF(BUYY,1),BP(SKVOL);
```

> Detail

https://www.fmz.com/strategy/425797

> Last Modified

2023-09-04 22:33:22