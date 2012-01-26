# -*- coding: utf-8 -*-
from geopy import geocoders
from geopy import distance as geopy_distance
from django import forms
import urllib, urllib2, json
from django.utils.encoding import smart_str
from django.db.models import get_model
    

import logging
logger = logging.getLogger(__name__)


def distance_oiseau((x1, y1), (x2, y2)): 
    if (x1, y1) == (x2, y2): 
        return 0 
    d = geopy_distance.distance((x1, y1), (x2, y2))  
    return d.meters 

#def get_lat_lng(location):
#    location = urllib.quote_plus(smart_str(location))
#    url = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % location
#    response = urllib2.urlopen(url).read()
#    try:
#        result = json.loads(response)
#    except:
#        raise forms.ValidationError("Problème d'accès au service de géolocalisation. Veuillez réessayer dans 1 minute")
#    if result['status'] == 'OK':
#        if result['results'][0].has_key('partial_match'):
#            raise forms.ValidationError("Erreure de geolocalisation de votre adresse. Mauvaise concordance rue/cp/ville")
#        else:
#            lat = result['results'][0]['geometry']['location']['lat']
#            lng = result['results'][0]['geometry']['location']['lng']
#            print lat, lng
#    else:
#        raise forms.ValidationError("Erreure de geolocalisation de votre adresse")
#    return lat, lng

def get_lat_lng(location, cp):
    print __name__
    logger.debug('Initialisation de la fonction de géolocalisation')
    results = {}
    location = urllib.quote_plus(smart_str(location))
    logger.debug('La géoloc se fait sur la chaine: %s' % location)
    url = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % location
    response = urllib2.urlopen(url).read()
    try:
        result = json.loads(response)
        print result
        print len(result['results'][0]['address_components'])
        logger.debug('Réponse JSON reçue de Google')
    except:
        logger.debug('Problème d\accès au service Google')
        raise forms.ValidationError("Problème d'accès au service de géolocalisation. Veuillez réessayer dans 1 minute")
    if result['status'] == 'OK':
        logger.debug('JSON status: OK')
        if result['results'][0].has_key('address_components'):
            logger.debug('JSON: Un élément address_components a été trouvé')
            for i in result['results'][0]['address_components']:
                if i['types'][0] == 'postal_code':
                    logger.debug('JSON: Un élément postal_code trouvé: %s ' % i['long_name'])
                    if i['long_name'] == cp:
                        logger.debug('JSON: Egalité des codes postaux: %s - %s' % (cp, i['long_name']))
                        lat = result['results'][0]['geometry']['location']['lat']
                        lng = result['results'][0]['geometry']['location']['lng']
                        results['lat']=lat
                        results['lng']=lng
                        results['status']=1
                    else:
                        logger.debug('JSON: Les codes postaux NE sont PAS identiques: %s - %s' % (cp, i['long_name']))
                        results['status']=0                 
                else:
                    logger.debug('JSON: pas d\'élément postal_code trouvé')
                    results['status']=0
        else:
            logger.debug('JSON: Pas d\'élément address_components')
            results['status']=0
    else:
        logger.debug('JSON: Statut de réponse PAS OK: %s' % result['status'])
        results['status']=0
    logger.debug('GEOLOCALISATION: Sortie de la fonction avec un statut: %s' % results['status'])
    return results
    
def routes(**kwargs):
    mlat = str(kwargs['mlat'])[0:10]
    mlng = str(kwargs['mlng'])[0:10]
    clat = str(kwargs['clat'])
    clng = str(kwargs['clng'])
    print "Coordonnées magasins", mlat, mlng
    print "Coordonnées client", clat, clng
    routeType = kwargs['routeType']
    data = {'locations':[{'latLng':{'lat':mlat, 'lng':mlng}}, {'latLng':{'lat':clat, 'lng':clng}}],'options' : {'allToAll': 'false', 'unit':'k', 'routeType': routeType}}
    print data
    #data = {'locations' : [{'street' : "1 rue de la paix", 'city' : 'Paris', 'postalCode' : '75001', 'country': 'France'},{'street' : "10 rue royale", 'city' : 'Paris', 'postalCode' : '75001', 'country': 'France'}],'options' : {'allToAll': 'false', 'unit':'k', 'routeType': 'fastest'}}
    data = json.JSONEncoder().encode(data)
    url = 'http://www.mapquestapi.com/directions/v1/routematrix?key=Fmjtd%7Cluu2n1u725%2Caa%3Do5-ha1s0&inFormat=json'
    req = urllib2.Request(url, data, {"Content-type": "application/json"})
    response = urllib2.urlopen(req).read()
    result = json.loads(response)
    print result
    #print json.dumps(result, indent=2)
    distance = int(result['distance'][1]*1000)
    temps = result['time'][1]
    print "Distance en metres:", distance
    print "Temps en secondes:", temps
    return distance, temps


