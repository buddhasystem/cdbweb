import	django_tables2	as tables

from django.utils.safestring		import mark_safe
from django.utils.html			import format_html

from django.urls	import reverse
from django.conf	import settings
from django.db.models	import Case, When

from .models		import *

import operator

#########################################################
############## Links formatters #########################
#########################################################
def makelink(what, key, value):
    return mark_safe('<a href="http://%s%s?%s=%s">%s</a>'
                     % (settings.domain, reverse(what), key, value, value))

def makeNamedLink(what, key, value, name):
    return mark_safe('<a href="http://%s%s?%s=%s">%s</a>'
                     % (settings.domain, reverse(what), key, value, name))

def makeTaglink(what, gtid, key, value, tag):
    return mark_safe('<a href="http://%s%s?gt4pl=%s&%s=%s">%s</a>'
                     % (settings.domain, reverse(what), gtid, key, value, tag))

def makeIDlink(what, id_value, value):
    return mark_safe('<a href="http://%s%s?id=%s">%s</a>'
                     % (settings.domain, reverse(what), id_value,  value))

#########################################################
def numberOfModules(gt):
    the_payloads	= GlobalTagPayload.objects.filter(global_tag_id=gt.global_tag_id).values_list('payload_id')
    the_modules		= Payload.objects.filter(payload_id__in=the_payloads).values_list('basf2_module_id', flat=True)


    howMany		= len(list(Basf2Module.objects.filter(basf2_module_id__in=the_modules).values_list('name', flat=True).distinct()))
    
    return howMany



#########################################################
########### Custom Tables (not model-based) #############
#########################################################
# ---
# Custom table for GT diffs
class GtDiffTable(tables.Table):
    diff	= tables.Column(empty_values=())
    name	= tables.Column()
    rev		= tables.Column()
    iov		= tables.Column()
    
#    exp_start	= tables.Column()
#    run_start	= tables.Column()
#    exp_end	= tables.Column()
#    run_end	= tables.Column()

    class Meta:
        attrs	= {'class': 'paleblue'}

# ---
# Custom table for aggregated payloads. First, the link generator:
def makeIOVlink(what, gtid, name):
    return mark_safe('<a href="http://%s%s?gt4pl=%s&name=%s">%s</a>'
                     % (settings.domain, reverse(what), gtid, name, name))

class PayloadLinkTable(tables.Table):
    name	= tables.Column(empty_values=())
    count	= tables.Column()
    gt		= tables.Column()
    
    def render_name(self, bound_row):
        return makeIOVlink('Payload', bound_row.record['gt'], bound_row.record['name'])
   
    class Meta:
        attrs	= {'class': 'paleblue'}
        exclude = ('gt',)


#########################################################
################# "Main" tables #########################
#########################################################
# Base abstract class for all the "general" tables in
# CDBweb. Due to the original naming convention where
# each pk has a different name in each table (!) we
# need to overload the id renderer where needed.


class CdbWebTable(tables.Table):
    def __init__(self, *args, **kwargs):
        try:
            self.extra=kwargs.pop('extra')
            # print(self.extra)
        except:
            pass

        super(CdbWebTable, self).__init__(*args, **kwargs)
         
    def render_id(self, value):
        thisItemName = self.Meta.model.__name__
        return makelink(thisItemName,	'id',		value)
    
    def render_as_id(self, id_value, value):
        thisItemName = self.Meta.model.__name__
        return makeIDlink(thisItemName, id_value,	value)
    
    def render_global_tag_id(self, value):
        return makelink('GlobalTag', 'gtid',		value)
    
    def render_global_tag_payload_id(self, value):
        return makelink('GlobalTagPayload', 'id',	value)
    
    def render_payload_id(self, value):
        return makelink('Payload', 'id',		value)
    
    def render_payload_iov_id(self, value):
        return makelink('PayloadIov', 'id',		value)
    
    def render_basf2_module_id(self, value):
        return makelink('Basf2Module', 'id',		value)

    def render_modified_by(self, value):
        thisItemName = self.Meta.model.__name__
        return makelink(thisItemName,	'modifiedby',	value)
    
    class Meta:
        attrs	= {'class': 'paleblue','width':'120%'}
        abstract=True # <------
#-------------------------------------------------------


#########################################################
class AppMessageTable(CdbWebTable):
    class Meta(CdbWebTable.Meta):
        model = AppMessage
#########################################################
class Basf2ModuleTable(CdbWebTable):
    def render_basf2_module_id(self, value):
        return self.render_id(value)

    def render_name(self, record):
        return makeIDlink('Basf2Module', record.basf2_module_id, record.name)
    
    class Meta(CdbWebTable.Meta):
        exclude = ('modified_by', 'description', )
        model = Basf2Module
