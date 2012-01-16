# -*- coding: utf-8 -*-

from django import forms
from clients.models import Customer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.localflavor.fr.forms import FRPhoneNumberField
from django.contrib.localflavor.fr.forms import FRZipCodeField
from commandes.geolocalisation import get_lat_lng
from categories.models import Categories

import logging
logger = logging.getLogger(__name__)

class Step1Form(forms.Form):

    logger.debug('Initialisation du step 1 du formulaire clients')
    email_adresse = forms.EmailField(max_length=255, label='Adresse Email*', help_text='Nécessaire pour recevoir les offres par SMS')
    telephone = FRPhoneNumberField(required=False, label='Téléphone portable', help_text='Nécessaire pour recevoir les offres par SMS')
    
    def clean(self):
        """
       Test de l'unicité de l'adresse Email dans la base de données
        
        """
        
        if 'email_adresse' in self.cleaned_data :
            email = self.cleaned_data['email_adresse']
            try:
                logger.debug('Test de la présence de l\'email saisi en BDD')
                Customer.objects.get(email_adresse=email)
            except ObjectDoesNotExist:
                logger.debug('%s non présent en BDD' % email)
                return self.cleaned_data
            msg = u"Cette adresse Email est déjà utilisée"
            logger.debug('%s déjà présent en BDD' % email)
            self._errors["email_adresse"] = self.error_class([msg])


class Step2Form(forms.Form):
    logger.debug('Initialisation du step 2 du formulaire clients')
    adresse = forms.CharField(max_length=255, label='Adresse*')
    cp = FRZipCodeField(label='Code postal*')
    ville = forms.CharField(widget=forms.TextInput , max_length=255, label='Ville*')
    distance_max_home = forms.ChoiceField(widget=forms.Select, help_text='Distance maximale entre cette adresse et le magasin', label='Distance max', choices=(
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
        logger.debug('Initialisation méthode clean step 2')
        if 'adresse' in self.cleaned_data and 'cp' in self.cleaned_data and 'ville' in self.cleaned_data :
            logger.debug('Les champs adresse, cp et ville sont valides')
            adresse = self.cleaned_data['adresse']
            cp = self.cleaned_data['cp']
            ville = self.cleaned_data['ville']
            location = '+'.join(filter(None, (adresse, cp, ville, 'FRANCE')))
            results =  get_lat_lng(location)
            if results['status'] == 0:
                logger.info('La géolocalisation a échouée')
                msg = u"Problème de géolocalisation"
                self._errors["adresse"] = self.error_class([msg])
                self._errors["cp"] = self.error_class([msg])
                self._errors["ville"] = self.error_class([msg])
                raise forms.ValidationError("Erreure de géolocalisation de votre adresse")
            else:
                self.cleaned_data['lat_home'] = results['lat']
                self.cleaned_data['lng_home'] = results['lng']
                logger.info('La géolocalisation est un succès')
                return self.cleaned_data

 
class Step3Form(forms.Form):
    logger.debug('Initialisation du step 3 du formulaire clients')
    adresse_pro = forms.CharField(max_length=255, label='Adresse professionnelle', required=False)
    cp_pro = FRZipCodeField(required=False, label='Code postal')
    ville_pro = forms.CharField(max_length=255, required=False, label='Ville')
    distance_max_pro = forms.ChoiceField(widget=forms.Select, label='Distance*', help_text='Distance maximale entre cette adresse et le magasin', required=False, choices=(
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
        logger.debug('Initialisation méthode clean step 3')
        if 'adresse_pro' in self.cleaned_data and 'cp_pro' in self.cleaned_data and 'ville_pro' in self.cleaned_data :
            logger.debug('Les champs adresse_pro, cp_pro et ville_pro sont valides')
            adresse = self.cleaned_data['adresse_pro']
            cp = self.cleaned_data['cp_pro']
            ville = self.cleaned_data['cp_pro']
            location = '+'.join(filter(None, (adresse, cp, ville, 'FRANCE')))
            results =  get_lat_lng(location)
            if results['status'] == 0:
                logger.info('La géolocalisation a échouée')
                msg = u"Problème de géolocalisation"
                self._errors["adresse_pro"] = self.error_class([msg])
                self._errors["cp_pro"] = self.error_class([msg])
                self._errors["ville_pro"] = self.error_class([msg])
                raise forms.ValidationError("Erreure de géolocalisation de votre adresse")
            else:
                self.cleaned_data['lat_pro'] = results['lat']
                self.cleaned_data['lng_pro'] = results['lng']
                logger.info('La géolocalisation est un succès')
                return self.cleaned_data

class Step4Form(forms.Form):
    logger.debug('Initialisation du step 4 du formulaire clients')
    sms = forms.BooleanField(required=False)
    email = forms.BooleanField(required=False)
    #phoneapp = forms.BooleanField()

class Step5Form(forms.Form):
    category = forms.ModelMultipleChoiceField(queryset=Categories.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)
    logger.debug('Initialisation du step 5 du formulaire clients')
    def clean(self):
        """
       Test pour savoir si l'utilisateur a au moins sélectionné MIN_NB_CAT catégories.
        """
        MIN_NB_CAT = 5
        logger.debug('MIN_NB_CAT = %s' % (MIN_NB_CAT))
        if self.cleaned_data.has_key('category'):
            logger.debug('Au moins 1 catégorie a été sélectionnée')
            nb_cat = len(self.cleaned_data['category'])
            if nb_cat < MIN_NB_CAT:
                logger.debug('%s catégories ont été sélectionnées. %s minimum' % (nb_cat, MIN_NB_CAT))
                raise forms.ValidationError(u'Vous devez sélectionner 5 thématiques au minimum')
            else:
                logger.debug('%s de catégories ont été sélectionnées' % nb_cat)
                return self.cleaned_data

    