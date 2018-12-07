from django.contrib import admin
from .models import AppMessage

############
class AppMessageAdmin(admin.ModelAdmin):
    list_display = ('app_message_id', 'code', 'message', 'dtm_ins', 'dtm_mod')
    empty_value_display = '-empty-'
    
admin.site.register(AppMessage, AppMessageAdmin)

