# Stub
from django.conf.urls import include, url

from . import views
from .listOfTables import listOfLinks

urlpatterns = [
    url(r'^$',		views.index,					name='index'),
    url(r'^gtcompare$',	views.gtcompare,				name='gtcompare'),
    url(r'^iovcheck$',	views.iovcheck,					name='iovcheck'),
]

for t in listOfLinks:
    u = t+'$'
    urlpatterns.append(url(u,views.data_handler,{'what':t},name=t))

    
#    url(r'/AppMessage',	views.data_handler,	{'what':'AppMessage'},	name='AppMessage'),
#    url(r'/Basf2Module',	views.data_handler,	{'what':'Basf2Module'},	name='Basf2Module'),

