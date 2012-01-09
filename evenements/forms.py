# -*- coding: utf-8 -*-

from django.forms.widgets import DateInput
from django import forms
from django.db import models
from evenements.models import Evenement


def make_custom_datefield(f):
    formfield = f.formfield()
    if isinstance(f, models.DateTimeField):
        formfield.widget.format = '%Y-%m-%d %H:%M:%S'
        formfield.widget.attrs.update({'class':'datePicker', 'readonly':'true'})
    return formfield


#from uni_form.helper import FormHelper
#from uni_form.layout import Submit, Layout, Fieldset, ButtonHolder
class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        
    date_debut = forms.CharField(min_length = 10, widget = DateInput(format="%Y-%m-%d"))
    date_fin = forms.CharField(min_length = 10, widget = DateInput(format="%Y-%m-%d"))
    
#    class Meta:
#        model = Evenement
#        
#    def __init__(self, *args, **kwargs):
#        self.helper = FormHelper()
#        self.helper.form_class = 'blueForms'
#        self.helper.form_method = 'post'
#        self.helper.form_action = ''
#        self.helper.form_id = 'id-evenementForm'
#        self.style= 'inline'
#        self.helper.layout = Layout(
#            Fieldset(
#                     'Ajouter / Modifier un évènement',
#                     'date_debut',
#                     'date_fin',
#                     'nom',
#                     'titre',
#                     'baseline',
#                     'mentions',
#                     ),
#            ButtonHolder(
#                Submit('submit', 'Envoyer')
#                )
#                )
#
#        return super(EvenementForm, self).__init__(*args, **kwargs)

    