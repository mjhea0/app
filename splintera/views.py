from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
import datetime
import logging
import string

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