# -*- coding: utf-8 -*-
from geopy import distance as geopy_distance
from clients.models import Customer
from commandes.models import Magcli
from django.db.models import get_model


def geocode_distance((x1, y1), (x2, y2)): 
    if (x1, y1) == (x2, y2): 
        return 0 
    d = geopy_distance.distance((x1, y1), (x2, y2))  
    return d.meters

def magcli_tout():
    Magasin = get_model('magasins','Magasin')
    client = Customer.objects.all()
    mag = Magasin.objects.all()
    for a in mag:
        for b in client:
            distance_home = geocode_distance((a.lat,a.lng),(b.lat_home, b.lng_home))
            distance_pro = geocode_distance((a.lat,a.lng),(b.lat_pro, b.lng_pro))
            d = Magcli(client=Customer.objects.get(pk=b.id), magasin=Magasin.objects.get(pk=a.id), distance_home=distance_home, distance_pro=distance_pro, match_category=0)
            try :
                d.save()
            except:
                magcli_with_pk = Magcli.objects.get(magasin=Magasin.objects.get(pk=a.id),client=Customer.objects.get(pk=b.id))
                magcli_with_pk.distance_home = distance_home
                magcli_with_pk.distance_pro = distance_pro
                magcli_with_pk.save()

def magcli_client(sender, **kwargs):
    Magasin = get_model('magasins','Magasin')
    client = Customer.objects.get(pk=client_id)
    mag = Magasin.objects.all()
    for a in mag:
        distance_home = geocode_distance((a.lat,a.lng),(client.lat_home, client.lng_home))
        distance_pro = geocode_distance((a.lat,a.lng),(client.lat_pro, client.lng_pro))
        d = Magcli(client=client, magasin=Magasin.objects.get(pk=a.id), distance_home=distance_home, distance_pro=distance_pro, match_category=0)
        d.save()

def magcli_magasin(mag_id, **kwargs):
    Magasin = get_model('magasins','Magasin')
    mag_id=mag_id
    mag = Magasin.objects.get(pk=mag_id)
    client = Customer.objects.all()
    for a in client:
        distance_home = geocode_distance((mag.lat,mag.lng),(a.lat_home, a.lng_home))
        distance_pro = geocode_distance((mag.lat,mag.lng),(a.lat_pro, a.lng_pro))
        d = Magcli(client=a, magasin=mag, distance_home=distance_home, distance_pro=distance_pro, match_category=0)
        try :
            d.save()
            print "creation"
        except:
            print "update"
            magcli_with_pk = Magcli.objects.get(magasin=Magasin.objects.get(pk=mag.id),client=Customer.objects.get(pk=a.id))
            magcli_with_pk.distance_home = distance_home
            magcli_with_pk.distance_pro = distance_pro
            magcli_with_pk.save()


#from django_mailer import send_mail
#from django.template.loader import get_template
#from django.template import Context
#import locale
#
#from django.db.models import F
#from django.db.models import Q
#from django.contrib.auth.decorators import login_required
#from django.utils.decorators import method_decorator
#
#class EvenementsMessages:
#    """
#    Classe qui fournit mes méthodes suivantes:
#        - evenement_match_client
#        - evenement_envoi_email
#    """
#    
#    #@method_decorator(login_required)
#    def __init__(self, magasin_id, evenement_id):
#        self.mag = int(magasin_id)
#        self.eve = evenement_id
#        self.liste_clients = []
#    
#    #@method_decorator(login_required)
#    def evenement_match_client(self):
#        """
#        Fonction qui fait le raprochement entre un évènement et les clients qui y sont élligibles.
#        Les criètres sont les distances home et pro ainsi que la catégorie.
#        Argument : magasin_id
#        """
#        #Sélection des clients répondant aux critères d'appétance et de distance géographiques
#        #liste_client = Magcli.objects.filter(Q(magasin=self.mag), Q(distance_home__gt= F('client__distance_max_home')) | Q(distance_pro__gt= F('client__distance_max_pro')), Q(magasin__category = F('client__category'))).select_related('client')
#        print"dadada"
#        liste_clients = Magcli.objects.filter(magasin=65)
#        print liste_clients
#        for i in liste_clients:
#            print "Distance_max_home %s - Distance_home %s" % (i.client.distance_max_home, i.distance_home)
#            print "Distance_max_pro %s - Distance_pro %s" % (i.client.distance_max_pro, i.distance_pro)
#            print i.magasin.pk
#        return liste_clients
#    
#    #@method_decorator(login_required)
#    def evenement_envoi_email(self):
#        """
#        Fonction de composition et d'envoi des Emails après l'activation d'un évènement
#        """
#    #    magasin_nom = kwargs['magasin_nom']
#    #    magasin_adresse = kwargs['magasin_adresse']
#    #    magasin_cp = kwargs['magasin_cp']
#    #    magasin_ville = kwargs['magasin_ville']
#        Magasin = get_model('magasins','Magasin')
#        magasin = Magasin.objects.get(pk=self.mag)
#        print magasin.pk
#        magasin_nom = magasin.name
#        magasin_adresse = magasin.adresse
#        magasin_cp = magasin.cps
#        magasin_ville = magasin.ville
#        
#        Evenement = get_model('evenements','Evenement')
#        evenement = Evenement.objects.get(pk=self.eve)
#        locale.setlocale(locale.LC_ALL, '')
#        jour = evenement.date_debut.strftime('%A %d %B')
#        heure_debut = '%sH%s' % (evenement.date_debut.strftime('%H'), evenement.date_debut.strftime('%M'))
#        heure_fin = '%sH%s' % (evenement.date_fin.strftime('%H'), evenement.date_fin.strftime('%M'))
#        print evenement.date_debut
#        print evenement.date_debut.strftime('%A %d %B %H %M')
#        d = Context({'magasin_nom' : magasin_nom,
#                     'magasin_adresse' : magasin_adresse,
#                     'magasin_cp' : '%05d' % magasin_cp,
#                     'magasin_ville' : magasin_ville,
#                     'jour' : jour,
#                     'heure_debut' : heure_debut,
#                     'heure_fin' : heure_fin
#                     #'evenement_date_debut' : evenement_date_debut,
#                     })
#        texte = get_template('emails/evenement.txt')
#        texte_contenu = texte.render(d)
#        print texte_contenu
#        send_mail('Nouvelle offre FLASH', texte_contenu, 'Alain <claudine.abraham8@orange.fr>', ['youpsla@gmail.com'])
#        #msg = EmailMultiAlternatives ('Nouvelle offre FLASH', texte_contenu, 'youpsla@free.fr', 'youpsla@free.fr')
#
#test = EvenementsMessages(65,14)
#test.evenement_match_client()
#test.evenement_envoi_email()
