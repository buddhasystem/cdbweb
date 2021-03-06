from django import forms

widgetSizes = {'run':'8', 'subrun':'4', 'dl':'3'}

#########################################################    
class boolSelector(forms.Form):
    def __init__(self, *args, **kwargs):
       self.what	= kwargs.pop('what')
       self.label	= kwargs.pop('label')
       self.init	= kwargs.pop('init')
       
       super(boolSelector, self).__init__(*args, **kwargs)
       # print(self.init)
       self.fields['check'] = forms.BooleanField(required=False, initial=self.init, label=self.label)

    def getval(self):
        check = self.cleaned_data['check']
        # print(check)
        return ('0','1')[check]
        
#########################################################    
class boxSelector(forms.Form):
    def __init__(self, *args, **kwargs):
       self.what	= kwargs.pop('what')
       self.states	= kwargs.pop('states')
       self.label	= kwargs.pop('label')

       super(boxSelector, self).__init__(*args, **kwargs)
       
       self.fields['stateChoice'].choices	= self.states # SELECTORS[self.what]['states']
       self.fields['stateChoice'].label		= self.label  # SELECTORS[self.what]['stateLabel']

    def handleBoxSelector(self):
        selectedStates = self.cleaned_data['stateChoice']
        if len(selectedStates):
            if('all' in selectedStates):
                return ''
            else:
                return 'state='+",".join(selectedStates)+'&'
        return ''

    stateChoice = forms.MultipleChoiceField(label='DUMMY',
                                            required=False,
                                            widget=forms.CheckboxSelectMultiple,
                                            choices=[('place', 'holder'),])

#########################################################    
class radioSelector(forms.Form):
    def __init__(self, *args, **kwargs):
       self.states	= kwargs.pop('states')
       self.label	= kwargs.pop('label')

       super(radioSelector, self).__init__(*args, **kwargs)
       
       self.fields['compChoice'].choices	= self.states
       self.fields['compChoice'].label		= self.label

    def handleRadioSelector(self):
        choice = self.cleaned_data['compChoice']
        return choice

    compChoice = forms.ChoiceField(label='DUMMY',
                                    required=False,
                                    widget=forms.RadioSelect,
                                    choices=[('place', 'holder'),])

#########################################################    
class dropDownGeneric(forms.Form):
    def __init__(self, *args, **kwargs):
       self.label	= kwargs.pop('label')
       self.choices	= kwargs.pop('choices')
       self.tag		= kwargs.pop('tag')
       self.fieldname	= self.tag # 'choice'
       
       super(dropDownGeneric, self).__init__(*args, **kwargs)
       
       self.fields[self.fieldname] = forms.ChoiceField(choices = self.choices, label = self.label, required=False)

    def handleDropSelector(self):
        selection = self.cleaned_data[self.fieldname]
        if(selection=='All' or selection==''):
            return ''
        else:
            return self.tag+'='+selection+'&'
#########################################################
#---
class twoFieldGeneric(forms.Form):
    def __init__(self, *args, **kwargs):
       self.label1	= kwargs.pop('label1')
       self.label2	= kwargs.pop('label2')
       
       self.field1	= kwargs.pop('field1')
       self.field2	= kwargs.pop('field2')
       
       self.init1	= kwargs.pop('init1')
       self.init2	= kwargs.pop('init2')

       super(twoFieldGeneric, self).__init__(*args, **kwargs)
       
       self.fields[self.field1] = forms.CharField(required=False, initial=self.init1, label=self.label1)
       self.fields[self.field2] = forms.CharField(required=False, initial=self.init2, label=self.label2)

    def getval(self, what):
        return self.cleaned_data[what]
   
#########################################################
#---
class oneFieldGeneric(forms.Form):
    def __init__(self, *args, **kwargs):
       self.label	= kwargs.pop('label')
       self.field	= kwargs.pop('field')
       try:
           self.init	= kwargs.pop('init')
       except:
           self.init	= ''


       super(oneFieldGeneric, self).__init__(*args, **kwargs)

       widgetSize = '10'
       if('idname' in self.field): widgetSize = 40
       
       self.fields[self.field] = forms.CharField(required=False, initial=self.init, label=self.label, widget=forms.TextInput(attrs={'size': widgetSize}) )

  
    def getval(self, what):
        # print(what, self[what].value()) # // diagnostics

        return self.cleaned_data[what]
   
#---
