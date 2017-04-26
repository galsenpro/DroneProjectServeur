#!/usr/bin/env python
# -*- coding: utf-8 -*-


import RestManager as RM

#recup des différentes interventions
print(RM.get_interventions())

print("Récupérations des interventions")
#affichage de numéro - nom intervention

interventions = RM.get_interventions()
i=0
for intervention in interventions:
    #print(intervention)
    iid = intervention["_id"]
    if "libelle" in intervention:
        ilibelle = intervention["libelle"]
    else:
        ilibelle = "Intervention sans libelle"
    if "adresse" in intervention:
        iadresse = intervention["adresse"]
    else:
        iadresse = "Adresses non disponible"

    print " "+str(i)+"  | "+ilibelle+"  "+"  "+iadresse
    i=i+1

var = raw_input("\n\r\nNuméro de l'intervention à sélectionner: ")
print "intervention n°", var

print interventions[int(var)]["_id"] # l'id de l'intervention