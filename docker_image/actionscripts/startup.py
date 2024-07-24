#!/usr/local/bin/python

# from get_data import getdata
import getdata
import requests
import json

# import psycopg2
import sys

# import os
import socket

'''
===================================================================
                             MAIN
===================================================================
'''
# Read in all the env values from secrets and configmaps
envs = {}
for dir in ['//actionscriptcreds', '//actionscriptrefs', '//externalhosts', '//sshkeys']:
    if socket.gethostname() == 'Nicks-MacBook-Pro.local':
        dir = f'/users/nickfreer{dir}'
    getdata.read_envs(dir, envs)
print(envs)

# Read in the data about the action
action_data = json.loads(sys.stdin.read())
# FOR DEBUG PURPOSES
# stdin_data = sys.stdin.read()
# requests.post('https://eo5tpbp6fxdjwit.m.pipedream.net/', stdin_data)
# action_data = json.loads(stdin_data)
server = action_data['actionItem'][0]['targetSE']['displayName']
print(server)

# open a DB connection and return a cursor
# vm_db - tuple: (id, name, startup cmd, shutdown cmd, status cmd)
vm_db = getdata.DatabaseAppVM(
    envs['db_name'], envs['db_host'], envs['db_port'], envs['db_user'], envs['db_pass']
)

# get the vm info from the DB
host_info = vm_db.execute(f"SELECT * FROM vms WHERE displayname = '{server}'")
if len(host_info) == 0:
    sys.exit(f'ERROR: VM {server} not found in database')
# print(f'HOST_INFO: {host_info}')
vm_id = host_info[0][0]
# get all the apps in the DB
# apps - tuple: (id, app environment, startup order, shutdown order)
apps = vm_db.execute("SELECT * FROM apps")

# map the start and stop dependencies
start_front = {}
start_back = {}
# stop_front = {}
# stop_back = {}

# for app in apps:
#     getdata.mapper(app[4].split(' '), vm_id, start_front, start_back)
# print('RESULTS')
# print('============START=============')
# print(start_front)
# print(start_back)
# print(start_front.keys())
# print(start_back.keys())

# use the maps to work out the start and stop orders
# start_list = []
start_list = []

# return orders
# getdata.order_maps(start_back, start_front, start_list, str(vm_id))
# start_list.reverse()
# print("START")
# print(start_list)

def getDates(datesStr):
    dates = json.loads(
        datesStr.replace("'", '"')
    )  # make sure we dont break when parsing
    return dates

for app in apps:
    dates = getDates(app[3])
    start_list = getdata.mapper_and_ordder(dates, host_info, start_list)
    # start_list.extend(ss)

print("start_list")
print(start_list)


# get vm data from the DB for those in the list
vms = vm_db.execute(f"SELECT * FROM vms WHERE id IN ({','.join(map(str, start_list))})")
del vm_db
if len(vms) != len(start_list):
    print(f'VMS from DB: {vms}')
    sys.exit(f'Not all the VMs were found in database for ids: {start_list}')

# log in to the turbo API
turbo = getdata.TurboApi('10.188.161.53', envs['turbouser'], envs['turbopass'])
# build the payload
ansible_payload = {'inventory': '', 'order': []}
for id in start_list:
    db_data = [host_line for host_line in vms if host_line[0] == id]
    turbo_data = turbo.search_turbo_data(db_data[0][1])
    ansible_payload['order'].append(getdata.build_vm_entry(id, db_data, turbo_data))
    for ip in turbo_data[0]['aspects']['virtualMachineAspect']['ip']:
        ansible_payload['inventory'] += f' {ip}'
ansible_payload['inventory'] = ansible_payload['inventory'].strip()

ansible_api = getdata.AnsibleApi(envs['ansible_host'], envs['ansible_user'], envs['ansible_pass'], 3, 1)
payload = {"extra_vars": json.dumps(ansible_payload)}
print(f'PAYLOAD- {payload}')
job = ansible_api.launch_job(envs['startup'], payload)
status = ansible_api.wait_for_job(job)
print(status)
