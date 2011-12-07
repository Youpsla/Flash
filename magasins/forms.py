# -*- coding: utf-8 -*-


from django.forms.widgets import RadioSelect
from django import forms
from magasins.models import Magasin
from django.contrib.localflavor.fr.forms import FRZipCodeField





class MagasinForm(forms.Form):
    adresse = forms.CharField(max_length=255)
    cp = FRZipCodeField()
    ville = forms.CharField(max_length=255)

    class Meta:
        model = Magasin
        