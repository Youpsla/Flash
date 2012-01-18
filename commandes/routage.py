# -*- coding: utf-8 -*-
from commandes.models import Magcli

from django_mailer import send_mail
from django.template.loader import get_template
from django.template import Context
import locale

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import logging
logger = logging.getLogger(__name__)

class Messages(object):
    """
    Classe qui fournit mes méthodes suivantes:
        - evenement_match_client
        - evenement_envoi_email
        
    Variables à fournir:
        - magasin_id
        - evenement_id
    """
    
    #@method_decorator(login_required)
    @method_decorator(login_required)
    def __init__(self, request, magasin, evenement):
        self.request = request
        self.magasin = magasin
        self.evenement = evenement
        self.emails_liste = []

    def liste_clients(self):
        self.liste_clients = Magcli.objects.filter(magasin=self.magasin, match = 1).select_related('client')
        logger.debug('%s clients match cet instant' % len(self.liste_clients))
        
    def liste_emails(self):
        for i in self.liste_clients:
            self.emails_liste.append(i.client.email_adresse)
        print self.emails_liste

    def evenement_envoi_email(self):
        """
        Fonction de composition et d'envoi des Emails après l'activation d'un évènement
        """
        logger.debug('Liste des emails des destinataires: %s' % self.liste_emails)
        #On récupère le nom, l'adresse, le cp et la ville du magasin
        magasin_nom = self.magasin.nom
        magasin_adresse = self.magasin.adresse
        magasin_cp = self.magasin.cp
        print type(magasin_cp)
        magasin_ville = self.magasin.ville
        
        locale.setlocale(locale.LC_ALL, '')
        jour = self.evenement.date_debut.strftime('%A %d %B')
        heure_debut = '%sH%s' % (self.evenement.date_debut.strftime('%H'), self.evenement.date_debut.strftime('%M'))
        heure_fin = '%sH%s' % (self.evenement.date_fin.strftime('%H'), self.evenement.date_fin.strftime('%M'))
        print self.evenement.date_debut
        print self.evenement.date_debut.strftime('%A %d %B %H %M')
        d = Context({'magasin_nom' : magasin_nom,
                     'magasin_adresse' : magasin_adresse,
                     'magasin_cp' : '%s' % magasin_cp,
                     'magasin_ville' : magasin_ville,
                     'jour' : jour,
                     'heure_debut' : heure_debut,
                     'heure_fin' : heure_fin,
                     })
        print d
        texte = get_template('emails/evenement.txt')
        texte_contenu = texte.render(d)
        print texte_contenu
        send_mail('Nouvelle offre FLASH', texte_contenu, 'Alain <youpsla@free.fr>', self.emails_liste)
        print "Email envoyé"

#test = EvenementsMessages(65,14)
#test.evenement_match_client()
#test.evenement_envoi_email()