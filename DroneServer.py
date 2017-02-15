from dronekit import LocationGlobalRelative

import MongoManager as MM
import VehiculeManager as VM
import time
import sched
import argparse

FREQUENCE = 1

#parser le paramettre --connect protocole:ip:port
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()
connection_string = args.connect
VM.ConnectToDrone(connection_string)

encours = False
goto = LocationGlobalRelative(0,0)
id = 0

def main():
    global encours
    global goto
    global id

    gps = VM.getGPSCoordonate()
    MM.insert_drone_gps(gps.lon, gps.lat)
    print("GPS")
    print(gps)

    if(not encours):
        command = MM.last_command_afaire()
        if(command):
            goto = LocationGlobalRelative(command['position'][0], command['position'][1], 20)
            id = command['_id']

            VM.goTo(goto, 10)
            encours = True
            print("GO TO")
            print(goto)
            MM.set_command_encours(id)
            print("COMMANDE EN COURS")
            print(id)
    else:
        distance = VM.get_distance_metres(gps, goto)
        print(distance)
        if (distance < 1):
            MM.set_command_fait(id)
            print("COMMANDE FAITE")
            print(id)
            encours = False

    s.enter(FREQUENCE, 1, main, ())


s = sched.scheduler(time.time, time.sleep)
s.enter(0, 1, main, ())
s.run()
