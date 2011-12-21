# -*- coding: utf-8 -*-


#from magasins.models import Magasin
#from categories.models import Categories
#from django.contrib.localflavor.fr.forms import FRZipCodeField
#from commandes.geolocalisation import get_lat_lng
#from django import forms
#from bootstrap.forms import BootstrapForm, Fieldset
#from django.forms import widgets
#from decimal import Decimal
#
#
#class MagasinForm(BootstrapForm):
#    class Meta:
#        model = Magasin
#        exclude = ('by',)
#        layout = (
#                  Fieldset("Enregistrement d'un nouveau magasin",
#                           "nom",
#                           "nom_commercial",
#                           "adresse",
#                           "cp",
#                           "ville",
#                           "pays",
#                           "category",),
#                  )
#
#    
#    class BlankIntField(forms.IntegerField):
#        def clean(self, value):
#            if not value:
#                value = 0
#            return Decimal(value)
#        
#    lat = BlankIntField(widget = widgets.HiddenInput())
#    lng = BlankIntField(widget = widgets.HiddenInput())
#    category = forms.ChoiceField(widget=forms.Select (attrs={'class':'span3'}), queryset=Categories.objects.all().order_by('nom'))
#    cp = FRZipCodeField(widget=forms.TextInput (attrs={'class':'span2'}))
#    pays = forms.CharField(widget=forms.TextInput (attrs={'class':'span2'}))
#    adresse = forms.CharField(widget=forms.TextInput (attrs={'class':'span5'}))
#    ville = forms.CharField(widget=forms.TextInput (attrs={'class':'span3'}))
#
#
#
#    def clean(self):
#        print "appel methode Clean"
#        if self.cleaned_data.has_key('adresse') and self.cleaned_data.has_key('cp') and self.cleaned_data.has_key('ville'):
#            print self.cleaned_data['adresse']
#            print self.cleaned_data['cp']
#            print self.cleaned_data['ville']
#            adresse = self.cleaned_data['adresse']
#            cp = str(self.cleaned_data['cp'])
#            ville = self.cleaned_data['ville']
#            location = '+'.join(filter(None, (adresse, cp, ville, 'FRANCE')))
#            (lat,lng) = get_lat_lng(location)
#            self.cleaned_data['lat'] = lat
#            self.cleaned_data['lng'] = lng
#            print "Lattitude: ", lat
#            print "Longitude: ", lng
#        else:
#            pass
#        return self.cleaned_data      