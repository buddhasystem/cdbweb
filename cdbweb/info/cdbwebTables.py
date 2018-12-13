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
        
