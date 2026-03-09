> Name

Enhanced-Fish-Net-Strategy

> Author

ChaoZhang

> Strategy Description


``` pinescript
// Copyright nilux: https://www.tradingview.com/u/nilux/
// Based on the original of dasanc: https://www.tradingview.com/u/dasanc/

strategy("FSCG-TSSL", "FSCG-TSSL Mod Backtest", default_qty_type = strategy.percent_of_equity, default_qty_value = 100, initial_capital = 100000, slippage = 5)
Price = input.source(close, "Source")
Length = input(20,"Period")
transform = input("Inphase-Quadrature","Use Transform?",options=["Hilbert","Inphase-Quadrature","False"])
min = input(108,"Min. Period")
buyTreshold = input(-2.41, title = "Buy Treshold (-)", type = float, defval=-2.0, minval = -2.50, maxval = -0.01, step = 0.01)
sellTreshold = input(2.43, title = "Sell Treshold (+)", type = float, defval=2.0, minval = 0.01, maxval = 2.50, step = 0.01)

// === TSSL ===
fixedSL = input(title="SL Activation", defval=300)
trailSL = input(title="SL Trigger", defval=1)
fixedTP = input(title="TP Activation", defval=150)
trailTP = input(title="TP Trigger", defval=50)

// === BACKTEST RANGE ===
FromMonth = input(defval = 1, title = "From Month", minval = 1, maxval = 12)
FromDay   = input(defval = 1, title = "From Day", minval = 1, maxval = 31)
FromYear  = input(defval = 2019, title = "From Year", minval = 2015)
ToMonth   = input(defval = 1, title = "To Month", minval = 1, maxval = 12)
ToDay     = input(defval = 1, title = "To Day", minval = 1, maxval = 31)
ToYear    = input(defval = 9999, title = "To Year", minval = 2015)
start     = timestamp(FromYear, FromMonth, FromDay, 00, 00)
finish    = timestamp(ToYear, ToMonth, ToDay, 23, 59)
window()  => time >= start and time <= finish ? true : false

getIQ(src,min,max) =>
    PI = 3.14159265359
    P = src - src[7]
    lenIQ = 0.0
    lenC = 0.0
    imult = 0.635
    qmult = 0.338
    inphase = 0.0
    quadrature = 0.0
    re = 0.0
    im = 0.0
    deltaIQ = 0.0
    instIQ = 0.0
    V = 0.0
    
    inphase := 1.25*(P[4] - imult*P[2]) + imult*nz(inphase[3])
    quadrature := P[2] - qmult*P + qmult*nz(quadrature[2])
    re := 0.2*(inphase*inphase[1] + quadrature*quadrature[1]) + 0.8*nz(re[1])
    im := 0.2*(inphase*quadrature[1] - inphase[1]*quadrature) + 0.8*nz(im[1])
    if (re!= 0.0)
        deltaIQ := atan(im/re)
    for i=0 to max
        V := V + deltaIQ[i]
        if (V > 2*PI and instIQ == 0.0)
            instIQ := i
    if (instIQ == 0.0)
        instIQ := nz(instIQ[1])
    lenIQ := 0.25*instIQ + 0.75*nz(lenIQ[1],1)
    length = lenIQ<min ? min : lenIQ


getHT(src) =>
    Price = src
    Imult = .635
    Qmult = .338
    PI = 3.14159
    InPhase = 0.0
    Quadrature = 0.0
    Phase = 0.0
    DeltaPhase = 0.0
    InstPeriod = 0.0
    Period = 0.0
    Value4 = 
```

``` pinescript
||Enhanced Fish Net Strategy

This strategy improves on the classic Fish Net strategy by adding buy/sell signal thresholds and trailing stop loss to form a more complete trend following system.

The Fish Net strategy judges market trends by calculating the price centroid force, which reflects the relationship between price and volume. Rising centroid force indicates strengthening bullish power, while falling represents bearish strength, so trading signals can be generated accordingly. 

The key in calculating centroid force lies in the relationship between price and time. In simple terms, recent price changes have greater weights in influencing the overall trend judgment, while older prices have smaller weights. So when calculating, a time-decaying weight is multiplied. This makes transactions happening at higher levels impact the total judgment more.

But the original Fish Net only judged long/short based on the direction of the centroid curve, easily getting caught in sideways movements. This improved version adds defined buy/sell signal thresholds, only generating signals when the centroid force exceeds certain magnitude, filtering out much noise.

In addition, the improved version implements a combined mechanism of trailing stop loss and fixed stop loss for exits. After entering a trend, the trailing stop loss can keep adjusting along with price action, achieving dynamic risk control. The fixed stop loss can more reliably prevent losses from sudden events.

Of course, the centroid force indicator has limited capabilities in complex markets, and trailing stops can also be penetrated if improperly set, so traders need to stay alert and optimize parameters in a timely manner. But overall, the enhanced mechanism of this improved Fish Net strategy is more comprehensive, and can generate decent steady returns.
```

> Strategy Arguments

``` pinescript
|Argument|Default|Description|
|----|----|----|
|v_input_source_1_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_1|20|Period|
|v_input_2|0|Use Transform?: Inphase-Quadrature|Hilbert|False|
|v_input_3|108|Min. Period|
|v_input_4|-2.41|Buy Treshold (-)|
|v_input_5|2.43|Sell Treshold (+)|
|v_input_6|300|SL Activation|
|v_input_7|true|SL Trigger|
|v_input_8|150|TP Activation|
|v_input_9|50|TP Trigger|
|v_input_10|true|From Month|
|v_input_11|true|From Day|
|v_input_12|2019|From Year|
|v_input_13|true|To Month|
|v_input_14|true|To Day|
|v_input_15|9999|To Year|
```