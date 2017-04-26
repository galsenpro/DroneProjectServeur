import requests

pathRest = 'http://148.60.11.238:8080/'

def get_interventions():
    res = requests.get(pathRest+'interventions')
    return res.json()

def post_position(value):
    requests.post(pathRest+'positiondrone',data = value)

def get_drone(id_intervention):
    res = requests.get(pathRest+'drones/'+id_intervention+'/intervention')
    return res.json()

"""def post_photo(value):
    requests.post(path+'photo',data = value)"""

def post_photo(position,date_heure,nom,path,position_pts):
    value = {}
    value['position'] = position
    value['path'] = path
    value['date_heure'] = date_heure
    value['nom'] = nom
    value['position_pts'] = position_pts
    requests.post(pathRest+'photo',data = value)