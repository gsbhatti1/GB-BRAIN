> Strategy Arguments


|Argument|Default|Description|
|---|---|---|
|v_input_1|D|TimeFrame|
|v_input_2|9|ATR length|
|v_input_3|5|SMA length|
|v_input_4|20|SMA CurTF length|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-01-28 00:00:00
end: 2024-02-03 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("Lancelot RR Strategy", overlay=false)
p = 9
CO = close - open
HL = high - low
value1 = (CO + 2 * CO[1] + 2 * CO[2] + CO[3]) / 6
value2 = (HL + 2 * HL[1] + 2 * HL[2] + HL[3]) / 6
num = sum(value1, p)
denom = sum(value2, p)
RVI = denom != 0 ? num / denom : 0
RVIsig = (RVI + 2 * RVI[1] + 2 * RVI[2] + RVI[3]) / 6

rvicloselongcondition = crossunder(RVI, RVIsig)
rvicloseshortcondition = crossover(RVI, RVIsig)

plot(RVI, color=green, style=line, linewidth=1)
plot(RVIsig, color=red, style=line, linewidth=1)
bgcolor(rvicloseshortcondition ? green : na, transp=75)
bgcolor(rvicloselongcondition ? red : na, transp=75)

///Renko///
TF = input(title='TimeFrame', defval="D")
ATRlength = input(title="ATR length",  defval=9, minval=2, maxval=100)
SMAlength = input(title="SMA length",  defval=5, minval=2, maxval=100)
SMACurTFlength = input(title="SMA CurTF length",  defval=20, minval=2, maxval=100)

HIGH = request.security(syminfo.tickerid, TF, high)
LOW = request.security(syminfo.tickerid, TF, low)
CLOSE = request.security(syminfo.tickerid, TF, close)
ATR = request.security(syminfo.tickerid, TF, atr(ATRlength))
SMA = request.security(syminfo.tickerid, TF, sma(CLOSE, SMAlength))
SMACurTF = sma(CLOSE, SMACurTFlength)

RENKOUP = na
RENKODN = na
H = na
COLOR = na
BUY = na
SELL = na
UP = na
DN = na
CHANGE = na

RENKOUP := na(RENKOUP[1]) ? ((HIGH + LOW) / 2) + (ATR / 2) : RENKOUP[1]
RENKODN := na(RENKOUP[1]) ? ((HIGH + LOW) / 2) - (ATR / 2) : RENKODN[1]
H := na(RENKOUP[1]) or na(RENKODN[1]) ? RENKOUP - RENKODN : RENKOUP[1] - RENKODN[1]
COLOR := na(COLOR[1]) ? white : COLOR[1]
BUY := na(BUY[1]) ? 0 : BUY[1]
SELL := na(SELL[1]) ? 0 : SELL[1]
UP := false
DN := false
CHANGE := false

if (not CHANGE and close >= RENKOUP[1] + H * 3)
    CHANGE := true
    UP := true
    RENKOUP := RENKOUP[1] + ATR * 3
    RENKODN := RENKOUP[1] + ATR * 2
    COLOR := lime
    SELL := 0
    BUY := BUY + 3

if (not CHANGE and close >= RENKOUP[1] + H * 2)
    CHANGE := true
    UP := true
    RENKOUP := RENKOUP[1] + ATR * 2
    RENKODN := RENKOUP[1] + ATR
    COLOR := lime
    SELL := 0
    BUY := BUY + 2

if (not CHANGE and close >= RENKOUP[1] + H)
    CHANGE := true
    UP := true
    RENKOUP := RENKOUP[1] + ATR
    RENKODN := RENKOUP[1]
    COLOR := lime
    SELL := 0
    BUY := BUY + 1

if (not CHANGE and close <= RENKODN[1] - H * 3)
    CHANGE := true
    DN := true
    RENKODN := RENKODN[1] - ATR * 3
    RENKOUP := RENKODN[1] - ATR * 2
    COLOR := red
    BUY := 0
    SELL := SELL + 3

if (not CHANGE and close <= RENKODN[1] - H * 2)
    CHANGE := true
    DN := true
    RENKODN := RENKODN[1] - ATR * 2
    RENKOUP := RENKOUP[1]
```

This completes the translation of your strategy document. The code blocks and numbers remain as-is, while all human-readable text is translated to English.