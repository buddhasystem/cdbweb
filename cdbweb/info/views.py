from django.shortcuts import render
from django.http			import HttpResponse


#########################################################    
def index(request):
    return HttpResponse('index')


# general request handler for summary type of a table
def data_handler(request, what):
    return HttpResponse(what)
