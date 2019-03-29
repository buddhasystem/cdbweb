3
# custom imports
import	django_tables2 as tables
from django.utils.safestring		import mark_safe
from django.utils.html			import format_html

from info.listOfTables import listOfTables


styles = ('','style="color:red"')

# ---
def NavBarData(domain, what):
    data = []
        
    myDict = {'col0':mark_safe('<a href="http://'+domain+'/"'+styles[what=='Home']+'>Home</a>')}

    i=1
    for t in listOfTables:
        myDict['col'+str(i)] = mark_safe('<a href="http://'+domain+'/'+t+'"'+styles[what==t]+'>'+t+'</a>')
        i+=1

    gtc='Global Tag Comparison'
    myDict['col'+str(i)] = mark_safe('<a href="http://'+domain+'/gtcompare"'+styles[what==gtc]+'>Global Tag Comparison</a>')
    i+=1

    data.append(myDict)
    return data

# ---
class NavTable(tables.Table):
    N = len(listOfTables)+2 # Adding count for non-table entries Home and GTcompare.
    for i in range(N):
        locals()['col'+str(i)] = tables.Column()
    
    def set_site(self, site=''):
        self.site=site
    class Meta:
        attrs	= {'class': 'paleblue'}

# ---
def TopTable(domain, what=None):
    content = NavBarData(domain, what)
    t = NavTable(content, show_header = False)
    t.set_site(domain)
    return t

