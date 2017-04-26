from Drone import Drone,Thread_position
from dronekit import LocationGlobalRelative
import RestManager as RM
from threading import Thread
import time

class ParcoursSegment():

    def __init__(self,drone,points,boucle_fermee = False):
        self.drone = drone
        """if self.drone.etat != 'SEGMENT':
           break"""
        self.points = points
        self.boucle_fermee = boucle_fermee
        self.drone.set_etat('SEGMENT')
        self.thread_position = Thread_position(drone)
        self.en_cours = True

    def parcourir_segments(self):
        # aller au départ
        print(str(self.points[0]))
        self.drone.aller_a(self.points[0],None)
        self.drone.attente_arrivee(self.points[0])
        #thread_position = Thread(None,self.drone.thread_position)
        print("début de parcours")
        self.thread_position.start()
        while self.en_cours:
            if self.boucle_fermee:
                while self.drone.etat == 'SEGMENT':
                    for point in self.points:
                        self.drone.aller_a(point,None)
                        # attendre arrivée
                        self.drone.attente_arrivee(point)
            else:
                while self.drone.etat == 'SEGMENT':
                    for point in self.points:
                        self.drone.aller_a(point,None)
                        # attendre arrivée
                        self.drone.attente_arrivee(point)
                        #self.drone.notifier_serveur_position()
                    for point in self.points[-1::-1]:
                        self.drone.aller_a(point,None)
                        # attendre arrivée
                        self.drone.attente_arrivee(point)
        self.thread_position.stop()
        print("demande d'arrêt")

    def stop_parcours(self):
        self.en_cours == False
#test

    """def stop_class(self):
        time.sleep(120)
        self.stop_parcours()
        print('parcours arrêté')"""


"""import dronekit_sitl
sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()
print(connection_string)"""
connection_string = 'tcp:127.0.0.1:5760'
drone = Drone(connection_string)
#ISTIC = 48.114971,-1.636686,20,0
parcours = []
parcours.append(LocationGlobalRelative(48.115,-1.636,20))
parcours.append(LocationGlobalRelative(48.1155,-1.6365,20))
parcours.append(LocationGlobalRelative(48.1158,-1.6362,20))
parcours.append(LocationGlobalRelative(48.1153,-1.6363,20))
boucle_fermee = True
"""id_intervention = 'test'
dronedb = RM.get_drone(id_intervention)
parcours = dronedb['segment'].points
boucle_fermee = dronedb['segment'].boucle_fermee"""
test_parcours = ParcoursSegment(drone,parcours,boucle_fermee)

parcourir = Thread(None,test_parcours.parcourir_segments)
parcourir.start()

#test_parcours.parcourir_segments()
print('attente fin')
time.sleep(30)
parcourir._stop()
#test_parcours.stop_parcours()

