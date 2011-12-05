# -*- coding: utf-8 -*-
from geopy import geocoders
from geopy import distance as geopy_distance
from django import forms

def geocoding(adr, cp, ville):
    print "geocoding"
    g = geocoders.Google(domain='maps.google.fr')
    try:
        place, (lat, lng) = g.geocode("%s %s %s" % (adr, cp, ville))
        print "Place :", place
    except :
        raise forms.ValidationError("Erreure de geolocalisation de votre adresse")
    print "%s: %.9f, %.9f" % (place, lat, lng)
    return lat, lng

def geocode_distance((x1, y1), (x2, y2)): 
    if (x1, y1) == (x2, y2): 
        return 0 
    d = geopy_distance.distance((x1, y1), (x2, y2))  
    return d.meters

# -*- coding: UTF-8 -*-

import urllib, urllib2, simplejson
from django.utils.encoding import smart_str

def get_lat_lng(location):
    location = urllib.quote_plus(smart_str(location))
    url = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % location
    response = urllib2.urlopen(url).read()
    try:
        result = simplejson.loads(response)
    except:
        raise forms.ValidationError("Problème d'accès au service de géolocalisation. Veuillez réessayer dans 1 minute")
    if result['status'] == 'OK':
        if result['results'][0].has_key('partial_match'):
            raise forms.ValidationError("Erreure de geolocalisation de votre adresse. Mauvaise concordance rue/cp/ville")
        else:
            lat = str(result['results'][0]['geometry']['location']['lat'])
            lng = str(result['results'][0]['geometry']['location']['lng'])
    else:
        raise forms.ValidationError("Erreure de geolocalisation de votre adresse")
    return lat, lng