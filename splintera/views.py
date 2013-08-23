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
    import urllib2
    response = urllib2.urlopen('http://python.org/')
    #file open
    f = open('/home/imran/Code/cs.php')
    f.close()

    test = simple(2,5)

    # get the latest traces from the database for this group
    group_id = 1
    import MySQLdb as mdb
    db = mdb.connect('dbase.akbars.net','skunkwerk','motherlode721!','splintera_app')
    cur = db.cursor()
    query = "SELECT t2.id, t2.file_name, t2.function_name FROM trace t1 JOIN test t2 ON (t2.trace_id=t1.id) WHERE t1.group_id=%s ORDER BY t1.date DESC LIMIT 5"
    result = cur.execute(query, (group_id))
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
    name = request.GET.get('name')
    user = request.user.username
    access_token = get_auth_key(user)
    trimmed_url = string.split(url,"github.com")[1]
    repo = "https://" + user + ":" + access_token + "@github.com" + trimmed_url
    # cd to /mnt/code_storage
    folder = "/home/imran/Code/code_storage/" + name
    proc = subprocess.Popen(["git","clone",repo,folder,"--progress"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = proc.communicate(None) # will wait for the process to finish
    # search for '100%' in errors to make sure it completed
    # if not, log the error
    # store which repo they've selected to test
    import MySQLdb as mdb
    SALT = 'BLHUepKp6LlqGkcU3DA3SizBYZnFTlBX'
    input_seed = user + str(time.time()) + str(get_client_ip(request)) + name + str(random.SystemRandom().random())
    unique_key = hashlib.sha256(input_seed + SALT).hexdigest()
    db = mdb.connect('dbase.akbars.net','skunkwerk','motherlode721!','splintera_app')
    cur = db.cursor()
    query = "INSERT INTO account_app_key(username,app_key) VALUES(%s,%s)"
    result = cur.execute(query, (user,unique_key))
    query = "INSERT INTO repository(app_key,url) VALUES(%s,%s)"
    result = cur.execute(query, (unique_key,url))
    db.commit() # for InnoDB tables
    return HttpResponse(json.dumps(result), content_type="application/json")

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
    # cd to /mnt/code_storage
    file_name = "/mnt/code_storage/" + name + 'test.py'
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