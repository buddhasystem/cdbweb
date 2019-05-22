# Little helper functions for "views",
# lightweight stuff factored out for readability

from django.conf	import settings
#########################################################    
# ---
def addSnapshot(d):
    try:
        d['snapshot']=settings.SNAPSHOT
    except:
        pass
        
    if(settings.DBSERVER!=''): d['dbserver']=settings.DBSERVER # purely for display
    return d
#########################################################    
# ---
def addIdOrName(query, id_or_name, one_or_two):
    addition = ''
    
    if(id_or_name!=''):
        if(id_or_name.isdigit()):
            addition = 'gtid'+one_or_two+'='+id_or_name+'&'
        else:
            addition = 'gtname'+one_or_two+'='+id_or_name+'&'
            
    return query+addition

#########################################################    
# ---
def add_payloads(opcode, list4diff, payloads):
    for p in payloads:
        myDict = {
            'diff':opcode,
            'name':p.name,
            'rev': p.rev,
            'iov': p.readable_iov(),
        }
        list4diff.append(myDict)

    return list4diff
