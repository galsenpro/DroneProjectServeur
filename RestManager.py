import requests

path = 'http://148.60.11.238:8080/'

def get_interventions():
    res = requests.get(path+'interventions')
    return res.json()

def post_position(value):
    requests.post(path+'positiondrone',data = value)

def get_drone(id_intervention):
    res = requests.get(path+'drones/'+id_intervention+'/intervention')

def post_photo(value):
    requests.post(path+'photo',data = value)