def liste_clients(mag):
    """
    Retourne la liste des clients qui ont au moins une catégorie commune avec le magasin passé
    en argument à la fonction
    
    Paramètre obligatoire:
    - Une instance de Magasin
    """
    liste_clients = []
    Clients = get_model('clients','Customer')
    liste_clients = Clients.objects.filter(category=mag.category)
    print "%s clients sont dans la même catégorie que le magasin" % len(liste_clients)
    return liste_clients

def magcli_magasin(mag, etat, **kwargs):
    """
    Met à jour la table Magcli lors de l'ajout ou la modification d'un magasin.
    
    Paramètres obligatoires:
    - Une instance de Magasin
    - etat : creation ou update
    """
    
    distance_home_voiture=0
    distance_pro_voiture=0
    distance_home_pied=0
    distance_pro_pied=0
    temps_home_voiture=0
    temps_pro_voiture=0
    temps_home_pied=0
    temps_pro_pied=0
    Magcli = get_model('commandes','Magcli')
    print "macli_magasin: ", etat
    clients=liste_clients(mag)
    print clients
    for c in clients:
        print "PK client:", c.pk
        distance_home = distance_oiseau((mag.lat,mag.lng),(c.lat_home, c.lng_home))
        distance_pro = distance_oiseau((mag.lat,mag.lng),(c.lat_pro, c.lng_pro))
        if distance_home > 0 and distance_home < 10000:
            distance_home_voiture, temps_home_voiture = routes(mlat=mag.lat, mlng=mag.lng, clat=c.lat_home, clng=c.lng_home, routeType='fastest')
        if distance_pro > 0 and distance_pro < 10000:
            distance_pro_voiture, temps_pro_voiture = routes(mlat=mag.lat, mlng=mag.lng, clat=c.lat_pro, clng=c.lng_pro, routeType='fastest')
        if distance_home > 0 and distance_home < 2000:
            distance_home_pied, temps_home_pied = routes(mlat=mag.lat, mlng=mag.lng, clat=c.lat_home, clng=c.lng_home, routeType='pedestrian')
        if distance_pro > 0 and distance_pro < 2000:
            distance_pro_pied, temps_pro_pied = routes(mlat=mag.lat, mlng=mag.lng, clat=c.lat_pro, clng=c.lng_pro, routeType='pedestrian')
        if etat=="creation":
            print "Magcli : création"
            mc = Magcli(client=c, magasin=mag, distance_home=distance_home, distance_pro=distance_pro, match_category=1,
                        distance_home_voiture=distance_home_voiture,
                        distance_pro_voiture=distance_pro_voiture,
                        distance_home_pied=distance_home_pied,
                        distance_pro_pied=distance_pro_pied,
                        temps_home_voiture=temps_home_voiture,
                        temps_pro_voiture=temps_pro_voiture,
                        temps_home_pied=temps_home_pied,
                        temps_pro_pied=temps_pro_pied,
                        match = 1,
                        )
            mc.save()
        elif etat == "update":
            print "Magcli : update"
            magcli_with_pk = Magcli.objects.get(magasin=mag,client=c)
            if distance_home_voiture !=0:
                magcli_with_pk.distance_home_voiture = distance_home_voiture
            if distance_pro_voiture !=0:
                magcli_with_pk.distance_pro_voiture=distance_pro_voiture
            if distance_home_pied !=0:
                magcli_with_pk.distance_home_pied=distance_home_pied
            if distance_pro_pied !=0:
                magcli_with_pk.distance_pro_pied=distance_pro_pied
            if temps_home_voiture !=0:
                magcli_with_pk.temps_home_voiture = temps_home_voiture
            if temps_pro_voiture !=0:
                magcli_with_pk.temps_pro_voiture=temps_pro_voiture
            if temps_home_pied !=0:
                magcli_with_pk.temps_home_pied=temps_home_pied
            if temps_pro_pied !=0:
                magcli_with_pk.temps_pro_pied=temps_pro_pied
            magcli_with_pk.distance_home = distance_home
            magcli_with_pk.distance_pro = distance_pro
            magcli_with_pk.match = 1
            magcli_with_pk.save()

