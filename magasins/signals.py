# -*- coding: utf-8 -*-
from django.db.models import signals
from commandes.geolocalisation import magcli_magasin

pre_save={}
flag = {}


def change_watcher(sender, instance, signal, *args, **kwargs):
    etat=''
    if signal == signals.post_init:
        print "Post init signal"
        if instance.id == None :
            flag[0] = 1
        else:
            pre_save[instance.id] = (instance.adresse, instance.cp, instance.ville)
            flag[0] = 2
    elif signal == signal.post_save:
        print "Signal Post Save"
        if flag[0] == 1:
            etat='creation'
            print "Création nouveau magasin"
            magcli_magasin(mag=instance, etat=etat)
        elif flag[0] == 2:
            etat='update'
            if pre_save[instance.id][0] != instance.adresse:
                print "Changed adresse"
            if pre_save[instance.id][1] != instance.cp:
                print "Changed cp"
            if pre_save[instance.id][2] != instance.ville:
                print "Changed ville"
            if pre_save[instance.id][0] != instance.adresse or pre_save[instance.id][1] != instance.cp or pre_save[instance.id][2] != instance.ville:
                print "Un update est fait"
                magcli_magasin(mag=instance, etat=etat)
            else:
                print "pas update ni creation"
        else:
            print "Signal postsave mais aucune activité"
    else:
        print "change watcher appelé mais aucun signal mis en oeuvre"