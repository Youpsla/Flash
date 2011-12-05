from django.db import models
from categories.models import Categories


class Customer (models.Model):

    email_adresse = models.EmailField(max_length=255, unique=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    telephone = models.CharField(max_length=14, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    cp = models.CharField(max_length=5)
    ville = models.CharField(max_length=255)
    pays = models.CharField(max_length=128, default='France')
    distance_max_home = models.CharField(max_length=5)
    lat_home = models.DecimalField(max_digits=13, decimal_places=10)
    lng_home = models.DecimalField(max_digits=13, decimal_places=10)
    adresse_pro = models.CharField(max_length=255, blank=True)
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

class TestUser (models.Model):
    email_adresse = models.EmailField(max_length=255, unique=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    

class TestAppetances (models.Model):
    client = models.IntegerField(max_length=11, unique=True)
    choix = models.BooleanField()
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return unicode(self.Customer)