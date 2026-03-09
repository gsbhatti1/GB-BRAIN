```javascript
function GetCurrencyEx(ex, baseOrQuote) {
  let curr = ex.GetCurrency()
  let s = curr.split('_')
  return s[baseOrQuote ? 0 : 1]
}

function cancelOrdersPending(ex, orderType, orderOffset) {
  while (true) {
    const orders = ex.GetOrders()
    if (!orders) {
      Sleep(retryDelay)
      continue
    }
    let processed = 0
    for (let i = 0; i < orders.length; i++) {
      if (typeof orderType === 'number' && orders[i].Type !== orderType) {
        continue
      }
      if (typeof orderOffset === 'number' && orders[i].Offset !== orderOffset) {
        continue
      }

      ex.CancelOrder(orders[i].Id)
      if (isDebug) Log('cancelOrdersPending - ', orders[i])

      processed++
      Sleep(retryDelay)
    }
    if (processed === 0) {
      break
    }
  }
}

function isDepthBid(depthSide) {
  return depthSide[0].Price > depthSide[1].Price
}

/**
 *
 * @param {*} ex
 * @param {*} orderType ORDER_TYPE_BUY | ORDER_TYPE_SELL
 * @param {*} price
 * @param {*} quantity 交易额
 * @param {*} precision 交易额的精度
 * @param {*} minQuantity 最小交易额
 * @param {*} orderOffset 期货需要传这个参数, ORDER_OFFSET_OPEN | ORDER_OFFSET_CLOSE
 * @param {*} errorCancel true - 直接返回null , false - 取消所有方向相同的pending order，重新挂单，直到成功挂单为止
 * @returns order id
 */
function trade(ex, orderType, price, quantity, precision, minQuantity, orderOffset, errorCancel) {
  let tradeFunc = orderType === ORDER_TYPE_BUY ? ex.Buy : ex.Sell
  let tradeDirection
  if (orderOffset === ORDER_OFFSET_OPEN) {
    tradeDirection = orderType === ORDER_TYPE_BUY ? 'buy' : 'sell'
  } else if (orderOffset === ORDER_OFFSET_CLOSE) {
    tradeDirection = orderType === ORDER_TYPE_BUY ? 'closesell' : 'closebuy'
  }
  if (tradeDirection) {
    ex.SetDirection(tradeDirection)
  }

  if (isDebug) Log('trade 1 - ', 'orderType: ', orderType, ', orderOffset: ', orderOffset, ', tradeDirection: ', tradeDirection)

  const qty = _N(quantity, precision)
  if (qty === 0) {
    Log(`trade quantity in precision error. ${quantity} ${precision} ${qty}`, '#FF0000')
    return null
  }
  if (qty < minQuantity) {
    Log(`trade quantity less than min quantity. ${quantity} ${minQuantity} ${qty}`, '#FF0000')
    return null
  }

  let orderID
  while (true) {
    const id = tradeFunc(price, qty)
    if (!id) {
      if (errorCancel) {
        Log('trade id is null. maybe trade has sent!', '#FF0000')
        return null
      }

      Sleep(retryDelay)
      cancelOrdersPending(ex, orderType, orderOffset)
      continue
    }
    if (isDebug) Log('trade 2 - ', 'id: ', id, ', price: ', price, ', quantity: ', quantity)

    orderID = id
    break
  }

  return orderID
}

$.AverageSmooth = function (values) {
  // 剔除偏差较大的量
  let mean = math.mean(values)
  let stde = math.std(values)

  // 过滤平均值±2*标准差
  let ml = mean - 2 * stde
  let mh = mean + 2 * stde

  if (isDebug) Log('AverageSmooth 1 - ', mean, stde, ml, mh)

  let vs = values.filter((e) => {
    let res = e > ml && e < mh
    if (isDebug && !res) {
      Log('AverageSmooth 2 - filter: ', e)
    }
    return res
  })
  if (!vs || vs.length === 0) {
    return 0
  }
  return math.mean(vs)
}

$.CountDecimals = function (num) {
  const numTrim = parseFloat(num)
  return String(numTrim).includes('.') ? String(numTrim).split('.')[1].length : 0
}

$.LiquidationRate = function (open, last, liq) {
  return 1 - math.abs(last - liq) / math.abs(open - liq)
}

$.GetCurrencyBase = function (ex) {
  return GetCurrencyEx(ex, true)
}

$.GetCurrencyQuote = function (ex) {
  return GetCurrencyEx(ex, false)
}

$.CurrencyExist = function (ex, symbol) {
  const old = ex.GetCurrency()
  ex.SetCurrency(symbol)
  let exist = Boolean(ex.GetTicker())
  ex.SetCurrency(old)
  return exist
}

$.PriceRate = function (last, open) {
  return _N((last - open) / open, 4)
}

$.GetDepthTotal = function (depthSide, pricePercent) {
  if (pricePercent <= 0) {
    Log('pricePercent 大于 0')
    return 0
  }
  let isBid = isDepthBid(depthSide)
  let priceTarget = depthSide[0].Price * (1 + pricePercent * (isBid ? -1 : 1))
  let depthStage = depthSide.filter((e) => (isBid ? e.Price >= priceTarget : e.Price <= priceTarget))
  let total = depthStage.map((e) => e.Amount).reduce((prev, curr) => prev + curr)

  if (isDebug) {
    Log('isBid: ', isBid)
    Log('price: ', depthSide[0].Price, ', priceTarget: ', priceTarget)
    Log('depthStage: ', depthStage[depthStage.length - 1])
    Log('total: ', total)
  }

  return total
}

/**
 * 查询操作 amountAccumate 将会对价格产生多大的影响
 *
 * @param {*} depthSide
 * @param {*} amountAccumulate
 *
 * @returns 影响的价格
 */
$.GetDepthTotalPrice = function (depthSide, amountAccumulate) {
  let priceAccumulate = -1

  let am = 0
  for (let i = 0; i < depthSide.length; ++i) {
    const e = depthSide[i]
    am += e.Amount

    if (isDebug) Log('GetDepthTotalPrice - ', 'index: ', i, ', depth: ', e, ', amountAcc: ', am)

    if (am >= amountAccumulate) {
      priceAccumulate = e.Price
      break
    }
  }

  return priceAccumulate
}

$.GetDepthAmounts = function (depthSide) {
  return depthSide.map((e) => e.Amount)
}

$.GetRecordsVolume = function (records) {
  return records.map((e) => e.Volume)
}

$.GetRecordsVolumeAmount = function (records) {
  return records.map((e) => e.Volume * e.Close)
}

$.GetRecordsAmplitude = function (records) {
  return records.map((e) => (e.High - e.Low) / e.Open)
}

$.GetRecordsClose = function (records) {
  return records.map((e) => e.Close)
}

$.GetRecordsHigh = function (records) {
  return records.map((e) => e.High)
}

$.GetRecordsLow = function (records) {
  return records.map((e) => e.Low)
}

$.IsFuture = function (ex) {
  return /(F|f)utures.*/.test(ex.GetName())
}

/**
 * 取消所有未完成的订单
 *
 * @param {*} ex
 * @param {*} orderType null
 */
```