from threading import Thread,Event
from Drone import Drone
from ParcoursSegment import ParcoursSegment
import RestManager as RM

class Thread_etat(Thread):
    def __init__(self,drone,refresh = 5.0):
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
            if new_etat != self.etat:
                self.etat = new_etat
                if self.etat == 'SEGMENT':
                    parcours = res['segment']
                    self.ps = ParcoursSegment(self.drone,parcours.points,parcours.boucle_fermee)
                    self.ps.parcourir_segments()
                if self.etat == 'STOP':
                    self.ps.stop_parcours()
                if self.etat == 'ZONE':
                    pass
