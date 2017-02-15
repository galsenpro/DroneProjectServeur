from dronekit import Vehicle, connect, VehicleMode, LocationGlobalRelative
import time


myvar = 42
vehicule = None # type: Vehicle

def test_func():
    print("Hello!")

# --connect tcp:127.0.0.1:5760
def ConnectToDrone(connection_string):
    global vehicule
    # Start SITL if no connection string specified
    if not connection_string:
        print 'merci de specifier l\'adresse de connexion'

    # Connect to the Vehicle
    print 'Connecting to vehicle on: %s' % connection_string
    vehicule = connect(connection_string, wait_ready=True)

    print 'is connected: %s' % vehicule

    sitl = None

def is_AlreadyFlying():
    # pas armer si atteri
    # altitude par rapport a la position de depart, si elle est au dessus du sol
    global vehicule # type: Vehicle
    assert isinstance(vehicule,Vehicle)
    if( vehicule.armed and vehicule.location.global_relative_frame.alt > 15):
        #deja en vol
        return True
    else:
        return False

def goTo(point,groundspeed):
    global vehicule
    if not is_AlreadyFlying():
        arm_and_takeoff(10)
        if not groundspeed:
            vehicule.simple_goto(point)
        else:
            vehicule.simple_goto(point,groundspeed)

def arm_and_takeoff(aTargetAltitude):
    global vehicule  # type: Vehicle
    assert isinstance(vehicule, Vehicle)

    """
       Arms vehicle and fly to aTargetAltitude.
       """

    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    while not vehicule.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)

    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicule.mode = VehicleMode("GUIDED")
    vehicule.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicule.armed:
        print " Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    vehicule.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", vehicule.location.global_relative_frame.alt
        # Break and return from function just below target altitude.
        if vehicule.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print "Reached target altitude"
            break
        time.sleep(1)

def setSpeed(speed):
    global vehicule  # type: Vehicle
    assert isinstance(vehicule, Vehicle)
    vehicule.airspeed = speed

def setAltitude(alt):
    global vehicule  # type: Vehicle
    assert isinstance(vehicule, Vehicle)
    vehicule.location.global_relative_frame.alt = alt

def RTLandFinish():
    global vehicule  # type: Vehicle
    assert isinstance(vehicule, Vehicle)
    print "Returning to Launch"
    vehicule.mode = VehicleMode("RTL")

    # Close vehicle object before exiting script
    print "Close vehicle object"
    vehicule.close()
