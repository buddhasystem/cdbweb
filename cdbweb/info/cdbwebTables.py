import	django_tables2	as tables

from django.urls	import reverse
from django.utils.safestring		import mark_safe
from django.conf	import settings

from .models		import *


def makelink(what, key, value):
    return mark_safe('<a href="http://%s%s?%s=%s">%s</a>'
                     % (settings.domain, reverse(what), key, value, value))


#########################################################
class CdbWebTable(tables.Table):
    def render_id(self, value):
        thisItemName = self.Meta.model.__name__
        return makelink(thisItemName,	'id',	value)
    
    def render_global_tag_id(self, value):
        return makelink('GlobalTag', 'gtid',	value)
    
    class Meta:
        attrs	= {'class': 'paleblue'}
        abstract=True
#-------------------------------------------------------


#########################################################

class AppMessageTable(CdbWebTable):
    class Meta(CdbWebTable.Meta):
        model = AppMessage
#########################################################
class Basf2ModuleTable(CdbWebTable):
    def basf2_module_id(self, value):
        return self.render_id(value)
    class Meta(CdbWebTable.Meta):
        model = Basf2Module
#########################################################
class GlobalTagTable(CdbWebTable):
    def render_global_tag_id(self, value):
        return self.render_id(value)
    class Meta(CdbWebTable.Meta):
        model = GlobalTag
#########################################################
class GlobalTagPayloadTable(CdbWebTable):
    def render_global_tag_payload_id(self, value):
        return self.render_id(value)
    class Meta(CdbWebTable.Meta):
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
class PayloadIovTable(tables.Table):
    class Meta:
        attrs	= {'class': 'paleblue'}
        model = PayloadIov
#########################################################
class PayloadIovRptTable(tables.Table):
    class Meta:
        attrs	= {'class': 'paleblue'}
        model = PayloadIovRpt
        
