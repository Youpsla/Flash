from django.db import models

class Magcli (models.Model):
    client = models.ForeignKey('clients.Customer', editable=False)
    magasin = models.ForeignKey('magasins.Magasin', editable=False)
    distance_home = models.IntegerField(null=True)
    distance_home_pied = models.IntegerField(null=True)
    distance_home_voiture = models.IntegerField(null=True)
    temps_home_pied = models.IntegerField(null=True)
    temps_home_voiture = models.IntegerField(null=True)
    distance_pro = models.IntegerField(null=True)
    distance_pro_pied = models.IntegerField(null=True)
    distance_pro_voiture = models.IntegerField(null=True)
    temps_pro_pied = models.IntegerField(null=True)
    temps_pro_voiture = models.IntegerField(null=True)
    match_category = models.NullBooleanField (null=True)
    match = models.NullBooleanField (null=True)
    
    class Meta:
        unique_together = ("client", "magasin")
    

    
