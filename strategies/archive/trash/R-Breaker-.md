> Name

R-Breaker Trading Strategy

> Author

Tai Ji

> Strategy Description

R-Breaker Trading Strategy


> Source (python)

``` python
#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
#R-Breaker Trading Strategy
#Strategy Provider @FJK   QQ:171938416
#Improved by @Tai Ji  QQ:7650371

def my_buy(): # Opening Position
    try:
        global buy_price, buy_qty
        initAccount = ext.GetAccount()  # Trading template's export function to get the account status and save the initial state before strategy runs.
        opAmount = 1
        PositionRatio = 1
        # Check if there are any coins in the position; if not, perform a purchase.
        if int(initAccount.Stocks) > 1:
            if buy_price < 1:
                buy_price = _C(exchange.GetTicker).Last
                buy_qty = initAccount.Stocks
            # Log('Opening Position Information 1 - Coins still in position:', initAccount.Stocks, 'Clearing out', '-- Opening Position Details:', initAccount)
            return 1
        if int(initAccount.Stocks) < 1:
            if int(str(initAccount.Stocks).replace('0.', '')) >= 3:
                if buy_price < 1:
                    buy_price = _C(exchange.GetTicker).Last
                    buy_qty = initAccount.Stocks
                # Log('Opening Position Information 2 - Coins still in position:', initAccount.Stocks, 'Clearing out', '-- Opening Position Details:', initAccount)
                return 1

        opAmount = _N(initAccount.Balance * PositionRatio, 3)  # Purchase amount
        Log("Opening Position with no coins first - Buying %s yuan" % (str(opAmount)))   # Generate LOG log

        Dict = ext.Buy(opAmount)  # Buy using ext.Buy
        if Dict:  # Confirm successful opening position
            buy_price = Dict['price']  # Purchase price   #{'price': 4046.446, 'amount': 1.5}
            buy_qty = Dict['amount']  # Purchase quantity
            # LogProfit(_N(gains,4),'Opening Position Information - Money:',initAccount.Balance,'-- Coins:',initAccount.Stocks,'-- Opening Position Details:',Dict)
            print_log(1, initAccount)
            return 1
        return 0

    except Exception as ex:
        Log('except Exception my_buy:', ex)
        return 0


import time
import datetime
def Caltime(date1, date2):   # Calculate running days
    try:
        date1 = time.strptime(date1, "%Y-%m-%d %H:%M:%S")
        date2 = time.strptime(date2, "%Y-%m-%d %H:%M:%S")
        date1 = datetime.datetime(date1[0], date1[1], date1[2], date1[3], date1[4], date1[5])
        date2 = datetime.datetime(date2[0], date2[1], date2[2], date2[3], date2[4], date2[5])
        return date2 - date1
    except Exception as ex:
        Log('except Exception Caltime:', ex)
        return "Exception"

start_timexx = time.localtime(time.time()) #time.clock()
start_time = time.strftime("%Y-%m-%d %H:%M:%S", start_timexx)
buy_price = 0 # Purchase price
buy_qty = 0  # Purchase quantity
gains = 0  # Profit

beng_Account = ext.GetAccount()  # Initialization information
beng_ticker = _C(exchange.GetTicker).Last# Ticker  Market conditions   Last transaction price
beng_Balance = (beng_Account.Stocks * beng_ticker) + beng_Account.Balance # Initial account money

def print_log(k_p, data=""):  # Output
    try:
        name = ""
        if k_p:
            name = "Opening Position"
        else:
            name = "Closing Position"
        global beng_Account, beng_ticker, beng_Balance
        global gains
        end_Account = ext.GetAccount()  # Current account information
        end_ticker = _C(exchange.GetTicker).Last# Ticker  Market conditions   Last transaction price
        #################################################
        date1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        msg_data0 = ("This session started at: %s - Running for: %s\r\n" % (start_time, Caltime(start_time, date1)))
        #################################################
        msg_data1 = ("Initialization Status: %s\n Current Status: %s\r\n" % (beng_Account, end_Account))
        #################################################
        end_Balance = (end_Account.Stocks * end_ticker) + end_Account.Balance # Money currently in the account
        msg_data2 = ("Initial Money: %s - Current Money: %s - Profit/Loss: %s\r\n" % (str(beng_Balance), str(end_Balance), str(end_Balance - beng_Balance)))
        #################################################
        total = end_Account.Balance + end_Account.Stocks * _C(exchange.GetTicker).Last # Total account value
        roi = ((total / beng_Balance) - 1) * 100
        msg_data3 = ("Current Status: %s -- Money: %s -- Coins: %s -- Value approximately: %.2f\r\n" % (str(name), str(end_Account.Balance), str(end_Account.Stocks), roi))
        #################################################
        income = total - beng_Account['Balance'] - beng_Account['Stocks'] * beng_ticker # Total profit or loss
        msg_data4 = ("This session's Profit/Loss: %s (RMB)\tTotal Profit/Loss: %.2f (RMB) %.2f\r\n" % (str(gains), income, roi))
        #################################################
        # Calculation method for profit:
        # Floating Profit: Based on (Current Coins - Initial Coins) * Current Price + (Current Money - Initial Money)
        diff_stocks = end_Account.Stocks - beng_Account.Stocks    # Difference in coins
        diff_balance = end_Account.Balance - beng_Account.Balance   # Difference in money
        new_end_balance = diff_stocks * end_ticker + diff_balance # Realized profit/loss  # Current profit
        # Calculation method for book profit:
        # Book Profit: (Current Coins * Current Price + Current Money) - (Initial Coins * Initial Price + Initial Money)
        new_end_balance2 = (end_Account.Stocks * end_ticker + end_Account.Balance) - (beng_Account.Stocks * beng_ticker + beng_Account.Balance)
        msg_data5 = ("Floating Profit: %s (RMB)\r\nBook Profit: %s (RMB)\r\n" % (_N(new_end_balance, 3), _N(new_end_balance2, 3)))
        #################################################
        LogStatus("Initial Investment on 2016/9/24 - Invested 0.2 coins = 800 RMB in the market\r\n",
                  msg_data0, msg_data1, msg_data2, msg_data3, msg_data4, msg_data5,
                  "Update Time: %s\r\n" % (date1),
                  "%s" % (data)
                  )
        #################################################
        #################################################
        #################################################
    except Exception as ex:
        Log('except Exception print_log:', ex)

def my_sell(): # Closing Position
    try:
        global buy_price, buy_qty, gains, ExitPeriod
        ExitPeriod = 0
        nowAccount = ext.GetAccount()  # Trading template's export function to get the account information
        if nowAccount.Stocks <= 0.002:  # Ensure that the transaction volume is met
            # Log('Does not meet minimum trading volume:', nowAccount.Stocks)
            return 1

        # history_Last = _N(Volume_averages(Ticker_list), 2)    # Historical average price
        # cur_last = _N(_C(exchange.GetTicker).Last, 2)

        # if _N(_C(exchange.GetTicker).Last, 2) > buy_price + ExitPeriod:   # Current price must be greater than the opening price
        if True:
            # if _N(_C(exchange.GetTicker).Last, 2) > buy_price + ExitPeriod and history_Last - cur_last > 0 and history_Last - cur_last < 2 :   # Current price must be greater than the opening price
            # Log('Historical price difference:', history_Last - cur_last)
```