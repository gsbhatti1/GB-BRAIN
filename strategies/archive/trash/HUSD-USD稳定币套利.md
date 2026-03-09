> Name

HUSD-USD Stablecoin Arbitrage

> Author

OnePunchBoy

> Strategy Description

### HUSD/USDT Stablecoin Arbitrage
Huobi had a promotion for a while, where transactions involving HUSD did not incur any fees. Thus, a script was created to take advantage of this. 
The strategy takes advantage of the tendency for prices to **revert to 1** for stable arbitrage.

> Strategy Arguments



|Argument|Default|Description|
|---|---|---|
|MAX_ATR|0.0001|Maximum ATR|
|ORDER_AMOUNT|1000|Single-order volume|
|PRICE_CEIL|false|(?Price Range) Resistance Level|
|PRICE_FLOOR|false|Support Level|
|FEE_RATE|false|(?Profit Rate) Fee Rate|
|PROFIT_RATE|1e-05|Profit Rate|
|PRICE_PRECISION|4|(?Precision) Price Precision|
|AMOUNT_PRECISION|4|Order Volume Precision|
|MIN_ORDER_AMOUNT|true|Minimum Order Volume|



|Button|Default|Description|
|---|---|---|
|profitRate|1e-05|Profit Rate|
|orderAmount|1000|Single-order volume|
|start|__button__|Start|
|stop|__button__|Stop|
|priceCeil|false|(?Price Range) Resistance Level|
|priceFloor|false|Support Level|
|maxATR|0.0001|Maximum ATR|


> Source (javascript)

``` javascript
var _running = false
var _tickTimeCost = 0
var _profit = _G('profit') || 0
var _config = {
    orderAmount: ORDER_AMOUNT,
    priceCeil: PRICE_CEIL,
    priceFloor: PRICE_FLOOR,
    maxATR: MAX_ATR,
    profitRate: PROFIT_RATE
}
var _arbitCount = _G('arbit_count') || 0
var _depthHistory = _G('depth_history') || []

function getNow() {
    return UnixNano() / 1000000
}

function getDepth() {
    var depth = _C(exchange.GetDepth)
    _depthHistory.push(depth)
    _depthHistory = _depthHistory.slice(-5)
    _G('_depthHistory', JSON.stringify(_depthHistory))
    return depth
}

function getBase(ex) {
    return ex.GetCurrency().split('_')[0]
}

function getTypeText(type) {
    var list = [
        [ORDER_TYPE_BUY, 'Buy', '购买', '#01bf6a'],
        [ORDER_TYPE_SELL, 'Sell', '出售', '#ff0000']
    ]
    var found = _.find(list, function(items) {
        return items[0] === type || items[1] === type
    })
    return found ? found[2] + found[3] : ''
}

function getPriceTypeText(type) {
    if (type === 0) {
        return '对手价'
    } else if (type === 1) {
        return '成交价'
    } else if (type === 2) {
        return '挂1价'
    }
}

function getStatusText(st, showColor) {
    showColor = showColor == null ? true : showColor
    var list = [
        [ORDER_STATE_CLOSED, '已完成', '#f4b300'],
        [ORDER_STATE_PENDING, '未完成', '#000000'],
        [ORDER_STATE_CANCELED, '已取消', '#a3a3a3'],
        [ORDER_STATE_UNKNOWN, '未知状态', '#777777']
    ]
    var found = _.find(list, function(item) {
        return item[0] === st
    })
    return found && found.length > 0 ? found[1] + (showColor ? found[2] : '') : ''
}

function logMyProfit(num) {
    var newProfit = _profit + num
    if (newProfit !== _profit) {
        LogProfit(newProfit)
        _profit = newProfit
        _G('profit', _profit)
    }
}

function cancelOrder(id) {
    while (1) {
        var order = _C(exchange.GetOrder, id)
        if (order.Status === ORDER_STATE_PENDING) {
            exchange.CancelOrder(id)
        } else {
            return
        }
        Sleep(200)
    }
}

function getLastATR() {
    var askPrices = _.flatten(_.pluck(_depthHistory, 'Asks').map(function(d) { return d[0].Price }))
    var slicedPrices = askPrices.slice(-5)
    var avgPrice = new Decimal(_.reduce(slicedPrices, function(p, n) {
        return new Decimal(p).plus(n).toNumber()
    }, 0)).div(slicedPrices.length).toNumber()
    var askVaiance = new Decimal(_.reduce(slicedPrices, function(p, n) {
        return new Decimal(p).plus(new Decimal(n).minus(avgPrice).pow(2)).toNumber()
    }, 0)).div(slicedPrices.length).toNumber()
    var askSD = new Decimal(askVaiance).sqrt().toNumber()
    return askSD
}

function getHighestPrice() {
    var records = _C(exchange.GetRecords, PERIOD_H1)
    var highestPrice = TA.Highest(records, 8, 'Close')
    return highestPrice
}

function onTick() {
    var depth = getDepth() //_C(exchange.GetDepth)
    var arbitOrders = JSON.parse(_G('arbit_orders')) || []

    arbitOrders = _.map(arbitOrders, function(arbitOrder) {
        if (arbitOrder.Status === ORDER_STATE_CLOSED) {
            var buyOrder = arbitOrder.BuyOrder || {}
            var sellOrder = arbitOrder.SellOrder || {}
            var buyTradePrice = new Decimal(buyOrder.AvgPrice || 0).mul(buyOrder.DealAmount || 0).toNumber()
            var sellTradePrice = new Decimal(sellOrder.AvgPrice || 0).mul(sellOrder.DealAmount || 0).toNumber()
            var profit = new Decimal(sellTradePrice).minus(buyTradePrice).toNumber()
            if (profit > 0) {
                _arbitCount++
                _G('arbit_count', _arbitCount)
                logMyProfit(profit)
                $.ddNotice('套利成功', [
                    '### 套利成功',
                    '- 买价: ' + buyOrder.Price,
                    '- 卖价: ' + sellOrder.Price,
                    '- 买量: ' + buyOrder.DealAmount,
                    '- 卖量: ' + sellOrder.DealAmount,
                    '- 买交易额: ' + buyTradePrice,
                    '- 卖交易额: ' + sellTradePrice,
                    '- 利润: ' + profit,
                    '- 耗时: ' + ((getNow() - arbitOrder.CreatedAt) / 1000).toFixed(2) + 's',
                ])
            }
            return null
        }
        return arbitOrder
    })
    arbitOrders = _.compact(arbitOrders)
    _G('arbit_orders', JSON.stringify(arbitOrders))

    arbitOrders = _.map(arbitOrders, function(arbitOrder) {
        if (arbitOrder.Status === ORDER_STATE_PENDING) {
            var buyOrder = _C(exchange.GetOrder, arbitOrder.BuyOrder.Id)
            var sellOrder = arbitOrder.SellOrder ? _C(exchange.GetOrder, arbitOrder.SellOrder.Id) : null

            // 标记订单完成
            if (buyOrder && sellOrder && buyOrder.Status !== ORDER_STATE_PENDING && sellOrder.Status !== ORDER_STATE_PENDING) {
                return _.extend(arbitOrder, {
                    Status: ORDER_STATE_CLOSED,
                    BuyOrder: buyOrder,
                    SellOrder: sellOrder,
                })
            }

            // 购买完成后发起出售订单
            if (buyOrder.Status !== ORDER_STATE_PENDING && !sellOrder) {
                var sellAmount = _N(buyOrder.DealAmount, AMOUNT_PRECISION)
                if (sellAmount
```