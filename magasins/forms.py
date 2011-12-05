# -*- coding: utf-8 -*-


from django.forms.widgets import RadioSelect
from django import forms
from magasins.models import Magasin
from django.contrib.localflavor.fr.forms import FRZipCodeField





class MagasinForm(forms.Form):
    adresse = forms.CharField(max_length=255)
    cp = FRZipCodeField()
    ville = forms.CharField(max_length=255)
    distance_max_home = forms.ChoiceField(widget=RadioSelect(), choices=(
                     ('1','100 m'),
                     ('2','200 m'),
                     ('3','300 m'),
                     ('5','500 m'),
                     ('10','1 km'),
                     ('20','2 km'),
                     ('50','5 km'),
                     ('100','10 km'),
                     ))

    class Meta:
        model = Magasin
        