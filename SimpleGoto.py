#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
© Copyright 2015-2016, 3D Robotics.
simple_goto.py: GUIDED mode "simple goto" example (Copter Only)

Demonstrates how to arm and takeoff in Copter and how to navigate to points using Vehicle.simple_goto.

Full documentation is provided at http://python.dronekit.io/examples/simple_goto.html
"""

from dronekit import VehicleMode, LocationGlobalRelative
import time
# importer tout le manager de vehicule
import VehiculeManager as VM
# Set up option parsing to get connection string
import argparse

#parser le paramettre --connect protocole:ip:port
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None

VM.ConnectToDrone(connection_string)

print "Set default/target airspeed to 3"
VM.setSpeed(3)

print "Going towards first point for 30 seconds ..."
point1 = LocationGlobalRelative(-35.361354, 149.165218, 20)
VM.vehicule.goTo(point1)

# sleep so we can see the change in map
time.sleep(30)

print "Going towards second point for 30 seconds (groundspeed set to 10 m/s) ..."
point2 = LocationGlobalRelative(-35.363244, 149.168801, 20)
VM.vehicule.goTo(point2, groundspeed=10)

# sleep so we can see the change in map
time.sleep(30)

VM.RTLandFinish()
