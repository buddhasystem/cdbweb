# core django
from django.shortcuts	import render
from django.http	import HttpResponse, HttpResponseRedirect
from django.conf	import settings
from django.utils.html	import format_html

# time
from django.utils			import timezone
from django.utils.timezone		import utc
from django.utils.timezone		import activate

# tables
from	django_tables2	import RequestConfig

# local utility classes
from utils.navbar	import TopTable

# data
from .models		import *
from .cdbwebTables	import *


from utils.selectorUtils import dropDownGeneric, oneFieldGeneric, boxSelector, boolSelector


#########################################################    

PAGECHOICES	= [('25','25'),('50','50'),('100','100'),('200','200'),('400','400'),('800','800'),]
GTSTATUSCHOICES	= [('All','All'),('NEW','New'),('PUBLISHED','Published'),('INVALID','Invalid'),]
GTTYPECHOICES	= [('All','All'),('RELEASE','Release'),('DEV','Dev'),]

EXCLUDE_ID = {
    'GlobalTagPayload':	{'pk':('global_tag_payload_id',)},
    'GlobalTag':	{'all':('global_tag_id',)},
    'Payload':		{'all':('payload_id',)},
}

COMPARISON_PROMPT = format_html('&lArr;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Specify the tags to compare&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rArr;')

#########################################################    
# ---
def makeQuery(page, q=''):
    gUrl= '/'+page
    qUrl= '/'+page+"?"

    if(q==''): return HttpResponseRedirect(gUrl)
    return HttpResponseRedirect(qUrl+q)

#########################################################    
# ---
def gtValidation(allGtps):
    itemStatus = None
    
    # validation 1: count IoVs for each global payload tag and make sure the count is same
    # validation 2: compare tuples

    validation1, validation2, listOfLengths, listOfTuples, referenceSet = True, True, [], [], None

    for gtp in allGtps: # iterate over individual global tag payloads
        pIoVs = PayloadIov.objects.filter(global_tag_payload_id=gtp.pk).order_by('-pk')
        listOfLengths.append(len(pIoVs))
        for piov in pIoVs:
            listOfTuples.append((piov.exp_start, piov.exp_end, piov.run_start, piov.run_end))
        currentSet = set(listOfTuples)
        
        if referenceSet is None:
            referenceSet = currentSet
        else:
            if bool(referenceSet.difference(currentSet)): validation2 = False
                    
    validation1 = (len(list(set(listOfLengths))) == 1)

    if(validation1):
        itemStatus = 'Diagnostic 1: same number of IoVs for all Payloads.<br/>'
        if(validation2):
            itemStatus+='Diagnostic 2: same set of IoVs for all Payloads.<br/>'
    else:
        itemStatus = 'Diagnostic 1: different number of IoVs for some Payloads.<br/>'

        
    the_payloads	= allGtps.values_list('payload_id', flat=True) # payload numbers for the GT we are handling
    # print('+++', len(the_payloads))
    selected_basf2	= Payload.objects.filter(payload_id__in=the_payloads).values_list('basf2_module_id', flat=True)
    basf2modules	= Basf2Module.objects.filter(basf2_module_id__in=selected_basf2).distinct('name')# .values_list('basf2_module_id', flat=True)

    #print('!!!!', len(basf2modules))
    #print(basf2modules)

    faultyList = []
    faultyNames = []
    
    for b in basf2modules:
        payloads4basf = Payload.objects.filter(payload_id__in=the_payloads).filter(basf2_module_id=b.basf2_module_id)
        gts4basf = allGtps.filter(payload_id__in=payloads4basf).values_list('global_tag_payload_id', flat=True)
        iovs = PayloadIov.objects.filter(global_tag_payload_id__in=gts4basf)
        
        run_starts = []
        run_ends = []
        
        # if(len(iovs)==1 and iovs[0].run_start==iovs[0].run_end): continue

        #print('---------------------------------')

        trivial = True
        
        for i in iovs:
            # print(i.exp_start, i.exp_end, i.run_start, i.run_end )
            
            run_starts.append(i.run_start)
            run_ends.append(i.run_end)

            if(i.run_start!=0 or i.run_end!=-1): trivial=False
            #if(i.run_end==-1):
            #    print('!', b.name,'!', i.run_start, i.run_end)

        #print(b.name,'trivial:', trivial)
        if(trivial): continue
        
        #run_starts.sort()
        #run_ends.sort()
        #print(b.name,'!', run_ends)
        
        #print('---------------------------------')

        mxRun = max(run_ends)
        for runEnd in run_ends:
            if(len(run_starts)==1 and len(run_ends)==1):
                if(run_starts[0]==run_ends[0]): continue
                
            if(runEnd==-1 or runEnd==0): continue
            if((runEnd+1) in run_starts):
                pass # print('OK')
            else:
                if(b.basf2_module_id in faultyList):
                    pass
                else:
                    # print('!', b.name, runEnd,mxRun)
                    if(runEnd==mxRun): # or ((-1) in run_ends)):
                        pass
                    else:
                        faultyList.append(b.basf2_module_id)
                        faultyNames.append(b.name)
                    
    if(len(faultyNames))>0:
        itemStatus+='<hr/>Potential IoV continuity problem for module(s)<br/>'+'<br/>'.join(faultyNames)

    return format_html(itemStatus)


