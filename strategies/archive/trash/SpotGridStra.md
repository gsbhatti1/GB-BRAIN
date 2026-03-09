Name

SpotGridStra

Author

ktrader

Strategy Description

Grid management of spot goods


Source(python)

```python
# Spot grid management
'''
#Example:

def main():
    spot_g_stra = ext.SpotGridStra({'exchange': exchanges[1], #Spot exchange
                                    'ZPrecision': 2,
                                    'XPrecision': 3,
                                    'MinStock': 0.001,
                                    'GridSize': 0.03,
                                    'Symbol': 'BNB',
                                    'BalancePoint': 0.5
                                    })
    while True:
        spot_g_stra.run()
        Sleep(60*10000)

'''


class SpotGridStra():

    def __init__(self, cfg):
        self.cfg = cfg
        self.exchange = cfg['exchange'] #Spot exchange
        self.ZPrecision = cfg['ZPrecision'] #Coin price precision, integer
        self.XPrecision = cfg['XPrecision'] #The minimum quantile of the currency’s trading volume, such as BNB is 2
        self.Symbol = cfg['Symbol'] #Coin symbol
        self.GridSize = cfg['GridSize'] #Adjust as much as the difference is
        self.MinStock = cfg['MinStock'] #The minimum transaction volume of the coin
        self.BalancePoint = cfg.get('BalancePoint', 0.5) #The balance point of the position of a specific currency

    def CancelPendingOrders(self):
        ret = False
        while True:
            orders = _C(self.exchange.GetOrders)
            if len(orders) == 0 :
                return ret

            for j in range(len(orders)):
                self.exchange.CancelOrder(orders[j].Id)
                ret = True
                if j < len(orders) - 1:
                    Sleep(1000)
            return ret

    def onTick(self):
        self.exchange.SetCurrency(self.Symbol + '_USDT')
        acc = _C(self.exchange.GetAccount)
        #Log(acc)
        ticker = _C(self.exchange.GetTicker)
        spread = ticker.Sell - ticker.Buy
        account_info = acc['Info']
        bals = account_info['balances']
        sel_asset = None
        usdt_val = 0.0
        for asset in bals:
            if asset['asset'] == self.Symbol:
                sel_asset = asset
            if asset['asset'] == 'USDT':
                usdt_val = float(asset['free'])
        assert sel_asset is not None, 'Corresponding asset not found:' + self.Symbol
        asset_val = ((float(sel_asset['free']) + float(sel_asset['locked'])) * ticker.Sell)
        total_val = usdt_val + asset_val
        Log(self.Symbol, total_val, '=', acc.Balance, '+', asset_val)
        diffAsset = (total_val*self.BalancePoint - asset_val)
        ratio = diffAsset / total_val
        #Log("ratio:", ratio, _D())
        if abs(ratio) < self.GridSize:
            return False
        if ratio > 0 :
            buyPrice = _N(ticker.Sell + spread, self.ZPrecision)
            buyAmount = _N(diffAsset / buyPrice, self.XPrecision)
            if buyAmount < self.MinStock:
                return False
            self.exchange.Buy(buyPrice, buyAmount, diffAsset, ratio)
        else :
            sellPrice = _N(ticker.Buy - spread, self.ZPrecision)
            sellAmount = _N(-diffAsset / sellPrice, self.XPrecision)
            if sellAmount < self.MinStock:
                return False
            self.exchange.Sell(sellPrice, sellAmount, diffAsset, ratio)
        return True

    def run(self):
        if self.onTick():
            Sleep(1000)
            self.CancelPendingOrders()

ext.SpotGridStra = SpotGridStra
```

Detail

https://www.fmz.com/strategy/276994

Last Modified

2021-04-29 17:49:31