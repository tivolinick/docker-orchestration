#!/usr/bin/python3
import psycopg2
import csv
import re
#==================================================================
#                             FUNCTIONS
#==================================================================

# function to build start and stop order lists for each application
def build_list(orderObj,order,id,application,environment):
    theKey=f'{application}@{environment}'
    try:
        if orderObj[theKey]:
            pass
    except KeyError:
        orderObj[theKey]=[]
    if len(orderObj[theKey]) <= int(order):
        orderObj[theKey].extend([''] * (int(order) - len(orderObj[theKey]) +1))
    orderObj[theKey][int(order)]=str(id)

# function to insert VM entries
def insertvm(vms,cursor,dnsname,startcmd,stopcmd,statuscmd):
    for i in range(len(vms)) :
        if vms[i][1]== dnsname:
            print('NAME')
            if vms[i][2] != startcmd or vms[i][3] != stopcmd or vms[i][4] != statuscmd:
                print('NO MATCH')
                print(f"UPDATE vms SET startcmd = '{startcmd}', stopcmd = '{stopcmd}', statuscmd = '{statuscmd}' WHERE id = {vms[i][0]}")
                cursor.execute(f"UPDATE vms SET startcmd = '{startcmd}', stopcmd = '{stopcmd}', statuscmd = '{statuscmd}' WHERE id = {vms[i][0]}")
            return vms[i][0]
    cursor.execute(f"INSERT INTO vms (dnsname, startcmd, stopcmd, statuscmd) VALUES ('{dnsname}','{startcmd}','{stopcmd}','{statuscmd}');" )
    cursor.execute(f"SELECT id, dnsname FROM vms where (dnsname = '{dnsname}');" )
    newvm=cursor.fetchone()
    return newvm[0]

# function to insert App entries
def insertapp(apps,cursor,start,stop):
    for theKey in start.keys():
        match=False
        print(theKey)
        startorder=' '.join(start[theKey]).strip()
        stoporder=' '.join(stop[theKey]).strip()
        print (f'{startorder}  {stoporder}')
        print(re.split(' +',startorder))
        print(re.split(' +',stoporder))
        for i in range(len(apps)):
            if f'{apps[i][1]}@{apps[i][2]}'==theKey :
                match=True
                print('NAME')
                if apps[i][3] != startorder or apps[i][4] != stoporder:
                    print('NO MATCH')
                    print(f"UPDATE apps SET startorder = '{startorder}', stoporder = '{stoporder}' WHERE id = {apps[i][0]}")
                    cursor.execute(f"UPDATE apps SET startorder = '{startorder}', stoporder = '{stoporder}' WHERE id = {apps[i][0]}")
                break
        if not match:
            uniqname=theKey.split('@')
            print(f"INSERT INTO apps (appname, environment, startorder, stoporder) VALUES ('{uniqname[0]}','{uniqname[1]}','{startorder}','{stoporder}');" )
            cursor.execute(f"INSERT INTO apps (appname, environment, startorder, stoporder) VALUES ('{uniqname[0]}','{uniqname[1]}','{startorder}','{stoporder}');" )

#==================================================================
#                               MAIN
#==================================================================

db_name='apps'
db_host='ndf-dbtest1.fyre.ibm.com'
db_user='admin'
db_pass='adm1nPa55'
db_port=5432
conn = psycopg2.connect(database=db_name,
                        host=db_host,
                        user=db_user,
                        password=db_pass,
                        port=db_port)

cursor = conn.cursor()
cursor.execute("SELECT * FROM apps")
apps=cursor.fetchall()
cursor.execute("SELECT * FROM vms")
vms=cursor.fetchall()

start={}
stop={}
with open('dbinput.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(f'row {row}')
        id=insertvm(vms,cursor,row['dnsname'],row['start cmd'],row['stop cmd'],row['status cmd'])
        print(f'ID: {id}')
        build_list(start,row['start order'],id,row['application'],row['environment'])
        build_list(stop,row['stop order'],id,row['application'],row['environment'])
    print(f'start {start}')
    print(f'stop {stop}')

print(vms)

insertapp(apps,cursor,start,stop)



conn.commit() 
conn.close()
