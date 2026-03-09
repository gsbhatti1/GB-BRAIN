> Name

BTCUSDT Quantitative Trading Execution Body

> Author

zomo

> Strategy Description

```
https://github.com/Find-Dream/BTCUSDT
```

> Currently, it only supports the OKEx API interface and BTCUSDT perpetual contract trading. The goal of quantitative trading is to achieve stable returns, so please do not set high leverage; it is recommended to keep the leverage multiplier at 5 or below.

- The Windows version is a graphical user interface (GUI) version. After downloading, first configure the exchange API via `set_api`, then run the `btcusdt` program to start automatic trading;
- The Python source code GUI version can be run on any desktop operating system as long as you have installed and configured the Python environment; it is recommended to use Python 3.7.7 and install the requests library, with a method similar to the Windows GUI version;
- The Python source code command-line version can be run on any operating system as long as you have installed and configured the Python environment; it is also recommended to use Python 3.7.7 and install the requests library. To configure the exchange API in `okex_api.json`, you can manually modify this file. On CentOS, you can use the following command to run the execution body in the background automatically:
```
nohup python3 start.py &
```
To terminate the process and stop trading, use the following command:
```
ps -aux | grep start.py
kill -9 <PID>
```


### API Notes:

- If you are not running on a fixed IP cloud host, do not set an IP binding; otherwise, it will be unusable;
- To ensure account security when applying for APIs, please select read-only and trading permissions but do not check withdrawal permissions;
- The `flag` in `okex_api.json` is the trading account option: 0 for real account, 1 for simulation account;

### Common Issues
##### Stuck after starting trading

- API settings are incorrect; please check if the API is configured correctly. Real accounts and simulation accounts use different APIs, so they need to be set separately;
- If domestic networks cannot access the exchange, please run the execution body on a foreign cloud host, such as one in Hong Kong;
- Do not start the execution body using proxy software domestically; due to compatibility issues, there is a high probability that it will fail to run with proxy software;

---

> Source (python)

