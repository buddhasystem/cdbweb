# Stub
from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^',		views.index,					name='index'),
    url(r'AppMessage',	views.data_handler,	{'what':'AppMessage'},	name='AppMessage'),
    url(r'Basf2Module', views.data_handler,	{'what':'Basf2Module'},	name='Basf2Module'),
]
