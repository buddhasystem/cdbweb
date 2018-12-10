# custom imports
import	django_tables2 as tables
from django.utils.safestring		import mark_safe
from django.utils.html			import format_html


# ---
def NavBarData(domain):
    data = []
    data.append({
        'col1':mark_safe('<a href="http://'+domain+'/info">Home</a>'),
        'col2':mark_safe('<a href="http://'+domain+'/info/AppMessage/">AppMessage</a>'),
        'col3':mark_safe('<a href="http://'+domain+'/info/Basf2Module/">Basf2Module</a>'),
    })

    return data
# ---
class NavTable(tables.Table):
    col1 = tables.Column()
    col2 = tables.Column()
    col3 = tables.Column()
    
    def set_site(self, site=''):
        self.site=site
    class Meta:
        attrs	= {'class': 'paleblue'}

# ---
def TopTable(domain):
    t = NavTable(NavBarData(domain), show_header = False)
    return t

