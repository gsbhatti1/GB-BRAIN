> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|20|Length|
|v_input_2|0.5|Delta|
|v_input_3|false|Beta|
|v_input_4|false|Gamma|
|v_input_5|false|Alpha|

> Strategy Code

```python
# Bandpass Filter Reversed Strategy by ChaoZhang

def init(context):
    set_option("use_real_price", True)
    context.Length = v_input(1, "Length")
    context.Delta = v_input(2, "Delta")
    context.Beta = v_input(3, "Beta")
    context.Gamma = v_input(4, "Gamma")
    context.Alpha = v_input(5, "Alpha")

def handle_data(context, data):
    xPrice = history_bars(context.Length + 1, bar_type=BarType.Price)
    
    BP = 0.5 * (1 - context.Alpha) * (xPrice[-1] - xPrice[-2]) \
        + context.Beta * (1 + context.Alpha) * nz(BP[-1]) \
        - context.Alpha * nz(BP[-2])
        
    if BP > context.TriggerLevel:
        order_target(context.security, 100)
    elif BP < -context.TriggerLevel:
        order_target(context.security, -100)

# Example Trigger Level value
context.TriggerLevel = 5
```