#########################################################
class GlobalTagTable(CdbWebTable):
    numberOfGlobalTagPayloads	= tables.Column(verbose_name='Total Payloads', empty_values=())
    basf2modules = tables.Column(verbose_name='Distinct Payloads',
                                 empty_values=(),
                                 attrs={'td': {'width': '"20%"'}, 'th': {'width': '"20%"'}}
    )

    def order_numberOfGlobalTagPayloads(self, QuerySet, is_descending):
        # ordered = sorted(QuerySet, key=numberOfModules)
        # for x in ordered:
        #    print(x, x.global_tag_id, numberOfModules(x))
        return (QuerySet, True)

    def order_basf2modules(self, QuerySet, is_descending):
        return (QuerySet, True)

    
    def render_global_tag_id(self, value):
        return self.render_id(value)

    def render_name(self, record):
        return makeIDlink('GlobalTag', record.global_tag_id, record.name)

    def render_global_tag_status_id(self, value):
        gts = GlobalTagStatus.objects.get(pk=value)
        return gts.name

    def render_global_tag_type_id(self, value):
        gts = GlobalTagType.objects.get(pk=value)
        return gts.name

    def render_basf2modules(self, record):
        the_payloads = GlobalTagPayload.objects.filter(global_tag_id=record.global_tag_id).values_list('payload_id')

        # -mxp- Decided to remove the partial list of names after a discussion with Benedict
        the_modules	= Payload.objects.filter(payload_id__in=the_payloads).values_list('basf2_module_id', flat=True)
        module_names	= list(Basf2Module.objects.filter(basf2_module_id__in=the_modules).values_list('name', flat=True).distinct())
        # separator = ','
        # joined =  separator.join(module_names)
        return str(len(module_names))

    # Decided to revert to the dumb display (above) since we are changing the navigation logic
        # id_link = self.render_as_id(record.global_tag_id, str(len(module_names)))
        
        # info = id_link # +":"+joined    ; see comment above
        
        # # info = info[:100] + (info[100:] and '...') ; see comment above
        
        # rendered_value = info
        # return mark_safe('<div style="max-width: 700px;">'+rendered_value+"</div>")
    

        
    def render_numberOfGlobalTagPayloads(self, record):
        the_global_tag_payloads	= GlobalTagPayload.objects.filter(global_tag_id=record.global_tag_id)
        return len(the_global_tag_payloads)

    def render_description(self,value):
        return mark_safe('<div style="max-width: 200px;">'+value+"</div>")

    
    class Meta(CdbWebTable.Meta):
        model = GlobalTag
        sequence = (
            'name',
            '...')
#########################################################
class GlobalTagPayloadTable(CdbWebTable):
    gtName	= tables.Column(verbose_name='Global Tag ID and Name', empty_values=())
    basf2module	= tables.Column(verbose_name='Payload Name', empty_values=())
    nIoVs	= tables.Column(verbose_name='# of IoVs', empty_values=())
    
    def render_global_tag_payload_id(self, value):
        return self.render_id(value)

    def render_gtName(self, record):
        theGt = GlobalTag.objects.get(global_tag_id=record.global_tag_id)
        return makeIDlink('GlobalTag', record.global_tag_id, str(record.global_tag_id)+': '+theGt.name)
    
    def render_nIoVs(self, record):
        # theGt = GlobalTag.objects.get(global_tag_id=record.global_tag_id)
        pIoVs = PayloadIov.objects.filter(global_tag_payload_id=record.pk).order_by('-pk')
        # listOfLengths.append(len(pIoVs))

        return str(len(pIoVs))
        
    def render_basf2module(self, record):
        
        the_payloads	= Payload.objects.filter(payload_id=record.payload_id)
        if(len(the_payloads)==0):
           return 'Not Found'

        p = the_payloads[0]
        the_modules	= Basf2Module.objects.filter(basf2_module_id=p.basf2_module_id)
        m = the_modules[0]
        
        return makeIDlink('Basf2Module', p.basf2_module_id, m.name)

    def value_basf2module(self, record):
        
        the_payloads	= Payload.objects.filter(payload_id=record.payload_id)
        if(len(the_payloads)==0):
           return 'Not Found'

        p = the_payloads[0]
        the_modules	= Basf2Module.objects.filter(basf2_module_id=p.basf2_module_id)
        m = the_modules[0]
        
        return m.name

    def order_basf2module(self, QuerySet, is_descending):
 
        ordered = sorted(QuerySet, key=lambda x: (x.basf2module()), reverse=is_descending)
        pk_list = []
        for o in ordered: pk_list.append(o.global_tag_payload_id)
        
        preserved	= Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)])
        ordered_qs	= GlobalTagPayload.objects.filter(pk__in=pk_list).order_by(preserved)

        return (ordered_qs, True)
    
    def order_nIoVs(self, QuerySet, is_descending):
        #ordered = sorted(QuerySet, key=basf2module)
        # for x in ordered:
        #    print(x, x.global_tag_id, numberOfModules(x))
        return (QuerySet, True)
    
    class Meta(CdbWebTable.Meta):
        exclude = ('global_tag_id', )
        sequence = ('global_tag_payload_id', 'gtName', 'payload_id', 'basf2module', '...')
        model = GlobalTagPayload
