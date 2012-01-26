# -*- coding: utf-8 -*-
from django.db.models import signals
from Instantaneus.commandes.geolocalisation import magcli_magasin

pre_save={}
flag = {}

print "dada"

def change_watcher(sender, instance, signal, *args, **kwargs):
    etat=''
    print kwargs
    if signal == signals.pre_save:
        print "Pre signal"
        if instance.id == None :
            print "instance id none"
            flag[0] = 1
        else:
            print "instance id existe"
            pre_save[instance.id] = (instance.adresse, instance.cp, instance.ville)
            flag[0] = 2
    elif signal == signals.post_save:
        print"Flag", flag[0]
        print "Signal Post Save"
        print kwargs
        if flag[0] == 1:
            etat='creation'
            print "Création nouveau magasin"
            magcli_magasin(mag=instance, etat=etat)
        elif flag[0] == 2:
            etat='update'
            magcli_magasin(mag=instance, etat=etat)
        else:
            print "Signal postsave mais aucune activité"
    else:
        print "change watcher appelé mais aucun signal mis en oeuvre"