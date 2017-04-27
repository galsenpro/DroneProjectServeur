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

def post_position(position, id_intervention):
    value = {"position": [position[0],position[1]], "idIntervention": id_intervention}
    requests.post(pathRest+'positiondrone',data = value)

def post_photo(position, dateheure, nom, path, positionPTS, id_intervention):
    value = {"position": [position[0],position[1]], "date_heure": dateheure, "nom": nom, "path": path, "positionPTS": [positionPTS[0],positionPTS[1]], "idintervention": id_intervention}
    requests.post(pathRest + 'photo', data=value)