#########################################################
class GlobalTagStatusTable(CdbWebTable):
    class Meta(CdbWebTable.Meta):
        model = GlobalTagStatus
#########################################################
class GlobalTagTypeTable(CdbWebTable):
    class Meta(CdbWebTable.Meta):
        model = GlobalTagType
#########################################################
class PayloadTable(CdbWebTable):
    iov = tables.Column(verbose_name='I0V:GT,Exp.Start,Run.Start,Exp.End,Run.End', empty_values=())

    def render_iov(self, record):
        retString=''
        gtps = GlobalTagPayload.objects.filter(payload_id=record.payload_id)
        if(gtps is None): return ''

        for gtp in gtps:
            gtn=GlobalTag.objects.get(global_tag_id=gtp.global_tag_id).name
            iovs=PayloadIov.objects.filter(global_tag_payload_id=gtp.global_tag_payload_id)
            if(iovs is None): return ''
            retString+=makeNamedLink('GlobalTag', 'gtid', gtp.global_tag_id, gtn)+'<br/>|  '
            #retString+='<b>'+gtn+'</b> ('+str(gtp.global_tag_id)+')<br/>|  '
            for iov in iovs:
                retString+=str(iov.exp_start)+','+str(iov.run_start)+','+str(iov.exp_end)+','+str(iov.run_end)+'  |  '

            retString+='<hr/>'

        return format_html(retString)
    
    def render_basf2_module_id(self, record):
        basf2name = Basf2Module.objects.get(pk=record.basf2_module_id).name
        
        return  mark_safe(makeIDlink('Payload', record.payload_id, basf2name)) # +':'+str(record.revision)
    
        ## can add this to the string if needed: basf2link = makelink('Basf2Module', 'id', value)
        #basf2name = Basf2Module.objects.get(pk=value).name
        #return mark_safe(makeIDlink('Basf2Module', value, basf2name)) # basf2link used to prepend



    # Retire this after initial experimentation as for large sets this is not performant
    # Effectively revert to separate sort on basf2 (payload name) and its revision
    # def order_basf2_module_id(self, QuerySet, is_descending):

    #     ordered = sorted(QuerySet, key=lambda x: (x.basf2moduleRev()), reverse=is_descending)
    #     pk_list = []
    #     for o in ordered: pk_list.append(o.payload_id)
        
    #     preserved	= Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)])
    #     ordered_qs	= Payload.objects.filter(pk__in=pk_list).order_by(preserved)

    #     return (ordered_qs, True)
    
        
    def render_payload_status_id(self, value):
        return PayloadStatus.objects.get(pk=value).name
        
    class Meta(CdbWebTable.Meta):
        model = Payload
        sequence = (
            'payload_id',
            'basf2_module_id',
            'revision',
            'checksum',
            'is_default',
            'deleted',
            'payload_url',
            'payload_status_id',
            'dtm_ins',
            'dtm_mod',
            'iov',
            '...')
        
        exclude = ('modified_by', 'description', 'base_url', )
#########################################################
class PayloadStatusTable(CdbWebTable):
    class Meta(CdbWebTable.Meta):
        model = PayloadStatus
#########################################################
class PayloadIovTable(CdbWebTable):
    def render_payload_iov_id(self, value):
        return self.render_id(value)

    class Meta(CdbWebTable.Meta):
        model = PayloadIov
        sequence = ('payload_iov_id', 'global_tag_payload_id', 'exp_start', 'exp_end', '...')
        exclude = ('modified_by', )
        
#########################################################
class PayloadIovRptTable(CdbWebTable):
    def render_payload_iov_rpt_id(self, value):
        return self.render_id(value)

    class Meta(CdbWebTable.Meta):
        model = PayloadIovRpt
        
