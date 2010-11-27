# Create your views here.
from django.http import HttpResponse
import subprocess
import sys
import re
sys.path.append('/home/Educator/rrdtool-trunk/bindings/python/build/lib.cygwin-1.7.5-i686-2.5')
import rrdtool

def getDifference(open_list, closed_list):
    '''Computes the difference between the largest open value and the smallest closed value in one bucket.
    
    open_list and closed_list should each be a list of tuples, each tuple representing the values in a bucket.  This will return a list of differences.'''
    try:
        maximums = [max([y for y in x if y != None]) for x in open_list]
        minimums = [min([y for y in x if y != None]) for x in closed_list]
    except ValueError:
        maximums = [0 for x in open_list];
        minimums = [0 for x in closed_list];
    return [maxi - mini for (maxi, mini) in zip(maximums, minimums)]

def split(vals, names, reg_expr, indicator):
    '''Splits the two lists by the indicator group of the regular expression applied to the name list.'''
    trim = len(indicator)
    new_names, new_vals = zip(*[(n[:n.find(indicator)] + n[n.find(indicator)+trim:], v) for (n,v) in zip(names,vals) if reg_expr.match(n)])
    return [list(new_vals), list(new_names)]

def createHTML(graph_1, graph_2, min_time=0, max_time=0, resolution=1):
    '''Creates a string that can be used to make a html webpage of a bar graph.'''

    '''Uses Protovis and Javascript.  Currently doesn't work in IE'''
    maximum = max(graph_1[0] + graph_2[0])
    label_str = '' #'.anchor("top").add(pv.Label).text(function(d) d)'
    name_str = '.visible(function(d) d%5 == 0)'
    try:
        height = 136 / maximum
    except ZeroDivisionError:
        height = 136
        label_str = ''
    interval = int(maximum) / 5
    interval -= interval % 100

    input_str = """<html>
<head>
	<title>RRD Histogram</title>
	<script src="static/protovis-r3.1.js" type="text/javascript"></script>
</head>
<body>
<p>
Histogram of accelerated and unaccelerated data between time """ + str(min_time) + """ and time """ + str(max_time) + """.
</p>
<script type="text/javascript+protovis">

var numbers_1 = """ + str(graph_1[0]) + """;

var data_names_1 = """ + str(graph_1[1]) + """;

var numbers_2 = """ + str(graph_2[0]) + """;

var data_names_2 = """ + str(graph_2[1]) + """;

var barWidth = 8;

var barSpacing = 0;

var panelWidth = barWidth*numbers_1.length;
var panelHeight = 150;

new pv.Panel().width(panelWidth).height(panelHeight)
        .bottom(20).left(30)
    .root.add(pv.Bar)
        .data(numbers_1)
        .height(function(d) d * """ + str(height) + """).width(barWidth-barSpacing)
        .bottom(0).left(function() this.index * barWidth)
        """ + label_str + """
    .root.add(pv.Rule)
        .data(function() pv.range(0, """ + str(maximum) + """, """ + str(interval) + """))
        .bottom(function(d) d * """ + str(height) + """)
        .strokeStyle(function(i) i ? "rgba(255, 255, 255, .7)" : "black")
        .anchor("left").add(pv.Label)
        .textMargin(5)
    .root.anchor("top").add(pv.Label)
        .textAlign("center")
        .text("Accelerated")
    .root.anchor("bottom").add(pv.Label)
        .data(data_names_1)
        .left(function() this.index * barWidth + barWidth/2 - 1)
        """ + name_str + """
        .textBaseline("top")
        .textMargin(5)
        .text(function(d) d)
    .root.render();

new pv.Panel().width(panelWidth).height(panelHeight)
        .bottom(20).left(30)
    .root.add(pv.Bar)
        .data(numbers_2)
        .height(function(d) d * """ + str(height) + """).width(barWidth-barSpacing)
        .bottom(0).left(function() this.index * barWidth - 1)
        """ + label_str + """
    .root.add(pv.Rule)
        .data(function() pv.range(0, """ + str(maximum) + """, """ + str(interval) + """))
        .bottom(function(d) d * """ + str(height) + """)
        .strokeStyle(function(i) i ? "rgba(255, 255, 255, .7)" : "black")
        .anchor("left").add(pv.Label)
        .textMargin(5)
    .root.anchor("top").add(pv.Label)
        .textAlign("center")
        .text("Unaccelerated")
    .root.anchor("bottom").add(pv.Label)
        .data(data_names_2)
        .left(function() this.index * barWidth + barWidth/2 - 1)
        """ + name_str + """
        .textBaseline("top")
        .textMargin(5)
        .text(function(d) d)
    .root.render();
</script>

</body>
</html>"""
    return input_str

def index(request):
    '''Takes a webpage request and uses it to grab information from rrdtool and diplay a bar graph.'''
    input_dict = request.GET #example url:  http://127.0.0.1:8000/rrd/?start=1000000000&length=12&file=count_per_rtt.rrd
    start = int(input_dict['start'])
    length = int(input_dict['length'])
    file = input_dict['file']

    # Get the values from the rrd file
    val_open = rrdtool.fetch(str(file), 'MAX', '--single', str(start+length), '--backwards', '--stop', str(start))
    times_open = zip(*val_open[2])
    
    val_closed = rrdtool.fetch(str(file), 'MIN', '--single', str(start), '--stop', str(val_open[0][1]))
    times_closed = zip(*val_closed[2])

    # Looks for NaNs.  Should only find NaNs if there is no data between the two times.
    if len([x for x in times_open if x[0] == None]) > 0:
        return HttpResponse('There is no data between those two times', mimetype='text/plain')
    if len([x for x in times_closed if x[0] == None]) > 0:
        return HttpResponse('There is no data between those times', mimetype='text/plain')

    rrd_names = list(val_open[1])
 
    # Rather touchy about the format of the names
    open_list = split(times_open[:], rrd_names[:], re.compile(r'^\w*\_arrive\_\d*$'), 'arrive_')
    closed_list = split(times_closed[:], rrd_names[:], re.compile(r'^\w*\_depart\_\d*$'), 'depart_')

    max_time = val_open[0][1]
    min_time = val_closed[0][0]
    resolution = val_closed[0][2]

    diff = getDifference(open_list[0], closed_list[0])
    # double checks to make sure that the names match; if they don't, that implies a problem.
    if str(open_list[1]) != str(closed_list[1]): print 'ERROR!!!' + str(open_list[1]) + '\n' + str(closed_list[1])
    rrd_names = open_list[1] # could be closed_list, but since they should match, it doesn't matter.

    # Rather touchy about the format of the names
    accel = split(diff[:], rrd_names[:], re.compile(r'^accel\_\d*$'), 'accel_')
    unaccel = split(diff[:], rrd_names[:], re.compile(r'^unaccel\_\d*$'), 'unaccel_')
    
    file_str = createHTML(accel, unaccel, min_time, max_time, resolution)
    return HttpResponse(file_str, mimetype='text/html')
