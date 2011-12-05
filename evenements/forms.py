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


class EvenementForm(forms.ModelForm):
    date_debut = forms.CharField(min_length = 10, widget = DateInput(format="%Y-%m-%d"))
    date_fin = forms.CharField(min_length = 10, widget = DateInput(format="%Y-%m-%d"))

    class Meta:
        model = Evenement

