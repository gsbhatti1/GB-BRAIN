> Name

Trade05-K line support and resistance ATR take profit

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
|LENTH|250|LENTH|
|percent|5|percent|


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

ATRS:=50;

// Trading volume
LOTS:=MAX(1,INTPART(percent/100*MONEY*C/(MARGIN*UNIT)));// Coin book

// Calculate the weighted average, resistance line and support line of the current K line
AVGP:=(HIGH + LOW + (CLOSE * 2)) / 4;
RS^^HHV((AVGP * 2) - LOW,LENTH);
ST^^LLV((AVGP * 2) - HIGH,LENTH);

// Calculate ATR
TR:=MAX(MAX((HIGH-LOW),ABS(REF(CLOSE,1)-HIGH)),ABS(REF(CLOSE,1)-LOW));
ATRVAL:=MA(TR,LENTH);

// Open a position
IF BKVOL<=1 AND HIGH >= REF(RS,1) AND VOL > 0 THEN BEGIN
1,BPK(LOTS);
END
IF SKVOL<=1 AND LOW <= REF(ST,1) AND VOL > 0 THEN BEGIN
1,SPK(LOTS);
END

// When opening a position, calculate the take profit price based on the ATR of the opening BAR.
IF BKVOL>0 AND BARSBK>0 THEN BEGIN
MYEXITPRICE:=BKPRICE + ATRVAL * ATRS;
END
IF SKVOL>0 AND BARSSK>0 THEN BEGIN
MYEXITPRICE:=SKPRICE - ATRVAL * ATRS;
END

// Close position
IF BKVOL>0 AND BARSBK>0 AND VOL>0 THEN BEGIN
// Take profit and exit
IF HIGH >= MYEXITPRICE THEN BEGIN
1,SP(LOTS);
END
END

IF SKVOL>0 AND BARSSK>0 AND VOL>0 THEN BEGIN
// Take profit and exit
IF LOW <= MYEXITPRICE THEN BEGIN
1,BP(LOTS);
END
END
```

> Detail

https://www.fmz.com/strategy/425800

> Last Modified

2023-09-04 22:33:45