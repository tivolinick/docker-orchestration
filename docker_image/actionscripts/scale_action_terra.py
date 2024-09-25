from git import *
import os
import requests
import json
import shutil
import sys


def create_pull_request(user,bb_pass,git_base_url,project, repo_name, title, description, head_branch, base_branch, git_token):
    user=user or 'x-token-auth'

    # bitbucket = Bitbucket(
    #     url=f'https://{git_base_url}',
    #     username=user,
    #     password=bb_pass
    # )

    # bitbucket.open_pull_request(project, repo_name, project, repo_name, head_branch, base_branch, title, description)

    """Creates the pull request for the head_branch against the base_branch"""
    # git_pulls_api = f"https://{git_base_url}/repos/{project}/{repo_name}/pullrequests"
    git_pulls_api = f"https://api.bitbucket.org/2.0/repositories/{project}/{repo_name}/pullrequests"
    print(f'API: {git_pulls_api}')
    headers = {
        "Authorization": f"Bearer {git_token}",
        "Content-Type": "application/json"}

    payload = {
        "title": "My Title",
        "source": {
            "branch": {
                "name": head_branch
            }
        }
    }
    
    r = requests.post(
        git_pulls_api,
        headers=headers,
        data=json.dumps(payload))

    if not r.ok:
        print(f"Request Failed: {r.text}, {r.status_code}")
    else:
        pull=json.loads(r.text)
        # print(pull)
        print(pull['links']['self']['href'])
        return pull['links']['self']['href']


def merge_pull_request(pull_url, title, message, git_token):
    """Creates the pull request for the head_branch against the base_branch"""
    git_merge_api = f"{pull_url}/merge"
    print (git_merge_api)
    headers = {
        "Authorization": f"Bearer {git_token}",
        "Content-Type": "application/json"}

    payload = {
        "commit_title": title,
        "commit_message": message
    }
    
    r = requests.put(
        git_merge_api,
        headers=headers,
        data=json.dumps(payload))

    if not r.ok:
        print(f"Request Failed: {r.text}, {r.status_code}")


def delete_branch(git_base_url,name,project,repo_name,git_token):
    ref_api = f"{git_base_url}/repos/{project}/{repo_name}/git/refs/heads/{name}"
    git_branch_api = f"{git_base_url}/repos/{project}/{repo_name}/branches/{name}"
    headers = {
        "Authorization": f"Bearer {git_token}",
        "Content-Type": "application/json"}

    r = requests.get(
        git_branch_api,
        headers=headers
        )

    if not r.ok:
        print(f"Request Failed: {r.text}, {r.status_code}")
    else:
        info=json.loads(r.text)
        print(info)
    
    r = requests.delete(
        ref_api,
        headers=headers
        )
    print(r.status_code)


def clone_and_branch(user,token,project,repo_name,branch,base):
    # https://nickfreer1@bitbucket.org/tivolinick/terrademo.git
    user=user or 'x-token-auth'
    url=f'https://{user}:{token}@{base}/{project}/{repo_name}.git'

    repo_dir=f'./{repo_name}'
    dirs=next(os.walk('.'))[1]
    print(dirs)
    if repo_name in dirs:
        print('repo dir exists, deleting it')
        shutil.rmtree(repo_name)
        
    print ('hi')
    Repo.clone_from(url, repo_dir)
    cloned_repo=Repo(repo_dir)
    new_branch = cloned_repo.create_head(branch)  # Create a new branch ...
    new_branch.checkout()
    return(cloned_repo)


def commit_changes(cloned_repo,branch,message):
    cloned_repo.git.config('--global','user.email','turbo@uk.ibm.com')
    cloned_repo.git.config('--global','user.name','turbo')
    cloned_repo.git.add(A=True)
    cloned_repo.git.commit(m=message)
    cloned_repo.git.push('--set-upstream', 'origin', branch)

import re

