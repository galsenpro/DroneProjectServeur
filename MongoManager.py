from datetime import datetime
from pymongo import MongoClient

cl = MongoClient('mongodb://148.60.11.238:27018')
db = cl.admin
collectiondrone = db.positiondrone
collectionobjectif = db.positionobjectif


def last_command_afaire():
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


def set_command_encours(id_cmd):
    collectionobjectif.update_one({"_id": id_cmd}, {'$set': {"etat": "encours"}})


def set_command_fait(id_cmd):
    collectionobjectif.update_one({"_id": id_cmd}, {'$set': {"etat": "fait"}})
