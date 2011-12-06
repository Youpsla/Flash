# -*- coding: utf-8 -*-
from commandes.models import Magcli
from django.db.models import get_model

from django_mailer import send_mail
from django.template.loader import get_template
from django.template import Context
import locale

from django.db.models import F
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class EvenementsMessages:
    """
    Classe qui fournit mes méthodes suivantes:
        - evenement_match_client
        - evenement_envoi_email
    """
    
    #@method_decorator(login_required)
    def __init__(self, magasin_id, evenement_id):
        self.mag = magasin_id
        self.eve = evenement_id
        self.liste_emails = []
    
    #@method_decorator(login_required)
    def evenement_match_client(self):
        """
        Fonction qui fait le raprochement entre un évènement et les clients qui y sont élligibles.
        Les criètres sont les distances home et pro ainsi que la catégorie.
        Argument : magasin_id
        """
        #liste_clients = Magcli.objects.filter(magasin=65)
        liste_clients = Magcli.objects.filter(Q(magasin=self.mag), Q(distance_home__gt= F('client__distance_max_home')) | Q(distance_pro__gt= F('client__distance_max_pro')), Q(magasin__category = F('client__category'))).select_related('client')
        print liste_clients
        for i in liste_clients:
            print "Distance_max_home %s - Distance_home %s" % (i.client.distance_max_home, i.distance_home)
            print "Distance_max_pro %s - Distance_pro %s" % (i.client.distance_max_pro, i.distance_pro)
            print i.magasin.pk
        liste_emails=[]
        for i in liste_clients:
            self.liste_emails.append(i.client.email_adresse)
    
    #@method_decorator(login_required)
    def evenement_envoi_email(self):
        """
        Fonction de composition et d'envoi des Emails après l'activation d'un évènement
        """
        print "Liste emails: ", self.liste_emails
        Magasin = get_model('magasins','Magasin')
        magasin = Magasin.objects.get(pk=self.mag)
        magasin_nom = magasin.name
        magasin_adresse = magasin.adresse
        magasin_cp = magasin.cp
        magasin_ville = magasin.ville
        
        Evenement = get_model('evenements','Evenement')
        evenement = Evenement.objects.get(pk=self.eve)
        locale.setlocale(locale.LC_ALL, '')
        jour = evenement.date_debut.strftime('%A %d %B')
        heure_debut = '%sH%s' % (evenement.date_debut.strftime('%H'), evenement.date_debut.strftime('%M'))
        heure_fin = '%sH%s' % (evenement.date_fin.strftime('%H'), evenement.date_fin.strftime('%M'))
        print evenement.date_debut
        print evenement.date_debut.strftime('%A %d %B %H %M')
        d = Context({'magasin_nom' : magasin_nom,
                     'magasin_adresse' : magasin_adresse,
                     'magasin_cp' : '%05d' % magasin_cp,
                     'magasin_ville' : magasin_ville,
                     'jour' : jour,
                     'heure_debut' : heure_debut,
                     'heure_fin' : heure_fin,
                     })
        texte = get_template('emails/evenement.txt')
        texte_contenu = texte.render(d)
        print texte_contenu
        send_mail('Nouvelle offre FLASH', texte_contenu, 'Alain <claudine.abraham8@orange.fr>', ['youpsla@gmail.com'])
        print "Email envoyé"
        #msg = EmailMultiAlternatives ('Nouvelle offre FLASH', texte_contenu, 'youpsla@free.fr', 'youpsla@free.fr')

test = EvenementsMessages(65,14)
test.evenement_match_client()
test.evenement_envoi_email()