def update_instance_type(file_path, vm_name, new_instance_type):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    in_a_block = 0
    vm_block_found = False
    type_found = False
    instance_type_updated = False

    for i, line in enumerate(lines):
        print(line)
        if re.search(r'{', line):
            in_a_block+=1
            print(f'BLOCK: {in_a_block}')
        if re.search(r'}', line):
            in_a_block-=1
            print(f'BLOCK: {in_a_block}')
            if in_a_block <= 1:
                type_found = False
                if vm_block_found:
                    break
        
        # Find the resource block for the specified VM
        if re.search(rf'\s*name\s*=\s*"{vm_name}"', line):
            name_ref = i
            indent=line.index('name')
            print(f'indent: {indent}')
            print("Found it")
            vm_block_found = True
            if type_found:
                lines[type_ref] = re.sub(r'".*"', f'"{new_instance_type}"', line)
                instance_type_updated = True
                break

        # If inside the VM block, find and update the instance type
        if re.match(r'\s*instance_type\s*=\s*".*"', line):
            if vm_block_found:
                lines[i] = re.sub(r'".*"', f'"{new_instance_type}"', line)
                instance_type_updated = True
                break
            else:
                type_found = True
                type_ref = i

    if not vm_block_found:
        print(f'VM resource "{vm_name}" not found in the file.')
        return

    if not instance_type_updated:
        print(f'Instance type not found VM "{vm_name}". Adding new line')
        newline=''
        for i in range(0,indent):
            newline += ' '
        newline += f'instance_type    = "{new_instance_type}"\n'
        print (f'NEW: {newline}')
        lines.insert(name_ref+1,newline)
        # return

    with open(f'{file_path}', 'w') as file:
        file.writelines(lines)

    print(f'Instance type for VM "{vm_name}" updated to "{new_instance_type}".')

    # read the environment vars from files created by secrets and config maps
def read_envs(dir_name, envs_obj):
    for filename in os.listdir(dir_name):
        if 'key' not in filename and '..' not in filename:
            f = open(f'{dir_name}/{filename}', 'r')
            envs_obj[filename] = f.readline().splitlines()[0]

# ======================================== Main ======================================== 

print ('reading configmaps and secrets')
envs = {}
for dir in ['//gitcreds', '//actionscriptrefs', '//sshkeys']:
    read_envs(dir, envs)
# print(envs)

token=envs['gittoken']
project=envs['gitproject']
branch_name=f'turbo-{action}'
repo_name=env['gitrepo']'terrademo'
user=''
base=envs['gitbaseurl']

print ('reading action data')
action_data = json.loads(sys.stdin.read())
server = action_data['actionItem'][0]['targetSE']['displayName']
old_instance_type=action_data['actionItem'][0]['currentSE']['displayName']
new_instance_type=action_data['actionItem'][0]['newSE']['displayName']
action=action_data['actionItem'][0]['uuid']
print (f'Action: {action} on {server} from {old_instance_type} to {new_instance_type}')

print('Cloning Repo....')
cloned_repo=clone_and_branch(user,token,project,repo_name,branch_name,base)

print("Making file...")
# f = open(f'{repo_name}/ndftest','w')
# f.write('Well Hello there!')
# f.close

print ('updating instance type')
terraform_file_path = f'{repo_name}/clients/psfe/locals_psfe.tf'
# vm_resource_name = 'compendium_client01'
# new_instance_type = 'zzzzzz'
update_instance_type(terraform_file_path, server, new_instance_type)

print('Commit and push branch')
message=f'Turbo updated {server} instance type from {old_instance_type} to {new_instance_type}'
commit_changes(cloned_repo,branch_name,message)

pull_url = create_pull_request(
    '',
    token,
    base, # base url - need https in front of it
    project, # project_name
    repo_name, # repo_name
    f'Turbo Resize for {server}', # title
    message, # description
    branch_name, # head_branch
    "main", # base_branch
    token, # git_token
)


print ('Done')