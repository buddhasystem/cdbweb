import	django_tables2	as tables

from django.urls	import reverse
from django.utils.safestring		import mark_safe
from django.conf	import settings

from .models		import *


def makelink(what, key, value):
    return mark_safe('<a href="http://%s%s?%s=%s">%s</a>'
                     % (settings.domain, reverse(what), key, value, value))


#########################################################
# Base abstract class for all the "general" tables in
# CDBweb. Due to the original naming convention where
# each pk has a different name in each table (!) we
# need to overload the id renderer where needed.


class CdbWebTable(tables.Table):
    def render_id(self, value):
        thisItemName = self.Meta.model.__name__
        return makelink(thisItemName,	'id',	value)
    
    def render_global_tag_id(self, value):
        return makelink('GlobalTag', 'gtid',	value)
    
    def render_global_tag_payload_id(self, value):
        return makelink('GlobalTagPayload', 'id',	value)
    
    def render_payload_id(self, value):
        return makelink('Payload', 'id',	value)
    
    def render_payload_iov_id(self, value):
        return makelink('PayloadIov', 'id',	value)
    
    def render_basf2_module_id(self, value):
        return makelink('Basf2Module', 'id',	value)

    class Meta:
        attrs	= {'class': 'paleblue'}
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

    class Meta(CdbWebTable.Meta):
        model = Basf2Module
#########################################################
class GlobalTagTable(CdbWebTable):
    numberOfGlobalTagPayloads	= tables.Column(verbose_name='# of GT Payloads', empty_values=())
    basf2modules		= tables.Column(verbose_name='Distinct Basf2 Modules', empty_values=())
    
    def render_global_tag_id(self, value):
        return self.render_id(value)

    def render_basf2modules(self, record):
        the_payloads = GlobalTagPayload.objects.filter(global_tag_id=record.global_tag_id).values_list('payload_id')
        if(len(the_payloads)==0):
            return 'Not Found'
        
        the_modules	= Payload.objects.filter(payload_id__in=the_payloads).values_list('basf2_module_id', flat=True)
        module_names	= list(Basf2Module.objects.filter(basf2_module_id__in=the_modules).values_list('name', flat=True).distinct())

    
        separator = ','
        f =  separator.join(module_names)
        rendered_value = str(len(module_names))+": "+f
        return rendered_value

        
    def render_numberOfGlobalTagPayloads(self, record):
        the_global_tag_payloads	= GlobalTagPayload.objects.filter(global_tag_id=record.global_tag_id)
        if(len(the_global_tag_payloads)==0):
           return 'Not Found'

        return len(the_global_tag_payloads)
        
    class Meta(CdbWebTable.Meta):
        model = GlobalTag
#########################################################
class GlobalTagPayloadTable(CdbWebTable):
    basf2module	= tables.Column(verbose_name='Basf2Module', empty_values=())
    
    def render_global_tag_payload_id(self, value):
        return self.render_id(value)

    def render_basf2module(self, record):
        
        the_payloads	= Payload.objects.filter(payload_id=record.payload_id)
        if(len(the_payloads)==0):
           return 'Not Found'

        p = the_payloads[0]
        the_modules	= Basf2Module.objects.filter(basf2_module_id=p.basf2_module_id)
        m = the_modules[0]
        
        return m.name

    class Meta(CdbWebTable.Meta):
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
    class Meta(CdbWebTable.Meta):
        model = Payload
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
#########################################################
class PayloadIovRptTable(CdbWebTable):
    def render_payload_iov_rpt_id(self, value):
        return self.render_id(value)

    class Meta(CdbWebTable.Meta):
        model = PayloadIovRpt
        
