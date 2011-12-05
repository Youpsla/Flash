from django.db import models
from django.contrib.localflavor.fr.forms import FRZipCodeField
from django.db.models.fields.__init__ import Field


class CpFrenchField(models.Field):
    empty_strings_allowed = False
    def __init__(self, *args, **kwargs):
        Field.__init__(self, *args, **kwargs)
        kwargs['max_length'] = 5
    
    def get_internal_type(self):
        return "CPFrenchField"
    
    def formfield(self, **kwargs):
        defaults = {'form_class':FRZipCodeField}
        defaults.update(kwargs)
        return super(CpFrenchField, self).formfield(**defaults)