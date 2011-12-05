from django.db import models

# Create your models here.

class Categories (models.Model):
    category = models.CharField(max_length=200)
        
    def __unicode__(self):
        return unicode(self.category)
