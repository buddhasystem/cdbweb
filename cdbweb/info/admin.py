from django.contrib import admin
from .models import AppMessage, Basf2Module, GlobalTag, GlobalTagType, Payload, \
 PayloadIov, PayloadIovRpt, PayloadStatus

############
class AppMessageAdmin(admin.ModelAdmin):
    list_display = ('app_message_id', 'code', 'message', 'dtm_ins', 'dtm_mod')
    empty_value_display = '-empty-'
    
admin.site.register(AppMessage, AppMessageAdmin)

############
class Basf2ModuleAdmin(admin.ModelAdmin):
    list_display = ('basf2_module_id', 'name', 'next_revision', 'description', 'dtm_ins','dtm_mod','modified_by')
    empty_value_display = '-empty-'
    
admin.site.register(Basf2Module, Basf2ModuleAdmin)

############
class GlobalTagAdmin(admin.ModelAdmin):
    list_display = ('global_tag_id',
                    'name',
                    'is_default',
                    'description',
                    'global_tag_status_id', # changed after model cleanup
                    'global_tag_type_id', # ditto
                    'dtm_ins',
                    'dtm_mod',
                    'modified_by')
    empty_value_display = '-empty-'
    
admin.site.register(GlobalTag, GlobalTagAdmin)

############
class GlobalTagTypeAdmin(admin.ModelAdmin):
    list_display = ('global_tag_type_id',
                    'name',
                    'description',
                    'dtm_ins',
                    'dtm_mod')

    empty_value_display = '-empty-'
    
admin.site.register(GlobalTagType, GlobalTagTypeAdmin)

############
class PayloadAdmin(admin.ModelAdmin):
    list_display = ('payload_id',
                    'basf2_module_id',
                    'revision',
                    'description',
                    'is_default',
                    'base_url',
                    'checksum',
                    'payload_status_id',
                    'deleted',
                    'dtm_ins',
                    'dtm_mod',
                    'modified_by')

    empty_value_display = '-empty-'
    
admin.site.register(Payload, PayloadAdmin)

############
class PayloadIovAdmin(admin.ModelAdmin):
    list_display = ('payload_iov_id',
                    'global_tag_payload_id',
                    'exp_start',
                    'run_start',
                    'exp_end',
                    'run_end',
                    'dtm_ins',
                    'dtm_mod',
                    'modified_by')

    empty_value_display = '-empty-'
    
admin.site.register(PayloadIov, PayloadIovAdmin)

############
class PayloadIovRptAdmin(admin.ModelAdmin):
    list_display = ('payload_iov_rpt_id',
                    'global_tag_payload_id',
                    'dtm_ins',
                    'dtm_mod',
                    'global_tag_id',
                    'gt_name',
                    'b2m_name',
                    'exp_start',
                    'exp_end',
                    'run_start',
                    'run_end',
                    'payload_id',
                    'payload_iov_id')

    empty_value_display = '-empty-'
    
admin.site.register(PayloadIovRpt, PayloadIovRptAdmin)

############
class PayloadStatusAdmin(admin.ModelAdmin):
    list_display = ('payload_status_id',
                    'name',
                    'description',
                    'dtm_ins',
                    'dtm_mod')

    empty_value_display = '-empty-'
    
admin.site.register(PayloadStatus, PayloadStatusAdmin)

