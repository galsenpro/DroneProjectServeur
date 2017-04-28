import requests

pathRest = 'http://148.60.11.238:8080/'

def get_interventions():
    res = requests.get(pathRest+'interventions')
    return res.json()

def post_position(value):
    requests.post(pathRest+'positiondrone',data = value)
    #print "post_position: ", pathRest,' positiondrone ',value

def post_photo(value):
    requests.post(pathRest+'photo',data = value)

def get_drone(id_intervention):
    res = requests.get(pathRest+'drones/'+id_intervention+'/intervention')
    return res.json()

def create_drone(id_intervention):
    value = {}
    value['idIntervention'] = id_intervention
    value['etat'] = 'STOP'
    requests.post(pathRest+'drones',data = value)

def post_positionParam(position, id_intervention):
    value = {}
    value['idIntervention'] = id_intervention
    value['position'] = [position.lat, position.lon]
    #print "Sending drone position ", position
    requests.post(pathRest+'positiondrone',data = value)

def post_photoParam(position, dateheure, nom, path, positionPTS, id_intervention):
    value = {"position": [position[0],position[1]], "date_heure": dateheure, "nom": nom, "path": path, "positionPTS": [positionPTS[0],positionPTS[1]], "idintervention": id_intervention}
    requests.post(pathRest + 'photo', data=value)