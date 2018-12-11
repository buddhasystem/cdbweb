# core django
from django.shortcuts	import render
from django.http	import HttpResponse

# tables
from	django_tables2	import RequestConfig

# local utility classes
from utils.navbar	import TopTable

# data
from .models		import *
from .cdbwebTables	import *
#########################################################    
#########################################################    
#########################################################    
def index(request):

    template = 'index.html'

    host	= request.GET.get('host','')
    domain	= request.get_host()

    navTable = TopTable(domain, 'Home')

    d = dict(domain=domain, host=host, what='Home', hometable=navTable)

    return render(request, template, d)

#########################################################

# general request handler for summary type of a table
def data_handler(request, what):
    objects = eval(what).objects.order_by('-pk') # newest on top

    n = len(objects)

    template = 'cdbweb_general_table.html'

    host	= request.GET.get('host','')
    domain	= request.get_host()

    navTable = TopTable(domain, what)
    table = eval(what+'Table')(objects)
    RequestConfig(request, paginate={'per_page': 25}).configure(table)
    
    #    table.set_site
    d = dict(domain=domain, host=host, what=what, hometable=navTable, table=table)

    return render(request, template, d)

