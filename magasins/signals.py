from django.db.models import signals
from commandes.views import magcli_magasin



pre_save={}
flag = {}

def change_watcher(sender, instance, signal, *args, **kwargs):
    if signal == signals.post_init:
        if instance.id == None :
            flag[0] = 1
        else:
            pre_save[instance.id] = (instance.adresse, instance.cp, instance.ville)
            flag[0] = 2
    else:
        if flag[0] == 1:
            print "une creation est faite"
            magcli_magasin(mag_id=instance.id)
        elif flag[0] == 2:
            if pre_save[instance.id][0] != instance.adresse:
                print "Changed adresse"
            if pre_save[instance.id][1] != instance.cp:
                print "Changed cp"
            if pre_save[instance.id][2] != instance.ville:
                print "Changed ville"
            if pre_save[instance.id][0] != instance.adresse or pre_save[instance.id][1] != instance.cp or pre_save[instance.id][2] != instance.ville:
                print "un update est fait"
                magcli_magasin(mag_id=instance.id)
            else:
                print "pas update ni creation"
        else:
            print "YA UN PB"