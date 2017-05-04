#!/usr/bin/env python
# -*- coding: utf-8 -*-


import RestManager as RM
from dronekit import LocationGlobalRelative
from Drone import Drone
from ParcoursSegment import ParcoursSegment
from ParcoursZoneRandom import DroneZoneRandom

#recup des différentes interventions
from Thread_position import Thread_position
from Thread_video import ThreadVideo
import time

#print(RM.get_interventions())

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
#print "intervention n°", var

#print interventions[int(var)]["_id"] # l'id de l'intervention
#print interventions[int(var)]

idIntervention = interventions[int(var)]["_id"]
position = interventions[int(var)]["position"]
#print idIntervention
#print position

#Start SITL if no connection string specified
sitl = None
import dronekit_sitl
#démarage du tread SITL avec comme position
sitl = dronekit_sitl.start_default(position[0],position[1]+0.0005)
connection_string = sitl.connection_string()
#print  connection_string

# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % connection_string

#connexion au drone
drone = Drone(connection_string, id_intervention=idIntervention,positionIntervention=[position[0],position[1]+0.0005])
#print drone.getGPSCoordonate()
#démarage du tread d'update de position
tetat = Thread_position(drone)
print('script start')
tetat.start()

tvideo = ThreadVideo(drone)
tvideo.start()
drone_dernierEtat = "STOP"
#thread de parcours (Segment ou Zone)
ps = None
while True:

    print('.')
    resDrone = RM.get_drone(drone.id_intervention)
    if resDrone:
        drone.set_etat(resDrone['etat'])
    if drone_dernierEtat != drone.etat:
        drone_dernierEtat = drone.etat
        if drone.etat == 'SEGMENT':
            print('un nouveau segment')
            parcours = resDrone['segment']
            ps = ParcoursSegment(drone,parcours['points'],parcours['boucleFermee'])
            ps.start()
        if drone.etat == 'ZONE':
            print('une nouvelle zone')
            zone = resDrone['zone']
            ps = DroneZoneRandom(drone, zone['contours'])
            ps.start()
            # demarer un thread pour la zone
        if drone.etat == 'STOP':
            print('STOP')
            if ps:
                if ps != None:
                    ps.stop()
                print('fin de parcours')
            drone.aller_a(drone.getGPSCoordonateRelatif())
            # stopper les thread zone et segment
        if drone.etat == 'PARKING':
            print('PARKING')
            drone.RTLandFinish()
    time.sleep(5)

"""goto1 = LocationGlobalRelative(position[0], position[1]+0.0005, 20)
goto2 = LocationGlobalRelative(position[0]+0.0006, position[1]-0.0010, 20)
drone.arm_and_takeoff(20)

while True:
    drone.aller_a(goto1)
    drone.attente_arrivee(goto1)
    print drone.getGPSCoordonate()
    # drone.notifier_serveur_position()

    drone.aller_a(goto2)
    drone.attente_arrivee(goto2)
    print drone.getGPSCoordonate()
    # drone.notifier_serveur_position()"""


if sitl is not None:
    sitl.stop()
    print('script stop')
    tetat.stop()
    tvideo.stop()