``` python
from okex.trade import trade, pos_info, acc_info, select_last
import okex.api as api
import okex.Trade_api as Trade
import time
import json
from okex.log import log

# Full source code download address: https://github.com/Find-Dream/BTCUSDT

def main():
    nowtime = time.time()
    st = time.localtime(nowtime)
    update = time.strftime('%Y-%m-%d', st)
    filenamedate = time.strftime('%Y%m%d', st)
    logfilename = 'mark_' + str(filenamedate)

    log(logfilename, '========================【获取基础信息开始】========================')

    btcusdt_api_data = api.btcusdt_api()

    log(logfilename, 'btcusdt_api_data：' + str(btcusdt_api_data))

    btcusdt_api = btcusdt_api_data['rule']
    log(logfilename, 'btcusdt_api' + str(btcusdt_api))

    pos_api = btcusdt_api_data['pos']
    log(logfilename, 'pos_api' + str(pos_api))

    pos_okex = {}
    acc_okex = {}

    try:
        acc_api = api.select_acc()
        log(logfilename, '读取本地保存的账户信息' + str(acc_api))
    except:
        acc_okex['lever'] = 1

    acc_info_data = acc_info()[0]['details']

    for i in acc_info_data:
        if i['ccy'] == 'USDT':
            acc_okex['ccy'] = i['cashBal']
            log(logfilename, '读取接口账户余额' + str(i['cashBal']))

    for i in pos_info():
        if i['mgnMode'] == 'cross' and i['posSide'] == 'long':
            pos_okex['long'] = i['pos']
            if i['pos'] != '0':
                acc_okex['lever'] = i['lever']
                log(logfilename, '读取接口long账户杠杆倍数：' + str(i['lever']))
            else:
                acc_okex['lever'] = acc_api['lever']
                log(logfilename, '读取本地long账户杠杆倍数：' + str(acc_api['lever']))

        elif i['mgnMode'] == 'cross' and i['posSide'] == 'short':
            pos_okex['short'] = i['pos']
            if i['pos'] != '0':
                acc_okex['lever'] = i['lever']
                log(logfilename, '读取接口short账户杠杆倍数：' + str(i['lever']))

    api.set_acc(json.dumps(acc_okex))
    log(logfilename, '写入本地账户信息：' + str(acc_okex))
    last = float(select_last())
    log(logfilename, '读取当前价格：' + str(last))

    max_sz = int(float(acc_okex['ccy']) * float(acc_okex['lever']) / last * 100)
    log(logfilename, '最大交易量：' + str(max_sz))

    sz_r = max_sz / 20
    log(logfilename, '交易量系数：' + str(sz_r))

    pos_api_id = int(btcusdt_api['id'])
    pos_api_posSide = btcusdt_api['posside']
    pos_api_side = btcusdt_api['side']
    pos_api_sz = int(int(btcusdt_api['sz']) * sz_r)
    pos_api_uptime = int(btcusdt_api['uptime'])
    pos_api_long = int(int(pos_api['long']) * sz_r)
    pos_api_short = int(int(pos_api['short']) * sz_r)

    log(logfilename, 'pos_api_long：' + str(pos_api_long) + ',pos_api_short:' + str(pos_api_short) + ',pos_api_sz:' + str(pos_api_sz))
    log(logfilename, '本地仓位信息pos_okex：' + str(pos_okex))

    try:
        pos_log_done = int(api.pos_log_done())
    except:
        pos_log_done = api.pos_log_done()

    log(logfilename, 'pos_log_done:' + str(pos_log_done))

    log(logfilename, '========================【获取基础信息结束】========================')
    log(logfilename, '========================【mark任务开始】========================')
    log(logfilename, '判断pos_log_done_id是否为int型：' + str(type(pos_log_done)))
    if isinstance(pos_log_done, int):
        log(logfilename, 'pos_log_done_id为int型，判断pos_log_done_id与pos_log_id,pos_api_id:' + str(pos_api_id) + ',pos_log_done:' + str(pos_log_done))
        if pos_api_id > pos_log_done:
            log(logfilename, 'API的pos_log_id大于pos_log_done_id，判断API更新时间是否在10秒以内，nowtime:' + str(nowtime) + ',pos_api_uptime:' + str(pos_api_uptime))
            if nowtime < (pos_api_uptime + 13):
                log(logfilename, 'api更新时间在10秒内，判断api交易方向，pos_api_posSide' + str(pos_api_posSide) + ',pos_api_side:' + str(pos_api_side))
                if pos_api_posSide == 'long' and pos_api_side == 'buy':
                    log(logfilename, 'api交易方向：long-buy，判断当前持仓信息与api是否一致')
                    if int(pos_okex['long']) + int(pos_api_sz) == int(pos_api_long):
                        log(logfilename, '当前持仓信息与api一致，执行交易，当前持仓：' + str(pos_okex['long']) + ',API持仓：' + str(pos_api_long) + ',API交易数量：' + str(pos_api_sz))
                        trade_ok = trade(pos_api_side, pos_api_posSide, pos_api_sz, pos_api_id)
                        log(logfilename, '执行结果：' + str(trade_ok))
                    elif int(pos_okex['long']) + int(pos_api_sz) < int(pos_api_long):
                        log(logfilename, '当前持仓信息与api一致，执行交易，当前持仓：' + str(pos_okex['long']) + ',API持仓：' + str(pos_api_long) + ',API交易数量：' + str(pos_api_sz))
                        trade_ok = trade(pos_api_side, pos_api_posSide, pos_api_sz, pos_api_id)
                        log(logfilename, '执行结果：' + str(trade_ok))
                    else:
                        log(logfilename, 'long仓信息不一致，请将long仓手动平仓后再进行自动交易，当前持仓：' + str(pos_okex['long']) + ',API持仓：' + str(pos_api_long) + ',API交易数量：' + str(pos_api_sz))

                elif pos_api_posSide == 'long' and pos_api_side == 'sell':
                    log(logfilename, 'api交易方向：long-sell，判断是否符合平仓条件')
                    if int(pos_okex['long']) > 0:
                        # The rest of the code is omitted for brevity
```