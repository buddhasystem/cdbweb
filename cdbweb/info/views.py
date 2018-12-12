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

PAGECHOICES = [('25','25'), ('50','50'), ('100','100'), ('200','200'), ('400','400'),]

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
    gtid	= request.GET.get('gtid','')
    pk		= request.GET.get('id','')

    if request.method == 'POST':
        q = ''
        
        idSelector	= oneFieldGeneric(request.POST, label="ID", field="id", init=pk)
        if idSelector.is_valid(): pk=idSelector.getval("id")
        if(pk!=''): q+= 'id='+pk+'&'
        
        gtidSelector	= oneFieldGeneric(request.POST, label="Global Tag ID", field="gtid", init=gtid)
        if gtidSelector.is_valid(): gtid=gtidSelector.getval("gtid")
        if(gtid!=''): q+= 'gtid='+gtid+'&'
        
        perPageSelector	= dropDownGeneric(request.POST,
                                          initial={'perpage':perpage},
                                          label='# per page',
                                          choices = PAGECHOICES, tag='perpage')
        if perPageSelector.is_valid(): q += perPageSelector.handleDropSelector()
        
        # We have built a query and will come to same page/view with a GET query
        return makeQuery(what, q)
    
    ##################################################################
    # The request was GET - populate the selectors
    
    selectors = []

    idSelector = oneFieldGeneric(label="ID", field="id", init=pk)
    selectors.append(idSelector)
        
    if(what=='GlobalTagPayload'):
        gtidSelector = oneFieldGeneric(label="Global Tag ID", field="gtid", init=gtid)
        selectors.append(gtidSelector)
    
    perPageSelector = dropDownGeneric(initial	= {'perpage':perpage},
                                      label	= 'items per page',
                                      choices	= PAGECHOICES,
                                      tag	= 'perpage')
    selectors.append(perPageSelector)

    objects = None

    if(pk!=''):
        objects = eval(what).objects.filter(pk=pk)
    else:
        if(gtid!=''):
            objects = eval(what).objects.filter(global_tag_id=gtid).order_by('-pk') # newest on top
        else:
            objects = eval(what).objects.order_by('-pk') # newest on top

    if objects is not None:
        Nfound = len(objects)
    else:
        Nfound=0

    template = 'cdbweb_general_table.html'

    host	= request.GET.get('host','')
    domain	= request.get_host()

    navTable = TopTable(domain, what)
    table = eval(what+'Table')(objects)
    
    RequestConfig(request, paginate={'per_page': int(perpage)}).configure(table)
    #    table.set_site
    selwidth=10*(len(selectors)+1)
    print(selwidth)
    d = dict(domain=domain,
             host=host,
             what=what+': '+str(Nfound)+' items found',
             hometable=navTable,
             table=table,
             selectors=selectors,
             selwidth=selwidth,
    )

    return render(request, template, d)

