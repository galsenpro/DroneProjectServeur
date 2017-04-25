from dronekit import Vehicle,LocationGlobalRelative,Command
from pymavlink.mavutil import mavlink
class DroneZone():
    # Hypothèse : zone concave
    contour = set() #
    d = 0

    def __init__(self,contour,d = 10):
        self.contour = contour
        self.vertices = []
        self.d = d
        self.switch = True
        self.nord = 1

    def point_ouest(self):
        #retourner le point de contour "le plus à gauche et en haut"
        res = self.contour[0]
        for point in self.contour[1:]:
            if point[0]<res[0]:
                res = point
        return res

    def point_est(self):
        #retourner le point de contour "le plus à droite" --> retour au départ
        res = self.contour[0]
        for point in self.contour[1:]:
            if point[0]>res[0]:
                res = point
        return res

    def suivre_contour(self,ptA):
        #suivre un contour à partir de ptA sur une distance d
        #trouver le contour à suivre
        absx = ptA[0]
        dep =
        #TODO

    def coef_directeur(self,pt):
        x = pt[0]
        y = pt[1]
        #
        for points in self.contour:
    def suivre_meridien(self,ptA,dir=1):
        #suivre un méridien vers le nord (dir=1) ou le sud (dir=-1)
        #TODO

    def intersection_meridien_contour(self,position):
        #retourne l'intersection entre le suivi de méridien et le contour
        if self.nord == 1:



    def attendre_parcours(self,drone,ptB):
        #attendre arrivée du drone à ptB
        while drone.get_distance_metres(drone.getGPSCoordonate,ptB)>1:
            pass
        return

    def changer_switch(self):
        if self.switch:
            self.switch == False
        else:
            self.switch == True

    def changer_sens(self):
        if self.nord == 1:
            self.nord == -1
        else:
            self.nord == 1

    def parcourir_zone(self,drone):
        #drone : VehiculeManager
        #se déplacer vers le point de départ
        pt_depart = self.point_ouest()
        pt_arrivee = self.point_est()
        while drone.etat == 'zone':
            drone.goTo(pt_depart)
            self.attendre_parcours(drone,pt_depart)
            self.switch = True
            while drone.get_distance_metres(drone.getGPSCoordonate(),pt_arrivee) > 1:
                if self.switch:
                    #suivre contour
                    self.suivre_contour(drone.getGPSCoordonate())
                    self.changer_switch()
                else:
                    #suivre meridien dans le sens de self.nord
                    self.suivre_meridien(drone.getGPSCoordonate(),self.nord)
                    self.changer_sens()
                    self.changer_switch()





drone = Vehicle()
points = []
points.append(LocationGlobalRelative(-5,5))
points.append(LocationGlobalRelative(-5,-6))
points.append(LocationGlobalRelative(-10,-8))
drone.simple_goto()

cmds = drone.commands
cmd = Command()
link = mavlink.MAV_CMD_NAV_
