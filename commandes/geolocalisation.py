# -*- coding: utf-8 -*-
from geopy import geocoders
from geopy import distance as geopy_distance
from django import forms
import urllib, urllib2, json
from django.utils.encoding import smart_str
from django.db.models import get_model

def distance_oiseau((x1, y1), (x2, y2)): 
    if (x1, y1) == (x2, y2): 
        return 0 
    d = geopy_distance.distance((x1, y1), (x2, y2))  
    return d.meters

def liste_clients(mag):
    liste_clients = []
    Clients = get_model('clients','Customer')
    liste_clients = Clients.objects.filter(category=mag.category)
    print "%s clients sont dans la même catégorie que le magasin" % len(liste_clients)
    return liste_clients


def get_lat_lng(location):
    location = urllib.quote_plus(smart_str(location))
    url = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % location
    response = urllib2.urlopen(url).read()
    try:
        result = json.loads(response)
    except:
        raise forms.ValidationError("Problème d'accès au service de géolocalisation. Veuillez réessayer dans 1 minute")
    if result['status'] == 'OK':
        if result['results'][0].has_key('partial_match'):
            raise forms.ValidationError("Erreure de geolocalisation de votre adresse. Mauvaise concordance rue/cp/ville")
        else:
            lat = result['results'][0]['geometry']['location']['lat']
            lng = result['results'][0]['geometry']['location']['lng']
    else:
        raise forms.ValidationError("Erreure de geolocalisation de votre adresse")
    return lat, lng
    
def routes(**kwargs):
    mlat = kwargs['mlat']
    mlng = kwargs['mlng']
    clat = kwargs['clat']
    clng = kwargs['clng']
    routeType = kwargs['types']
    data = {'locations':({'latLng':{'lat':mlat, 'lng':mlng}, 'latLng':{'lat':clat, 'lng':clng}}),'options' : {'allToAll': 'false', 'unit':'k', 'routeType': routeType}}
    #data = {'locations' : [{'street' : "1 rue de la paix", 'city' : 'Paris', 'postalCode' : '75001', 'country': 'France'},{'street' : "10 rue royale", 'city' : 'Paris', 'postalCode' : '75001', 'country': 'France'}],'options' : {'allToAll': 'false', 'unit':'k', 'routeType': 'fastest'}}
    data = json.JSONEncoder().encode(data)
    url = 'http://www.mapquestapi.com/directions/v1/routematrix?key=Fmjtd%7Cluu2n1u725%2Caa%3Do5-ha1s0&inFormat=json'
    req = urllib2.Request(url, data, {"Content-type": "application/json"})
    response = urllib2.urlopen(req).read()
    result = json.loads(response)
    #print json.dumps(result, indent=2)
    distance = int(result['distance'][1]*1000)
    temps = result['time'][1]
    print "Distance en metres:", distance
    print "Temps en secondes:", temps
    return distance, temps

def magcli_magasin(mag, etat, **kwargs):
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
    for c in clients:
        print c.pk
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
                       temps_pro_pied=temps_pro_pied
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
            magcli_with_pk.save()