#########################################################    
def index(request):

    template = 'index.html'

    host	= request.GET.get('host','')
    domain	= request.get_host()

    navtable	= TopTable(domain, 'Home')
    banner	= "Welcome to CDBweb! Please make your selection above..."

    now = timezone.now()
    d = dict(domain=domain, host=host, what=banner, navtable=navtable, now=now)

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
        d['what']='Welcome to CDBweb!'

    if(settings.DBSERVER!=''): d['dbserver']=settings.DBSERVER
        
    return render(request, template, d)

#########################################################    
def test(request):
    template = 'cdbweb_base.html'
    
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
    validate	= rg.get('validate','0')

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
        basf2Selector	= oneFieldGeneric(request.POST, label='Basf2Module ("Global Tag Payload filter", can be partial)',
                                          field="basf2", init=basf2)
        
        if basf2Selector.is_valid(): basf2=basf2Selector.getval("basf2")
        if(basf2!=''): q+= 'basf2='+basf2+'&'
        
        # "Modified by" selector
        modifiedBySelector	= oneFieldGeneric(request.POST, label="Modified by", field="modifiedby", init=modifiedby)
        if modifiedBySelector.is_valid(): modifiedby=modifiedBySelector.getval("modifiedby")
        if(modifiedby!=''): q+= 'modifiedby='+modifiedby+'&'


        validateSelector = boolSelector(request.POST, label='Run IoV diagnostics', what='validate', init=(validate=='1'))
        if validateSelector.is_valid():
            q+='validate='+validateSelector.getval()+'&'
        
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
            basf2Selector = oneFieldGeneric(label='Basf2Module ("Global Tag Payload" filter, can be partial)',
                                            field="basf2", init=basf2)
            selectors.append(basf2Selector)

    if(what=='GlobalTagPayload') and pk=='':
        gtidSelector	= oneFieldGeneric(label="Global Tag ID", field="gtid", init=gtid)
        selectors.append(gtidSelector)

        nameSelector	= oneFieldGeneric(label="GT Name (Can be partial)", field="name", init=name)
        selectors.append(nameSelector)

        basf2Selector = oneFieldGeneric(label="Name (can be partial)", field="basf2", init=basf2)
        selectors.append(basf2Selector)

        
    # Keep for later...
    # if(what=='Payload'):
    #     gtpidSelector = oneFieldGeneric(label="Global Tag Payload ID", field="gtpid", init=gtpid)
    #     selectors.append(gtpidSelector)

    if(what=='Payload' and pk==''):
        basf2Selector = oneFieldGeneric(label="Name (can be partial)", field="basf2", init=basf2)
        selectors.append(basf2Selector)

    perPageSelector = dropDownGeneric(initial	= {'perpage':perpage},
                                      label	= 'items per page',
                                      choices	= PAGECHOICES,
                                      tag	= 'perpage')
    selectors.append(perPageSelector)

    if(what=='GlobalTag' and pk!=''):
        validateSelector = boolSelector(label='Run IoV diagnostics', what='validate', init=(validate=='1'))
        selectors.append(validateSelector)

    
    selwidth=15*(len(selectors)+1)
    if(selwidth>100):
        selwidth=100
    
    # --- END building selectors
    #################################################################################################
    
    objects	= None
    itemStatus	= None
    
    # *******> TEMPLATE <*******
    template = 'cdbweb_general_table.html'
    aux_tables = []


    ### PRIMARY KEY ON OBJECTS TAKES PRECEDENCE
    if(pk!=''):
        theObject  = None

        try:
            theObject = eval(what).objects.get(pk=pk)
        except:
            banner	= 'No '+what+' database entries were found using your selection criteria'
            template	= 'cdbweb_general_table_empty.html' # custom template for empty set
            d		= dict(domain=domain, host=host, what=banner, selectors=selectors, navtable=navtable)
            return render(request, template, d)

        # create a table for the object fetched by the primary key
        table = eval(what+'Table')([theObject,])
        RequestConfig(request).configure(table)

        try:
            table.exclude = EXCLUDE_ID[what]['pk']
        except:
            pass
        
        banner=what+' '+str(pk)

        ##########################################################################
        #      Now fetch related items depending on the primary object type:
        ##########################################################################
        ### GLOBAL TAG
        if what=='GlobalTag': # list Global Tag Payloads
            objects	= GlobalTagPayload.objects.using('default').filter(global_tag_id=pk).order_by('-pk') # newest on top
            Nobj	= len(objects)

            if(validate=='1'): itemStatus = gtValidation(objects)
            
            comment = ''
            if(basf2!=''): # selection for auxiliary tables
                the_payloads		= objects.values_list('payload_id', flat=True) # payload numbers for the GT we are handling
                selected_basf2		= Basf2Module.objects.filter(name__istartswith=basf2).values_list('basf2_module_id', flat=True)
                # JOIN
                selected_payloads	= Payload.objects.filter(payload_id__in=the_payloads, basf2_module_id__in=selected_basf2).values_list('payload_id', flat=True)
                
                objects = objects.filter(payload_id__in=selected_payloads)
                comment = ', selected '+str(len(objects))+' based on the basf2 module name pattern "'+basf2+'"'
                                                                                                                                   
            theGt = GlobalTag.objects.get(global_tag_id=pk)
            aux_title	= 'Found a total of '+str(Nobj)+' "Global Tag Payload" items for the Global Tag '+str(pk)+' "'+theGt.name+'" '+comment
            aux_table	= GlobalTagPayloadTable(objects)
            aux_table.exclude = ('global_tag_id', 'gtName')
            RequestConfig(request, paginate={'per_page': int(perpage)}).configure(aux_table)
            
            tableDict	= {'title':aux_title, 'table':aux_table}
            aux_tables.append(tableDict)

        ##########################################################################
        ### GLOBAL TAG PAYLOAD
        if what=='GlobalTagPayload': # list gt payloadIovs
            objects	= PayloadIov.objects.filter(global_tag_payload_id=pk).order_by('-pk') # newest on top
            Nobj	= len(objects)

            aux_title	= 'Found '+str(Nobj)+' "PayloadIov" items for the Global Tag Payload '+str(pk)
            aux_table	= PayloadIovTable(objects)
            aux_table.exclude = ('global_tag_payload_id',)
            RequestConfig(request, paginate={'per_page': int(perpage)}).configure(aux_table)

            tableDict	= {'title':aux_title, 'table':aux_table}
            aux_tables.append(tableDict)

        ##########################################################################
        ### PAYLOAD
        if what=='Payload': # list gt gt payloads
            objects	= GlobalTagPayload.objects.filter(payload_id=pk).order_by('-pk') # newest on top
            Nobj	= len(objects)
            
            aux_title	= 'Found '+str(Nobj)+' "Global Tag Payload" items for the Payload '+str(pk)
            aux_table	= GlobalTagPayloadTable(objects)
            aux_table.exclude = ('payload_id', )
            RequestConfig(request, paginate={'per_page': int(perpage)}).configure(aux_table)

            tableDict	= {'title':aux_title, 'table':aux_table}
            aux_tables.append(tableDict)
            
           
        now = timezone.now()
        d = dict(domain		=	domain,
                 host		=	host,
                 what		=	banner,
                 status		=	itemStatus,
                 navtable	=	navtable,
                 table		=	table,
                 aux_tables	=	aux_tables,
                 selectors	=	selectors,
                 selwidth	=	selwidth,
                 now		=	now,
        )
        
        try:
            d['snapshot']=settings.SNAPSHOT
        except:
            pass
        
        if(settings.DBSERVER!=''): d['dbserver']=settings.DBSERVER
        return render(request, template, d)

    ##########################################################################
    ##################SELECTION OTHER THAN PRIMARY KEY########################
    ##########################################################################
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
            gtStatus	= GlobalTagStatus.objects.filter(name=status)[0]
            objects	= objects.filter(global_tag_status_id=gtStatus.pk)
        if(gttype!='All' and gttype!=''):
            gtType	= GlobalTagType.objects.filter(name=gttype)[0]
            objects	= objects.filter(global_tag_type_id=gtType.pk)
        if(modifiedby!=''):
            objects	= objects.filter(modified_by=modifiedby)
        else:
            pass


    ### TAKE STOCK OF WHAT'S BEEN FOUND
    if objects is not None and len(objects)!=0:
        Nfound = len(objects)
    else:
        Nfound	= 0
        banner	= 'No '+what+' database entries were found using your selection criteria'
        template= 'cdbweb_general_table_empty.html'
        d = dict(domain=domain, host=host, what=banner, selectors=selectors, navtable=navtable)
        if(settings.DBSERVER!=''): d['dbserver']=settings.DBSERVER
        return render(request, template, d)

    # AUTO-CREATE APPROPRIATE TABLE
    table = eval(what+'Table')(objects)
    RequestConfig(request, paginate={'per_page': int(perpage)}).configure(table)
    
    try:
        table.exclude = EXCLUDE_ID[what]['all']
    except:
        pass
    



    # We reserve space on top of the table for the selectors + the submit
    # button, estimate how much is needed here (in percent of the page width)
    
    banner = what+': '+str(Nfound)+' items found'
    
    now = timezone.now()
    d = dict(domain=	domain,
             host=	host,
             what=	banner,
             navtable=	navtable,
             table=	table,
             selectors=	selectors,
             selwidth=	selwidth,
             now=	now,
    )

    try:
        d['snapshot']=settings.SNAPSHOT
    except:
        pass
    # *******> TEMPLATE <*******
    template = 'cdbweb_general_table.html'

    if(settings.DBSERVER!=''): d['dbserver']=settings.DBSERVER
    return render(request, template, d)



