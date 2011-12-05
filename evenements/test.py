# -*- coding: UTF-8 -*-

from django_mailer import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives
import settings
from django.db.models import get_model
import locale


def composition_message(**kwargs):
#    magasin_nom = kwargs['magasin_nom']
#    magasin_adresse = kwargs['magasin_adresse']
#    magasin_cp = kwargs['magasin_cp']
#    magasin_ville = kwargs['magasin_ville']
    Magasin = get_model('magasins','Magasin')
    magasin = Magasin.objects.get(pk=65)
    print magasin.pk
    magasin_nom = magasin.name
    magasin_adresse = magasin.adresse
    magasin_cp = magasin.cp
    magasin_ville = magasin.ville
    
    Evenement = get_model('evenements','Evenement')
    evenement = Evenement.objects.get(pk=14)
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
                 'heure_fin' : heure_fin
                 #'evenement_date_debut' : evenement_date_debut,
                 })
    texte = get_template('emails/evenement.txt')
    texte_contenu = texte.render(d)
    print texte_contenu
    send_mail('Nouvelle offre FLASH', texte_contenu, 'Alain <claudine.abraham8@orange.fr>', ['youpsla@gmail.com'])
    #msg = EmailMultiAlternatives ('Nouvelle offre FLASH', texte_contenu, 'youpsla@free.fr', 'youpsla@free.fr')

composition_message()
