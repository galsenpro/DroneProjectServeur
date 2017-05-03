import dronekit_sitl
from dronekit import Vehicle,LocationGlobalRelative,Command
from pymavlink.mavutil import mavlink

from Drone import Drone


class DroneZoneRandom():
    # Hypothese : zone concave
    contour = set() #
    d = 0

    def __init__(self,contour=None,d = 10):
        self.contour = contour
        self.d = d

    def convertionArrayLonLat(contours):
        liste = None
        for point in contours:
            liste.append(LocationGlobalRelative(point[0],point[1]))
        return liste

    def parcourir_zone(self,drone):
        listeinit = self.convertionArrayLonLat(self.contour)
        listeTotal = None

        for i in range(listeinit):
            if i == listeinit.size -1:
                None#calculer les points intermediaires entre le dernier et le 1er
            else:

                None# calculer la liste des points intermediaire listeinit[i] listeinit[i+1]

        while True:
            randomNumber = None
            #(generaterandom * listeTotal.size)%listeTotal.size/2
            drone.goTo(listeTotal[randomNumber])
            self.attendre_parcours(drone,listeTotal[randomNumber])






points = []
points.append(LocationGlobalRelative(-5,5))
points.append(LocationGlobalRelative(-5,-6))
points.append(LocationGlobalRelative(-10,-8))

sitl = dronekit_sitl.start_default(0,0)
connection_string = sitl.connection_string()
#print  connection_string

# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % connection_string

dzr = DroneZoneRandom(points)
drone = Drone(connection_string)
drone.setAltitude(20)
dzr.parcourir_zone()
