# core django
from django.shortcuts	import render
from django.http	import HttpResponse

from utils.navbar	import TopTable

#########################################################    
def index(request):

    template = 'index.html'

    host	= request.GET.get('host','')
    domain	= request.get_host()

    navTable = TopTable(domain)
    navTable.set_site(domain)
    d = dict(domain=domain, host=host, hometable=navTable)

    return render(request, template, d)


# general request handler for summary type of a table
def data_handler(request, what):
    return HttpResponse(what)
