#!/usr/local/bin/python
import requests
import json
import sys
import os.path
import time

intervalSecs=10
timeoutMins=2
maxDays=7
path = (r'/tmp/')
now=time.time()

# remove any stray files older than 7 days
for tmpFile in [path+file for file in os.listdir(path) if file.isdigit() and len(file) == 15 and os.path.isfile(path+file) ]:
    if now - maxDays * 3600 * 7 > os.stat(tmpFile).st_mtime:
        os.remove(tmpFile)

f = open("/var/log/stdout", "w")
f.write("PRE Script\n")

read_data = sys.stdin.read()
# print (read_data)

data = json.loads(read_data)
f.write (data['actionType'])
f.write ("\n")
#print (len(data['actionItem']))
#print (data['actionItem'][0]['actionType'])

# print ('target:')
#print (data['actionItem'][0]['currentComm'])
#print (data['actionItem'][0]['newComm'])
dataName=data['actionItem'][0]['currentComm']['commodityType'].lower() + 'Data'

if data['actionItem'][0]['newComm']['capacity'] < data['actionItem'][0]['currentComm']['capacity']:
    hotUpdate=data['actionItem'][0]['newComm'][dataName]['hotRemoveSupported']
elif data['actionItem'][0]['newComm']['capacity'] > data['actionItem'][0]['currentComm']['capacity']:
    hotUpdate=data['actionItem'][0]['newComm'][dataName]['hotAddSupported']
else:
    print(True)
    hotUpdate=True

f.write (f'hotUpdate: {str(hotUpdate)}\n')
if hotUpdate == True:
    f.write ('No shutdown needed\n')
else:
    requests.post('https://eo5tpbp6fxdjwit.m.pipedream.net/',read_data)
    timeoutCount=int(timeoutMins*60/intervalSecs)
    count=0
    while not os.path.exists(path + str(data['actionOid'])):
        f.write (f'....{count}')
        time.sleep(intervalSecs)
        count+=1
        if count >= timeoutCount:
            sys.exit('Timed out')

f.write('\n')
f.flush()
f.close()
