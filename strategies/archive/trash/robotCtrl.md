Name

robotCtrl teaching strategy

Author

Inventor Quantification-Little Dream

Strategy Description

Related articles: https://www.fmz.com/digest-topic/5011

Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|strRobotParams|["175708,14:55:33-15:10:33"]|Robot timing parameters|
|isPushMsg|false|Whether to push to WeChat|
|accessKey|$$$__enc__$$$|ACCESS KEY of FMZ platform extension API|
|secretKey|$$$__enc__$$$|SECRET KEY of FMZ platform extension API|


Source(python)

```python
# -*- coding: utf-8 -*-
import time
import json

try:
    import md5
    import urllib2
    from urllib import urlencode
except ImportError:
    import hashlib as md5
    import urllib.request as urllib2
    from urllib.parse import urlencode

def api(method, *args):
    d = {
        'version': '1.0',
        'access_key': accessKey,
        'method': method,
        'args': json.dumps(list(args)),
        'nonce': int(time.time() * 1000),
    }

    d['sign'] = md5.md5(('%s|%s|%s|%d|%s' % (d['version'], d['method'], d['args'], d['nonce'], secretKey)).encode('utf-8')).hexdigest()
    return json.loads(urllib2.urlopen('https://www.fmz.com/api/v1', urlencode(d).encode('utf-8')).read().decode('utf-8'))

RobotParams = json.loads(strRobotParams)

def main():
    global RobotParams
    arrParams = []
    nowDay = 0
    strPush = ""
    if isPushMsg:
        strPush = "@"

    for i in range(len(RobotParams)):
        param = {}
        arr = RobotParams[i].split(",")
        if len(arr) != 2:
            raise Exception("String configuration error: delimiter,")
        param["id"] = arr[0]
        param["isProcessOpenThisDay"] = False
        param["isProcessCloseThisDay"] = False

        arr = arr[1].split("-")
        if len(arr) != 2:
            raise Exception("String configuration error: delimiter -")

        begin = arr[0]
        arrBegin = begin.split(":")
        if len(arrBegin) != 3:
            raise Exception("String configuration error: starting time delimiter:")

        param["begin"] = {}
        param["begin"]["hour"] = float(arrBegin[0])
        param["begin"]["min"] = float(arrBegin[1])
        param["begin"]["sec"] = float(arrBegin[2])

        end = arr[1]
        arrEnd = end.split(":")
        if len(arrEnd) != 3:
            raise Exception("String configuration error: end time delimiter:")

        param["end"] = {}
        param["end"]["hour"] = float(arrEnd[0])
        param["end"]["min"] = float(arrEnd[1])
        param["end"]["sec"] = float(arrEnd[2])
        arrParams.append(param)

    # test
    Log("Output parameters", arrParams, "#FF0000")

    while True:
        nowTime = time.localtime(time.time())
        nowHour = nowTime.tm_hour
        nowMin = nowTime.tm_min
        nowSec = nowTime.tm_sec

        tbl = {
            "type": "table",
            "title": "msg",
            "cols": ["id", "begin", "end", "Whether a startup has been executed today", "Whether a stop has been executed today"],
            "rows": []
        }

        for i in range(len(arrParams)):
            tbl["rows"].append([arrParams[i]["id"], json.dumps(arrParams[i]["begin"]), json.dumps(arrParams[i]["end"]), arrParams[i]["isProcessOpenThisDay"], arrParams[i]["isProcessCloseThisDay"]])
            if nowDay != nowTime.tm_mday:
                arrParams[i]["isProcessOpenThisDay"] = False
                arrParams[i]["isProcessCloseThisDay"] = False

            if not arrParams[i]["isProcessOpenThisDay"]:
                if nowHour == arrParams[i]["begin"]["hour"] and nowMin >= arrParams[i]["begin"]["min"] and nowSec >= arrParams[i]["begin"]["sec"]:
                    ret = api('RestartRobot', int(arrParams[i]["id"]))
                    arrParams[i]["isProcessOpenThisDay"] = True
                    Log("Robot ID:", arrParams[i]["id"], "Execute startup, please log in to the platform to check whether the startup is successful", "Extended API return value:", ret, strPush)

            if not arrParams[i]["isProcessCloseThisDay"]:
                if nowHour == arrParams[i]["end"]["hour"] and nowMin >= arrParams[i]["end"]["min"] and nowSec >= arrParams[i]["end"]["sec"]:
                    ret = api('StopRobot', int(arrParams[i]["id"]))
                    arrParams[i]["isProcessCloseThisDay"] = True
                    Log("Robot ID:", arrParams[i]["id"], "Execution stopped, please log in to the platform to check whether the stop is successful", "Extended API return value:", ret, strPush)

            if nowDay != nowTime.tm_mday:
                nowDay = nowTime.tm_mday

        LogStatus(_D(), nowTime, "\n`" + json.dumps(tbl) + "`")
        Sleep(500)
```

Detail

https://www.fmz.com/strategy/184600

Last Modified

2020-05-08 10:47:52