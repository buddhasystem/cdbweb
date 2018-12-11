# Stub
from django.conf.urls import include, url

from . import views
from .listOfTables import listOfTables

urlpatterns = [
    url(r'^$',		views.index,					name='index'),
]

for t in listOfTables:
    u = t+'$'
    urlpatterns.append(url(u,views.data_handler,{'what':t},name=t))

    
#    url(r'/AppMessage',	views.data_handler,	{'what':'AppMessage'},	name='AppMessage'),
#    url(r'/Basf2Module',	views.data_handler,	{'what':'Basf2Module'},	name='Basf2Module'),

