from Drone import Drone,Thread_position
from dronekit import LocationGlobalRelative
import RestManager as RM
from threading import Thread,Event
import time

class ParcoursSegment(Thread):

    def __init__(self,drone,points,boucle_fermee = False):
        super(ParcoursSegment,self).__init__()
        self.drone = drone
        self.points = points
        self.boucle_fermee = boucle_fermee
        #self.drone.set_etat('SEGMENT')
        #self.thread_position = Thread_position(drone)
        self._stopevent = Event()

    def run(self):
        # boucle des points à parcourir
        parcours = [idx for idx in range(0,len(self.points))]
        if not self.boucle_fermee:
            parcours += [idx for idx in range(len(self.points)-2,0,-1)]
        # aller au départ
        #print(str(self.points[0]))
        """self.drone.aller_a(self.points[0],None)
        self.drone.attente_arrivee(self.points[0])"""
        #thread_position = Thread(None,self.drone.thread_position)
        print("début de parcours")
        #self.thread_position.start()
        count = 0
        while not self._stopevent.isSet():
            point = self.points[parcours[count]]
            self.drone.aller_a(point,None)
            self.drone.attente_arrivee(point)
            count += 1
            if count == len(parcours):
                count = 0
            """if self.boucle_fermee:
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
                        self.drone.attente_arrivee(point)"""
        #self.thread_position.stop()
        print("demande d'arrêt")

    def stop(self):
        self._stopevent.set()
#test
"""import dronekit_sitl
sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()
print(connection_string)"""
#connection_string = 'tcp:127.0.0.1:5760'
drone = Drone()
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
test_position = Thread_position(drone)
test_parcours.start()
test_position.start()

#test_parcours.parcourir_segments()
print('attente fin')
time.sleep(30)
test_parcours.stop()
time.sleep(5)
test_position.stop()
#test_parcours.stop_parcours()

