from datetime import datetime as dt
import time
import subprocess as sub

while True:
    # print(dt.now().date())
    time.sleep(360)
    try:
        sub.call(["rm","nohup.out"])
    except:
        pass
