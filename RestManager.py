import requests

class RestManager():
    
    def __init__(self):
        self.path = 'http://148.60.11.238:8080/'

    def get_interventions(self):
        res = requests.get(self.path+'interventions')
        return res.json()

    def post_position(self,value):
        requests.post(self.path+'positiondrone',data = value)

    def get_drone(self,id_intervention):
        res = requests.get(self.path+'drones/'+id_intervention+'/intervention')

    def post_photo(self,value):
        requests.post(self.path+'photo',data = value)