def liste_magasins(client):
    logger.debug('Initialisation de la fonction liste_magasins')
    """
    Retourne la liste des magasins qui ont au moins une catégorie commune avec le client passé
    en argument à la fonction
    
    Paramètre obligatoire:
    - Une instance de Client
    """
    liste_magasins = []
    Magasin = get_model('magasins','Magasin')
    liste_magasins = Magasin.objects.filter(category__in=client.category.all())
    print liste_magasins
    print "%s magasins sont dans la même catégorie que le client" % len(liste_magasins)
    return liste_magasins

def magcli_client(client, **kwargs):
    """
    Met à jour la table Magcli lors de l'ajout ou la modification d'un magasin.
    
    Paramètre obligatoire:
    - Une instance de Magasin
    """
    logger.debug('Initialisation de la fonction de magcli_client')
    distance_home_voiture = None
    distance_pro_voiture = None
    distance_home_pied = None
    distance_pro_pied = None
    temps_home_voiture = None
    temps_pro_voiture = None
    temps_home_pied = None
    temps_pro_pied = None
    Magcli = get_model('commandes','Magcli')
    magasins=liste_magasins(client)
    logger.debug('Il y a %s magasins qui match le client' % len(magasins))
    for m in magasins:
        logger.debug('Traitement du magasin %s pour le client %s' % (m.pk, client))
        distance_home = distance_oiseau((client.lat_home,client.lng_home),(m.lat, m.lng))
        logger.debug('Distance_home: %s' % distance_home)
        distance_pro = distance_oiseau((client.lat_pro,client.lng_pro),(m.lat, m.lng))
        logger.debug('Distance_pro: %s' % distance_pro)
        if client.lng_home is not None:
            logger.debug('Calcul distance HOME')
            if distance_home > 0 and distance_home < 10000:
                distance_home_voiture, temps_home_voiture = routes(clat=client.lat_home, clng=client.lng_home, mlat=m.lat, mlng=m.lng, routeType='fastest')
            if distance_home > 0 and distance_home < 2000:
                distance_home_pied, temps_home_pied = routes(clat=client.lat_home, clng=client.lng_home, mlat=m.lat, mlng=m.lng, routeType='pedestrian')
        if client.lng_pro is not None:
            logger.debug('Calcul distance PRO')        
            if distance_pro > 0 and distance_pro < 10000:
                distance_pro_voiture, temps_pro_voiture = routes(clat=client.lat_pro, clng=client.lng_pro, mlat=m.lat, mlng=m.lng, routeType='fastest')
            if distance_pro > 0 and distance_pro < 2000:
                distance_pro_pied, temps_pro_pied = routes(clat=client.lat_pro, clng=client.lng_pro, mlat=m.lat, mlng=m.lng, routeType='pedestrian')

        mc = Magcli(magasin=m, client=client, distance_home=distance_home, distance_pro=distance_pro, match_category=1,
                    distance_home_voiture=distance_home_voiture,
                    distance_pro_voiture=distance_pro_voiture,
                    distance_home_pied=distance_home_pied,
                    distance_pro_pied=distance_pro_pied,
                    temps_home_voiture=temps_home_voiture,
                    temps_pro_voiture=temps_pro_voiture,
                    temps_home_pied=temps_home_pied,
                    temps_pro_pied=temps_pro_pied,
                    match = 1,
                    )
        mc.save()
