# -*- coding: utf-8 -*-

from django.forms.widgets import DateInput
from django import forms
from django.db import models
from Instantaneus.evenements.models import Evenement


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


    