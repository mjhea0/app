from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
import requests
import datetime
import logging
import string
import json
import subprocess
import os
import random
import hashlib
import time

logger = logging.getLogger(__name__)

@login_required()
def dashboard(request):
    #socket with urllib2
    user = request.user.username
    import urllib2
    response = urllib2.urlopen('http://python.org/')
    #file open
    f = open('/home/ubuntu/sandbox/splintera-server/requirements.txt')
    f.close()

    test = simple(2,5)

    # get the latest traces from the database for this group
    import MySQLdb as mdb
    db = mdb.connect('dbase.akbars.net','skunkwerk','motherlode721!','splintera_app')
    cur = db.cursor()
    query = "SELECT t3.id, t3.file_name, t3.function_name FROM trace t1 JOIN account_app_key t2 ON (t1.app_key=t2.app_key) JOIN test t3 ON (t3.trace_id=t1.id) WHERE t2.username=%s ORDER BY t1.date DESC LIMIT 5"
    result = cur.execute(query, (user))
    traces = []
    for id, file_name, function_name in cur.fetchall():
        traces.append([id,str(file_name) + '/' + str(function_name)])
    return render_to_response('dashboard.html', {"traces": traces})

def simple(x,y):
    if x<y:
        val = x * x
    elif x>y:
        val = y/2
    return [val]

def get_auth_key(username):
    import MySQLdb as mdb
    db = mdb.connect('dbase.akbars.net','skunkwerk','motherlode721!','splintera_app')
    cur = db.cursor()
    query = "SELECT t2.extra_data FROM auth_user t1 JOIN social_auth_usersocialauth t2 ON (t1.id=t2.user_id) WHERE t1.username=%s"
    cur.execute(query, (username))
    result = cur.fetchone()
    #import ast
    #data = ast.literal_eval(extra_data)
    extra_data = result[0] #access_token = '2d3f3f4720a1bc8e1f03a14f4f388b0b655fb12b' # get their access token from the database
    extra_data = string.split(extra_data,",")[0]
    extra_data = string.split(extra_data,":")[1].strip()
    access_token = extra_data.replace('"','').strip()
    return access_token

def repos(request):#user
    """
    colons indicate a URL parameter that you need to replace with a value
    http://developer.github.com/v3/repos/
    """
    user = request.user.username #user = 'skunkwerk'
    access_token = get_auth_key(user)
    # first get any personal repos
    all_repos = []
    r = requests.get("https://api.github.com/users/" + user + "/repos",auth=(user, access_token))
    if r.status_code==200:
        for repo in r.json():
            all_repos.append({'name':repo['name'],'url':repo['clone_url'],'language':repo['language']})
            # to get all languages:
            #r = requests.get("https://api.github.com/repos/skunkwerk/splintera-web/languages",auth=('skunkwerk', '2d3f3f4720a1bc8e1f03a14f4f388b0b655fb12b'))
    # now get any repos of organizations the user is a member of
    r = requests.get("https://api.github.com/users/" + user + "/orgs", auth=(user, access_token))
    if r.status_code==200:
        for org in r.json():
            url = org['repos_url']
            org_r = requests.get(url, auth=(user, access_token))
            if org_r.status_code==200:
                for repo in org_r.json():
                    all_repos.append({'name':repo['name'],'url':repo['clone_url'],'language':repo['language']})
    return HttpResponse(json.dumps(all_repos), content_type="application/json")

