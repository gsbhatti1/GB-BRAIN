> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|20|Length|
|v_input_2|0.5|Delta|
|v_input_3|false|Beta|
|v_input_4|false|Gamma|
|v_input_5|false|Alpha|
|v_input_6|50|TriggerLevel|
|v_input_7|10|StopLossLevel|


> Strategy Code


```python
# Bandpass-Filter-Reversed-Strategy

import numpy as np
from pandas import DataFrame

def init():
    global Length, Delta, Beta, Gamma, Alpha, TriggerLevel, StopLossLevel
    
    Length = v_input_1
    Delta = v_input_2
    Beta = v_input_3 if isinstance(v_input_3, (int, float)) else 0.5 * (1 + np.cos(np.pi / Length))
    Gamma = v_input_4 if isinstance(v_input_4, (int, float)) else 0.5 * Delta
    Alpha = v_input_5 if isinstance(v_input_5, (int, float)) else Beta * Gamma
    
    TriggerLevel = v_input_6
    StopLossLevel = v_input_7

def on_bar(symbol, bar):
    global BP
    
    xPrice = bar.close
    BP = 0.5 * (1 - Alpha) * (xPrice - BP[-2]) + Beta * (1 + Alpha) * nz(BP[-1]) - Alpha * nz(BP[-2])
    
    if BP > TriggerLevel:
        buy()
    elif BP < -TriggerLevel:
        sell()
    
def on_stop_loss(symbol, bar):
    global BP
    
    xPrice = bar.close
    BP = 0.5 * (1 - Alpha) * (xPrice - BP[-2]) + Beta * (1 + Alpha) * nz(BP[-1]) - Alpha * nz(BP[-2])
    
    if BP < StopLossLevel:
        sell()
    elif BP > -StopLossLevel:
        buy()

BP = 0
```