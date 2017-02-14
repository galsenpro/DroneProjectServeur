import sched, time
from datetime import datetime
from pymongo import MongoClient

FREQUENCE = 5

cl = MongoClient('mongodb://148.60.11.238:27018')
db = cl.admin
collectiondrone = db.positiondrone
collectionobjectif = db.positionobjectif


def last_command():
    cursor = list(collectionobjectif.find({"etat": "afaire"}).sort('dated', -1).limit(1))

    if len(cursor) > 0:
        return cursor[0]
    else:
        return None


def nearest_command(lng, lat):
    cursor = list(collectionobjectif.find({"etat": "afaire", "position": {"$near": (lng, lat)}}).limit(1))

    if len(cursor) > 0:
        return cursor[0]
    else:
        return None


def insert_drone_gps(lng, lat):
    position = {"position": [lng, lat], "dated": datetime.utcnow()}
    collectiondrone.insert_one(position)


def main():
    print(last_command())
    print(nearest_command(41, 43))
    s.enter(FREQUENCE, 1, main, ())


s = sched.scheduler(time.time, time.sleep)
s.enter(0, 1, main, ())
s.run()
