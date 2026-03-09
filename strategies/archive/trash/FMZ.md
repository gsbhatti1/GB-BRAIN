> Name

FMZ Real Offer Robot Automatically Detects and Restarts Program with WeChat Push

> Author

eason04

> Strategy Description

**FMZ real-time robot automatically detects and restarts the program (WeChat push)**
![IMG](https://www.fmz.com/upload/asset/27d06163dac4df7fe8520.png)
Fill in the API and APIkey you applied for on the FMZ platform here
![IMG](https://www.fmz.com/upload/asset/27cef09a09fbccac93116.png)
The variable token is the code used to send WeChat push. The following is the application method:
Open the website: [https://www.pushplus.plus/](https://www.pushplus.plus/)
Log in with your own WeChat and follow the official account (not advertising)
![IMG](https://www.fmz.com/upload/asset/27d5d579fa87c8f486136.png)
Click for one-to-one message
![IMG](https://www.fmz.com/upload/asset/27d526d1a1f71b1e4fc15.png)
Copy the token and fill it in the token variable
![IMG](https://www.fmz.com/upload/asset/27dd43d36cf1e78165bc7.png)
Fill in the robotId variable with the number of the real robot you need to monitor (list format)
![IMG](https://www.fmz.com/upload/asset/27e6ff0ca668d74343caf.png)
The real offer robot number can be opened on the FMZ web version and obtained on the website.

**The code can be run directly locally,
But you need to turn on the computer all the time.
You can also run it on your own server.
Running on the server requires installing third-party libraries in advance.**

> Source(python)

```python
'''
The code can be directly run locally.
However, you need to turn on the computer all the time, or you can run it on your own server.
'''

import time
import json
import ssl
import requests
ssl._create_default_https_context = ssl._create_unverified_context

try:
    import md5
    import urllib2
    from urllib import urlencode
except ImportError:
    import hashlib as md5
    import urllib.request as urllib2
    from urllib.parse import urlencode

accessKey = '48xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxde'
secretKey = '91xxxxxxxxxxxxxxxxxxxxxxxxxxxx84'

def api(method, *args):
    d = {
        'version': '1.0',
        'access_key': accessKey,
        'method': method,
        'args': json.dumps(list(args)),
        'nonce': int(time.time() * 1000),
    }

    d['sign'] = md5.md5(('%s|%s|%s|%d|%s' % (d['version'], d['method'], d['args'], d['nonce'], secretKey)).encode('utf-8')).hexdigest()
    # Note: urllib2.urlopen function, timeout problem, you can set the timeout, urllib2.urlopen('https://www.fmz.com/api/v1', urlencode(d).encode('utf-8'), timeout=10) sets the timeout to 10 seconds
    return json.loads(urllib2.urlopen('https://www.fmz.com/api/v1', urlencode(d).encode('utf-8')).read().decode('utf-8'))

def send_wechat(msg):
    token = '93xxxxxxxxxxxxxxxxxxxxxxxxxxxx57' # Copy to that token
    title = '[Waring] Strategy Information'
    content = msg
    template = 'html'
    url = f"https://www.pushplus.plus/send?token={token}&title={title}&content={content}&template={template}"
    r = requests.get(url=url)
    print(json.loads(r.text)['msg'])

robotId = [xxx,xxx,xxx] #Robot code that needs to be monitored


while True:
    for j in range(len(robotId)):
        detail = api('GetRobotDetail', robotId[j])
        if detail['data']['result']['robot']['status'] == 1 and detail['data']['result']['robot']['wd'] == 1:
            print(f"The real disk {robotId[j]} status is normal status = {detail['data']['result']['robot']['status']}, real disk monitoring has been turned on wd = {detail['data']['result']['robot']['wd']}")
        pass
        elif detail['data']['result']['robot']['status'] == 1 :
            print(f"The real disk {robotId[j]} status is normal status = {detail['data']['result']['robot']['status']}, real disk monitoring is not turned on wd = {detail['data']['result']['robot']['wd']}")
        pass
        else:
            print(f"The real disk {robotId[j]} status is abnormal status = {detail['data']['result']['robot']['status']}")
            #Try to restart the real disk. Number of attempts = 4. Try once every 5 seconds.
            status=False
            for i in range(4):
                api('RestartRobot', robotId[j])
                robotDetail = api('GetRobotDetail', robotId[j])
                print(f"Try to restart the real disk {robotId[j]} for the {i+1}th time")
                if robotDetail['data']['result']['robot']['status'] == 1 :
                    mess = api('GetRobotLogs',robotId[j],0, 0, 0, 2, 0, 0, 0, 0)
                    print(f"Real disk {robotId[j]} restart completed status = {api('GetRobotDetail', robotId[j])['data']['result']['robot']['status']}\n"
                          f"Return error message 1: {mess['data']['result']['logs'][0]['Arr'][0][6]}\n"
                          f"Return error message 2: {mess['data']['result']['logs'][0]['Arr'][1][6]}\n")
                    send_wechat(f"Real disk {robotId[j]} restart completed status = {api('GetRobotDetail', robotId[j])['data']['result']['robot']['status']}\n"
                                f"Return error message 1: {mess['data']['result']['logs'][0]['Arr'][0][6]}\n"
                                f"Return error message 2: {mess['data']['result']['logs'][0]['Arr'][1][6]}\n")
                    status=True
                    break
                else:
                    print(f"The {i+1}th restart failed!!")
                    time.sleep(5)
            if status == False :
                print(f"Failed to restart the real disk {robotId[j]} 4 times and sent a warning message!!")
                send_wechat(f"Attempts to restart the real disk {robotId[j]} 4 times failed, please check in time!!\nAttempts 4 times to restart the real disk {robotId[j]} failed, please check in time!!\nAttempts 4 times to restart the real disk {robotId[j]} failed, please check in time!!\n")
            time.sleep(60*10)
```

> Detail

https://www.fmz.com/strategy/383695

> Last Modified

2022-09-22 18:27:23