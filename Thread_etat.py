from threading import Thread,Event
from Drone import Drone
#from ParcoursSegment import ParcoursSegment
import RestManager as RM
import time

class Thread_etat(Thread):
    def __init__(self,drone,refresh = 5.0):
        super(Thread_etat, self).__init__()
        self.drone = drone
        self._stopevent = Event()
        self.refresh = refresh
        self.etat = None
        self.ps = None

    def run(self):
        id_inter = self.drone.id_intervention
        while not self._stopevent.isSet():
            res = RM.get_drone(id_inter)
            new_etat = res['etat']
            print(new_etat)
            """if new_etat != self.etat:
                self.etat = new_etat
                if self.etat == 'SEGMENT':
                    parcours = res['segment']
                    self.ps = ParcoursSegment(self.drone,parcours.points,parcours.boucle_fermee)
                    self.ps.parcourir_segments()
                if self.etat == 'STOP':
                    self.ps.stop_parcours()
                if self.etat == 'ZONE':
                    pass"""
            self._stopevent.wait(self.refresh)
        print('fin du thread')

    def stop(self):
        self._stopevent.set()

drone = Drone()
drone.set_intervention('58ddf84c212566155e8e98ec')
print('drone OK, début lecture commandes')
tetat = Thread_etat(drone)
tetat.start()
time.sleep(30)
print('fin du script')
tetat.stop()
