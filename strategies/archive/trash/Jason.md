> Name

Iceberg commissioned buying-Jason

> Author

Jason_MJ

> Strategy Description

**1. Prerequisite:**
Learning writing strategies for the first time - iceberg commission:
This article mainly refers to the big brother’s strategy: https://www.fmz.com/strategy/188435
It's basically the same as the boss's strategy, but the writing is a little rougher. Mainly used for learning introduction. Please give me some advice.

**2. Antecedents**
When buying or selling large amounts of digital currencies, the market price of the currency you want to buy/sell may be affected due to the large transaction amount. This is even more true for digital currencies with poor liquidity. A large buy order can **pull the market**, and a large sell order can **smash the market**.
①Pulling: Pull up the price and raise the currency price
②Selling the currency: Regardless of the price, sell the currency directly, causing the currency price to fall.
③Trading currency Stocks: The currency used for trading, taking the BTC/USDT trading pair as an example, **BTC is the trading currency**
④Pricing currency Balance: The currency that users denominate, take the BTC/USDT trading pair as an example, **USDT is the pricing currency**

**Iceberg Commission:**
Operation: Refers to automatically splitting a large order into **multiple orders**, and automatically placing small orders based on the current latest buy/sell price and the price strategy set by the customer. **When the previous order is fully traded or the latest price deviates significantly from the current order, the order is automatically re-placed**.
Effect: Reduce the impact of large buy/sell orders on the market price. When making large purchases, you can **prevent your buying costs from increasing due to price increases caused by large buy orders**; when selling large amounts, you can **prevent your selling profits from lowering prices due to large sell orders**.

**Data Parameter Comparison:**
1. Order price = latest buying price X (1 - order depth)
2. Actual market order depth = (last transaction price - last order price) / last order price
3. Random single purchase quantity = average single purchase quantity X (100 - single average floating point number) % + (single average floating point number X 2) %
4. Available amount = Take the account denominated currency, a random single purchase quantity, and the minimum remaining total purchase amount.
5. Purchase quantity = available amount / commission price
6. Total remaining purchase amount = total purchase amount - (initial account denominated currency - account denominated currency)

**Rules:**
1. The order is automatically canceled when the distance between the latest transaction price and the order exceeds 2 X the order depth (indicating that the deviation is too large).
2. Stop the order when the total trading volume of the strategy equals the total order quantity.
3. Stop the order if the latest transaction price is higher than the maximum buying price.
4. Restore the order when the latest transaction price is lower than the maximum buying price.

**Main Parameters:**
1. Purchase amount
2. Single purchase quantity
3. Depth of commission
4. Maximum price
5. Price polling interval
6. Single purchase quantity average floating point number
7. Minimum transaction volume

**Idea:**
1. Get all unfilled orders and cancel them.
2. Get the initial account balance and determine whether it is greater than the total purchase amount.
3. Calculate the order price.
4. Calculate single purchase quantity.
5. Calculate available amount.
6. Calculate purchase quantity.
7. Execute buy.
8. Take a designated break.
9. Determine whether the last order was purchased successfully.
10. Successful output log.
11. Failure to judge whether the deviation is too large. If it is too large, it needs to be cancelled.

**Suggestion**
1. It is recommended to use ETH_USDT backtesting.

**The strategy is not perfect, I hope the bosses passing by can give me some advice**

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|buyAmount|10000|Buy Amount|
|buyNum|100|Average single purchase quantity|
|depthStatus|0.1|Delegation depth|
|highPrice|20000|Highest price|
|priceInterval|true|Ask price interval|
|minBuyNum|0.0001|Minimum transaction volume|
|buyOncePoint|10|Average floating point number of single purchase quantity|

> Source(python)

```python
import random


def main():
    # Get all unfilled orders in the account
    Log("Cancel all unfilled orders")
    orders = _C(exchange.GetOrders)
    if len(orders) > 0:
        for i in range(len(orders)):
            exchange.CancelOrder(orders[i]["Id"])
            Sleep(priceInterval*1000)

    # Compare account balances
    Log("Get user initialization account")
    initAccount = _C(exchange.GetAccount)
    if initAccount["Balance"] < buyAmount:
        Log("Account balance insufficient")
        return

    # Compare the average number of single purchases * Whether the market purchase price is greater than the account balance
    ticker = _C(exchange.GetTicker)
    if (ticker['Last'] * buyNum) > initAccount['Balance']:
        Log("The average price of a single purchase is greater than the account balance, please adjust the parameters")
        return

    lastBuyPrice = 0

    while True:
        Sleep(priceInterval*1000)
        # Get account information
        account = _C(exchange.GetAccount)
        # Get the current market conditions
        ticker = _C(exchange.GetTicker)
        # The last purchase price is not empty. Check whether the order is completed. If not, cancel it.
        if lastBuyPrice > 0:
            orders1 = exchange.GetOrders()
            if len(orders1) > 0:
                for j in range(len(orders1)):
                    # Calculate the actual market order depth
                    if ticker["Last"] > lastBuyPrice and ((ticker["Last"] - lastBuyPrice)/lastBuyPrice) > (2 * (depthStatus/100)):
                        Log("The order price deviates too much, latest transaction price:",ticker["Last"],"Order price",lastBuyPrice)
                        exchange.CancelOrder(orders1[j]["Id"])
                        lastBuyPrice = 0
                        continue
                    else:
                        Log("Buy order completed, cumulative cost:", _N(initAccount["Balance"] - account["Balance"]), "Average buying price:", _N((initAccount["Balance"] - account["Balance"]) / buyNum))
                        break

```