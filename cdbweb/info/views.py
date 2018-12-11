# core django
from django.shortcuts	import render
from django.http	import HttpResponse

# tables
import	django_tables2	as tables
from	django_tables2	import RequestConfig

# local utility classes
from utils.navbar	import TopTable

# data
from .models import *

#########################################################
class AppMessageTable(tables.Table):
    class Meta:
        attrs	= {'class': 'paleblue'}
        model = AppMessage
#########################################################
class Basf2ModuleTable(tables.Table):
    class Meta:
        attrs	= {'class': 'paleblue'}
        model = Basf2Module
#########################################################
class GlobalTagTable(tables.Table):
    class Meta:
        attrs	= {'class': 'paleblue'}
        model = GlobalTag
#########################################################
class GlobalTagPayloadTable(tables.Table):
    class Meta:
        attrs	= {'class': 'paleblue'}
        model = GlobalTagPayload
#########################################################
class GlobalTagStatusTable(tables.Table):
    class Meta:
        attrs	= {'class': 'paleblue'}
        model = GlobalTagStatus
#########################################################
class GlobalTagTypeTable(tables.Table):
    class Meta:
        attrs	= {'class': 'paleblue'}
        model = GlobalTagType
#########################################################
class PayloadTable(tables.Table):
    class Meta:
        attrs	= {'class': 'paleblue'}
        model = Payload
#########################################################
class PayloadStatusTable(tables.Table):
    class Meta:
        attrs	= {'class': 'paleblue'}
        model = PayloadStatus
#########################################################
class PayloadContentTable(tables.Table):
    class Meta:
        attrs	= {'class': 'paleblue'}
        model = PayloadContent
#########################################################
class PayloadIovTable(tables.Table):
    class Meta:
        attrs	= {'class': 'paleblue'}
        model = PayloadIov
#########################################################
class PayloadIovRptTable(tables.Table):
    class Meta:
        attrs	= {'class': 'paleblue'}
        model = PayloadIovRpt
        
#########################################################    
#########################################################    
#########################################################    
def index(request):

    template = 'index.html'

    host	= request.GET.get('host','')
    domain	= request.get_host()

    navTable = TopTable(domain)

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

    navTable = TopTable(domain)
    table = eval(what+'Table')(objects)
    RequestConfig(request, paginate={'per_page': 25}).configure(table)
    
    #    table.set_site
    d = dict(domain=domain, host=host, what=what, hometable=navTable, table=table)

    return render(request, template, d)

