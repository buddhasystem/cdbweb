# core django
from django.shortcuts	import render
from django.http	import HttpResponse, HttpResponseRedirect
from django.conf	import settings

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
    gUrl= '/'+page
    qUrl= '/'+page+"?"

    if(q==''): return HttpResponseRedirect(gUrl)
    return HttpResponseRedirect(qUrl+q)



#########################################################    
def index(request):

    template = 'index.html'

    host	= request.GET.get('host','')
    domain	= request.get_host()

    navtable	= TopTable(domain, 'Home')
    banner	= "Welcome to CDBweb! Please make your selection above..."

    d = dict(domain=domain, host=host, what=banner, navtable=navtable)

    return render(request, template, d)


#########################################################
# general request handler for summary type of a table
def data_handler(request, what):
    perpage	= request.GET.get('perpage','25')
    gtid	= request.GET.get('gtid','')	# GT ID
    gtpid	= request.GET.get('gtpid','')	# GT payload ID
    pk		= request.GET.get('id','')

    ##################################################################
    ####################      POST      ##############################
    ##################################################################
    if request.method == 'POST':
        q = ''
        
        idSelector	= oneFieldGeneric(request.POST, label="ID", field="id", init=pk)
        if idSelector.is_valid(): pk=idSelector.getval("id")
        if(pk!=''): q+= 'id='+pk+'&'
        
        gtidSelector	= oneFieldGeneric(request.POST, label="Global Tag ID", field="gtid", init=gtid)
        if gtidSelector.is_valid(): gtid=gtidSelector.getval("gtid")
        if(gtid!=''): q+= 'gtid='+gtid+'&'
        
        gtpidSelector	= oneFieldGeneric(request.POST, label="Global Tag Payload ID", field="gtpid", init=gtpid)
        if gtpidSelector.is_valid(): gtpid=gtpidSelector.getval("gtpid")
        if(gtpid!=''): q+= 'gtpid='+gtpid+'&'
        
        perPageSelector	= dropDownGeneric(request.POST,
                                          initial={'perpage':perpage},
                                          label='# per page',
                                          choices = PAGECHOICES, tag='perpage')
        if perPageSelector.is_valid(): q += perPageSelector.handleDropSelector()
        
        # We have built a query and will come to same page/view with a GET query
        return makeQuery(what, q)
    
    ##################################################################
    ########################    GET    ###############################
    ##################################################################
    # prepare the top nav bar and other attributes no matter what...
    
    host	= request.GET.get('host','')
    domain	= request.get_host()
    settings.domain = domain # replaces  table.set_site below
    navtable = TopTable(domain, what)


    selectors = [] # The request was GET - populate the selectors

    idSelector = oneFieldGeneric(label="ID", field="id", init=pk)
    selectors.append(idSelector)
        
    if(what=='GlobalTagPayload'):
        gtidSelector = oneFieldGeneric(label="Global Tag ID", field="gtid", init=gtid)
        selectors.append(gtidSelector)

    # Keep for later...
    # if(what=='Payload'):
    #     gtpidSelector = oneFieldGeneric(label="Global Tag Payload ID", field="gtpid", init=gtpid)
    #     selectors.append(gtpidSelector)
    
    perPageSelector = dropDownGeneric(initial	= {'perpage':perpage},
                                      label	= 'items per page',
                                      choices	= PAGECHOICES,
                                      tag	= 'perpage')
    selectors.append(perPageSelector)
    selwidth=10*(len(selectors)+1)
    # --- END building selectors

    objects = None

    if(pk!=''): # takes precedence
        aux_tables = []
        theObject  = None

        try:
            theObject = eval(what).objects.get(pk=pk)
        except:
            banner='No '+what+' database entries were found using your selection criteria'
            # *******> TEMPLATE <*******
            template = 'cdbweb_general_table_empty.html'
            d = dict(domain=domain, host=host, what=banner, selectors=selectors, navtable=navtable)
            return render(request, template, d)

            
        table = eval(what+'Table')([theObject,])
        banner=what+' '+str(pk)+' detail'

        if what=='GlobalTag': # list gt payloads
            objects	= GlobalTagPayload.objects.filter(global_tag_id=pk).order_by('-pk') # newest on top
            Nobj	= len(objects)

            aux_title	= 'Found '+str(Nobj)+' "Global Tag Payload" items for the Global Tag '+str(pk)
            aux_table	= GlobalTagPayloadTable(objects)
            RequestConfig(request, paginate={'per_page': int(perpage)}).configure(aux_table)
            
            tableDict	= {'title':aux_title, 'table':aux_table}
            aux_tables.append(tableDict)

        if what=='GlobalTagPayload': # list gt payloadIovs
            objects	= PayloadIov.objects.filter(global_tag_payload_id=pk).order_by('-pk') # newest on top
            Nobj	= len(objects)

            aux_title	= 'Found '+str(Nobj)+' "PayloadIov" items for the Global Tag Payload '+str(pk)
            aux_table	= PayloadIovTable(objects)
            RequestConfig(request, paginate={'per_page': int(perpage)}).configure(aux_table)

            tableDict	= {'title':aux_title, 'table':aux_table}
            aux_tables.append(tableDict)
            
        if what=='Payload': # list gt gt payloads
            objects	= GlobalTagPayload.objects.filter(payload_id=pk).order_by('-pk') # newest on top
            Nobj	= len(objects)

            aux_title	= 'Found '+str(Nobj)+' "Global Tag Payload" items for the Payload '+str(pk)
            aux_table	= GlobalTagPayloadTable(objects)
            RequestConfig(request, paginate={'per_page': int(perpage)}).configure(aux_table)

            tableDict	= {'title':aux_title, 'table':aux_table}
            aux_tables.append(tableDict)
            

        d = dict(domain		=	domain,
                 host		=	host,
                 what		=	banner,
                 navtable	=	navtable,
                 table		=	table,
                 aux_tables	=	aux_tables,
                 selectors	=	selectors,
                 selwidth	=	selwidth,
        )
        
        # *******> TEMPLATE <*******
        template = 'cdbweb_general_table.html'
        return render(request, template, d)

    else:
        if(gtid!=''):
            objects = eval(what).objects.filter(global_tag_id=gtid).order_by('-pk') # newest on top
        elif(gtpid!=''):
            objects = eval(what).objects.filter(global_tag_payload_id=gtpid).order_by('-pk') # newest on top
        else:
            objects = eval(what).objects.order_by('-pk') # newest on top

    if objects is not None and len(objects)!=0:
        Nfound = len(objects)
    else:
        Nfound=0
        banner='No '+what+' database entries were found using your selection criteria'
        # *******> TEMPLATE <*******
        template = 'cdbweb_general_table_empty.html'
        d = dict(domain=domain, host=host, what=banner, selectors=selectors, navtable=navtable)
        return render(request, template, d)

    # General case:
    table = eval(what+'Table')(objects)
    
    RequestConfig(request, paginate={'per_page': int(perpage)}).configure(table)


    # We reserve space on top of the table for the selectors + the submit
    # button, estimate how much is needed here (in percent of the page width)
    
    banner = what+': '+str(Nfound)+' items found'
    
    d = dict(domain=	domain,
             host=	host,
             what=	banner,
             navtable=	navtable,
             table=	table,
             selectors=	selectors,
             selwidth=	selwidth,
    )

    # *******> TEMPLATE <*******
    template = 'cdbweb_general_table.html'

    return render(request, template, d)

