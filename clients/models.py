from django.db import models
from Instantaneus.categories.models import Categories

import logging
logger = logging.getLogger(__name__)

class Customer (models.Model):

    email_adresse = models.EmailField(max_length=255, unique=True, verbose_name = "Adresse Email")
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    telephone = models.CharField(max_length=14, blank=True)
    adresse = models.CharField(max_length=255)
    cp = models.CharField(max_length=5)
    ville = models.CharField(max_length=255)
    pays = models.CharField(max_length=128, default='France')
    distance_max_home = models.CharField(max_length=5)
    lat_home = models.DecimalField(max_digits=13, decimal_places=10)
    lng_home = models.DecimalField(max_digits=13, decimal_places=10)
    adresse_pro = models.CharField(max_length=255, verbose_name = "Adresse professionnelle", blank=True)
    cp_pro = models.CharField(max_length=5)
    ville_pro = models.CharField(max_length=255)
    pays_pro = models.CharField(max_length=128, default='France')
    distance_max_pro = models.CharField(max_length=5)
    lat_pro = models.DecimalField(max_digits=13, decimal_places=10)
    lng_pro = models.DecimalField(max_digits=13, decimal_places=10)
    sms = models.BooleanField()
    email = models.BooleanField()
    phoneapp = models.BooleanField()
    category = models.ManyToManyField(Categories)

    
    # def __unicode__(self):
        # return unicode(self.Customer)

from django.db.models import signals
from django.dispatch import receiver
from Instantaneus.commandes.geolocalisation import magcli_client

@receiver(signals.post_save, sender=Customer, dispatch_uid="Customer_post_save_1")
def Customer_post_save(sender, instance, **kwargs):
    print 'signal Customer_post_save_1'
    print instance
    print 'pk', instance.pk
    print 'email', instance.email
    print 'category', instance.category
    magcli_client(client=instance)


