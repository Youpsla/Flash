# -*- coding: UTF-8 -*-
from django.db import models
from Flash.magasins.models import Magasin
import djangotasks
from clients.models import Customer
from commandes.models import Magcli
#from django.db.models import signals

class Evenement (models.Model):
    magasin = models.ForeignKey(Magasin, editable=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    nom = models.CharField(max_length=250)
    titre = models.CharField(max_length=250)
    baseline = models.CharField(max_length=500)
    mentions = models.TextField()
    activation = models.BooleanField(editable=False)

    def clean(self):
        """
        Surcharge de la méthode clean().
        Vérification que la date de début d'évènement est antérieure à celle de fin.
        """
        from django.core.exceptions import ValidationError
        if(self.date_debut > self.date_fin):
            raise ValidationError('La date de début doit être antérieure à la date de fin de votre évènement')

#for signal in (signals.post_init, signals.post_save):
#    signal.connect(change_watcher, sender = Magasin, dispatch_uid=signal)



    




