import os.path
import time
import sys

intervalSecs=10
timeoutMins=2
timeoutCount=int(timeoutMins*60/intervalSecs)
count=0
print (f'count {count}, timeoutcount {timeoutCount}')
while not os.path.exists('/tmp/123456'):
    print (f'....{count}')
    time.sleep(intervalSecs)
    count+=1
    if count >= timeoutCount:
        sys.exit('Timed out')