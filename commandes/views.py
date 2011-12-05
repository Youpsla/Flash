from geopy import distance as geopy_distance
from clients.models import Customer
from commandes.models import Magcli
from django.db.models import get_model


Magasin = get_model('magasins','Magasin')

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



    
