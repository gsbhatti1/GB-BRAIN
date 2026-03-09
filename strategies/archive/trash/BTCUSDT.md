> Name

BTCUSDT Quantitative Trading Execution Body

> Author

zomo

> Strategy Description

```
https://github.com/Find-Dream/BTCUSDT
```

> Currently, it only supports the OKEx API interface and BTCUSDT perpetual contract trading. The goal of quantitative trading is to pursue stable returns, so please do not set high leverage; it is recommended that the leverage be 5x or less.

- The Windows version is a GUI version. After downloading, configure the exchange API via `set_api` first, then run the `btcusdt` program to start automated trading;
- The Python source code GUI version can run on any desktop operating system as long as the Python environment is properly installed and configured; it is recommended to use Python 3.7.7, and you need to install the `requests` library. The usage method is similar to the Windows version of the GUI;
- The Python source code CLI version can run on any operating system as long as the Python environment is properly installed and configured; it is recommended to use Python 3.7.7, and you need to install the `requests` library. Manually modify the `okex_api.json` file to configure the exchange API. On CentOS, you can start the execution body in the background automatically with the following command:
```
nohup python3 start.py &
```
To stop the process and cease trading, use the following commands:
```
ps -aux | grep start.py
kill -9 进程号 获取到的进程号
```


### API Notes:

- If you are not running on a cloud host with a fixed IP address, do not set an IP binding; otherwise, it will be unable to use;
- For your account security, when applying for the API, check only read and trade permissions; do not check withdraw permission;
- The `flag` in `okex_api.json` is for trading account options. 0 represents a real account, and 1 represents a simulation account;

### Common Issues

#### Stuck at the Start of Trading

- Incorrect API configuration, please check if the API has been configured correctly; the API differs between real accounts and simulation accounts, so they need to be set separately;
- Domestic networks cannot access the exchange. Please run the execution body on an overseas cloud host; it is recommended to use a Hong Kong-based cloud host;
- Do not start the execution body using a proxy software domestically, as compatibility issues may render it non-functional;