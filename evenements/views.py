# -*- coding: UTF-8 -*-
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from evenements.forms import EvenementForm
from django.shortcuts import get_object_or_404
from evenements.models import Evenement
from magasins.models import Magasin
from commandes.tests import EvenementsMessages

class EvenementCreateView(CreateView):
    form_class = EvenementForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.magasin = get_object_or_404(Magasin, pk=kwargs['magasin_id'])
        #print "id_magasin est: %s" % self.magasin.pk
        return super(EvenementCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form, **kwargs):
        magasin = Magasin.objects.get(pk=self.magasin.pk)
        self.tmp=form.save(commit=False)
        print "pk", self.tmp.pk
        self.tmp.magasin = magasin
        print self.success_url
        self.tmp.save()
        pk = self.tmp.pk
        magasin_id=self.tmp.magasin.id
        return HttpResponseRedirect(reverse('evenement_details', args=[int(magasin_id), int(pk)]))

class EvenementDetailView(DetailView):
    model=Evenement
    context_object_name='evenement'


class EvenementUpdateView(UpdateView):
    form_class = EvenementForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.magasin = get_object_or_404(Magasin, pk=kwargs['magasin_id'])
        #print "id_magasin est: %s" % self.magasin.pk
        return super(EvenementUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form, **kwargs):
        magasin = Magasin.objects.get(pk=self.magasin.pk)
        self.tmp=form.save(commit=False)
        print "pk", self.tmp.pk
        self.tmp.magasin = magasin
        print self.success_url
        self.tmp.save()
        pk = self.tmp.pk
        magasin_id=self.tmp.magasin.id
        return HttpResponseRedirect(reverse('evenement_details', args=[int(magasin_id), int(pk)]))


class EvenementDeleteView(DeleteView):
    model=Evenement

@login_required
def activation(request, **kwargs):
    """ Fonction qui active un évènement et envoi les messages Emails.
        Appel à la classe EvenementsMessages.
        Prends en argument id_magasin et pk (Clé primaire de l'évènement).
        Retour sur la page de détail de l'évènement.
        """
    print kwargs
    magasin_id = kwargs['magasin_id']
    pk = kwargs['pk']
    evenement = get_object_or_404(Evenement, pk=pk)
    evenement.activation=1
    evenement.save()
    try:
        messages = EvenementsMessages(magasin_id, pk)
        messages.evenement_match_client()
        messages.evenement_envoi_email()
    except:
        print "Erreur dans l'envoi des messages"
    return HttpResponseRedirect(reverse('evenement_details', args=[int(magasin_id), int(pk)]))


