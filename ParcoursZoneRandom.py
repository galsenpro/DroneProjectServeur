import random

import sys
from dronekit import LocationGlobalRelative
from threading import Thread,Event

from Drone import Drone


class DroneZoneRandom(Thread):
    # Hypothese : zone concave
    contour = set() #
    d = 0

    def __init__(self,drone=None, contour=None,d = 10):
        self.contour = contour
        self.listeTotal = []
        self._stopevent = Event()
        self.drone = drone
        self.d = d

    def convertionArrayLonLat(self,contours):
        liste = None
        for point in contours:
            liste.append(LocationGlobalRelative(point[0],point[1]))
        return liste

    def calculPointsIntermediaires(self, pts1, pts2):
        print "from "+str(pts1.lat)+" "+str(pts1.lon)+"   to   "+str(pts2.lat)+" "+str(pts2.lon)
        vec = LocationGlobalRelative(0, 1)
        vec.lat = pts2.lat - pts1.lat
        vec.lon = pts2.lon - pts1.lon
        for nb in range(1, 10, 1):
            npts = LocationGlobalRelative(pts1.lat+vec.lat*nb/10.0,pts1.lon+vec.lon*nb/10.0)
            print " "+str(npts.lat)+" "+str(npts.lon)
            self.listeTotal.append(npts)

    def run(self):
        # listeinit = self.convertionArrayLonLat(self.contour)
        listeinit = self.contour

        for i in range(len(listeinit)):
            if i == len(listeinit) -1:
                print "1"+str(i)
                self.calculPointsIntermediaires(listeinit[0],listeinit[len(listeinit)-1])
                None#calculer les points intermediaires entre le dernier et le 1er
            else:
                print "2"+str(i)
                self.calculPointsIntermediaires(listeinit[i], listeinit[i+1])
                None# calculer la liste des points intermediaire listeinit[i] listeinit[i+1]

        position = 0
        while not self._stopevent.isSet():
            randomNumber = random.randint(0,len(self.listeTotal)-1)/2
            position = ((position + (len(self.listeTotal)/4))+randomNumber)%len(self.listeTotal)
            print "Position "+str(position)

            self.drone.goTo(self.listeTotal[position])
            self.attendre_parcours(self.drone,self.listeTotal[position])



    def stop(self):
            self._stopevent.set()
            self.drone.aller_a(self.drone.getGPSCoordonateRelatif())
            sys.exit(0)

pointss = []
pointss.append(LocationGlobalRelative(5.0,5.0))
pointss.append(LocationGlobalRelative(6.0,4.0))
pointss.append(LocationGlobalRelative(6.0,6.0))
# sitl = None
# import dronekit_sitl
# sitl = dronekit_sitl.start_default(lat=10.0,lon=20.0)
# connection_string = sitl.connection_string()
# #print  connection_string
#
# # Connect to the Vehicle
# print 'Connecting to vehicle on: %s' % connection_string
#
# drone = Drone(connection_string,20,id_intervention="ididi")
# drone.arm_and_takeoff(20)
# drone.aller_a(LocationGlobalRelative(20, 21+0.0005), 20)
dzr = DroneZoneRandom(pointss)
dzr.parcourir_zone(None)
