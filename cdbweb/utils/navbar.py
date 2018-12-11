# custom imports
import	django_tables2 as tables
from django.utils.safestring		import mark_safe
from django.utils.html			import format_html

from info.listOfTables import listOfTables

# ---
def NavBarData(domain, what):
    data = []
    if(what=='Home'):
        style = 'style="color:red"'
    else:
        style = ''
    myDict = {'col0':mark_safe('<a href="http://'+domain+'/info"'+style+'>Home</a>')}

    i=1
    for t in listOfTables:
        if(what==t):
            style = 'style="color:red"'
        else:
            style=''

        myDict['col'+str(i)] = mark_safe('<a href="http://'+domain+'/info/'+t+'"'+style+'>'+t+'</a>')
        i+=1

    data.append(myDict)

    return data

# ---
class NavTable(tables.Table):
    N = len(listOfTables)
    for i in range(N):
        locals()['col'+str(i)] = tables.Column()
    
    def set_site(self, site=''):
        self.site=site
    class Meta:
        attrs	= {'class': 'paleblue'}

# ---
def TopTable(domain, what=None):
    t = NavTable(NavBarData(domain, what), show_header = False)
    t.set_site(domain)
    return t

