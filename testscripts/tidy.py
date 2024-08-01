import sys
import time
import os
maxDays=7
path = (r'/tmp/')
print (path)

now=time.time()
# contents=os.listdir(path)
# print(contents)
# print(type (contents))

for f in [path+file for file in os.listdir(path) if file.isdigit() and len(file) == 15 and os.path.isfile(path+file) ]:
    # print (os.stat(path+f))
    print(f'{f}: {len(f)}')
    print(os.stat(f).st_mtime)
    print(now - maxDays * 60)
    if now - maxDays * 60 > os.stat(f).st_mtime:
        print('OLD '+f)
        os.remove(f)

