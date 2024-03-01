import requests
import socket
import os
import json

def read_envs(dir_name, envs_obj):
    # dir_name = f'//users//nickfreer{dir_name}'
    for filename in os.listdir(dir_name):
        if 'key' not in filename and '..' not in filename:
            f = open(f'{dir_name}/{filename}', 'r')
            envs_obj[filename] = f.readline().splitlines()[0]


def get_job_status(job_id,url):
        url = f'{url}/jobs/{job_id}/job_events/'
        print(url)
        r = requests.get(url, auth=auth, verify=False)
        print(json.loads(r.text)['results'])
        # r_event = json.loads(r.text)['related']['job_events']
        # print(r_event)
        # j = requests.get(f'{url}job_events/',auth=auth, verify=False)
        # return j.text
        


envs={}
for dir in ['//actionscriptcreds', '//actionscriptrefs', '//externalhosts', '//sshkeys']:
    if socket.gethostname() == 'Nicks-MacBook-Pro.local':
        dir = f'/users/nickfreer{dir}'
    read_envs(dir, envs)

url = f'https://{envs['ansible_host']}/api/v2'
auth = (envs['ansible_user'], envs['ansible_pass'])
headers = {"Content-Type": "application/json"}

stat=json.loads(get_job_status(263,url))
print(stat.results)

for theLine in [line['stdout'] for line in stat['results'] if 'STATUS:' in line['stdout']]:
     print(theLine)

    

