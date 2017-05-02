# -*- coding: utf-8 -*-
from threading import Thread,Event
from sympy.geometry import Point,Polygon

import math
import RestManager as RM
"""from Drone import Drone
import time
import dronekit_sitl"""

class ParcoursZone(Thread):
    # Hypothèse : zone convexe

    def __init__(self,drone,zone,pas = 10):
        super(ParcoursZone,self).__init()
        self.drone = drone
        sommets = lister_sommets(zone)
        cotes = generer_cotes(sommets)
        if not cotes.is_convex():
            print 'zone non convexe'
            #raise Exception
        self.points = generer_parcours(cotes,sommets,pas)
        print(self.points)
        self._stopevent = Event()

    def run(self):
        parcours = [idx for idx in range(0,len(self.points))]
        while not self._stopevent.isSet():
            point = self.points[parcours[count]]
            self.drone.aller_a(point, None)
            self.drone.attente_arrivee(point)
            count += 1
            if count == len(parcours):
                count = 0
        print "demande d'arrêt"

    def stop(self):
        self._stopevent.set()


def lister_sommets(sommets):
    res = []
    for point in sommets:
        res.append(Point(point))
    return res


def generer_cotes(sommets):
    return Polygon(sommets)


def retourner_plus_grand_cote(cotes):
    #cotes = Polygon.sides
    ma = max([s.length for s in cotes])
    for seg in cotes:
        if seg.length == ma:
            return seg


def retourner_point_oppose(cote,sommets):
    ma = max([cote.distance(point) for point in sommets])
    for sommet in sommets:
        if cote.distance(sommet) == ma:
            return sommet,ma


def translater_parallele(ligne,direction,pas):
    angle = math.atan(direction)
    x = pas*math.cos(angle)
    y = pas*math.sin(angle)
    ligne.translate(x,y)


def retourner_intersections(ligne,polygone):
    return polygone.intersection(ligne)


def generer_parcours(cotes,sommets,pas):
    depart = retourner_plus_grand_cote(cotes.sides)
    axe_pas = depart.perpendicular_line(depart.p1).slope
    fin,ma = retourner_point_oppose(depart,sommets)
    d = pas
    parcours = [depart.p1,depart.p2]
    dernier_point = parcours[-1]
    line = depart.parallel_line(depart.p1)
    while d < ma:
        # tracer un parallèle à départ à distance d
        translater_parallele(line,axe_pas,pas)
        inter = retourner_intersections(line,sommets)
        if len(inter)==0:
            print "Oh oh, pas d'intersection"
            #raise Exception
        if dernier_point.distance(inter[0]) < dernier_point.distance(inter[1]):
            parcours.append(inter[0])
            parcours.append(inter[1])
            dernier_point = inter[1]
        else:
            parcours.append(inter[1])
            parcours.append(inter[0])
            dernier_point = inter[0]
        d += pas
    parcours.append(fin)
    return parcours


if __name__ == 'main':
    id_intervention = '590359d44cd5ba2ce8795578'
    position = [50.1115921388017,8.677800446748732]


    # démarage du tread SITL avec comme position
    """sitl = dronekit_sitl.start_default(position[0], position[1] + 0.0005)
    connection_string = sitl.connection_string()

    drone = Drone(connection_string, id_intervention=id_intervention)"""
    res = RM.get_drone(id_intervention)
    zone = res['zone']
    print "zone : ",zone
    sommets = lister_sommets(zone['contours'])
    print "sommets : ",sommets
    cotes = generer_cotes(sommets)
    parcours = generer_parcours(cotes, sommets, 0.01)
    print "parcours : ",parcours

    """pz = ParcoursZone(drone,zone['contours'],0.01)
    pz.start()
    time.sleep(120)
    pz.stop()"""