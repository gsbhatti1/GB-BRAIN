Name

python-status bar table-display button example

Author

Inventor Quantification-Little Dream


Source(python)

```python
import json

def main():
    tab = {
        "type" : "table",
        "title" : "demo",
        "cols" : ["a", "b", "c"],
        "rows" : [["1", "2", {"type" : "button", "cmd" : "coverAll", "name" : "Close Position"}]] # Configure a button on the first row and third column of the status bar table. The name is Close Position
    }

    LogStatus("`" + json.dumps(tab) + "`")
```

Detail

https://www.fmz.com/strategy/147155

Last Modified

2019-05-10 11:35:13