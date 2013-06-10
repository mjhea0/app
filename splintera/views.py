from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
import datetime
import logging

logger = logging.getLogger(__name__)

def busy():
    print 'called busy'
    import random
    f = open('test_data.txt','a')# open file and append
    f.write(str(random.random()) + '\n')
    f.close()

@login_required()
def homepage(request):
    i = 0
    while(i<10):
        busy()
        i+=1
    return render_to_response('index.html', {"foo": "bar"})

def one(request):
    # sql query - insert
    import MySQLdb as mdb
    db = mdb.connect('mysql.akbars.net','skunkwerk','motherlode721!','backhaul')
    cur = db.cursor()
    cur.execute("INSERT INTO splintera(email) VALUES ('test@nothing.com');")
    cur.execute("INSERT INTO splintera(email) VALUES ('test@nothing.com');")
    cur.execute("INSERT INTO splintera(email) VALUES ('test@nothing.com');")
    cur.execute("INSERT INTO splintera(email) VALUES ('test@nothing.com');")
    cur.execute("INSERT INTO splintera(email) VALUES ('test@nothing.com');")
    return render_to_response('index.html', {"foo": "bar"})

def two(request):
    # computationally intensive
    import gzip
    f_in = open('book.pdf')
    f_out = gzip.open('compressed.gz', 'wb')
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()
    return render_to_response('index.html', {"foo": "bar"})

def three(request):
    # s3 get
    from boto.s3.connection import S3Connection
    con = S3Connection('AKIAISIDHI6SG5JKS2ZA','aJPmtc1MGmfewCih8T98ttlWP7GsrENciyzHgw87')
    b = con.get_bucket('splintera') # substitute your bucket name here
    from boto.s3.key import Key
    k = Key(b)
    k.key = 'ajax.php'
    data = k.get_contents_as_string()
    return render_to_response('index.html', {"foo": "bar"})

def four(request):
    # sql query - select
    import MySQLdb as mdb
    db = mdb.connect('mysql.akbars.net','skunkwerk','motherlode721!','backhaul')
    cur = db.cursor()
    cur.execute("SELECT * FROM splintera;")
    row = cur.fetchone() # database query
    return render_to_response('index.html', {"foo": "bar"})

@login_required()
def api(request):
    response_data['nodes'] = []
    response_data['nodes'].append({ "x": 60, "y": 30, "group":1, "size":8, "children": [1,2,3], "name":"Databases", "status":"closed" })
    response_data['nodes'].append({ "x": 70, "y": 60, "group":2, "size":8, "children": [1,2,3,4,5], "name":"Memcached", "status":"closed" })
    response_data['nodes'].append({ "x": 30, "y": 45, "group":4, "size":6, "name":"S3" })
    response_data['nodes'].append({ "x": 40, "y": 72, "group":4, "size":6, "name":"CDN" })
    response_data['nodes'].append({ "x": 70, "y": 37, "group":2, "size":6, "name":"Solr" })
    response_data['nodes'].append({ "x": 35, "y": 59, "group":4, "size":6, "name":"Payments" })
    response_data['nodes'].append({ "x": 45, "y": 32, "group":4, "size":6, "name":"Mailchimp" })
    response_data['nodes'].append({ "x":50, "y": 50, "group":6, "size":10, "name":"Internet" })
    response_data['links'] = []
    response_data['links'].append([{"node":7},{"node":0},{"node":0}])
    response_data['links'].append([{"node":7},{"node":1},{"node":1}])       ,
    response_data['links'].append([{"node":7},{"node":2},{"node":2}])
    response_data['links'].append([{"node":7},{"node":3},{"node":3}])
    response_data['links'].append([{"node":7},{"node":4},{"node":4}])
    response_data['links'].append([{"node":7},{"node":5},{"node":5}])
    response_data['links'].append([{"node":7},{"node":6},{"node":6}])
    return HttpResponse(simplejson.dumps(response_data), content_type="application/json")