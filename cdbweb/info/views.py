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
GTSTATUSCHOICES = [('All','All'), ('NEW','New'), ('PUBLISHED','Published'), ('INVALID','Invalid'),]
GTTYPECHOICES = [('All','All'), ('RELEASE','Release'), ('DEV','Dev'),]

EXCLUDE_ID = {'GlobalTagPayload':('global_tag_payload_id',)}

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

    try:
        if(settings.STATUS=='maintenance'):
            template = 'maintenance.html'
            return render(request, template, d)
    except:
        pass

    try:
        d['snapshot']=settings.SNAPSHOT
        d['what']='Welcome to CDBweb! This test service reflects the DB snapshot taken on '+settings.SNAPSHOT+'.'
    except:
        pass
        
    return render(request, template, d)

#########################################################    
def iovcheck(request):
    template = 'cdbweb_iov_chart.html'
    
    host	= request.GET.get('host','')
    domain	= request.get_host()
    settings.domain = domain # replaces  table.set_site below
    navtable	= TopTable(domain, 'test')
    
    d = dict(domain=	domain,
             host=	host,
             what=	'test',
             navtable=	navtable,
    )

    return render(request, template, d)


#########################################################
# general request handler for summary type of a table
def data_handler(request, what):
    rg = request.GET
    
    perpage	= rg.get('perpage','25')
    gtid	= rg.get('gtid','')		# GT ID
    gtpid	= rg.get('gtpid','')		# GT payload ID
    pk		= rg.get('id','')
    name	= rg.get('name','')
    status	= rg.get('status','All')
    gttype	= rg.get('gttype','All')
    basf2	= rg.get('basf2','')
    modifiedby	= rg.get('modifiedby','')

    ##################################################################
    ####################      POST      ##############################
    ##################################################################
    if request.method == 'POST':
        q = ''

        # General ID selector
        idSelector	= oneFieldGeneric(request.POST, label="ID", field="id", init=pk)
        if idSelector.is_valid(): pk=idSelector.getval("id")
        if(pk!=''): q+= 'id='+pk+'&'

        # Global Tag ID
        gtidSelector	= oneFieldGeneric(request.POST, label="Global Tag ID", field="gtid", init=gtid)
        if gtidSelector.is_valid(): gtid=gtidSelector.getval("gtid")
        if(gtid!=''): q+= 'gtid='+gtid+'&'
        
        # Global Tag Payload ID
        gtpidSelector	= oneFieldGeneric(request.POST, label="Global Tag Payload ID", field="gtpid", init=gtpid)
        if gtpidSelector.is_valid(): gtpid=gtpidSelector.getval("gtpid")
        if(gtpid!=''): q+= 'gtpid='+gtpid+'&'

        # General name selector
        nameSelector	= oneFieldGeneric(request.POST, label="Name", field="name", init=name)
        if nameSelector.is_valid(): name=nameSelector.getval("name")
        if(name!=''): q+= 'name='+name+'&'

        # gt status selector
        statusSelector = dropDownGeneric(request.POST,
                                         initial={'status':status},
                                         label	= 'Status',
                                         choices= GTSTATUSCHOICES,
                                         tag	= 'status')
        if statusSelector.is_valid(): q+=statusSelector.handleDropSelector()
        
        # gt type selector
        typeSelector = dropDownGeneric(request.POST,
                                       initial	={'gttype':gttype},
                                       label	= 'Type',
                                       choices	= GTTYPECHOICES,
                                       tag	= 'gttype')
        if typeSelector.is_valid(): q+=typeSelector.handleDropSelector()
        
        # Basf2Module selector
        basf2Selector	= oneFieldGeneric(request.POST, label="Basf2Module (gt payload filter, can be partial)", field="basf2", init=basf2)
        if basf2Selector.is_valid(): basf2=basf2Selector.getval("basf2")
        if(basf2!=''): q+= 'basf2='+basf2+'&'
        
        # "Modified by" selector
        modifiedBySelector	= oneFieldGeneric(request.POST, label="Modified by", field="modifiedby", init=modifiedby)
        if modifiedBySelector.is_valid(): modifiedby=modifiedBySelector.getval("modifiedby")
        if(modifiedby!=''): q+= 'modifiedby='+modifiedby+'&'
        
        # --- entries per page
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
    
    host	= rg.get('host','')
    domain	= request.get_host()
    settings.domain = domain # replaces  table.set_site below
    navtable = TopTable(domain, what)


    selectors = [] # The request was GET - populate the selectors

    idSelector = oneFieldGeneric(label="ID", field="id", init=pk)
    selectors.append(idSelector)
        
    if(what=='Basf2Module'):
        nameSelector = oneFieldGeneric(label="Name (can be partial)",	field="name", init=name)
        selectors.append(nameSelector)

    if(what=='GlobalTag' and pk==''):
        nameSelector = oneFieldGeneric(label="Name (can be partial)",	field="name", init=name)
        selectors.append(nameSelector)
        
        statusSelector = dropDownGeneric(initial= {'status':status},
                                         label	= 'Status',
                                         choices= GTSTATUSCHOICES,
                                         tag	= 'status')
        selectors.append(statusSelector)

        typeSelector = dropDownGeneric(initial	={'gttype':gttype},
                                       label	= 'Type',
                                       choices	= GTTYPECHOICES,
                                       tag	= 'gttype')
        selectors.append(typeSelector)

        
        modifiedBySelector = oneFieldGeneric(label="Modified by",	field="modifiedby", init=modifiedby)
        selectors.append(modifiedBySelector)

    if(what=='GlobalTag' and pk!=''):
            basf2Selector = oneFieldGeneric(label="Basf2Module (gt payload filter, can be partial)", field="basf2", init=basf2)
            selectors.append(basf2Selector)

    if(what=='GlobalTagPayload') and pk=='':
        gtidSelector	= oneFieldGeneric(label="Global Tag ID", field="gtid", init=gtid)
        selectors.append(gtidSelector)

        nameSelector	= oneFieldGeneric(label="GT Name (Can be partial)", field="name", init=name)
        selectors.append(nameSelector)

        basf2Selector = oneFieldGeneric(label="Basf2Module name (can be partial)", field="basf2", init=basf2)
        selectors.append(basf2Selector)

        
    # Keep for later...
    # if(what=='Payload'):
    #     gtpidSelector = oneFieldGeneric(label="Global Tag Payload ID", field="gtpid", init=gtpid)
    #     selectors.append(gtpidSelector)

    if(what=='Payload' and pk==''):
        basf2Selector = oneFieldGeneric(label="Basf2Module name (can be partial)", field="basf2", init=basf2)
        selectors.append(basf2Selector)

    perPageSelector = dropDownGeneric(initial	= {'perpage':perpage},
                                      label	= 'items per page',
                                      choices	= PAGECHOICES,
                                      tag	= 'perpage')
    selectors.append(perPageSelector)
    selwidth=12*(len(selectors)+1)
    if(selwidth>100): selwidth=100
    # --- END building selectors

    objects = None
    
    # *******> TEMPLATE <*******
    template = 'cdbweb_general_table.html'
    aux_tables = []
    
    if(pk!=''): # takes precedence
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
        RequestConfig(request).configure(table)

        try:
            table.exclude = EXCLUDE_ID[what]
        except:
            pass
        
        banner=what+' '+str(pk)+' detail'

        if what=='GlobalTag': # list Global Tags
            objects	= GlobalTagPayload.objects.using('default').filter(global_tag_id=pk).order_by('-pk') # newest on top
            Nobj	= len(objects)

            comment = ''
            if(basf2!=''):
                the_payloads = objects.values_list('payload_id', flat=True)
                # print('Total pl:', len(the_payloads))
                
                selected_basf2 = Basf2Module.objects.filter(name__istartswith=basf2).values_list('basf2_module_id', flat=True)
                # print('Selected basf2:', len(selected_basf2))
                
                selected_payloads = Payload.objects.filter(payload_id__in=the_payloads, basf2_module_id__in=selected_basf2).values_list('payload_id', flat=True)
                # print('-----------------------------\n', selected_payloads)
                
                objects = objects.filter(payload_id__in=selected_payloads)
                # print('Selected pl:', len(objects))
                comment = ', selected '+str(len(objects))+' based on the basf2 module name pattern '+basf2
                                                                                                                                   
            theGt = GlobalTag.objects.get(global_tag_id=pk)
            aux_title	= 'Found a total of '+str(Nobj)+' "Global Tag Payload" items for the Global Tag "'+theGt.name+'", ID: '+str(pk)+comment
            aux_table	= GlobalTagPayloadTable(objects)
            aux_table.exclude = ('global_tag_id', 'gtName')
            RequestConfig(request, paginate={'per_page': int(perpage)}).configure(aux_table)
            
            tableDict	= {'title':aux_title, 'table':aux_table}
            aux_tables.append(tableDict)

        if what=='GlobalTagPayload': # list gt payloadIovs
            objects	= PayloadIov.objects.filter(global_tag_payload_id=pk).order_by('-pk') # newest on top
            Nobj	= len(objects)

            aux_title	= 'Found '+str(Nobj)+' "PayloadIov" items for the Global Tag Payload '+str(pk)
            aux_table	= PayloadIovTable(objects)
            aux_table.exclude = ('global_tag_payload_id',)
            RequestConfig(request, paginate={'per_page': int(perpage)}).configure(aux_table)

            tableDict	= {'title':aux_title, 'table':aux_table}
            aux_tables.append(tableDict)
            
            # objects	= PayloadIovRpt.objects.filter(global_tag_payload_id=pk).order_by('-pk') # newest on top
            # Nobj	= len(objects)

            # aux_title	= 'Found '+str(Nobj)+' "PayloadIovRpt" items for the Global Tag Payload '+str(pk)
            # aux_table	= PayloadIovRptTable(objects)
            # aux_table.exclude = ('global_tag_payload_id', 'payload_id', 'global_tag_id', 'gt_name', 'b2m_name',)
            # RequestConfig(request, paginate={'per_page': int(perpage)}).configure(aux_table)

            # tableDict	= {'title':aux_title, 'table':aux_table}
            # aux_tables.append(tableDict)
            
        if what=='Payload': # list gt gt payloads
            objects	= GlobalTagPayload.objects.filter(payload_id=pk).order_by('-pk') # newest on top
            Nobj	= len(objects)
            
            aux_title	= 'Found '+str(Nobj)+' "Global Tag Payload" items for the Payload '+str(pk)
            aux_table	= GlobalTagPayloadTable(objects)
            aux_table.exclude = ('payload_id', )
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
        
        return render(request, template, d)

    else:
        objects = eval(what).objects.order_by('-pk') # newest on top
        if(gtid!=''):	objects = objects.filter(global_tag_id=gtid)
        if(gtpid!=''):	objects = objects.filter(global_tag_payload_id=gtpid)
        if(name!=''):
            if(what!='GlobalTagPayload'):
                objects = objects.filter(name__icontains=name)
            else:
                gts = GlobalTag.objects.filter(name__icontains=name).values_list('global_tag_id', flat=True)
                objects = objects.filter(global_tag_id__in=gts)

        if(basf2!='' and (what=='Payload' or what=='GlobalTagPayload')):
            selected_basf2	= Basf2Module.objects.filter(name__istartswith=basf2).values_list('basf2_module_id', flat=True)
            selected_payloads	= Payload.objects.filter(basf2_module_id__in=selected_basf2).values_list('payload_id', flat=True)
            objects		= objects.filter(payload_id__in=selected_payloads)
        
        if(status!='All' and status!=''):
            gtStatus = GlobalTagStatus.objects.filter(name=status)[0]
            objects = objects.filter(global_tag_status_id=gtStatus.pk)
        if(gttype!='All' and gttype!=''):
            gtType = GlobalTagType.objects.filter(name=gttype)[0]
            objects = objects.filter(global_tag_type_id=gtType.pk)
        if(modifiedby!=''):
            objects = objects.filter(modified_by=modifiedby)
        else:
            pass

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

    try:
        d['snapshot']=settings.SNAPSHOT
    except:
        pass
    # *******> TEMPLATE <*******
    template = 'cdbweb_general_table.html'

    return render(request, template, d)

