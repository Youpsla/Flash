# -*- coding: utf-8 -*-

from django.forms.widgets import RadioSelect
from django import forms
from clients.models import Customer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.localflavor.fr.forms import FRPhoneNumberField
from django.contrib.localflavor.fr.forms import FRZipCodeField
from geolocalisation import get_lat_lng
from categories.models import Categories


class Step1Form(forms.Form):
    email_adresse = forms.EmailField(max_length=255)
    telephone = FRPhoneNumberField(required=False)
    
    def clean(self):
        """
       Test de l'unicité de l'aresse Email dans la base de données
        
        """
        
        if 'email_adresse' in self.cleaned_data :
            email = self.cleaned_data['email_adresse']
            try:
                Customer.objects.get(email_adresse=email)
            except ObjectDoesNotExist:
                return self.cleaned_data
            raise forms.ValidationError(u'Cette adresse Email est deja utilisée')

class Step2Form(forms.Form):
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
    def clean(self):
        """
       Géocoding de l'adresse domicile
        
        """
        
        if 'adresse' in self.cleaned_data :
            adresse = self.cleaned_data['adresse']
        if 'cp' in self.cleaned_data :
            cp = self.cleaned_data['cp']
        if 'ville' in self.cleaned_data :
            ville = self.cleaned_data['cp']
        location = '+'.join(filter(None, (adresse, cp, ville, 'FRANCE')))
        (lat,lng) = get_lat_lng(location)
        print (lat,lng)
        self.cleaned_data['lat_home'] = lat
        self.cleaned_data['lng_home'] = lng
        return self.cleaned_data

 
class Step3Form(forms.Form):
    adresse_pro = forms.CharField(max_length=255, required=False)
    cp_pro = FRZipCodeField(required=False)
    ville_pro = forms.CharField(max_length=255, required=False)
    distance_max_pro = forms.ChoiceField(widget=RadioSelect(), choices=(
                     ('1','100 m'),
                     ('3','300 m'),
                     ('5','500 m'),
                     ('10','1 km'),
                     ('20','2 km'),
                     ('50','5 km'),
                     ('100','10 km'),
                     ))

    def clean(self):
        """
       Géocoding de l'adresse pro
        
        """
        if 'adresse_pro' in self.cleaned_data :
            adresse_pro = self.cleaned_data['adresse_pro']
        if 'cp_pro' in self.cleaned_data :
            cp_pro = self.cleaned_data['cp_pro']
        if 'ville_pro' in self.cleaned_data :
            ville_pro = self.cleaned_data['cp_pro']
        location = '+'.join(filter(None, (adresse_pro, cp_pro, ville_pro, 'FRANCE')))
        (lat,lng) = get_lat_lng(location)
        print (lat,lng)
        self.cleaned_data['lat_pro'] = lat
        self.cleaned_data['lng_pro'] = lng
        return self.cleaned_data

class Step4Form(forms.Form):
    sms = forms.BooleanField(required=False)
    email = forms.BooleanField(required=False)
    #phoneapp = forms.BooleanField()

class Step5Form(forms.Form):
    category = forms.ModelMultipleChoiceField(queryset=Categories.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)
    
    def clean(self):
        """
       Test pour savoir si l'utilisateur a au moins sélectionné 5 appétances.
        
        """
        d = self.cleaned_data.iteritems()
        print d
        
        for k,v in d:
            print k,v
            print "Nbr de choix %s" % len(v)
            if len(v) < 5:
                raise forms.ValidationError(u'Vous devez sélectionner 5 choix au minimum')
            else:
                print self.cleaned_data
                print "dada"
                return self.cleaned_data

        
class TestUserForm(forms.Form):
    email_adresse = forms.EmailField(max_length=255)
    
class TestAppetancesForm (forms.Form):
    id = forms.IntegerField()
    choix = forms.BooleanField()
    