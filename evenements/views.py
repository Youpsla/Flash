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
from commandes.models import Magcli
from django.db.models import F
from django.db.models import Q
from django_mailer import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives
import settings

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



class EnvoiMessages():
    
    @method_decorator(login_required)
    def match_evenement_clients(self,magasin_id):
        magasin_id=magasin_id
        """
        Fonction qui fait le raprochement entre un évènement et les clients qui y sont élligibles.
        Les criètres sont les distances home et pro ainsi que la catégorie.
        Argument : magasin_id
        """
        #Sélection des clients répondant aux critères d'appétance et de distance géographiques
        liste_client_magcli = Magcli.objects.filter(Q(magasin=magasin_id), Q(distance_home__gt= F('client__distance_max_home')) | Q(distance_pro__gt= F('client__distance_max_pro')), Q(magasin__category = F('client__category'))).select_related('client')
        for i in liste_client_magcli:
            print "Distance_max_home %s - Distance_home %s" % (i.client.distance_max_home, i.distance_home)
            print "Distance_max_pro %s - Distance_pro %s" % (i.client.distance_max_pro, i.distance_pro)
            print i.magasin.pk
        return liste_client_magcli
    
#    @method_decorator(login_required)
#    def envoi(self, **kwargs):
#        liste = kwargs[liste_client_magcli]
#        pass

    @method_decorator(login_required)
    def composition_message(self, **kwargs):
        magasin_nom = kwargs['magasin_nom']
        magasin_adresse = kwargs['magasin_adresse']
        magasin_cp = kwargs['magasin_cp']
        magasin_ville = kwargs['magasin_ville']
        
        d = Context({'magasin_nom' : magasin_nom,
                     'magasin_adresse' : magasin_adresse,
                     'magasin_cp' : magasin_cp,
                     'magasin_ville' : magasin_ville,
                     })
        texte = get_template('evenement.txt')
        
        texte_contenu = texte.render(d)
        send_mail('Nouvelle offre FLASH', texte_contenu, settings.DEFAULT_FROM_EMAIL, 'youpsla@free.fr')
        #msg = EmailMultiAlternatives ('Nouvelle offre FLASH', texte_contenu, 'youpsla@free.fr', 'youpsla@free.fr')
        
        
    
@login_required
def activation(request, **kwargs):
    """ Fonction qui active un évènement.
        Prends en argument id_magasin et pk (Clé primaire de l'évènement).
        Retour sur la page de détail de l'évènement
        """
    print kwargs
    magasin_id = kwargs['magasin_id']
    pk = kwargs['pk']
    evenement = get_object_or_404(Evenement, pk=pk)
    evenement.activation=1
    evenement.save()
    return HttpResponseRedirect(reverse('evenement_details', args=[int(magasin_id), int(pk)]))