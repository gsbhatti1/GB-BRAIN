> Name

Bn - Obtain the smallest unit of change in accuracy - essential for a stable trading system

> Author

BTC【Strategy Ghostwriting】Team



> Source(python)

```python
#!Python3

"""
"Strategy Ghostwriting" and (Help for this program), write to QQ: 35787501

Binance Futures can be used to solve the problem of abnormal ordering due to accuracy, obtain the minimum unit of change, and use it to stabilize the operation of the trading system.
"""

import requests


def get_min_size(symbol: str, host="https://www.binancezh.jp"):

    """
    Get the minimum change unit
    Args:
        symbol: trading pair (str)
        For example: ETHUSDT etc.
        host: domain name will affect access timeout
        Foreign address: https://fapi.binance.com
        Domestic address (needs to be replaced after change): https://www.binancezh.jp
    Returns:
        Minimum change price (str), minimum change quantity (str)
    """

    tick_size, step_size = None, None
    symbols_info = requests.get(f"{host}/fapi/v1/exchangeInfo", timeout=5).json()["symbols"]

    for info in symbols_info:
        if symbol == info["symbol"]:
            tick_size, step_size = info["filters"][0]["tickSize"], info["filters"][1]["stepSize"]
            break

    return tick_size, step_size


def main():
    tick_size, step_size = get_min_size("ETHUSDT")
    Log(tick_size, step_size)

```

> Detail

https://www.fmz.com/strategy/347942

> Last Modified

2023-04-20 11:26:23