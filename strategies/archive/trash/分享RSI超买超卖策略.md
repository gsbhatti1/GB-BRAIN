Name

Share RSI Overbought and Oversold Strategy

Author

Tagpangou - Strategy Rental


Source(python)

```python
import talib
import numpy as np
import time

# Initialize strategy parameters
symbol = 'huobip/btc_usdt'
period = '1m'
rsi_period = 14
rsi_buy = 30
rsi_sell = 70
amount = 0.01
last_buy_price = 0

# Connect API
exchange = Exchange()
exchange.SetContractType(symbol)
exchange.SetPeriod(period)

# Main loop
while True:
    # Get K-line data
    klines = exchange.GetRecords()
    if not klines:
        continue

    # Calculate RSI indicator
    close_prices = np.array([float(k['Close']) for k in klines])
    rsi = talib.RSI(close_prices, rsi_period)

    # Get the current price
    current_price = float(klines[-1]['Close'])

    # Determine whether it is overbought or oversold
    if rsi[-1] < rsi_buy and last_buy_price == 0:
        # oversold, buy
        buy_price = current_price
        buy_amount = amount / buy_price
        exchange.Buy(buy_price, buy_amount)
        last_buy_price = buy_price
        print('buy', buy_amount, 'BTC, price', buy_price)
    elif rsi[-1] > rsi_sell and last_buy_price != 0:
        # Overbought, Sell
        sell_price = current_price
        sell_amount = amount / sell_price
        exchange.Sell(sell_price, sell_amount)
        last_buy_price = 0
        print('sell', sell_amount, 'BTC, price', sell_price)

    # Wait for the next loop
    time.sleep(60)
```


Detail

https://www.fmz.com/strategy/410112

Last Modified

2023-04-18 12:46:08