######################################################### . . . . . . . . . . . . .
######################################################### . . . . . . . . . . . . .
####################  GTCOMPARE  ######################## . . . . . . . . . . . . .
######################################################### . . . . . . . . . . . . .
######################################################### . . . . . . . . . . . . .
#
def gtcompare(request):
    domain		= request.get_host()
    navtable		= TopTable(domain, 'Global Tag Comparison')
    
    settings.domain	= domain
    
    template		= 'gtcompare.html'

    ##################################################################
    ####################      POST      ##############################
    ##################################################################
    if request.method == 'POST':
        q = '' # placeholder for potential query

        # Generic ID selectors
        gtSelector1 = oneFieldGeneric(request.POST, label="Id/Name 1", field="idname1", init='')
        if gtSelector1.is_valid():
            idname1=gtSelector1.getval("idname1")
            if(idname1!=''):
                if(idname1.isdigit()):
                    q+= 'gtid1='+idname1+'&'
                else:
                    q+= 'gtname1='+idname1+'&'

        gtSelector2 = oneFieldGeneric(request.POST, label="Id/Name 2", field="idname2", init='')
        if gtSelector2.is_valid():
            idname2=gtSelector2.getval("idname2")
            if(idname2!=''):
                if(idname2.isdigit()):
                    q+= 'gtid2='+idname2+'&'
                else:
                    q+= 'gtname2='+idname2+'&'

        # We have built a query and will come to same page/view with a GET query
        return makeQuery('gtcompare', q)

    ##################################################################
    ####################      GET       ##############################
    ##################################################################

    host	= request.GET.get('host','')
    
    gtid1	= request.GET.get('gtid1','')
    gtid2	= request.GET.get('gtid2','')

    gtname1	= request.GET.get('gtname1','')
    gtname2	= request.GET.get('gtname2','')

    gt1, gt2 = None, None

    # --- Populate the selector section!
    selectors	= []
    what	= 'Comparison of Global Tags. Specify a pair of IDs or a pair of names.'

    now = timezone.now()
    
    if(gtid1=='' or gtid2==''): # some IDs missing, try names
        
        if(gtname1=='' or gtname2==''): # try names

            gtSelector1 = oneFieldGeneric(label="ID/NAME 1", field="idname1", init='')
            selectors.append(gtSelector1)

            selectors.append(COMPARISON_PROMPT)
    
            gtSelector2 = oneFieldGeneric(label="ID/NAME 2", field="idname2", init='')
            selectors.append(gtSelector2)
        
            # selwidth=30*(len(selectors)+1)
            # if(selwidth>100):

            selwidth=100
            
            d = dict(domain=domain,	host=host,	what=what,	navtable=navtable,
	             selectors=selectors,		selwidth=selwidth, now=now,
            )
            
            try:
                d['snapshot']=settings.SNAPSHOT
            except:
                pass

            # CREATE the global tag table
            allGts = GlobalTag.objects.order_by('-pk') # newest on top
            gtTable = GlobalTagTable(allGts)
            RequestConfig(request, paginate={'per_page': 25}).configure(gtTable)

            d['gtTable'] = gtTable
            
            if(settings.DBSERVER!=''): d['dbserver']=settings.DBSERVER
            return render(request, template, d)
        else:
            gtSelector1 = oneFieldGeneric(label="ID/NAME 1", field="idname1", init=gtname1)
            selectors.append(gtSelector1)
    
            selectors.append(COMPARISON_PROMPT)
            
            gtSelector2 = oneFieldGeneric(label="ID/NAME 2", field="idname2", init=gtname2)
            selectors.append(gtSelector2)

            try:
                gt1 = GlobalTag.objects.using('default').filter(name=gtname1)[0]
                gt2 = GlobalTag.objects.using('default').filter(name=gtname2)[0]
                gtid1=gt1.global_tag_id
                gtid2=gt2.global_tag_id
            except:
                pass

            
    else: # proceed with search on IDs
        
        gtSelector1 = oneFieldGeneric(label="ID/NAME 1", field="idname1", init=gtid1)
        selectors.append(gtSelector1)

        selectors.append(COMPARISON_PROMPT)
    
        gtSelector2 = oneFieldGeneric(label="ID/NAME 2", field="idname2", init=gtid2)
        selectors.append(gtSelector2)

        try:
            gt1 = GlobalTag.objects.using('default').get(global_tag_id=gtid1)
            gt2 = GlobalTag.objects.using('default').get(global_tag_id=gtid2)
            gtname1=gt1.name
            gtname2=gt2.name
        except:
            pass


    # disables in the template, comment this out for now
    # selwidth=30*(len(selectors)+1)
    # if(selwidth>100):
    
    selwidth=100
    
    if(gt1 is None or gt2 is None):
        error='Check values: last query did not produce valid results.'
        d = dict(domain=domain,	host=host, what=what, error=error, navtable=navtable,
	         selectors=selectors,	selwidth=selwidth, now=now,
        )

        try:
            d['snapshot']=settings.SNAPSHOT
        except:
            pass
        
        if(settings.DBSERVER!=''): d['dbserver']=settings.DBSERVER
        return render(request, template, d)
    #---
       
    table1 = GlobalTagTable([gt1,])
    table2 = GlobalTagTable([gt2,])
    
    table1.exclude = ('global_tag_id', 'name', 'description',)
    table2.exclude = ('global_tag_id', 'name', 'description',)
    
    RequestConfig(request).configure(table1)
    RequestConfig(request).configure(table2)
        
    
    th1		= str(gtid1)+': "'+gtname1+'"'
    th2		= str(gtid2)+': "'+gtname2+'"'

    desc1	= gt1.description
    desc2	= gt2.description


    gtp1	= GlobalTagPayload.objects.using('default').filter(global_tag_id=gtid1).order_by('-pk')
    gtp2	= GlobalTagPayload.objects.using('default').filter(global_tag_id=gtid2).order_by('-pk')

    gtp_exclude = ('global_tag_id', 'gtName', 'dtm_ins', 'dtm_mod',)

    aux_table1	= GlobalTagPayloadTable(gtp1)
    aux_table1.exclude = gtp_exclude
    RequestConfig(request).configure(aux_table1)

    aux_table2	= GlobalTagPayloadTable(gtp2)
    aux_table2.exclude = gtp_exclude
    RequestConfig(request).configure(aux_table2)

    now = timezone.now()
    d = dict(domain=domain, host=host, what=what, navtable=navtable,
             now=now,
	     selectors	= selectors,	selwidth=selwidth,
             th1	= th1,		th2	= th2,
             desc1	= desc1,	desc2	= desc2,
             table1	= table1,	table2	= table2,
             aux_table1	= aux_table1,	aux_table2=aux_table2
    )

    try:
        d['snapshot']=settings.SNAPSHOT
    except:
        pass
    
    if(settings.DBSERVER!=''): d['dbserver']=settings.DBSERVER
    return render(request, template, d)


#################################################################################################
# DeferredRPT
# objects	= PayloadIovRpt.objects.filter(global_tag_payload_id=pk).order_by('-pk') # newest on top
# Nobj	= len(objects)

# aux_title	= 'Found '+str(Nobj)+' "PayloadIovRpt" items for the Global Tag Payload '+str(pk)
# aux_table	= PayloadIovRptTable(objects)
# aux_table.exclude = ('global_tag_payload_id', 'payload_id', 'global_tag_id', 'gt_name', 'b2m_name',)
# RequestConfig(request, paginate={'per_page': int(perpage)}).configure(aux_table)

# tableDict	= {'title':aux_title, 'table':aux_table}
# aux_tables.append(tableDict)


