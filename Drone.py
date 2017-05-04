from dronekit import connect, VehicleMode,LocationGlobalRelative
import time
import math
import RestManager as RM
from pymavlink.mavutil import mavlink
from GetAndSendPictures.DronePicture import DronePicture
import google_earth_fly_link_file

class Drone():
    # tcp:127.0.0.1:5760
    def __init__(self,connection_string = '/dev/ttyUSB1',altitude = 20,id_intervention = "", positionIntervention = [40.76793169992044, -73.98180484771729]):
        self.drone = connect(connection_string, wait_ready = True, baud = 57600)
        self.arm_and_takeoff(altitude)
        self.set_etat('STOP')
        self.id_intervention = id_intervention
        self.destination = LocationGlobalRelative(positionIntervention[0],positionIntervention[1],20)
        # camera
        self.camera = DronePicture()

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
        if isinstance(point,LocationGlobalRelative):
            self.destination = point
            self.destination.alt = 20
        else:
            self.destination = LocationGlobalRelative(point[0],point[1],20)
        #print(str(self.destination))
        if not self.is_AlreadyFlying():
            self.arm_and_takeoff(20.5)
        if not groundspeed:
            self.drone.simple_goto(self.destination)
        else:
            self.drone.simple_goto(self.destination, groundspeed)

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
            print " Altitude: ", self.drone.location.global_relative_frame.alt
            # Break and return from function just below target altitude.
            if self.drone.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
                print "Reached target altitude"
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
        #self.drone.close()

    def attente_arrivee(self,destination):
        while get_distance_metres(self.getGPSCoordonate(),destination) > 1:
            time.sleep(1)
        print('arrivee a destination :'+str(destination))

    def orienter_vers_nord(self):
        msg = self.drone.message_factory.command_long_encode(0,0,mavlink.MAV_CMD_CONDITION_YAW,0,0,0,1,0,0,0,0)
        self.drone.send_mavlink(msg)

    def notifier_serveur_position(self):
        RM.post_positionParam(self.getGPSCoordonate(),self.id_intervention)

    def prendre_photo(self):
        photo = self.camera.getPicture(Intervention = self.id_intervention)
        position = self.getGPSCoordonate()
        photo['position'] = [float(position.lat),float(position.lon)]
        photo['idIntervention'] = self.id_intervention
        photo['positionPTS'] = [float(self.destination.lat),float(self.destination.lon)]
        RM.post_photo(photo)

    def prendre_video(self):
        self.camera.makeVideoDrone(Intervention= self.id_intervention)

    def maj_googleearth(self):
        position = self.getGPSCoordonateRelatif()
        google_earth_fly_link_file.GenerateKML(position.lon,position.lat,position.alt,
                                               self.drone.attitude.yaw,self.drone.attitude.pitch)
        #print('MAJ google earth')

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