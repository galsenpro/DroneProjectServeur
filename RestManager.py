import requests

pathRest = 'http://148.60.11.238:8080/'

def get_interventions():
    try:
        res = requests.get(pathRest+'interventions')
        if res.status_code == 404:
            print "404"
            return None
        elif res.status_code == 200:
            print "200"
            return res.json()
    except Exception as e:
        return None

def post_position(value):
    try:
        requests.post(pathRest+'positiondrone',data = value)
        print "post_position: ", pathRest,' positiondrone ',value
    except Exception as e:
        print "Error sending position"

def get_drone(id_intervention):
    try:
        res = requests.get(pathRest+'drones/'+id_intervention+'/intervention')
        print "==: ", res, " : ", res.status_code
        if res.status_code == 404:
            print "404"
            return None
        elif res.status_code == 200:
            print "200"
            return res.json()
    except Exception as e:
        return None

def post_positionParam(position, id_intervention):
    try:
        value = {}
        value['idIntervention'] = id_intervention
        value['position'] = [position.lat, position.lon]
        print "Sending drone position ", position
        requests.post(pathRest+'positiondrone',data = value)
    except Exception as e:
        print "Error sending position"

def post_photoParam(position, dateheure, nom, path, positionPTS, id_intervention):
    try:
        value = {}
        value['position'] = [position.lat, position.lon]
        value['date_heure'] = [dateheure]
        value['nom'] = [nom]
        value['path'] = [path]
        value['positionPTS'] = [positionPTS[0],positionPTS[1]]
        value['idintervention'] = [id_intervention]
        requests.post(pathRest + 'photo', data=value)
    except Exception as e:
        print "Error sending position"