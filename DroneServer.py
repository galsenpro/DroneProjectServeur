from dronekit import LocationGlobalRelative

import MongoManager as MM
import VehiculeManager as VM
import time
import sched

FREQUENCE = 10


def main():
    # print("- - - GPS du Drone - - -")
    # gps = VM.getGPSCoordonate()
    # print(gps)
    # MM.insert_drone_gps(gps.lon, gps.lat)

    print("- - - Commande - - -")
    command = MM.last_command_afaire()
    print(command)
    if (command != None):
        id = command['_id']
        # MM.set_command_encours(id)
        goto = LocationGlobalRelative(command['position'][0], command['position'][1], 20)
        print(command)
        print(goto)
        VM.goTo(goto, 10)

    s.enter(FREQUENCE, 1, main, ())


s = sched.scheduler(time.time, time.sleep)
s.enter(0, 1, main, ())
s.run()
