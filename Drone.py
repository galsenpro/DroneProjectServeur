from dronekit import connect, VehicleMode
import time
import math
import RestManager as RM
from threading import Thread,Event

class Drone():

    def __init__(self,connection_string = 'tcp:127.0.0.1:5760',altitude = 20,id_intervention = "", positionIntervention = [40.76793169992044, -73.98180484771729]):
        self.drone = connect(connection_string, wait_ready = True, baud = 57600)
        self.arm_and_takeoff(altitude)
        self.set_etat('STOP')
        self.id_intervention = id_intervention
        self.positionIntervention = positionIntervention

    def set_intervention(self,id_intervention):
        self.id_intervention = id_intervention

    def set_etat(self,etat):
        #pour le moment pas de verifications
        self.etat = etat

    def is_AlreadyFlying(self):
        # pas armer si atteri
        # altitude par rapport a la position de depart, si elle est au dessus du sol
        if (self.drone.armed and self.drone.location.global_relative_frame.alt > 5):
            # deja en vol
            return True
        else:
            return False

    def aller_a(self,point,groundspeed=10):
        if not self.is_AlreadyFlying():
            self.arm_and_takeoff(20.5)
        if not groundspeed:
            self.drone.simple_goto(point)
        else:
            self.drone.simple_goto(point, groundspeed)

    def arm_and_takeoff(self,aTargetAltitude=20):
        while not self.drone.is_armable:
            print('waiting initialisation...')
            time.sleep(1)
        # Copter should arm in GUIDED mode
        self.drone.mode = VehicleMode("GUIDED")
        self.drone.armed = True

        # Confirm vehicle armed before attempting to take off
        while not self.drone.armed:
            print('waiting for arming...')
            time.sleep(1)
        print('taking off!')
        self.drone.simple_takeoff(aTargetAltitude)  # Take off to target altitude

        # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
        #  after Vehicle.simple_takeoff will execute immediately).
        while True:
            """print
            " Altitude: ", vehicule.location.global_relative_frame.alt"""
            # Break and return from function just below target altitude.
            if self.drone.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
                """print
                "Reached target altitude"""""
                break
            time.sleep(1)

    def setSpeed(self,speed):
        self.drone.airspeed = speed

    def setAltitude(self,alt):
        self.drone.location.global_relative_frame.alt = alt

    # Fonction to get the GPS location
    def getGPSCoordonate(self):
        return self.drone.location.global_frame

    def getGPSCoordonateRelatif(self):
        return self.drone.location.global_relative_frame

    def RTLandFinish(self):
        self.drone.mode = VehicleMode("RTL")
        self.drone.close()

    def attente_arrivee(self,destination):
        while get_distance_metres(self.getGPSCoordonate(),destination)>1:
            time.sleep(1)
        print('arrivee a destination :'+str(destination))

    def notifier_serveur_position(self):
        value = {}
        value['id_intervention'] = self.id_intervention
        position = self.getGPSCoordonate()
        value['position'] = [position.lat, position.lon]
        RM.post_position(value)

    #def flux_video(self):

    """def thread_position(self):
        while True:
            self.notifier_serveur_position()
            time.sleep(5)

    def thread_video(self):
        while True:
            self.flux_video()
            time.sleep()"""


class Thread_position(Thread):
    def __init__(self,drone,refresh = 5.0):
        super(Thread_position, self).__init__()
        self.drone = drone
        self.refresh = refresh
        self._stopevent = Event()

    def run(self):
        while not self._stopevent.isSet():
            self.drone.notifier_serveur_position()
            self._stopevent.wait(self.refresh)
        print("thread position termine")

    def stop(self):
        self._stopevent.set()


"""class Thread_video(Thread):
    def __init__(self,drone,refresh = 5.0):
        self.drone = drone
        self._stopevent = Event()
        self.refresh = refresh

    def run(self):
        while not self._stopevent.isSet():
            self.drone.flux_video()
            self._stopevent.wait(self.refresh)

    def stop(self):
        self._stopevent.set()"""

def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the
    earth's poles. It comes from the ArduPilot test code:
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    dlong *= math.cos(aLocation2.lat * math.pi / 180.0)
    return math.sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5