def clone_repo(request):
    """
    besides downloading a copy of the repository
    we also generate a unique ID for the (account & repository)
    that will be used to identify traces
    """
    url = request.GET.get('url')
    repo_name = request.GET.get('name')
    user = request.user.username
    access_token = get_auth_key(user)
    trimmed_url = string.split(url,"github.com")[1]
    repo = "https://" + user + ":" + access_token + "@github.com" + trimmed_url
    # cd to /mnt/storage/customer/code
    folder = "/mnt/storage/customer/code/" + user + "/" + repo_name
    proc = subprocess.Popen(["git","clone",repo,folder,"--progress"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = proc.communicate(None) # will wait for the process to finish
    # search for '100%' in errors to make sure it completed
    # if not, log the error
    
    # store which repo they've selected to test
    import MySQLdb as mdb
    SALT = 'BLHUepKp6LlqGkcU3DA3SizBYZnFTlBX'
    input_seed = user + str(time.time()) + str(get_client_ip(request)) + repo_name + str(random.SystemRandom().random())
    unique_key = hashlib.sha256(input_seed + SALT).hexdigest()
    db = mdb.connect('dbase.akbars.net','skunkwerk','motherlode721!','splintera_app')
    cur = db.cursor()
    query = "INSERT INTO account_app_key(username,app_key) VALUES(%s,%s)"
    result = cur.execute(query, (user,unique_key))

    # create a new virtualenv
    venv_folder = user + "/" + repo_name
    proc = subprocess.Popen("source /usr/local/bin/virtualenvwrapper.sh && mkvirtualenv -i mock " + venv_folder, executable='bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, errors = proc.communicate(None) # will wait for the process to finish

    # if they have a requirements.txt file in the repo, use it to download their dependencies
    r = requests.get("https://api.github.com/repos/" + user + "/" + repo_name + "/git/trees/master?recursive=1", auth=(user, access_token))
    results = r.json()
    files = []
    for result in results['tree']:
        if result['type']=='blob':
            files.append([result['path'].split("/")[-1],result['path']])
    path_to_requirements = None
    for pair in files:
        if pair[0]=='requirements.txt':
            path_to_requirements = pair[1]
            break
    if path_to_requirements is not None:
        local_path_to_requirements_file = "/mnt/storage/customer/code/" + user + "/" + repo_name + "/" + path_to_requirements
        proc = subprocess.Popen("source /usr/local/bin/virtualenvwrapper.sh && workon " + user + "/" + repo_name + " && pip install -r" + local_path_to_requirements_file, executable='bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, errors = proc.communicate(None) # will wait for the process to finish

    # if they have a settings.py file in the repo, use it to set the correct Python paths
    results = r.json()
    files = []
    for result in results['tree']:
        if result['type']=='blob':
            files.append([result['path'].split("/")[-1],result['path']])
    path_to_settings = None
    for pair in files:
        if pair[0]=='settings.py':
            path_to_settings = pair[1]
            break
    venv_folder = "/mnt/storage/customer/environments/" + user + "/" + repo_name
    if path_to_settings is not None:
        local_path_to_settings_file = "/mnt/storage/customer/code/" + user + "/" + repo_name + "/" + path_to_settings
        python_path = "export PYTHONPATH=" + folder
        proc = subprocess.Popen("echo \"" + python_path + "\" >> " + venv_folder + "/bin/postactivate", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, errors = proc.communicate(None) # will wait for the process to finish
        # figure out relative path from repo_name folder to the settings file
        from os.path import relpath
        relative = relpath(local_path_to_settings_file,folder)
        relative_stripped = relative.strip(".py")
        django_settings_path = relative_stripped.replace("/",".")
        django_settings = "export DJANGO_SETTINGS_MODULE='" + django_settings_path + "'"
        proc = subprocess.Popen("echo \"" + django_settings + "\" >> " + venv_folder + "/bin/postactivate", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, errors = proc.communicate(None) # will wait for the process to finish

    if path_to_requirements is not None and path_to_settings is not None:
        # store this path in the database for the repo
        query = "INSERT INTO repository(app_key,url,dependencies_file,settings_file) VALUES(%s,%s,%s,%s)"
        result = cur.execute(query, (unique_key,url,path_to_requirements,path_to_settings))
    elif path_to_requirements is not None:
        query = "INSERT INTO repository(app_key,url,dependencies_file) VALUES(%s,%s,%s)"
        result = cur.execute(query, (unique_key,url,path_to_requirements))
    elif path_to_settings is not None:
        query = "INSERT INTO repository(app_key,url,settings_file) VALUES(%s,%s,%s)"
        result = cur.execute(query, (unique_key,url,path_to_settings))
    else:
        query = "INSERT INTO repository(app_key,url) VALUES(%s,%s)"
        result = cur.execute(query, (unique_key,url))
    db.commit() # for InnoDB tables
    return HttpResponse(json.dumps([output,errors]), content_type="application/json")

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def attach(branch, trunk):
    '''
    Insert a branch of directories on its trunk.
    '''
    parts = branch.split('/', 1)
    if len(parts) == 1:  # no more folders
        trunk.append({parts[0]:[]})
    else:
        node, others = parts
        index = None
        #find the index of the node
        for idx,val in enumerate(trunk):
            if node in val.keys():
                index = idx
                break
        if index==None:
            trunk.append({node:[]})
            index = len(trunk)
        attach(others, trunk[index][node])

def code_tree(request):
    """
    """
    user = request.user.username
    access_token = get_auth_key(user)
    repo_name = request.GET.get('repo')
    folders = []
    r = requests.get("https://api.github.com/repos/" + user + "/" + repo_name + "/git/trees/master?recursive=1", auth=(user, access_token))
    results = r.json()
    for result in results['tree']:
        if result['type']=='tree':
            folders.append(result['path'])

    main_dict = {'root':[{'/':[]}]}
    for folder in folders:
        attach(folder, main_dict['root'])
    print main_dict

    # convert to HTML
    folders.insert(0,'/')
    html = "<ul id='tree_list' class='collapsibleList'>"
    html, counter = print_tree(html,main_dict['root'],folders,0)
    html += "</ul>"
    return HttpResponse(json.dumps(html), content_type="application/json")

def store_test_in_folder(request):
    """
    """
    user = request.user.username
    folder = request.GET.get('folder')
    url = request.GET.get('url')
    import MySQLdb as mdb
    db = mdb.connect('dbase.akbars.net','skunkwerk','motherlode721!','splintera_app')
    cur = db.cursor()
    query = "UPDATE repository SET folder_to_store_tests_in=%s WHERE username=%s AND url =%s"
    result = cur.execute(query, (folder,user,url))
    return HttpResponse(json.dumps(result), content_type="application/json")

def print_tree(html,node,folders,counter):
    for item in node:
        for key,value in item.items():
            html += "<li><span class='tree-button'></span> <a href='#' class='tree' path='" + folders[counter] + "'>" + key + "</a>"
            counter += 1
            if len(value)>0:
                new_html, counter = print_tree("",value,folders,counter)
                html += "<ul>" + new_html + "</ul>"
            html += "</li>"
    return [html, counter]

def commit_test_to_repo(request):
    """
    """
    url = request.GET.get('url')
    message = request.GET.get('message')
    user = request.user.username
    access_token = get_auth_key(user)
    trimmed_url = string.split(url,"github.com")[1]
    repo = "https://" + user + ":" + access_token + "@github.com" + trimmed_url
    # cd to /mnt/storage/customer/code
    file_name = "/mnt/storage/customer/code/" + name + 'test.py'
    #TODO: use the github api to commit via PUSH
    proc = subprocess.Popen(["git","add",file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = proc.communicate(None) # will wait for the process to finish
    proc = subprocess.Popen(["git","commit","-m '" + message + "'"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = proc.communicate(None) # will wait for the process to finish
    proc = subprocess.Popen(["git","push","origin"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = proc.communicate(None) # will wait for the process to finish
    #TODO: store this event in the database
    result = output
    return HttpResponse(json.dumps(result), content_type="application/json")

@login_required()
def code(request, test_id):
    # get the code to display for the trace
    import MySQLdb as mdb
    db = mdb.connect('dbase.akbars.net','skunkwerk','motherlode721!','splintera_app')
    cur = db.cursor()
    query = "SELECT code, lines_executed, input_parameters, return_value, test_code FROM test WHERE id=%s"
    result = cur.execute(query, (test_id))
    traces = []
    row = cur.fetchone()
    code_object = row[0].decode('string_escape')
    code_tuple = eval(code_object)
    start_line_number = code_tuple[1]
    lines = eval(row[1])
    input_parameters = row[2]
    return_value = row[3]
    lines_executed = map(lambda line: int(line) - int(start_line_number), lines)
    code_list = code_tuple[0]
    code_lines = map(lambda line: line.rstrip(), code_list)
    test_code = row[4].lstrip('\"').rstrip('\"').decode('string_escape')
    #test_code = string.split(test_code,"\n")

    # get the input parameters
    # get the return value
    # get the lines executed
    # get the unit test code
    return render_to_response('code.html', {"code": code_lines, "lines_executed": lines_executed, "input_parameters": input_parameters, "return_value": return_value, "test_code": test_code })
#return HttpResponse(simplejson.dumps(response_data), content_type="application/json")