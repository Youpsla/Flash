# -*- coding: utf-8 -*-


from django.forms.widgets import RadioSelect
from django.forms import ModelForm
from django import forms
from magasins.models import Magasin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.localflavor.fr.forms import FRPhoneNumberField
from django.contrib.localflavor.fr.forms import FRZipCodeField
from geolocalisation import geocoding





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
    # def clean(self):
        # """
       # Géocoding de l'adresse domicile

        # """
#         
        # if 'adresse' in self.cleaned_data :
            # adresse = self.cleaned_data['adresse']
        # if 'cp' in self.cleaned_data :
            # cp = self.cleaned_data['cp']
        # if 'ville' in self.cleaned_data :
            # ville = self.cleaned_data['cp']
        # (lat,lng) = geocoding(adresse, cp, ville)
        # print (lat,lng)
        # self.cleaned_data['lat_home'] = lat
        # self.cleaned_data['lng_home'] = lng
        # return self.cleaned_data

    class Meta:
        model = Magasin
        