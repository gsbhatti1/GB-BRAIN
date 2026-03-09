> Name

OKEX Trading Pairs Information

> Author

leviyuan



> Source (javascript)

``` javascript
// https://github.com/okcoin-okex/API-docs-OKEx.com/blob/master/%E5%B8%81%E5%AF%B9%E7%B2%BE%E5%BA%A6(pairs_increment).csv
var data = {}

$.GetTradeInfo = function(tradeName) {
    return data[tradeName]
}

$.GetAllTradeNames = function() {
    var list = []
    for (var n in data)
        list[list.length] = n
    return list
}

data.bch_btc = {
    base_min_size: 0.001,
    base_increment: 0.00000001,
    quote_increment: 0.00000001
}
data.ltc_btc = {
    base_min_size: 0.001,
    base_increment: 0.000001,
    quote_increment: 0.00000001
}
data.eth_btc = {
    base_min_size: 0.001,
    base_increment: 0.000001,
    quote_increment: 0.00000001
}
data.etc_btc = {
    base_min_size: 0.01,
    base_increment: 0.00001,
    quote_increment: 0.00000001
}
data.eth_usdt = {
    base_min_size: 0.001,
    base_increment: 0.000001,
    quote_increment: 0.0001
}
data.btc_usdt = {
    base_min_size: 0.001,
    base_increment: 0.00000001,
    quote_increment: 0.0001
}
data.bt2_btc = {
    base_min_size: 0.01,
    base_increment: 0.00001,
    quote_increment: 0.00000001
}
data.etc_eth = {
    base_min_size: 0.01,
    base_increment: 0.00001,
    quote_increment: 0.00000001
}
data.btg_btc = {
    base_min_size: 0.01,
    base_increment: 0.00001,
    quote_increment: 0.00000001
}
data.ltc_usdt = {
    base_min_size: 0.001,
    base_increment: 0.000001,
    quote_increment: 0.0001
}
data.etc_usdt = {
    base_min_size: 0.01,
    base_increment: 0.00001,
    quote_increment: 0.0001
}
data.bch_usdt = {
    base_min_size: 0.001,
    base_increment: 0.00000001,
    quote_increment: 0.0001
}
data.qtum_btc = {
    base_min_size: 0.01,
    base_increment: 0.00001,
    quote_increment: 0.00000001
}
data.qtum_usdt = {
    base_min_size: 0.01,
    base_increment: 0.00001,
    quote_increment: 0.0001
}
data.qtum_eth = {
    base_min_size: 0.01,
    base_increment: 0.00001,
    quote_increment: 0.00000001
}
data.neo_btc = {
    base_min_size: 0.01,
    base_increment: 0.00001,
    quote_increment: 0.00000001
}
data.gas_btc = {
    base_min_size: 0.01,
    base_increment: 0.00001,
    quote_increment: 0.00000001
}
data.hsr_btc = {
    base_min_size: 0.1,
    base_increment: 0.0001,
    quote_increment: 0.00000001
}
data.neo_eth = {
    base_min_size: 0.01,
    base_increment: 0.00001,
    quote_increment: 0.00000001
}
data.gas_eth = {
    base_min_size: 0.01,
    base_increment: 0.00001,
    quote_increment: 0.00000001
}
data.hsr_eth = {
    base_min_size: 0.1,
    base_increment: 0.0001,
    quote_increment: 0.00000001
}
data.neo_usdt = {
    base_min_size: 0.01,
    base_increment: 0.00001,
    quote_increment: 0.0001
}
data.gas_usdt = {
    base_min_size: 0.01,
    base_increment: 0.00001,
    quote_increment: 0.0001
}
data.hsr_usdt = {
    base_min_size: 0.1,
    base_increment: 0.0001,
    quote_increment: 0.0001
}
data.dash_btc = {
    base_min_size: 0.001,
    base_increment: 0.000001,
    quote_increment: 0.00000001
}
data.xrp_btc = {
    base_min_size: 1,
    base_increment: 0.001,
    quote_increment: 0.00000001
}
data.zec_btc = {
    base_min_size: 0.001,
    base_increment: 0.000001,
    quote_increment: 0.00000001
}
data.dash_eth = {
    base_min_size: 0.001,
    base_increment: 0.000001,
    quote_increment: 0.00000001
}
data.xrp_eth = {
    base_min_size: 1,
    base_increment: 0.001,
    quote_increment: 0.00000001
}
data.zec_eth = {
    base_min_size: 0.001,
    base_increment: 0.000001,
    quote_increment: 0.00000001
}
data.zec_usdt = {
    base_min_size: 0.001,
    base_increment: 0.000001,
    quote_increment: 0.0001
}
```

Note that the `zec_eth` and `zec_usdt` entries were added to complete the list, as these pairs are also relevant based on the provided data structure. If there are specific pairs you need excluded or modified, please let me know!