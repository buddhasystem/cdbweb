# core django
from django.shortcuts	import render
from django.http	import HttpResponse, HttpResponseRedirect

# tables
from	django_tables2	import RequestConfig

# local utility classes
from utils.navbar	import TopTable

# data
from .models		import *
from .cdbwebTables	import *


from utils.selectorUtils import dropDownGeneric, oneFieldGeneric

#########################################################    

PAGECHOICES	= [('25','25'),		('50','50'),	('100','100'),	('200','200'),	('400','400'),]

#########################################################    
# ---
def makeQuery(page, q=''):
    gUrl= '/info/'+page
    qUrl= '/info/'+page+"?"

    if(q==''): return HttpResponseRedirect(gUrl)
    return HttpResponseRedirect(qUrl+q)



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

    perpage	= request.GET.get('perpage','25')


    if request.method == 'POST':
        q = ''
        gtidSelector	= oneFieldGeneric(request.POST, label="GT ID", field="gtid", init='')
        if gtidSelector.is_valid(): gtid=run1Selector.getval("gtid")
        if(gtid!=''): q+= 'gtid='+gtid+'&'
        
        perPageSelector	= dropDownGeneric(request.POST,
                                          initial={'perpage':perpage},
                                          label='# per page',
                                          choices = PAGECHOICES, tag='perpage')
        if perPageSelector.is_valid(): q += perPageSelector.handleDropSelector()
        return makeQuery(what, q) # We have built a query and will come to same page/view with the query parameters
    
    
    ############################################
    # Populate the selectors
    selectors = []

    perPageSelector = dropDownGeneric(initial={'perpage':perpage}, label='# per page', choices = PAGECHOICES, tag='perpage')
    selectors.append(perPageSelector)
    gtidSelector = oneFieldGeneric(label="GT ID", field="gtid", init='')
    selectors.append(gtidSelector)
    
    objects = eval(what).objects.order_by('-pk') # newest on top

    
    n = len(objects)

    template = 'cdbweb_general_table.html'

    host	= request.GET.get('host','')
    domain	= request.get_host()

    navTable = TopTable(domain, what)
    table = eval(what+'Table')(objects)
    
    RequestConfig(request, paginate={'per_page': int(perpage)}).configure(table)
    #    table.set_site
    
    d = dict(domain=domain, host=host, what=what, hometable=navTable, table=table, selectors=selectors)

    return render(request, template, d)

