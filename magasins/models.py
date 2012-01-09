# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.forms import widgets
from decimal import Decimal
from django.db.models import signals
from django.dispatch import receiver
from commandes.geolocalisation import magcli_magasin
from django.db.models import get_model
from categories.models import Categories
from datetime import datetime
from django.contrib.localflavor.fr.forms import FRPhoneNumberField


class MagasinOwnerProfile(models.Model):
    GENDER_CHOICES = (
            ('M', 'Monsieur'),
            ('MDE', 'Madame'),
            ('MELLE', 'Mademoiselle'),
        )
    user = models.ForeignKey(User, unique=True)
    genre = models.CharField(max_length=5, choices=GENDER_CHOICES)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, verbose_name = "Prénom")
    telephone = models.CharField(max_length=14, verbose_name = "Téléphone")
    
class MagasinOwnerProfileForm(ModelForm):
    telephone = FRPhoneNumberField(label='Téléphone')

    class Meta:
        model = MagasinOwnerProfile
        exclude = ('user',)

class Magasin (models.Model):
    nom = models.CharField(max_length=255, verbose_name = "Raison sociale")
    nom_commercial = models.CharField(max_length=255, verbose_name = "Nom commercial")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    adresse = models.CharField(max_length=255)
    cp = models.CharField(max_length=5)
    ville = models.CharField(max_length=255)
    pays = models.CharField(max_length=128, default='France')
    category = models.ForeignKey(Categories, verbose_name = "Catégorie")
    lat = models.DecimalField(max_digits=13, decimal_places=10)
    lng = models.DecimalField(max_digits=13, decimal_places=10)
    by = models.ForeignKey(User, editable=False)

    def magasin_evenements(self):
        Evenement = get_model('evenements','Evenement')
        return Evenement.objects.filter(magasin=self)
    
    @property
    def is_locked(self):
        etat = ''
        Evenement = get_model('evenements','Evenement')
        liste_evenements=Evenement.objects.filter(magasin=self)
        for e in liste_evenements:
            if e.activation == True:
                if e.date_fin > datetime.now():
                    etat = True
                    break
        else:
            etat = False
        print etat
        return etat


    
@receiver(signals.post_save, sender=Magasin, dispatch_uid="Magasin_most_save")
def Magasin_post_save(sender, instance, **kwargs):
    if kwargs['created']==True:
        etat='creation'
        magcli_magasin(mag=instance, etat=etat)
    elif kwargs['created']==False:
        etat='update'
        magcli_magasin(mag=instance, etat=etat)

            
#from magasins.signals import change_watcher
#for signal in (signals.pre_save, signals.post_save):
#    signal.connect(change_watcher, sender = Magasin, dispatch_uid=signal)


from django.contrib.localflavor.fr.forms import FRZipCodeField
from commandes.geolocalisation import get_lat_lng

class MagasinForm(ModelForm):
    class BlankIntField(forms.IntegerField):
        def clean(self, value):
            if not value:
                value = 0
            return Decimal(value)
    lat = BlankIntField(widget = widgets.HiddenInput())
    lng = BlankIntField(widget = widgets.HiddenInput())
    category = forms.ModelChoiceField(widget=forms.Select , queryset=Categories.objects.all().order_by('nom'))
    cp = FRZipCodeField(widget=forms.TextInput )


    class Meta:
        model = Magasin
        exclude = ('by',)

    def clean(self):
        print "Appel methode Clean de la class MagasinForm"
        if self.cleaned_data.has_key('adresse') and self.cleaned_data.has_key('cp') and self.cleaned_data.has_key('ville'):
            adresse = self.cleaned_data['adresse']
            cp = str(self.cleaned_data['cp'])
            ville = self.cleaned_data['ville']
            print "Les données saisies sont: %s, %s, %s" % (adresse, cp, ville)
            location = '+'.join(filter(None, (adresse, cp, ville, 'FRANCE')))
            tmp = get_lat_lng(location)
            lat = tmp['lat']
            lng = tmp['lng']
            status = tmp['status']
            print "Résultat du géocodage : statut - %s, latitude - %s, longitude - %s" % (lat, status, lng)
            self.cleaned_data['lat'] = lat
            self.cleaned_data['lng'] = lng
        else:
            print "Des champs sont vides dans le formulaire : adresse, cd ou ville"
            pass
        return self.cleaned_data 
