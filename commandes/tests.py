# -*- coding: utf-8 -*-
import urllib, urllib2, json
from django.utils.encoding import smart_str
from django.db.models import get_model

#Version avec traitement unitaire
def maj_totale_mag_clients():
    Magasin = get_model('magasins','Magasin')
    Customer = get_model('clients','Customer')
    Magcli = get_model('commandes','Magcli')
    clients = Customer.objects.all()
    mags = Magasin.objects.all()
    print "Nombre de magasins: ", len(mags)
    #print "Nombre de clients: ", len(clients)
    for m in mags:
        origins = ''
        destination = ''
        origins = "%s,%s" % (m.lat, m.lng)
        org = urllib.quote_plus(smart_str(origins))
        for c in clients:
            destination = "%s,%s" % (c.lat_home, c.lng_home)
            dest = urllib.quote_plus(smart_str(destination))
            url = 'http://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&mode=driving&language=fr-FR&sensor=false' % (org, dest)
            response = urllib2.urlopen(url).read()
            result = json.loads(response)
            if result['status'] == 'OK':
                temps = result['rows'][0]['elements'][0]['duration']['value']
                distance = result['rows'][0]['elements'][0]['distance']['value']
                try:
                    record = Magcli.objects.get(magasin=m, client=c)
                    pk=record.pk
                    tmp = Magcli(pk=pk, magasin=m, client=c, distance_home=distance, temps_home_pied=temps)
                    print "Enregistrement existant: ", m.pk, "-", c.pk
                    tmp.save()
                except:
                    print "Enregistrement non trouvé"
                    tmp = Magcli(magasin=m, client=c, distance_home=distance, temps_home_pied=temps)
                    tmp.save()
            else:
                print "probleme"
                
maj_totale_mag_clients()

## Version avec traitement en batch
#def maj_totale_mag_clients():
#    Magasin = get_model('magasins','Magasin')
#    Customer = get_model('clients','Customer')
#    clients = Customer.objects.all()
#    mags = Magasin.objects.all()
#    print "Nombre de magasins: ", len(mags)
#    print "Nombre de clients: ", len(clients)
#    dic_maj = []
#    for m in mags:
#        counter = 0
#        origins = ''
#        destinations = ''
#        origins = "%s,%s" % (m.lat, m.lng)
#        org = urllib.quote_plus(smart_str(origins))
#        for c in clients:
#            dic_maj[counter] = {'mag_id' : m.pk, 'client_id' : c.pk}
#            tmp_c = "%s,%s" % (c.lat_home, c.lng_home)
#            if counter == 0:
#                destinations = tmp_c
#            else:
#                destinations = destinations + "|" + tmp_c
#            counter += 1
#            if counter == 50 or counter == len(clients):
#                dest = urllib.quote_plus(smart_str(destinations))
#                url = 'http://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&mode=walking&language=fr-FR&sensor=false' % (org, dest)
#                response = urllib2.urlopen(url).read()
#                result = json.loads(response)
#                print result
#                print dic_maj
#                destinations = ''
#                counter = 0
