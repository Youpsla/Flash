# -*- coding: UTF-8 -*-
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from evenements.forms import EvenementForm
from django.shortcuts import get_object_or_404
from evenements.models import Evenement
from magasins.models import Magasin
from commandes.routage import Messages

import logging
logger = logging.getLogger(__name__)


class EvenementCreateView(CreateView):
    form_class = EvenementForm
    
    def dispatch(self, *args, **kwargs):
        self.magasin = get_object_or_404(Magasin, pk=kwargs['magasin_id'])
        return super(EvenementCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form, **kwargs):
        logger.debug('Début de validation du formulaire de création d\'évènement')
        magasin = Magasin.objects.get(pk=self.magasin.pk)
        logger.debug('Magasin: %s' % magasin.pk)
        self.tmp=form.save(commit=False)
        self.tmp.magasin = magasin
        self.tmp.save()
        pk = self.tmp.pk
        magasin_id=self.tmp.magasin.id
        logger.debug('Le formulaire de création du magasin a passé les contrôles de validation')
        return HttpResponseRedirect(reverse('evenement_details', args=[int(magasin_id), int(pk)]))

class EvenementDetailView(DetailView):
    print __name__
    model=Evenement
    context_object_name='evenement'
    logger.debug('Affichage détaillé de l\'évènement: %s' % object)


class EvenementUpdateView(UpdateView):
    form_class = EvenementForm

    def dispatch(self, *args, **kwargs):
        self.magasin = get_object_or_404(Magasin, pk=kwargs['magasin_id'])
        #print "id_magasin est: %s" % self.magasin.pk
        return super(EvenementUpdateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form, **kwargs):
        logger.debug('Modification évènement: %s - magasin: %s' % (self.get_object().pk, self.magasin.pk))
        self.tmp=form.save(commit=False)
        self.tmp.magasin = self.magasin
        self.tmp.save()
        logger.debug('Modification évènement: %s - magasin: %s sauvegardées' % (self.get_object().pk, self.magasin.pk))
        pk = self.tmp.pk
        magasin_id=self.magasin.id
        return HttpResponseRedirect(reverse('evenement_details', args=[int(magasin_id), int(pk)]))


class EvenementDeleteView(DeleteView):
    model=Evenement
    logger.debug('Suppression évènement: %s' % (object))

@login_required
def activation(request, **kwargs):
    """ Fonction qui active un évènement et envoi les messages Emails.
        Appel à la classe Messages.
        Prends en argument pk (Clé primaire de l'évènement).
        Retour sur la page de détail de l'évènement.
        """
    magasin_id = kwargs['magasin_id']
    pk = kwargs['pk']
    evenement = get_object_or_404(Evenement, pk=pk)
    print evenement.__dict__
    magasin =  evenement.magasin

    logger.debug('Début activation évènement: %s - magasin: %s' % (evenement.pk, magasin_id))
    messages = Messages(request, magasin, evenement)
    messages.liste_clients()
    messages.liste_emails()
    messages.evenement_envoi_email()
    magasin =  evenement.Magasin
    evenement.activation=1
    evenement.save()
    return HttpResponseRedirect(reverse('evenement_details', args=[int(magasin_id), int(pk)]))