#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
from math import cos, sin, pi, sqrt
import random

kml_template = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Test camera KML</name>
    <open>1</open>
    <Camera>
      <longitude>{longitude}</longitude>
      <latitude>{latitude}</latitude>
      <altitude>{altitude}</altitude>
      <heading>{heading}</heading>
      <tilt>{tilt}</tilt>
      <altitudeMode>relativeToGround</altitudeMode>
    </Camera>
  </Document>
</kml>'''

coord = {	'longitude': -1.6401, 
			'latitude': 48.1168+0.002*0,
			'altitude': 50.0+30,
			'heading': 160.0+80,
			'tilt': 70.0 }

r = 6400.0e3;  # Approximate mean earth radius
speed = 25.0; # m/s
Te = 0.05; # s

dt = Te
now = time.time()

# while True:
# 	coord['heading'] += random.gauss(0.5*dt, sqrt(dt) * 0.1)
#
# 	vx = speed * cos((-coord['heading']+90.0)*pi/180.0)
# 	vy = speed * sin((-coord['heading']+90.0)*pi/180.0)
#
# 	coord['latitude'] += dt *180.0/pi * vy / r
# 	coord['longitude'] += dt *180.0/pi * vx / (r*cos(coord['latitude']*pi/180.0))
#
# 	with open("camera_tmp.kml", "w") as kml_file:
# 		kml_file.write(kml_template.format(**coord))
#
# 	time.sleep(Te)
#
# 	last_time = now
# 	now = time.time()
# 	dt = now - last_time

def GenerateKML(longitude,latitude,altitude,heading,tilt):
    coord['longitude'] = longitude
    coord['latitude'] = latitude
    #coord['altitude'] = altitude+30
    coord['altitude'] = 30
    coord['heading'] = heading/3.14*360
    coord['tilt'] = tilt/3.14*360

    with open("Camera/camera_tmp.kml", "w") as kml_file:
        kml_file.write(kml_template.format(**coord))

#GenerateKML(1,2,3,4,5)