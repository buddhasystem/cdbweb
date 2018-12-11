import	django_tables2	as tables
from .models		import *

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
class PayloadIovTable(tables.Table):
    class Meta:
        attrs	= {'class': 'paleblue'}
        model = PayloadIov
#########################################################
class PayloadIovRptTable(tables.Table):
    class Meta:
        attrs	= {'class': 'paleblue'}
        model = PayloadIovRpt
        
