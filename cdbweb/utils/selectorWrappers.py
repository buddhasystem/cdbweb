from .selectorUtils import dropDownGeneric, oneFieldGeneric, boxSelector, boolSelector, radioSelector


# ---
def gtStatusSelector(request, status, gtStatusChoices):
    if request is None:
        return dropDownGeneric(initial={'status':status}, label='Status', choices=gtStatusChoices, tag='status')
    else:
        return dropDownGeneric(request.POST, initial={'status':status}, label='Status', choices=gtStatusChoices, tag='status')

# ---
def gtTypeSelector(request, gttype, gtTypeChoices):
    if request is None:
        return dropDownGeneric(initial={'gttype':gttype}, label='Type', choices=gtTypeChoices, tag = 'gttype')
    else:
        return dropDownGeneric(request.POST, initial={'gttype':gttype}, label='Type', choices=gtTypeChoices, tag = 'gttype')

# ---
def pageSelector(request, perpage, pageChoices):
    if request is None:
        return dropDownGeneric(initial = {'perpage':perpage}, label = 'items per page', choices=pageChoices, tag = 'perpage')
    else:
        return dropDownGeneric(request.POST, initial = {'perpage':perpage}, label = 'items per page', choices=pageChoices, tag = 'perpage')

# ---
def checkAndAdd(query, selector, key):
    value = None
    addition = ''
    if selector.is_valid():
        value=selector.getval(key)
    else:
        return query
    
    if value=='':
        return query
    else:
        addition=key+'='+value+'&'
        return query+addition
        
