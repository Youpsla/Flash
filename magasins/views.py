# -*- coding: UTF-8 -*-
# Create your views here.
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from magasins.models import Magasin, MagasinForm
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_list
from django.views.generic import CreateView
import logging



@login_required
def user_magasins(request):
    magasins_list=Magasin.objects.filter(by=request.user)
    return object_list(request,
                       queryset=magasins_list,
                       template_object_name = "magasins",
                       )


class MagasinCreateView(CreateView):
    form_class = MagasinForm
    def form_valid(self,form):
        obj = form.save(commit=False)
        obj.by=self.request.user
        obj.save()
        return HttpResponseRedirect(reverse('user_magasins'))

@login_required
def redirectprofile(request):
        try: 
                profile = request.user.get_profile() 
                return HttpResponseRedirect(reverse('magasin'))
        except: 
                print "profil NOT found"
                return HttpResponseRedirect(reverse('profiles_create_profile'))
    